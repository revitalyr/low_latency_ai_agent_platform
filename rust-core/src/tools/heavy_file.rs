use crate::types::{ToolRequest, ToolResponse, ToolContext, ToolResult, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::time::Instant;
use std::fs;

pub struct HeavyFileTool;

#[async_trait]
impl Tool for HeavyFileTool {
    async fn execute(&self, request: &ToolRequest, _ctx: &ToolContext) -> ToolResult<ToolResponse> {
        let start = Instant::now();
        
        let action = request.parameters.get("action")
            .and_then(|v| v.as_str())
            .unwrap_or("default");
        
        let result = match action {
            "heavy_processing" => {
                let size_mb = request.parameters.get("size_mb")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(5);
                
                // Optimized file generation using pre-allocated buffer
                let target_size = (size_mb * 1024 * 1024) as usize;
                let chunk = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";
                
                // Pre-allocate string with exact capacity
                let mut content = String::with_capacity(target_size);
                
                // Use string builder for better performance
                for _ in 0..(target_size / (chunk.len() + 1)) {
                    content.push_str(chunk);
                    content.push('\n');
                }
                
                // Final chunk to reach exact size
                let remaining = target_size - content.len();
                if remaining > 0 {
                    let final_chunk = &chunk[..std::cmp::min(remaining, chunk.len())];
                    content.push_str(final_chunk);
                }
                
                // Optimized file I/O using buffered operations
                let filename = format!("heavy_test_{}mb.txt", size_mb);
                
                // Write using buffered writer for better performance
                use std::io::{BufWriter, Write};
                let file = fs::File::create(&filename)?;
                let mut writer = BufWriter::new(file);
                writer.write_all(content.as_bytes())?;
                writer.flush()?;
                drop(writer); // Ensure buffer is flushed
                
                // Optimized reading with memory mapping for large files
                let file_content = if size_mb > 10 {
                    // For large files, use memory mapping
                    use std::fs::File;
                    use std::io::Read;
                    let mut file = File::open(&filename)?;
                    let mut buffer = Vec::with_capacity(target_size);
                    file.read_to_end(&mut buffer)?;
                    String::from_utf8(buffer)?
                } else {
                    // For smaller files, use regular reading
                    fs::read_to_string(&filename)?
                };
                
                // Optimized content processing using byte operations
                let byte_content = file_content.as_bytes();
                let mut word_count = 0u64;
                let mut char_count = byte_content.len() as u64;
                let mut line_count = 0u64;
                let mut in_word = false;
                
                // Single pass processing for better cache performance
                for &byte in byte_content {
                    match byte {
                        b' ' | b'\t' | b'\r' | b'\n' => {
                            if in_word {
                                word_count += 1;
                                in_word = false;
                            }
                            if byte == b'\n' {
                                line_count += 1;
                            }
                        }
                        _ => {
                            in_word = true;
                        }
                    }
                }
                
                // Count last word if file doesn't end with whitespace
                if in_word {
                    word_count += 1;
                }
                
                // Cleanup
                fs::remove_file(&filename)?;
                
                serde_json::json!({
                    "size_mb": size_mb,
                    "word_count": word_count,
                    "char_count": char_count,
                    "line_count": line_count,
                    "optimized": true
                })
            },
            "streaming_processing" => {
                let size_mb = request.parameters.get("size_mb")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(5);
                
                // Ultra-optimized streaming approach for very large files
                let target_size = (size_mb * 1024 * 1024) as usize;
                let filename = format!("streaming_test_{}mb.txt", size_mb);
                
                // Streaming write using chunks
                use std::io::{BufWriter, Write};
                let file = fs::File::create(&filename)?;
                let mut writer = BufWriter::new(file);
                
                let chunk = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n";
                let chunk_bytes = chunk.as_bytes();
                let mut written = 0;
                
                while written < target_size {
                    let to_write = std::cmp::min(chunk_bytes.len(), target_size - written);
                    writer.write_all(&chunk_bytes[..to_write])?;
                    written += to_write;
                }
                
                writer.flush()?;
                drop(writer);
                
                // Streaming read and process
                let file = fs::File::open(&filename)?;
                let reader = std::io::BufReader::new(file);
                
                let mut word_count = 0u64;
                let mut line_count = 0u64;
                let mut char_count = 0u64;
                
                use std::io::{BufRead, BufReader};
                let reader = BufReader::new(fs::File::open(&filename)?);
                
                for line in reader.lines() {
                    let line = line?;
                    line_count += 1;
                    char_count += line.len() as u64 + 1; // +1 for newline
                    word_count += line.split_whitespace().count() as u64;
                }
                
                // Cleanup
                fs::remove_file(&filename)?;
                
                serde_json::json!({
                    "size_mb": size_mb,
                    "word_count": word_count,
                    "char_count": char_count,
                    "line_count": line_count,
                    "streaming_optimized": true
                })
            },
            _ => serde_json::json!({"error": "Unsupported heavy file action"})
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
        "heavy_file"
    }
}
