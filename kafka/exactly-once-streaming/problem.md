# Problem: Duplicate Processing in Streaming Pipelines

Kafka provides at-least-once delivery by default.

Failures can cause:
- Message reprocessing
- Duplicate writes
- Incorrect aggregates

End-to-end exactly-once is hard because it spans:
- Kafka
- Stream processor
- External sinks
