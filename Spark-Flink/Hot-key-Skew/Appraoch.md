# The Approach

### Salting
To fix this, we artificially break the "Hot Key" into smaller, manageable chunks so they can be processed in parallel across multiple nodes, and then we combine the results at the end.

- Phase 1 (Local Aggregation with Salt): Add a random suffix (a "salt") to the key (e.g., Justin_1, Justin_2... Justin_10). This forces the data for "Justin" to be spread across 10 different nodes.

- Phase 2 (Global Aggregation): Aggregate the data based on the salted key.

- Phase 3 (Final Merge): Remove the salt and aggregate one last time to get the true total.