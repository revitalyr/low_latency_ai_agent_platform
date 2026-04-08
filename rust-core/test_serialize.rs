use serde_json; use crate::types::ToolType; fn main() { println!("{}", serde_json::to_string(&ToolType::Compute).unwrap()); }
