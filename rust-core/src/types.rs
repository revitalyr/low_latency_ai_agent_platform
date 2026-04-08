use std::collections::HashMap;
use std::string::FromUtf8Error;
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};
use reqwest;
use serde_json;
use anyhow;

/// Domain-specific error types for better error handling
#[derive(Debug, thiserror::Error)]
pub enum ToolError {
    #[error("Timeout error: {0}")]
    Timeout(String),
    
    #[error("Network error: {0}")]
    Network(String),
    
    #[error("Invalid input: {0}")]
    InvalidInput(String),
    
    #[error("Execution failed: {0}")]
    ExecutionFailed(String),
    
    #[error("Tool not found: {0}")]
    ToolNotFound(String),
    
    #[error("Cache error: {0}")]
    CacheError(String),
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
    
    #[error("HTTP error: {0}")]
    HttpError(#[from] reqwest::Error),
    
    #[error("JSON error: {0}")]
    JsonError(#[from] serde_json::Error),
    
    #[error("Anyhow error: {0}")]
    AnyhowError(#[from] anyhow::Error),
    
    #[error("UTF-8 error: {0}")]
    Utf8Error(#[from] FromUtf8Error),
}

/// Type alias for Result with domain error
pub type ToolResult<T> = std::result::Result<T, ToolError>;

/// Tool execution context for better control
#[derive(Debug, Clone)]
pub struct ToolContext {
    pub request_id: String,
    pub timeout_ms: Option<u64>,
    pub retry_count: u32,
}

impl ToolContext {
    pub fn new(request_id: String) -> Self {
        Self {
            request_id,
            timeout_ms: Some(10000), // 10 second default timeout
            retry_count: 0,
        }
    }
    
    pub fn with_timeout(mut self, timeout_ms: u64) -> Self {
        self.timeout_ms = Some(timeout_ms);
        self
    }
    
    pub fn no_timeout(mut self) -> Self {
        self.timeout_ms = None;
        self
    }
}

/// Represents the type of tool to execute
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum ToolType {
    Http,
    File,
    Compute,
    HeavyCompute,
    HeavyFile,
}

impl std::fmt::Display for ToolType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ToolType::Http => write!(f, "http"),
            ToolType::File => write!(f, "file"),
            ToolType::Compute => write!(f, "compute"),
            ToolType::HeavyCompute => write!(f, "heavy_compute"),
            ToolType::HeavyFile => write!(f, "heavy_file"),
        }
    }
}

/// Represents a request to execute a specific tool
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolRequest {
    /// Unique identifier for this specific tool execution
    pub id: Uuid,
    /// Type of tool to execute (HTTP, File, Compute)
    pub tool_type: ToolType,
    /// Parameters specific to the tool being executed
    pub parameters: HashMap<String, serde_json::Value>,
    /// Timestamp when the request was created
    pub timestamp: DateTime<Utc>,
}

/// Represents the response from a tool execution
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolResponse {
    /// Unique identifier matching the original request
    pub id: Uuid,
    /// The result data from the tool execution
    pub result: serde_json::Value,
    /// Execution time in milliseconds
    pub execution_time_ms: u64,
    /// Whether this result was retrieved from cache
    pub cached: bool,
    /// Timestamp when the response was generated
    pub timestamp: DateTime<Utc>,
}

/// Represents a complete agent task with multiple tool requests
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentTask {
    /// Unique identifier for this task
    pub id: Uuid,
    /// The original prompt from the user
    pub prompt: String,
    /// List of tool requests to execute
    pub tools: Vec<ToolRequest>,
    /// Timestamp when the task was created
    pub timestamp: DateTime<Utc>,
}

/// Represents the final response after executing all tools
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentResponse {
    /// Unique identifier matching the original task
    pub id: Uuid,
    /// The synthesized result from all tool executions
    pub result: String,
    /// List of responses from each tool execution
    pub tool_responses: Vec<ToolResponse>,
    /// Total execution time for all tools in milliseconds
    pub total_execution_time_ms: u64,
    /// Timestamp when the response was generated
    pub timestamp: DateTime<Utc>,
}
