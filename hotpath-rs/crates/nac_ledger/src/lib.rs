use std::io::{self, Write};

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct HotpathEvent {
    pub event_id: String,
    pub seq: u64,
    pub account_id: String,
    pub event_type: String,
    pub checksum: String,
}

impl HotpathEvent {
    pub fn to_json_line(&self) -> String {
        format!(
            "{{\"event_id\":\"{}\",\"seq\":{},\"account_id\":\"{}\",\"event_type\":\"{}\",\"checksum\":\"{}\"}}\n",
            escape_json(&self.event_id),
            self.seq,
            escape_json(&self.account_id),
            escape_json(&self.event_type),
            escape_json(&self.checksum)
        )
    }
}

pub fn append_jsonl(mut writer: impl Write, events: &[HotpathEvent]) -> io::Result<u64> {
    let mut written = 0_u64;
    for event in events {
        writer.write_all(event.to_json_line().as_bytes())?;
        written += 1;
    }
    Ok(written)
}

fn escape_json(value: &str) -> String {
    value
        .replace('\\', "\\\\")
        .replace('"', "\\\"")
        .replace('\n', "\\n")
}

#[cfg(test)]
mod tests {
    use super::{append_jsonl, HotpathEvent};

    #[test]
    fn appends_json_lines_without_losing_events() {
        let events = vec![
            HotpathEvent {
                event_id: "evt-1".to_string(),
                seq: 1,
                account_id: "paper.demo-01".to_string(),
                event_type: "accepted".to_string(),
                checksum: "sha256:a".to_string(),
            },
            HotpathEvent {
                event_id: "evt-2".to_string(),
                seq: 2,
                account_id: "paper.demo-01".to_string(),
                event_type: "filled".to_string(),
                checksum: "sha256:b".to_string(),
            },
        ];

        let mut output = Vec::new();
        let written = append_jsonl(&mut output, &events).expect("append_jsonl should write");
        let text = String::from_utf8(output).expect("jsonl should be utf8");

        assert_eq!(written, 2);
        assert_eq!(text.lines().count(), 2);
        assert!(text.contains("\"seq\":2"));
    }
}

