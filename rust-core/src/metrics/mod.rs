use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

pub struct Metrics {
    pub total_requests: Arc<AtomicU64>,
    pub total_execution_time_ms: Arc<AtomicU64>,
    pub cache_hits: Arc<AtomicU64>,
    pub cache_misses: Arc<AtomicU64>,
    pub success_count: Arc<AtomicU64>,
    pub failure_count: Arc<AtomicU64>,
}

impl Metrics {
    pub fn new() -> Self {
        Self {
            total_requests: Arc::new(AtomicU64::new(0)),
            total_execution_time_ms: Arc::new(AtomicU64::new(0)),
            cache_hits: Arc::new(AtomicU64::new(0)),
            cache_misses: Arc::new(AtomicU64::new(0)),
            success_count: Arc::new(AtomicU64::new(0)),
            failure_count: Arc::new(AtomicU64::new(0)),
        }
    }

    pub fn record_request(&self) {
        self.total_requests.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_execution_time(&self, time_ms: u64) {
        self.total_execution_time_ms.fetch_add(time_ms, Ordering::Relaxed);
    }

    pub fn record_cache_hit(&self) {
        self.cache_hits.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_cache_miss(&self) {
        self.cache_misses.fetch_add(1, Ordering::Relaxed);
    }

    pub fn increment_cache_hits(&self) {
        self.record_cache_hit();
    }

    pub fn increment_success_count(&self) {
        self.success_count.fetch_add(1, Ordering::Relaxed);
    }

    pub fn increment_failure_count(&self) {
        self.failure_count.fetch_add(1, Ordering::Relaxed);
    }

    pub fn average_execution_time_ms(&self) -> f64 {
        let requests = self.total_requests.load(Ordering::Relaxed);
        if requests == 0 {
            0.0
        } else {
            self.total_execution_time_ms.load(Ordering::Relaxed) as f64 / requests as f64
        }
    }

    pub fn cache_hit_rate(&self) -> f64 {
        let hits = self.cache_hits.load(Ordering::Relaxed);
        let misses = self.cache_misses.load(Ordering::Relaxed);
        let total = hits + misses;
        if total == 0 {
            0.0
        } else {
            hits as f64 / total as f64
        }
    }

    pub fn get_stats(&self) -> serde_json::Value {
        serde_json::json!({
            "total_requests": self.total_requests.load(Ordering::Relaxed),
            "total_execution_time_ms": self.total_execution_time_ms.load(Ordering::Relaxed),
            "cache_hits": self.cache_hits.load(Ordering::Relaxed),
            "cache_misses": self.cache_misses.load(Ordering::Relaxed),
            "success_count": self.success_count.load(Ordering::Relaxed),
            "failure_count": self.failure_count.load(Ordering::Relaxed),
            "average_execution_time_ms": self.average_execution_time_ms(),
            "cache_hit_rate": self.cache_hit_rate()
        })
    }
}

impl Default for Metrics {
    fn default() -> Self {
        Self::new()
    }
}
