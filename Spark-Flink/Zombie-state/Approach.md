# The Approach: State TTL (Time-To-Live)
You must define a "survival window" for your data. If the matching event doesn't arrive within X hours, you assume it never will and delete the partial state.

There are two ways to implement this:

- __Engine Native__: Configure a global TTL on the State Descriptor (Flink) or Watermark delay (Spark).

- __Custom Logic (Timer Service)__: Register a timer to "wake up" the process and clean specific keys if they haven't been matched.