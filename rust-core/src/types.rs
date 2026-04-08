use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

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
    pub timestamp: chrono::DateTime<chrono::Utc>,
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
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

/// Supported tool types in the system
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ToolType {
    /// HTTP API tool for external requests
    Http,
    /// File system operations tool
    File,
    /// Mathematical computations tool
    Compute,
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
    pub timestamp: chrono::DateTime<chrono::Utc>,
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
    pub timestamp: chrono::DateTime<chrono::Utc>,
}
