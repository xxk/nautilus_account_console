import { Activity, AlertTriangle, Radio, RefreshCw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { fetchAccounts, fetchEvents, openEventStream } from "./api";
import type { AccountSnapshot, OrderEvent } from "./types";

function formatMoney(value: number): string {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 2
  }).format(value);
}

export function App() {
  const [accounts, setAccounts] = useState<AccountSnapshot[]>([]);
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null);
  const [events, setEvents] = useState<OrderEvent[]>([]);
  const [streamStatus, setStreamStatus] = useState<"live" | "stale">("stale");
  const [error, setError] = useState<string | null>(null);

  const selectedAccount = useMemo(
    () => accounts.find((account) => account.account_id === selectedAccountId) ?? accounts[0],
    [accounts, selectedAccountId]
  );

  useEffect(() => {
    fetchAccounts()
      .then((rows) => {
        setAccounts(rows);
        setSelectedAccountId(rows[0]?.account_id ?? null);
      })
      .catch((reason: unknown) => setError(String(reason)));
  }, []);

  useEffect(() => {
    if (!selectedAccount) {
      return;
    }
    fetchEvents(selectedAccount.account_id)
      .then(setEvents)
      .catch((reason: unknown) => setError(String(reason)));
  }, [selectedAccount?.account_id]);

  useEffect(() => {
    if (!selectedAccount) {
      return;
    }
    const cursor = events.at(-1)?.seq ?? 0;
    const source = openEventStream(
      selectedAccount.account_id,
      cursor,
      (event) => {
        setEvents((current) => {
          if (current.some((row) => row.seq === event.seq)) {
            return current;
          }
          return [...current, event].slice(-500);
        });
      },
      setStreamStatus
    );
    return () => source.close();
  }, [selectedAccount?.account_id]);

  return (
    <main className="shell" data-testid="account-console">
      <header className="topbar">
        <div>
          <h1>Nautilus Account Console</h1>
          <p>Read-only account, order, fill and report message projection.</p>
        </div>
        <div className={`stream-pill ${streamStatus}`} data-testid="event-stream-status">
          <Radio size={16} />
          {streamStatus}
        </div>
      </header>

      {error ? (
        <section className="blocker" data-testid="account-blocker">
          <AlertTriangle size={18} />
          {error}
        </section>
      ) : null}

      <section className="layout">
        <aside className="accounts" data-testid="account-overview">
          <div className="section-title">
            <Activity size={16} />
            Accounts
          </div>
          {accounts.map((account) => (
            <button
              key={account.account_id}
              className={account.account_id === selectedAccount?.account_id ? "account-row selected" : "account-row"}
              data-testid="account-row"
              onClick={() => setSelectedAccountId(account.account_id)}
              type="button"
            >
              <span>{account.account_id}</span>
              <small>{account.account_kind}</small>
            </button>
          ))}
        </aside>

        <section className="detail" data-testid="account-detail">
          {selectedAccount ? (
            <>
              <div className="summary-grid" data-testid="account-summary">
                <Metric label="Equity" value={formatMoney(selectedAccount.equity)} />
                <Metric label="Available" value={formatMoney(selectedAccount.available_cash)} />
                <Metric label="Margin" value={formatMoney(selectedAccount.margin_used)} />
                <Metric label="Last seq" value={String(selectedAccount.last_seq)} />
              </div>

              <div className="tape-header">
                <div className="section-title">
                  <RefreshCw size={16} />
                  Order Event Tape
                </div>
                <span>{events.length} events</span>
              </div>
              <div className="event-tape" data-testid="order-event-tape">
                {events.map((event) => (
                  <article className="event-row" key={event.event_id}>
                    <div className="event-main">
                      <strong>#{event.seq}</strong>
                      <span>{event.event_type}</span>
                      <span>{event.order_status}</span>
                      <span>{event.instrument_id}</span>
                    </div>
                    <div className="event-sub" data-testid="report-msg-drawer">
                      {event.report_msg_excerpt}
                    </div>
                  </article>
                ))}
              </div>
            </>
          ) : (
            <div className="empty">No account snapshots loaded.</div>
          )}
        </section>
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

