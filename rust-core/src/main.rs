mod types;
mod engine;
mod tools;
mod cache;
mod metrics;

use axum::{
    extract::Json,
    http::StatusCode,
    response::Json as ResponseJson,
    routing::{get, post},
    Router,
};
use serde_json::Value;
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::sync::RwLock;
use tower_http::cors::{Any, CorsLayer};
use tracing::{info, error};
use tracing_subscriber;

use crate::types::{AgentTask, AgentResponse, ToolRequest};
use crate::engine::ExecutionEngine;
use crate::tools::{ToolRegistry, HttpTool, FileTool, ComputeTool};
use crate::cache::Cache;
use crate::metrics::Metrics;

#[derive(Clone)]
pub struct AppState {
    pub tool_registry: Arc<ToolRegistry>,
    pub cache: Arc<RwLock<Cache>>,
    pub metrics: Arc<Metrics>,
    pub engine: Arc<ExecutionEngine>,
}

impl AppState {
    pub fn new() -> Self {
        let mut tool_registry = ToolRegistry::new();
        tool_registry.register(HttpTool);
        tool_registry.register(FileTool);
        tool_registry.register(ComputeTool);
        
        Self {
            tool_registry: Arc::new(tool_registry),
            cache: Arc::new(RwLock::new(Cache::new(1000))),
            metrics: Arc::new(Metrics::new()),
            engine: Arc::new(ExecutionEngine::new()),
        }
    }
}

async fn health_check() -> StatusCode {
    StatusCode::OK
}

async fn execute_task(
    axum::extract::State(state): axum::extract::State<AppState>,
    Json(task): Json<AgentTask>,
) -> Result<ResponseJson<AgentResponse>, StatusCode> {
    let start_time = std::time::Instant::now();
    
    info!("Received task: {}, tools: {}", task.id, task.tools.len());
    
    state.metrics.record_request();
    
    let mut tool_responses = Vec::new();
    
    for request in &task.tools {
        let mut cache = state.cache.write().await;
        
        if let Some(cached_response) = cache.get(request) {
            info!("Cache hit: {}", request.id);
            state.metrics.record_cache_hit();
            tool_responses.push(cached_response);
            continue;
        }
        
        state.metrics.record_cache_miss();
        drop(cache);
        
        match state.tool_registry.execute_tool(request).await {
            Ok(response) => {
                let mut cache = state.cache.write().await;
                cache.put(request, response.clone());
                tool_responses.push(response);
            }
            Err(e) => {
                error!("Tool execution failed: {} - {}", request.id, e);
                return Err(StatusCode::INTERNAL_SERVER_ERROR);
            }
        }
    }
    
    let total_execution_time = start_time.elapsed().as_millis() as u64;
    state.metrics.record_execution_time(total_execution_time);
    
    let agent_response = AgentResponse {
        id: task.id,
        result: format!("Executed {} tools successfully", tool_responses.len()),
        tool_responses,
        total_execution_time_ms: total_execution_time,
        timestamp: chrono::Utc::now(),
    };
    
    info!(
        "Task completed: {} in {}ms",
        agent_response.id, total_execution_time
    );
    
    Ok(ResponseJson(agent_response))
}

async fn metrics(
    axum::extract::State(state): axum::extract::State<AppState>,
) -> ResponseJson<Value> {
    let metrics = &state.metrics;
    let cache = state.cache.read().await;
    
    let metrics_json = serde_json::json!({
        "total_requests": metrics.total_requests.load(std::sync::atomic::Ordering::Relaxed),
        "average_execution_time_ms": metrics.average_execution_time_ms(),
        "cache_hit_rate": metrics.cache_hit_rate(),
        "cache_utilization": cache.hit_rate()
    });
    
    ResponseJson(metrics_json)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    
    let state = AppState::new();
    
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/execute", post(execute_task))
        .route("/metrics", get(metrics))
        .layer(
            CorsLayer::new()
                .allow_origin(Any)
                .allow_methods(Any)
                .allow_headers(Any),
        )
        .with_state(state);
    
    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    info!("Starting server on {}", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    
    Ok(())
}
