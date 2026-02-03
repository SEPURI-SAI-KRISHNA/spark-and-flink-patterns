# CODE

## The "Naive" Approach (Fails):

### This crashes the worker handling 'Justin_Bieber'

```
df.groupBy("user_id").count()
```


## The "Salting" Approach:

## Spark
```
# CONFIG: Salt factor (N) - number of splits for the hot key
N = 10

# STEP 1: Add Salt
# We create a new column 'salted_key' by appending a random number (0 to N-1)
# Function: concat(user_id, "_", random(0, N-1))
df_salted = df.withColumn("salt", random(0, N)) \
              .withColumn("salted_key", concat(col("user_id"), lit("_"), col("salt")))

# STEP 2: First Aggregation (Heavy Lifting)
# This runs in parallel across the cluster.
# 'Justin_1' goes to Node A, 'Justin_2' goes to Node B, etc.
df_partial = df_salted.groupBy("salted_key").count().withColumnRenamed("count", "partial_count")

# STEP 3: Remove Salt
# We strip the suffix to get the original key back
df_unsalted = df_partial.withColumn("original_user_id", split(col("salted_key"), "_")[0])

# STEP 4: Final Aggregation (Lightweight)
# Now we just sum up the partial counts.
# instead of summing 100M rows, we are summing just N (10) rows for Justin.
df_final = df_unsalted.groupBy("original_user_id").sum("partial_count")
```

## Flink

```
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;
import java.util.Random;

// Input: Tuple2<String, Integer> -> (Key, 1)
DataStream<Tuple2<String, Integer>> inputStream = ...;

int saltFactor = 10;
Random rand = new Random();

// PHASE 1: SALT & DISTRIBUTE
DataStream<Tuple2<String, Integer>> partialCounts = inputStream
    .map(event -> {
        // Append random suffix: "Justin" -> "Justin_3"
        String saltedKey = event.f0 + "_" + rand.nextInt(saltFactor);
        return Tuple2.of(saltedKey, event.f1);
    })
    .keyBy(value -> value.f0) // Distribute based on salted key (Perfect Balance)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
    .sum(1); // Partial Count

// PHASE 2: MERGE
DataStream<Tuple2<String, Integer>> finalCounts = partialCounts
    .map(event -> {
        // Strip suffix: "Justin_3" -> "Justin"
        String originalKey = event.f0.substring(0, event.f0.lastIndexOf("_"));
        return Tuple2.of(originalKey, event.f1);
    })
    .keyBy(value -> value.f0) // Distribute based on original key (Light Load)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
    .sum(1); // Final Sum

finalCounts.print();
```

__Scenario__: We want to count events per key in a streaming window. One key is hot. Logic:

- __Map__: Append random suffix (key -> key_random(0-9)).

- __KeyBy (Salted)__: Distribute heavily on the salted key.

- __Window & Aggregate__: Count partial results.

- __Map__: Strip the suffix (key_random(0-9) -> key).

- __KeyBy (Original)__: Distribute normally (now dealing with much less data).

- __Window & Aggregate__: Sum the partial counts.