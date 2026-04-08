use crate::types::{ToolRequest, ToolResponse, ToolContext, ToolResult, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::time::Instant;

pub struct ComputeTool;

#[async_trait]
impl Tool for ComputeTool {
    async fn execute(&self, request: &ToolRequest, _ctx: &ToolContext) -> ToolResult<ToolResponse> {
        let start = Instant::now();
        
        let operation = request.parameters.get("operation")
            .and_then(|v| v.as_str())
            .unwrap_or("default");
        
        let result = match operation {
            "add" => {
                let a = request.parameters.get("a")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.0);
                let b = request.parameters.get("b")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.0);
                
                // Optimized addition with overflow checking
                let result = if a.is_finite() && b.is_finite() {
                    a + b
                } else {
                    f64::NAN
                };
                
                serde_json::json!({
                    "result": result,
                    "operation": "add",
                    "optimized": true
                })
            },
            "multiply" => {
                let a = request.parameters.get("a")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.0);
                let b = request.parameters.get("b")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.0);
                
                // Optimized multiplication with overflow checking
                let result = if a.is_finite() && b.is_finite() {
                    a * b
                } else {
                    f64::NAN
                };
                
                serde_json::json!({
                    "result": result,
                    "operation": "multiply",
                    "optimized": true
                })
            },
            "percentage_change" => {
                let old = request.parameters.get("old")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.0);
                let new = request.parameters.get("new")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.0);
                
                // Optimized percentage change calculation
                let (percentage_change, direction) = if old.abs() < f64::EPSILON {
                    (0.0, "flat")
                } else {
                    let change = ((new - old) / old) * 100.0;
                    let direction = if change > f64::EPSILON {
                        "up"
                    } else if change < -f64::EPSILON {
                        "down"
                    } else {
                        "flat"
                    };
                    (change, direction)
                };
                
                serde_json::json!({
                    "percentage_change": percentage_change,
                    "direction": direction,
                    "operation": "percentage_change",
                    "optimized": true
                })
            },
            "batch_operations" => {
                // Optimized batch processing for multiple operations
                let operations = request.parameters.get("operations")
                    .and_then(|v| v.as_array())
                    .cloned()
                    .unwrap_or_else(|| vec![]);
                
                let mut results = Vec::with_capacity(operations.len());
                
                for op in operations {
                    if let Some(op_obj) = op.as_object() {
                        let op_type = op_obj.get("type")
                            .and_then(|v| v.as_str())
                            .unwrap_or("add");
                        
                        let result = match op_type {
                            "add" => {
                                let a = op_obj.get("a").and_then(|v| v.as_f64()).unwrap_or(0.0);
                                let b = op_obj.get("b").and_then(|v| v.as_f64()).unwrap_or(0.0);
                                a + b
                            },
                            "multiply" => {
                                let a = op_obj.get("a").and_then(|v| v.as_f64()).unwrap_or(0.0);
                                let b = op_obj.get("b").and_then(|v| v.as_f64()).unwrap_or(0.0);
                                a * b
                            },
                            _ => f64::NAN
                        };
                        
                        results.push(serde_json::json!({
                            "type": op_type,
                            "result": result
                        }));
                    }
                }
                
                serde_json::json!({
                    "batch_results": results,
                    "operation": "batch_operations",
                    "optimized": true
                })
            },
            "vector_operations" => {
                // Optimized vector/matrix operations
                let vector_a = request.parameters.get("vector_a")
                    .and_then(|v| v.as_array())
                    .cloned()
                    .unwrap_or_else(|| vec![]);
                let vector_b = request.parameters.get("vector_b")
                    .and_then(|v| v.as_array())
                    .cloned()
                    .unwrap_or_else(|| vec![]);
                let op_type = request.parameters.get("vector_op")
                    .and_then(|v| v.as_str())
                    .unwrap_or("add");
                
                let mut results = Vec::new();
                
                match op_type {
                    "add" => {
                        let len = std::cmp::min(vector_a.len(), vector_b.len());
                        results.reserve(len);
                        
                        for i in 0..len {
                            if let (Some(a), Some(b)) = (vector_a[i].as_f64(), vector_b[i].as_f64()) {
                                results.push(a + b);
                            }
                        }
                    },
                    "multiply" => {
                        let len = std::cmp::min(vector_a.len(), vector_b.len());
                        results.reserve(len);
                        
                        for i in 0..len {
                            if let (Some(a), Some(b)) = (vector_a[i].as_f64(), vector_b[i].as_f64()) {
                                results.push(a * b);
                            }
                        }
                    },
                    "dot_product" => {
                        let len = std::cmp::min(vector_a.len(), vector_b.len());
                        let mut dot_product = 0.0;
                        
                        for i in 0..len {
                            if let (Some(a), Some(b)) = (vector_a[i].as_f64(), vector_b[i].as_f64()) {
                                dot_product += a * b;
                            }
                        }
                        
                        results.push(dot_product);
                    },
                    _ => {}
                }
                
                serde_json::json!({
                    "vector_results": results,
                    "operation": "vector_operations",
                    "vector_op": op_type,
                    "optimized": true
                })
            },
            _ => serde_json::json!({"error": "Unsupported compute operation"})
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
        ToolType::Compute
    }
    
    fn name(&self) -> &'static str {
        "compute"
    }
}
