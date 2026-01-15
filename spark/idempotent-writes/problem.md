# Problem: Non-Idempotent Writes in Distributed Jobs

Spark jobs can fail and retry at any point due to:
- Executor failures
- Network issues
- Preemptions
- Manual restarts

If writes are not idempotent, retries can produce:
- Duplicate records
- Corrupted aggregates
- Inconsistent downstream data
