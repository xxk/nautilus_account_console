import { Clipboard } from "lucide-react";

export function formatLabel(value: string): string {
  return value.replaceAll("_", " ");
}

export function stateTone(value: string): string {
  if (value === "blocked" || value === "gap" || value === "missing") {
    return "blocked";
  }
  if (value === "stale") {
    return "stale";
  }
  if (value === "partial" || value === "warning") {
    return "partial";
  }
  if (value === "empty") {
    return "empty";
  }
  return "healthy";
}

export function StateBadge({ value }: { value: string }) {
  return <span className={`state-badge ${stateTone(value)}`}>{formatLabel(value)}</span>;
}

export function CopyableCode({ label, value }: { label: string; value: string }) {
  function copyValue() {
    if (navigator.clipboard) {
      void navigator.clipboard.writeText(value);
    }
  }

  return (
    <span className="copyable-code">
      <code>{value}</code>
      <button aria-label={`Copy ${label}`} onClick={copyValue} title={`Copy ${label}`} type="button">
        <Clipboard size={13} />
      </button>
    </span>
  );
}
