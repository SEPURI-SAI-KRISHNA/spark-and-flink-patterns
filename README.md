# ⚡ Spark & Flink Patterns

> Production-grade patterns for building reliable, scalable, and fault-tolerant data pipelines with Apache Spark & Apache Flink.

![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=flat-square&logo=apachespark&logoColor=white)
![Apache Flink](https://img.shields.io/badge/Apache%20Flink-E6526F?style=flat-square&logo=apacheflink&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

This repository focuses on the **recurring problems** encountered in real streaming systems and their **battle-tested solutions** — including the trade-offs each one makes.

## 🎯 Patterns covered

- **Exactly-once semantics** — end-to-end correctness guarantees
- **Late & out-of-order data** — watermarks, allowed lateness
- **Idempotent writes** — safe retries and replays
- **State management & TTL** — bounded, expiring state
- **Backpressure & checkpoints** — stable throughput under load

## 📂 Structure

- [`spark/`](spark/) — Apache Spark patterns
- [`Spark-Flink/`](Spark-Flink/) — cross-engine comparisons & shared patterns
- [`kafka/`](kafka/) — Kafka integration patterns

Each pattern explains **the problem, the solution, and the trade-offs** — not just the code.

---

<sub>📂 Part of my data-engineering work — explore more at **[sepuri-sai-krishna.pages.dev](https://sepuri-sai-krishna.pages.dev)** · by [Sepuri Sai Krishna](https://github.com/SEPURI-SAI-KRISHNA)</sub>
