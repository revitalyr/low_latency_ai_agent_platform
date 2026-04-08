use crate::types::{ToolRequest, ToolResponse, ToolType, ToolContext, ToolError, ToolResult};
use crate::tools::Tool;
use async_trait::async_trait;
use reqwest::Client;
use std::time::Instant;
use std::time::Duration;
use serde_json::Value;
use anyhow::Result;

pub struct HttpTool;

#[async_trait]
impl Tool for HttpTool {
    async fn execute(
        &self, 
        request: &ToolRequest, 
        _ctx: &ToolContext
    ) -> ToolResult<ToolResponse> {
        let start = Instant::now();
        
        let method = request.parameters.get("method")
            .and_then(|v| v.as_str())
            .unwrap_or("GET");
        
        let url = request.parameters.get("url")
            .and_then(|v| v.as_str())
            .unwrap_or("https://httpbin.org/get");
        
        let body = request.parameters.get("body")
            .and_then(|v| v.as_object())
            .cloned();
        
        // Optimized HTTP client with connection pooling
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(10))
            .connection_verbose(false)
            .pool_max_idle_per_host(10)
            .pool_idle_timeout(Duration::from_secs(30))
            .build()
            .map_err(|e| ToolError::Network(e.to_string()))?;
        
        let result = match method {
            "GET" => {
                let response = client
                    .get(url)
                    .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                    .send()
                    .await
                    .map_err(|e| ToolError::Network(e.to_string()))?;
                
                let status = response.status().as_u16();
                let response_text = response.text().await
                    .map_err(|e| ToolError::Network(e.to_string()))?;
                
                serde_json::json!({
                    "status": status,
                    "response": response_text,
                    "method": "GET",
                    "optimized": true
                })
            },
            "POST" => {
                let response = if let Some(body_obj) = body {
                    client
                        .post(url)
                        .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                        .header("Content-Type", "application/json")
                        .json(&body_obj)
                        .send()
                        .await
                        .map_err(|e| ToolError::Network(e.to_string()))?
                } else {
                    client
                        .post(url)
                        .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                        .send()
                        .await
                        .map_err(|e| ToolError::Network(e.to_string()))?
                };
                
                let status = response.status().as_u16();
                let response_text = response.text().await
                    .map_err(|e| ToolError::Network(e.to_string()))?;
                
                serde_json::json!({
                    "status": status,
                    "response": response_text,
                    "method": "POST",
                    "optimized": true
                })
            },
            "PUT" => {
                let response = if let Some(body_obj) = body {
                    client
                        .put(url)
                        .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                        .header("Content-Type", "application/json")
                        .json(&body_obj)
                        .send()
                        .await
                        .map_err(|e| ToolError::Network(e.to_string()))?
                } else {
                    client
                        .put(url)
                        .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                        .send()
                        .await
                        .map_err(|e| ToolError::Network(e.to_string()))?
                };
                
                let status = response.status().as_u16();
                let response_text = response.text().await
                    .map_err(|e| ToolError::Network(e.to_string()))?;
                
                serde_json::json!({
                    "status": status,
                    "response": response_text,
                    "method": "PUT",
                    "optimized": true
                })
            },
            "DELETE" => {
                let response = client
                    .delete(url)
                    .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                    .send()
                    .await
                    .map_err(|e| ToolError::Network(e.to_string()))?;
                
                let status = response.status().as_u16();
                let response_text = response.text().await
                    .map_err(|e| ToolError::Network(e.to_string()))?;
                
                serde_json::json!({
                    "status": status,
                    "response": response_text,
                    "method": "DELETE",
                    "optimized": true
                })
            },
            "batch_requests" => {
                // Optimized batch HTTP requests
                let urls = request.parameters.get("urls")
                    .and_then(|v| v.as_array())
                    .cloned()
                    .unwrap_or_else(|| vec![]);
                
                let mut results = Vec::with_capacity(urls.len());
                
                // Use futures for concurrent requests
                let mut futures = Vec::new();
                
                for url_obj in urls {
                    if let Some(url_str) = url_obj.as_str() {
                        let future = client
                            .get(url_str)
                            .header("User-Agent", "Low-Latency-AI-Agent/1.0")
                            .send();
                        futures.push(future);
                    }
                }
                
                // Execute all requests concurrently
                let responses = futures::future::join_all(futures).await;
                
                for response in responses {
                    match response {
                        Ok(resp) => {
                            let status = resp.status().as_u16();
                            let response_text = resp.text().await.unwrap_or_default();
                            results.push(serde_json::json!({
                                "status": status,
                                "response": response_text
                            }));
                        },
                        Err(e) => {
                            results.push(serde_json::json!({
                                "error": e.to_string()
                            }));
                        }
                    }
                }
                
                serde_json::json!({
                    "batch_results": results,
                    "method": "batch_requests",
                    "optimized": true
                })
            },
            _ => serde_json::json!({"error": "Unsupported HTTP method"})
        };
        
        let execution_time = start.elapsed().as_millis() as u64;
        
        Ok(ToolResponse {
            id: request.id,
            result,
            execution_time_ms: execution_time,
            cached: false,
            timestamp: chrono::Utc::now(),
        })
    }
    
    fn tool_type(&self) -> ToolType {
        ToolType::Http
    }
    
    fn name(&self) -> &'static str {
        "http"
    }
}
