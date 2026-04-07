use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolRequest {
    pub id: Uuid,
    pub tool_type: ToolType,
    pub parameters: HashMap<String, serde_json::Value>,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolResponse {
    pub id: Uuid,
    pub result: serde_json::Value,
    pub execution_time_ms: u64,
    pub cached: bool,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ToolType {
    Http,
    File,
    Compute,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentTask {
    pub id: Uuid,
    pub prompt: String,
    pub tools: Vec<ToolRequest>,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentResponse {
    pub id: Uuid,
    pub result: String,
    pub tool_responses: Vec<ToolResponse>,
    pub total_execution_time_ms: u64,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}
