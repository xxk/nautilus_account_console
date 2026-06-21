import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ib.live.u3028269";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p019-u3028269-real-ui-parity");
const evidencePath = path.resolve(
  "..",
  "docs",
  "acceptance",
  "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
);

function asNumber(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function asText(value: unknown, fallback = "unknown"): string {
  return typeof value === "string" && value.length > 0 ? value : fallback;
}

function formatMoney(value: number | null, currency: string): string {
  if (value === null) {
    return "missing";
  }
  return `${currency} ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

function normalizedOrderStatus(value: unknown): string {
  const normalized = asText(value, "unknown").toLowerCase();
  if (["submitted", "presubmitted", "working", "accepted"].includes(normalized)) {
    return "working";
  }
  if (["cancelled", "canceled"].includes(normalized)) {
    return "canceled";
  }
  return normalized;
}

test("P019 U3028269 real UI parity is blocked until same-slice TWS API source package is ready", async ({
  page
}, testInfo) => {
  const projectionResponse = await page.request.get(
    `http://127.0.0.1:8775/api/mirror/accounts/${encodeURIComponent(accountId)}`
  );
  expect(projectionResponse.ok()).toBeTruthy();
  const projection = await projectionResponse.json();

  await page.goto(`/accounts/${accountId}`);
  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountId);
  await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
  await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);
  await expect(page.getByText(/password=|auth_code=|front=tcp:\/\/|api_key=|secret=/i)).toHaveCount(0);

  mkdirSync(evidenceDir, { recursive: true });
  const screenshot = path.join(evidenceDir, `${testInfo.project.name}-acct-ib-live-u3028269-real-ui-parity.png`);
  await page.screenshot({ fullPage: true, path: screenshot });

  const baseEvidence = {
    schema: "account-console.p019-u3028269-real-ui-parity-evidence.v1",
    proposal_id: "p019-broker-observation-session-foundation",
    account_id: accountId,
    display_alias: "U3028269",
    route: `/accounts/${accountId}`,
    source_kind: projection.source_kind,
    source_ref: projection.source_ref,
    source_checksum: projection.source_checksum,
    projection_checkpoint_id: projection.projection_checkpoint_id,
    projection_checksum: projection.projection_checksum,
    browser_evidence: [
      {
        project: testInfo.project.name,
        screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/")
      }
    ],
    boundaries: {
      raw_secret_values_recorded: false,
      screenshot_used_for_funds_positions: false,
      broker_truth: projection.boundaries.broker_truth === true,
      order_action: projection.boundaries.order_action === true
    }
  };

  if (projection.capabilities.observation.mirror_state !== "ready") {
    await expect(page.getByTestId("tws-funds-blocker")).toBeVisible();
    await expect(page.getByTestId("account-positions-table")).toContainText(
      "No position rows in this fixture projection."
    );
    if (testInfo.project.name === "desktop") {
      writeFileSync(
        evidencePath,
        JSON.stringify(
          {
            ...baseEvidence,
            status: "blocked_waiting_for_real_tws_api_source_package",
            verdict: "blocked",
            blocker_id: projection.source_health.blocker_id ?? "tws_api_readiness_missing",
            blocker_kind: projection.blockers[0]?.type ?? "source_unavailable",
            parity: {
              funds_parity: "blocked",
              positions_parity: "blocked",
              orders_fills_parity: "blocked",
              execution_reports_table_parity: "blocked",
              execution_reports_persistence_parity: "blocked"
            },
            explicit_non_claims: [
              "does_not_prove_real_u3028269_funds",
              "does_not_prove_real_u3028269_positions",
              "does_not_close_real_ui_parity",
              "does_not_use_screenshot_for_funds_positions",
              "does_not_enable_command_capability"
            ]
          },
          null,
          2
        )
      );
    }
    return;
  }

  expect(projection.source_health.api_transport).toBe("ib_tws_api");
  expect(projection.source_health.screenshot_used_for_values).toBe(false);
  expect(projection.boundaries.order_action).toBe(false);
  expect(projection.boundaries.broker_truth).toBe(false);
  expect(projection.balances.length).toBeGreaterThan(0);

  const fundsTable = page.getByTestId("tws-multi-currency-funds-table");
  const currencyBalances = projection.balances.filter((balance: Record<string, unknown>) => balance.currency !== "BASE");
  expect(currencyBalances.length).toBeGreaterThanOrEqual(2);
  expect(currencyBalances.map((balance: Record<string, unknown>) => balance.currency)).toContain("USD");
  await expect(page.getByTestId("tws-currency-balance-row")).toHaveCount(currencyBalances.length);
  for (const balance of currencyBalances) {
    const currency = asText(balance.currency, "USD");
    const cash = asNumber(balance.cash ?? balance.total_cash ?? balance.equity);
    const available = asNumber(balance.available_cash);
    const buyingPower = available;
    const margin = asNumber(balance.margin_used);
    const equity = asNumber(balance.equity ?? balance.net_liquidation_by_currency);
    const unrealizedPnl = asNumber(balance.unrealized_pnl ?? balance.position_profit);

    await expect(fundsTable).toContainText(currency);
    await expect(fundsTable).toContainText(formatMoney(cash, currency));
    await expect(fundsTable).toContainText(formatMoney(available, currency));
    await expect(fundsTable).toContainText(formatMoney(buyingPower, currency));
    await expect(fundsTable).toContainText(formatMoney(margin, currency));
    await expect(fundsTable).toContainText(formatMoney(equity, currency));
    await expect(fundsTable).toContainText(formatMoney(unrealizedPnl, currency));
  }

  const positionRows = page.getByTestId("account-position-projection-row");
  await expect(positionRows).toHaveCount(projection.positions.length);
  for (const [index, position] of projection.positions.entries()) {
    const row = page.getByTestId("account-position-projection-row").nth(index);
    await expect(row).toContainText(asText(position.instrument));
    await expect(row).toContainText(String(position.net_qty ?? "missing"));
    await expect(row).toContainText(String(position.available_qty ?? "missing"));
    await expect(row).toContainText(String(position.avg_price ?? "missing"));
    await expect(row).toContainText(asText(position.source_ref, projection.source_ref));
  }

  const openOrderRows = page.getByTestId("tws-open-order-row");
  await expect(page.getByTestId("tws-open-orders-table")).toBeVisible();
  await expect(page.getByTestId("tws-open-order-count")).toContainText(String(projection.orders.length));
  await expect(openOrderRows).toHaveCount(projection.orders.length);
  for (const [index, order] of projection.orders.entries()) {
    const row = page.getByTestId("tws-open-order-row").nth(index);
    await expect(row).toContainText(asText(order.client_order_id));
    await expect(row).toContainText(asText(order.instrument));
    await expect(row).toContainText(asText(order.side));
    await expect(row).toContainText(normalizedOrderStatus(order.status));
    await expect(row).toContainText(String(order.quantity ?? "missing"));
    await expect(row).toContainText(String(order.filled_quantity ?? "missing"));
    await expect(row).toContainText(String(order.remaining_quantity ?? "missing"));
    await expect(row).toContainText(String(order.limit_price ?? "missing"));
    await expect(row).toContainText(asText(order.source_ref, projection.source_ref));
  }

  const fillRows = page.getByTestId("tws-fill-row");
  await expect(page.getByTestId("tws-fills-table")).toBeVisible();
  await expect(page.getByTestId("tws-fill-count")).toContainText(String(projection.fills.length));
  await expect(fillRows).toHaveCount(projection.fills.length);
  if (projection.fills.length === 0) {
    await expect(page.getByTestId("tws-fill-empty-state")).toContainText("No fill rows in this mirror projection.");
  }
  for (const [index, fill] of projection.fills.entries()) {
    const row = page.getByTestId("tws-fill-row").nth(index);
    await expect(row).toContainText(asText(fill.report_id, asText(fill.trade_id)));
    await expect(row).toContainText(asText(fill.client_order_id));
    await expect(row).toContainText(asText(fill.instrument_id, asText(fill.instrument)));
    await expect(row).toContainText(asText(fill.side));
    await expect(row).toContainText(String(fill.filled_quantity ?? "missing"));
    await expect(row).toContainText(asText(fill.source_ref, projection.source_ref));
  }

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          ...baseEvidence,
          status: "ready_real_tws_api_source_package_ui_parity_checked",
          verdict: "pass",
          parity: {
            funds_parity: "pass",
            positions_parity: "pass",
            orders_fills_parity: projection.orders.length === 0 && projection.fills.length === 0 ? "blocked" : "pass",
            execution_reports_table_parity:
              projection.orders.length === 0 && projection.fills.length === 0 ? "blocked" : "pass",
            execution_reports_persistence_parity: "blocked",
            open_orders_parity: "pass",
            fills_parity: projection.source_health.executions_query_success === true ? "pass" : "blocked"
          },
          compared_against: {
            api_route: `/api/mirror/accounts/${accountId}`,
            balance_count: projection.balances.length,
            rendered_balance_count: currencyBalances.length,
            rendered_balance_currencies: currencyBalances.map((balance: Record<string, unknown>) => balance.currency),
            position_count: projection.positions.length,
            order_count: projection.orders.length,
            rendered_open_order_count: projection.orders.length,
            rendered_open_order_client_order_ids: projection.orders.map((order: Record<string, unknown>) =>
              asText(order.client_order_id)
            ),
            fill_count: projection.fills.length,
            rendered_fill_count: projection.fills.length,
            rendered_fill_report_ids: projection.fills.map((fill: Record<string, unknown>) =>
              asText(fill.report_id, asText(fill.trade_id))
            ),
            execution_report_rows: projection.source_health.execution_report_rows ?? projection.fills.length,
            execution_report_state: projection.source_health.execution_report_state ?? "unknown",
            executions_query_success: projection.source_health.executions_query_success === true,
            executions_complete_history_claimed:
              projection.source_health.executions_readonly_query?.complete_history_claimed === true,
            executions_order_action_sent:
              projection.source_health.executions_readonly_query?.order_action_sent === true
          }
        },
        null,
        2
      )
    );
  }
});
