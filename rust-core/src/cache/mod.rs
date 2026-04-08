use crate::types::{ToolRequest, ToolResponse};
use lru::LruCache;
use std::num::NonZeroUsize;

pub struct Cache {
    cache: LruCache<String, ToolResponse>,
}

impl Cache {
    pub fn new(capacity: usize) -> Self {
        Self {
            cache: LruCache::new(NonZeroUsize::new(capacity).unwrap()),
        }
    }

    pub fn get(&mut self, key: &str) -> Option<ToolResponse> {
        self.cache.get(key).cloned()
    }

    pub fn put(&mut self, key: String, response: ToolResponse) {
        self.cache.put(key, response);
    }

    pub fn hit_rate(&self) -> f64 {
        if self.cache.cap().get() == 0 {
            0.0
        } else {
            self.cache.len() as f64 / self.cache.cap().get() as f64
        }
    }
}

impl Default for Cache {
    fn default() -> Self {
        Self::new(1000)
    }
}
