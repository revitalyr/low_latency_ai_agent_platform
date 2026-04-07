# Demo Scenarios

## 1. Market Analysis Scenario

**Prompt**: "Check BTC price and tell me if it increased in the last hour"

**Expected Tool Chain**:
1. HTTP Tool: Fetch current BTC price from API
2. HTTP Tool: Fetch historical price data
3. Compute Tool: Calculate percentage change
4. Agent reasoning: Analyze trend and provide recommendation

**Demo Value**: Shows real-time data processing + financial analysis

## 2. Multi-step Reasoning Scenario

**Prompt**: "Calculate 15% of 250, multiply by 2, and save the result to a file called calculation.txt"

**Expected Tool Chain**:
1. Compute Tool: Calculate 15% of 250
2. Compute Tool: Multiply result by 2
3. File Tool: Save result to file
4. Agent reasoning: Confirm operation completed

**Demo Value**: Shows sequential tool execution + file operations

## 3. Performance Comparison Scenario

**Purpose**: Demonstrate Rust vs Python performance difference

**Method**:
- Execute 10 simple calculations using Rust backend
- Simulate naive Python execution (2-3x slower)
- Show latency metrics and cache hit rates

**Demo Value**: Quantifies performance benefits of Rust architecture

## 4. Cache Effectiveness Scenario

**Purpose**: Show caching in action

**Method**:
- Execute same API call multiple times
- First call: full execution time
- Subsequent calls: cached response (much faster)
- Display cache hit rates

**Demo Value**: Demonstrates intelligent caching strategy

## 5. Error Handling Scenario

**Prompt**: "Fetch data from invalid API endpoint"

**Expected Behavior**:
- Tool execution fails gracefully
- Agent receives error information
- Provides meaningful error message to user
- System remains stable

**Demo Value**: Shows production-grade error handling
