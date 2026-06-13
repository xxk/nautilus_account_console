use nac_ledger::HotpathEvent;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RawReport {
    pub account_id: String,
    pub report_id: String,
    pub report_type: String,
}

pub fn normalize_report(seq: u64, report: RawReport) -> HotpathEvent {
    let checksum = stable_checksum(seq, &report.account_id, &report.report_id, &report.report_type);
    HotpathEvent {
        event_id: format!("evt-{}-{}", report.account_id, seq),
        seq,
        account_id: report.account_id,
        event_type: report.report_type,
        checksum,
    }
}

fn stable_checksum(seq: u64, account_id: &str, report_id: &str, report_type: &str) -> String {
    let mut hash = 1469598103934665603_u64;
    for byte in format!("{seq}|{account_id}|{report_id}|{report_type}").bytes() {
        hash ^= u64::from(byte);
        hash = hash.wrapping_mul(1099511628211);
    }
    format!("fnv64:{hash:016x}")
}

#[cfg(test)]
mod tests {
    use super::{normalize_report, RawReport};

    #[test]
    fn normalizes_raw_report_to_hotpath_event() {
        let event = normalize_report(
            7,
            RawReport {
                account_id: "paper.demo-01".to_string(),
                report_id: "r-7".to_string(),
                report_type: "accepted".to_string(),
            },
        );

        assert_eq!(event.seq, 7);
        assert_eq!(event.account_id, "paper.demo-01");
        assert_eq!(event.event_type, "accepted");
        assert!(event.checksum.starts_with("fnv64:"));
    }
}

