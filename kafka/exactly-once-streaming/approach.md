# Approach: Coordinated Offsets and State

Key principles:
- Offset commits must align with state updates
- Writes must be transactional or idempotent

Common strategies:
- Kafka transactions (producer side)
- Flink checkpoints with KafkaSource
- Idempotent sinks (MERGE, UPSERT)

Exactly-once breaks at system boundaries, not inside Kafka.
