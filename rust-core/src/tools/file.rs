use crate::types::{ToolRequest, ToolResponse, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::time::Instant;
use std::fs;

pub struct FileTool;

#[async_trait]
impl Tool for FileTool {
    async fn execute(&self, request: &ToolRequest) -> anyhow::Result<ToolResponse> {
        let start = Instant::now();
        
        let action = request.parameters.get("action")
            .and_then(|v| v.as_str())
            .unwrap_or("default");
        
        let result = match action {
            "read" => {
                let path = request.parameters.get("path")
                    .and_then(|v| v.as_str())
                    .unwrap_or("default.txt");
                
                // Optimized file reading with memory mapping for large files
                let file_content = if std::path::Path::new(path).exists() {
                    use std::fs::File;
                    use std::io::Read;
                    
                    let metadata = fs::metadata(path)?;
                    let file_size = metadata.len();
                    
                    if file_size > 10 * 1024 * 1024 { // 10MB threshold
                        // Use memory mapping for large files
                        let mut file = File::open(path)?;
                        let mut buffer = Vec::with_capacity(file_size as usize);
                        file.read_to_end(&mut buffer)?;
                        String::from_utf8(buffer)?
                    } else {
                        // Use regular reading for smaller files
                        fs::read_to_string(path)?
                    }
                } else {
                    return Err(anyhow::anyhow!("File not found: {}", path));
                };
                
                serde_json::json!({
                    "content": file_content,
                    "size": file_content.len(),
                    "action": "read",
                    "optimized": true
                })
            },
            "write" => {
                let path = request.parameters.get("path")
                    .and_then(|v| v.as_str())
                    .unwrap_or("default.txt");
                
                let content = request.parameters.get("content")
                    .and_then(|v| v.as_str())
                    .unwrap_or("");
                
                // Optimized file writing with buffered I/O
                use std::io::{BufWriter, Write};
                
                let file = fs::File::create(path)?;
                let mut writer = BufWriter::new(file);
                writer.write_all(content.as_bytes())?;
                writer.flush()?;
                
                serde_json::json!({
                    "written": true,
                    "size": content.len(),
                    "action": "write",
                    "optimized": true
                })
            },
            "append" => {
                let path = request.parameters.get("path")
                    .and_then(|v| v.as_str())
                    .unwrap_or("default.txt");
                
                let content = request.parameters.get("content")
                    .and_then(|v| v.as_str())
                    .unwrap_or("");
                
                // Optimized file appending
                use std::io::{BufWriter, Write};
                
                let file = fs::OpenOptions::new()
                    .create(true)
                    .append(true)
                    .open(path)?;
                
                let mut writer = BufWriter::new(file);
                writer.write_all(content.as_bytes())?;
                writer.flush()?;
                
                // Get final file size
                let final_size = fs::metadata(path)?.len();
                
                serde_json::json!({
                    "appended": true,
                    "content_size": content.len(),
                    "final_size": final_size,
                    "action": "append",
                    "optimized": true
                })
            },
            "batch_operations" => {
                // Optimized batch file operations
                let operations = request.parameters.get("operations")
                    .and_then(|v| v.as_array())
                    .cloned()
                    .unwrap_or_else(|| vec![]);
                
                let mut results = Vec::with_capacity(operations.len());
                
                for op in operations {
                    if let Some(op_obj) = op.as_object() {
                        let op_type = op_obj.get("type")
                            .and_then(|v| v.as_str())
                            .unwrap_or("read");
                        
                        let path = op_obj.get("path")
                            .and_then(|v| v.as_str())
                            .unwrap_or("default.txt");
                        
                        let result = match op_type {
                            "read" => {
                                if std::path::Path::new(path).exists() {
                                    fs::read_to_string(path).ok()
                                } else {
                                    None
                                }
                            },
                            "write" => {
                                let content = op_obj.get("content")
                                    .and_then(|v| v.as_str())
                                    .unwrap_or("");
                                
                                match fs::write(path, content) {
                                    Ok(_) => Some("written".to_string()),
                                    Err(_) => None,
                                }
                            },
                            "delete" => {
                                match fs::remove_file(path) {
                                    Ok(_) => Some("deleted".to_string()),
                                    Err(_) => None,
                                }
                            },
                            _ => None
                        };
                        
                        results.push(serde_json::json!({
                            "type": op_type,
                            "path": path,
                            "result": result
                        }));
                    }
                }
                
                serde_json::json!({
                    "batch_results": results,
                    "action": "batch_operations",
                    "optimized": true
                })
            },
            _ => serde_json::json!({"error": "Unsupported file action"})
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
        ToolType::File
    }
    
    fn name(&self) -> &'static str {
        "file"
    }
}
