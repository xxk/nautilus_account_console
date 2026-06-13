import type { AccountSnapshot, OrderEvent, OrderExecutionReports } from "./types";

const API_BASE = "";

export async function fetchAccounts(): Promise<AccountSnapshot[]> {
  const response = await fetch(`${API_BASE}/api/accounts`);
  if (!response.ok) {
    throw new Error(`accounts request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchEvents(accountId: string, cursor = 0): Promise<OrderEvent[]> {
  const response = await fetch(`${API_BASE}/api/accounts/${accountId}/events?cursor=${cursor}`);
  if (!response.ok) {
    throw new Error(`events request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchOrderExecutionReports(
  accountId: string,
  clientOrderId: string
): Promise<OrderExecutionReports> {
  const response = await fetch(
    `${API_BASE}/api/accounts/${accountId}/orders/${clientOrderId}/execution-reports`
  );
  if (!response.ok) {
    throw new Error(`execution reports request failed: ${response.status}`);
  }
  return response.json();
}

export function openEventStream(
  accountId: string,
  cursor: number,
  onEvent: (event: OrderEvent) => void,
  onStatus: (status: "live" | "stale") => void
): EventSource {
  const source = new EventSource(`${API_BASE}/api/accounts/${accountId}/events/stream?cursor=${cursor}`);
  source.addEventListener("open", () => onStatus("live"));
  source.addEventListener("error", () => onStatus("stale"));
  source.addEventListener("order_event", (message) => {
    onEvent(JSON.parse((message as MessageEvent).data) as OrderEvent);
  });
  return source;
}
