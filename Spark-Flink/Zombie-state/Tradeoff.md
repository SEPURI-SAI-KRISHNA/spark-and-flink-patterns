# The Tradeoff
### Pros:

- Stable Memory: Prevents infinite growth; state size becomes predictable.

- Performance: Smaller checkpoints = faster snapshots and recovery.

### Cons:

- Data Loss (Correctness): If a user clicks the ad 25 hours later, but your TTL was 24 hours, the record is dropped (or handled as a "late/orphan" click). You lose that revenue attribution.

- Overhead: In aggressive TTL scenarios, the system spends significant CPU cycles constantly purging expired keys.