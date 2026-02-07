# The Problem

In batch processing, you load data, process it, and free the memory. In streaming, you often need to remember things (State).

Consider a classic "Ad Tech" use case: Join Impressions (View) with Clicks.

- __Flow__: User sees an Ad (Impression) -> Wait -> User Clicks Ad (Click).

- __The Issue__: You store the "Impression" in memory waiting for the "Click" to arrive so you can join them.

- __The Reality__: 99% of users never click the ad.

- __Result__: The "Impression" data sits in your state backend (RocksDB/Memory) forever, waiting for a click that will never come. Over weeks, your state grows to terabytes, checkpoints become massive, recovery takes hours, and eventually, the job crashes due to storage limits. This is "Zombie State."