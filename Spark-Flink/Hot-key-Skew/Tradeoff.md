# The Tradeoff


## Pros:

- __Eliminates OOM__: No single node is overwhelmed.

- __Massive Parallelism__: Utilizing the full cluster for the heavy lifting.

## Cons:

- __Increased Network Shuffle__: You are forcing data to move across the network twice (once for the salted key, once for the final key).

- __Complexity__: The code is harder to read and maintain than a simple groupBy.

- __Latency (Flink)__: In streaming, this adds an extra layer of windowing/state, potentially increasing end-to-end latency slightly.