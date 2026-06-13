import { Activity, AlertTriangle, FileText, Radio, RefreshCw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { fetchAccounts, fetchEvents, fetchOrderExecutionReports, openEventStream } from "./api";
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
  const [selectedClientOrderId, setSelectedClientOrderId] = useState<string | null>(null);
  const [executionReports, setExecutionReports] = useState<OrderEvent[]>([]);
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
      .then((rows) => {
        setEvents(rows);
        setSelectedClientOrderId(rows[0]?.client_order_id ?? null);
      })
      .catch((reason: unknown) => setError(String(reason)));
  }, [selectedAccount?.account_id]);

  useEffect(() => {
    if (!selectedAccount || !selectedClientOrderId) {
      setExecutionReports([]);
      return;
    }
    fetchOrderExecutionReports(selectedAccount.account_id, selectedClientOrderId)
      .then((payload) => setExecutionReports(payload.reports))
      .catch((reason: unknown) => setError(String(reason)));
  }, [selectedAccount?.account_id, selectedClientOrderId]);

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
          setSelectedClientOrderId((selected) => selected ?? event.client_order_id);
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

              <div className="order-workspace">
                <div>
                  <div className="tape-header">
                    <div className="section-title">
                      <RefreshCw size={16} />
                      Order Event Tape
                    </div>
                    <span>{events.length} events</span>
                  </div>
                  <div className="event-tape" data-testid="order-event-tape">
                    {events.map((event) => (
                      <button
                        className={
                          event.client_order_id === selectedClientOrderId
                            ? "event-row selected"
                            : "event-row"
                        }
                        key={event.event_id}
                        onClick={() => setSelectedClientOrderId(event.client_order_id)}
                        type="button"
                      >
                        <div className="event-main">
                          <strong>#{event.seq}</strong>
                          <span>{event.client_order_id}</span>
                          <span>{event.order_status}</span>
                          <span>{event.instrument_id}</span>
                        </div>
                        <div className="event-sub">{event.report_msg_excerpt}</div>
                      </button>
                    ))}
                  </div>
                </div>

                <aside className="report-panel" data-testid="order-execution-reports">
                  <div className="section-title">
                    <FileText size={16} />
                    Order Execution Reports
                  </div>
                  {selectedClientOrderId ? (
                    <div className="selected-order">
                      <span>Selected order</span>
                      <strong>{selectedClientOrderId}</strong>
                    </div>
                  ) : null}
                  <div className="report-list" data-testid="report-msg-drawer">
                    {executionReports.map((report) => (
                      <article className="report-row" data-testid="execution-report-row" key={report.event_id}>
                        <div className="report-row-head">
                          <strong>#{report.seq}</strong>
                          <span>{report.event_type}</span>
                          <span>{report.order_status}</span>
                        </div>
                        <dl>
                          <div>
                            <dt>Report type</dt>
                            <dd>{report.report_msg_type ?? "-"}</dd>
                          </div>
                          <div>
                            <dt>Latency</dt>
                            <dd>{report.latency_ms ?? "-"} ms</dd>
                          </div>
                          <div>
                            <dt>Ref</dt>
                            <dd>{report.report_msg_ref ?? "-"}</dd>
                          </div>
                          <div>
                            <dt>Checksum</dt>
                            <dd>{report.report_msg_checksum ?? "-"}</dd>
                          </div>
                        </dl>
                        <p>{report.report_msg_excerpt}</p>
                      </article>
                    ))}
                    {executionReports.length === 0 ? (
                      <div className="empty">Select an order to inspect execution reports.</div>
                    ) : null}
                  </div>
                </aside>
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
