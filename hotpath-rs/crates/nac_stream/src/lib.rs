use nac_ledger::HotpathEvent;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EventBatch {
    pub first_seq: u64,
    pub last_seq: u64,
    pub events: Vec<HotpathEvent>,
}

pub fn batch_by_count(events: Vec<HotpathEvent>, max_batch_size: usize) -> Vec<EventBatch> {
    assert!(max_batch_size > 0, "max_batch_size must be positive");

    events
        .chunks(max_batch_size)
        .map(|chunk| EventBatch {
            first_seq: chunk.first().map(|event| event.seq).unwrap_or_default(),
            last_seq: chunk.last().map(|event| event.seq).unwrap_or_default(),
            events: chunk.to_vec(),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use nac_ledger::HotpathEvent;

    use super::batch_by_count;

    #[test]
    fn batches_events_without_reordering() {
        let events = (1..=5)
            .map(|seq| HotpathEvent {
                event_id: format!("evt-{seq}"),
                seq,
                account_id: "paper.demo-01".to_string(),
                event_type: "accepted".to_string(),
                checksum: format!("sha256:{seq}"),
            })
            .collect();

        let batches = batch_by_count(events, 2);

        assert_eq!(batches.len(), 3);
        assert_eq!(batches[0].first_seq, 1);
        assert_eq!(batches[0].last_seq, 2);
        assert_eq!(batches[2].first_seq, 5);
        assert_eq!(batches[2].events.len(), 1);
    }
}

