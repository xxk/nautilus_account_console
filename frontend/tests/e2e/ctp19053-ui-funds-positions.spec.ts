import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "ctp19053-ui-funds-positions"
);
const evidencePath = path.resolve(
  "..",
  "docs",
  "acceptance",
  "2026-06-15-ctp19053-real-login-ui-acceptance-evidence.json"
);

function money(value: number) {
  return `CNY ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

test("acct.ctp.paper.19053 UI uses real-login source package or fails closed", async ({ page }, testInfo) => {
  const accountId = "acct.ctp.paper.19053";
  const projectionResponse = await page.request.get(`/api/mirror/accounts/${encodeURIComponent(accountId)}`);
  expect(projectionResponse.ok()).toBeTruthy();
  const projection = await projectionResponse.json();

  expect(projection.account_id).toBe(accountId);
  expect(projection.display_alias).toBe("19053");
  expect(projection.boundaries.read_only_projection).toBe(true);
  expect(projection.boundaries.order_action).toBe(false);
  expect(projection.boundaries.broker_truth).toBe(false);

  await page.goto(`/accounts/${accountId}`);
  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountId);
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText("19053");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
  await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);

  mkdirSync(evidenceDir, { recursive: true });
  const screenshot = path.join(evidenceDir, `${testInfo.project.name}-acct-ctp-paper-19053.png`);

  if (projection.source_health.state === "blocked") {
    await expect(page.getByTestId("account-source-health-panel")).toContainText("typed_blocker");
    await expect(page.getByTestId("account-blocker-row")).toContainText("source unavailable");
    await expect(page.getByTestId("account-summary-cash")).toContainText("missing");
    await expect(page.getByTestId("account-positions-table")).toContainText(
      "No position rows in this fixture projection."
    );
    await page.screenshot({ fullPage: true, path: screenshot });
    if (testInfo.project.name === "desktop") {
      writeFileSync(
        evidencePath,
        JSON.stringify(
          {
            schema: "account-console.ctp19053-real-login-ui-acceptance-evidence.v1",
            status: "blocked_waiting_for_real_login_source_package",
            account_id: accountId,
            display_alias: "19053",
            route: `/accounts/${accountId}`,
            source_ref: projection.source_ref,
            source_checksum: projection.source_checksum,
            projection_checkpoint_id: projection.projection_checkpoint_id,
            projection_checksum: projection.projection_checksum,
            blocker_id: projection.blockers[0]?.blocker_id ?? "ctp19053_real_login_source_unavailable",
            next_action: projection.blockers[0]?.next_action,
            browser_evidence: [
              {
                project: testInfo.project.name,
                screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/"),
              },
            ],
            explicit_non_claims: [
              "does_not_display_repo_local_sample_as_real_account",
              "does_not_prove_current_broker_truth_without_external_source_package",
              "does_not_enable_command_capability",
              "does_not_submit_orders",
            ],
            verdict: "blocked",
          },
          null,
          2
        )
      );
    }
    return;
  }

  expect(projection.source_ref).toBe("output/account_capability/ctp-paper-19053/source-package.json");
  expect(projection.source_health.state).toBe("ready");
  const balance = projection.balances[0];
  expect(balance).toBeTruthy();
  expect(balance.currency).toBe("CNY");
  const positions = projection.positions;
  expect(Array.isArray(positions)).toBeTruthy();
  expect(projection.source_health.open_order_rows).toBe(projection.orders.length);
  expect(projection.source_health.fill_rows).toBe(projection.fills.length);

  await expect(page.getByTestId("account-source-health-panel")).toContainText("normalized_read_model");
  await expect(page.getByTestId("account-summary-cash")).toContainText(money(balance.equity));
  await expect(page.getByTestId("account-summary-available-cash")).toContainText(money(balance.available_cash));
  await expect(page.getByTestId("account-summary-buying-power")).toContainText(money(balance.available_cash));
  await expect(page.getByTestId("account-summary-margin")).toContainText(money(balance.margin_used));
  await expect(page.getByTestId("account-summary-unrealized-pnl")).toContainText(money(balance.position_profit));
  await expect(page.getByTestId("account-summary-position-count")).toContainText(String(positions.length));

  for (const position of positions) {
    const table = page.getByTestId("account-positions-table");
    await expect(table).toContainText(position.instrument);
    await expect(table).toContainText(String(position.net_qty));
    await expect(table).toContainText(String(position.available_qty));
    await expect(table).toContainText(position.source_ref);
  }
  await expect(page.getByTestId("tws-open-orders-table")).toBeVisible();
  await expect(page.getByTestId("tws-open-order-count")).toContainText(String(projection.orders.length));
  if (projection.orders.length === 0) {
    await expect(page.getByTestId("tws-open-order-empty-state")).toContainText(
      "No open order rows in this mirror projection."
    );
  } else {
    await expect(page.getByTestId("tws-open-order-row")).toHaveCount(projection.orders.length);
    for (const order of projection.orders) {
      await expect(page.getByTestId("tws-open-orders-table")).toContainText(order.instrument);
      await expect(page.getByTestId("tws-open-orders-table")).toContainText(order.source_ref);
    }
  }
  await expect(page.getByTestId("tws-fills-table")).toBeVisible();
  await expect(page.getByTestId("tws-fill-count")).toContainText(String(projection.fills.length));
  if (projection.fills.length === 0) {
    await expect(page.getByTestId("tws-fill-empty-state")).toContainText("No fill rows in this mirror projection.");
  } else {
    await expect(page.getByTestId("tws-fill-row")).toHaveCount(projection.fills.length);
    for (const fill of projection.fills) {
      await expect(page.getByTestId("tws-fills-table")).toContainText(fill.instrument);
      await expect(page.getByTestId("tws-fills-table")).toContainText(fill.source_ref);
    }
  }
  await expect(page.getByTestId("account-evidence-rail")).toContainText(projection.source_ref);
  await page.screenshot({ fullPage: true, path: screenshot });

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.ctp19053-real-login-ui-acceptance-evidence.v1",
          status: "implementation_browser_evidence",
          account_id: accountId,
          display_alias: "19053",
          route: `/accounts/${accountId}`,
          source_ref: projection.source_ref,
          source_checksum: projection.source_checksum,
          projection_checkpoint_id: projection.projection_checkpoint_id,
          projection_checksum: projection.projection_checksum,
          observed_at: projection.source_health.observed_at,
          source_mode: projection.source_mode,
          source_health_state: projection.source_health.state,
          comparison_basis: "real-login read-only CTP account and position queries via source package",
          funds_parity: "pass",
          positions_parity: "pass",
          open_orders_parity: "pass",
          fills_parity: "pass",
          balances: projection.balances,
          positions: projection.positions,
          orders: projection.orders,
          fills: projection.fills,
          order_count: projection.orders.length,
          rendered_open_order_count: projection.orders.length,
          open_orders_state: projection.source_health.open_orders_state,
          fill_count: projection.fills.length,
          rendered_fill_count: projection.fills.length,
          fills_state: projection.source_health.fills_state,
          td_order_truth_login_success: projection.source_health.td_order_truth_login_success === true,
          td_order_truth_ready: projection.source_health.td_order_truth_ready === true,
          td_order_truth_observed_order_event_count:
            projection.source_health.td_order_truth_observed_order_event_count,
          td_order_truth_observed_trade_event_count:
            projection.source_health.td_order_truth_observed_trade_event_count,
          browser_evidence: [
            {
              project: testInfo.project.name,
              screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/"),
            },
          ],
          explicit_non_claims: [
            "does_not_enable_command_capability",
            "does_not_submit_orders",
          ],
          verdict: "passed",
        },
        null,
        2
      )
    );
  }
});
