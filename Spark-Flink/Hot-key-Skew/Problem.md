# The Problem

In distributed systems, data is partitioned by a key (e.g., user_id, region_id) so that all data for a specific key ends up on the same worker node.

The "Ideal" scenario assumes data is evenly distributed. The Real World scenario is that data follows a "Power Law" (Zipfian distribution).

- __Scenario__: You are aggregating tweet counts by user_id.

- __Issue__: 99% of users have 10 tweets. One user (e.g., "Justin Bieber" or a bot account) has 100 million tweets.

- __Result__: The worker node assigned the "Justin Bieber" key gets 100GB of data, while other nodes get 10MB. The "Justin" node runs out of memory (OOM) or takes 10 hours to finish while the other 99 nodes sit idle. This is called a straggler.

