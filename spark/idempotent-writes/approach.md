# Approach: Make Writes Retry-Safe

Key ideas:
- Deterministic record keys
- Partition-level commits
- Upserts instead of appends

Common techniques:
- MERGE INTO for table formats (Iceberg, Delta)
- Deduplication using primary keys
- Commit markers for batch boundaries

Design assumption:
> The job may run more than once for the same data.
