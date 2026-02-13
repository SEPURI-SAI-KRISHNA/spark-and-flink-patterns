# CODE

# Spark

```
from pyspark.sql.functions import expr

# 1. Define Watermarks (Allow 10 mins late data)
# Without this, Spark will keep state forever!
impressionsWithWatermark = impressions \
  .withWatermark("impressionTime", "10 minutes") 

clicksWithWatermark = clicks \
  .withWatermark("clickTime", "10 minutes")

# 2. Join with Time Constraint (The "TTL")
# Logic: Click must occur AFTER Impression AND within 1 hour of Impression.
# If clickTime > impressionTime + 1 hour, the state is dropped/ignored.
joinedStream = impressionsWithWatermark.join(
  clicksWithWatermark,
  expr("""
    impressionId = clickId AND 
    clickTime >= impressionTime AND 
    clickTime <= impressionTime + interval 1 hour
  """)
)

# 3. Output
query = joinedStream \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
```


# Flink

```
class ImpressionClickJoin extends KeyedCoProcessFunction<String, Impression, Click, JoinedEvent> {

    // State to hold the Impression waiting for a click
    // We assume 1 impression per ID for simplicity
    private ValueState<Impression> impressionState;
    
    // Constant: How long do we wait?
    private final long TTL_MS = 24 * 60 * 60 * 1000; // 24 Hours

    @Override
    public void open(Configuration parameters) {
        // OPTION 1: Native State TTL (The "Lazy" cleanup)
        // Flink will clean this up in the background if not accessed
        StateTtlConfig ttlConfig = StateTtlConfig
            .newBuilder(Time.milliseconds(TTL_MS))
            .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
            .cleanupFullSnapshot()
            .build();

        ValueStateDescriptor<Impression> desc = new ValueStateDescriptor<>("impression", Impression.class);
        desc.enableTimeToLive(ttlConfig);
        impressionState = getRuntimeContext().getState(desc);
    }

    // Handle Impression Stream
    @Override
    public void processElement1(Impression imp, Context ctx, Collector<JoinedEvent> out) {
        // 1. Store the impression
        impressionState.update(imp);
        
        // OPTION 2: Timer-based (The "Aggressive" cleanup)
        // Register a timer to wake us up in 24 hours to delete this if no click comes
        long timerTimestamp = ctx.timestamp() + TTL_MS;
        ctx.timerService().registerEventTimeTimer(timerTimestamp);
    }

    // Handle Click Stream
    @Override
    public void processElement2(Click click, Context ctx, Collector<JoinedEvent> out) {
        Impression imp = impressionState.value();
        
        if (imp != null) {
            // MATCH FOUND! Emit result
            out.collect(new JoinedEvent(imp, click));
            
            // CRITICAL: Clear the state immediately. Don't wait for TTL.
            impressionState.clear();
            
            // Optimization: You could delete the timer here to save overhead, 
            // but usually valid to let it fire and do nothing.
        } else {
            // ORPHAN CLICK: The impression expired or never arrived. 
            // Log to "Late Data" side output.
        }
    }

    // The Garbage Collector
    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<JoinedEvent> out) {
        // If the state still exists when timer fires, it means no click arrived.
        if (impressionState.value() != null) {
            impressionState.clear(); // DELETE THE ZOMBIE
        }
    }
}
```