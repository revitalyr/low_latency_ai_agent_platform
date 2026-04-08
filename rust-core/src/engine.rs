use crate::types::{ToolRequest, ToolResponse, ToolType, ToolContext, ToolResult};
use crate::tools::ToolRegistry;
use crate::cache::Cache;
use crate::metrics::Metrics;
use futures::future::join_all;
use std::time::Instant;
use std::sync::Arc;
use tokio::sync::RwLock;
use tokio::task::LocalSet;
use anyhow::Result;

/// High-performance execution engine for AI agent tools
/// 
/// This component handles orchestration and execution of tool requests,
/// providing parallel execution capabilities, retry logic, and performance tracking.
/// Optimized for single-threaded low-latency execution.
pub struct ExecutionEngine {
    /// Metrics collector for performance tracking
    metrics: Arc<Metrics>,
}

impl ExecutionEngine {
    /// Creates a new execution engine instance
    /// 
    /// # Returns
    /// 
    /// A new ExecutionEngine with initialized metrics
    pub fn new() -> Self {
        Self {
            metrics: Arc::new(Metrics::new()),
        }
    }

    /// Executes a batch of tool requests using parallel execution with retry logic
    /// 
    /// # Arguments
    /// 
    /// * `tool_requests` - Vector of tool requests to execute
    /// * `tool_registry` - Registry containing available tools
    /// * `cache` - Shared cache for result caching
    /// 
    /// # Returns
    /// 
    /// Result containing vector of tool responses or error
    /// 
    /// # Performance Features
    /// 
    /// - Parallel execution of all tools
    /// - Exponential backoff retry logic (3 retries)
    /// - Result caching for performance optimization
    /// - Comprehensive metrics tracking
    /// - Budgeted execution for tight loops
    pub async fn execute_plan(
        &self,
        tool_requests: Vec<ToolRequest>,
        tool_registry: &ToolRegistry,
        cache: Arc<RwLock<Cache>>,
    ) -> Result<Vec<ToolResponse>> {
        let futures = tool_requests.into_iter().map(|request| {
            let registry = tool_registry.clone();
            let cache = cache.clone();
            let metrics = self.metrics.clone();
            
            async move {
                // Use LocalSet for single-threaded optimization
                LocalSet::new().run_until(async move {
                    let start = Instant::now();
                    
                    // Check cache first
                    let cache_key = format!("{}:{:?}", request.tool_type, request.parameters);
                    if let Some(cached) = {
                        let cache_read = cache.read().await;
                        cache_read.get(&cache_key)
                    } {
                        metrics.record_cache_hit();
                        tracing::info!(
                            tool_type = ?request.tool_type,
                            "Cache hit for tool"
                        );
                        return Ok(cached);
                    }

                    // Execute with retry and budgeting
                    let result = retry_with_backoff_budgeted(
                        || registry.execute_tool(&request, &ToolContext::new(request.id.to_string())),
                        3
                    ).await;

                    let elapsed = start.elapsed().as_millis() as u64;
                    metrics.record_execution_time(elapsed);

                    match result {
                        Ok(mut res) => {
                            res.execution_time_ms = elapsed;
                            
                            // Cache the result
                            {
                                let mut cache_write = cache.write().await;
                                cache_write.put(cache_key, res.clone());
                            }
                            
                            metrics.record_success();
                            tracing::info!(
                                tool_type = ?request.tool_type,
                                execution_time_ms = elapsed,
                                cached = res.cached,
                                "Tool executed successfully"
                            );
                            Ok(res)
                        }
                        Err(e) => {
                            metrics.record_failure();
                            tracing::error!(
                                tool_type = ?request.tool_type,
                                error = %e,
                                "Tool execution failed after retries"
                            );
                            Err(e)
                        }
                    }
                }).await
            }
        });

        let results = join_all(futures).await;
        results.into_iter().collect()
    }

    /// Get reference to metrics collector
    pub fn get_metrics(&self) -> Arc<Metrics> {
        self.metrics.clone()
    }
}

/// Retry logic with exponential backoff and budgeting for resilient execution
async fn retry_with_backoff_budgeted<F, T, E>(
    operation: F,
    max_retries: usize,
) -> Result<T, E>
where
    F: Fn() -> futures::future::BoxFuture<'static, Result<T, E>>,
    E: std::fmt::Display,
{
    let mut attempt = 0;
    let mut delay = tokio::time::Duration::from_millis(100);

    loop {
        // Use budgeted execution for tight loops
        let result = tokio::task::budget(move || {
            operation()
        }).await;

        match result {
            Ok(operation_result) => {
                match operation_result {
                    Ok(result) => return Ok(result),
                    Err(e) if attempt < max_retries => {
                        attempt += 1;
                        tracing::warn!(
                            attempt = attempt,
                            max_retries = max_retries,
                            error = %e,
                            delay = ?delay,
                            "Execution failed, retrying"
                        );
                        tokio::time::sleep(delay).await;
                        delay *= 2; // Exponential backoff
                    }
                    Err(e) => {
                        tracing::error!(
                            attempts = attempt,
                            error = %e,
                            "Execution failed after all retries"
                        );
                        return Err(e);
                    }
                }
            }
            Err(_) => {
                // Budget exhausted - yield control
                tokio::task::yield_now().await;
                continue;
            }
        }
    }
}

impl Default for ExecutionEngine {
    fn default() -> Self {
        Self::new()
    }
}
