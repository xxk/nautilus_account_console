import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.live.025292";
const accountRoute = "/accounts/acct.ctp.live.025292";
const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "legacy-025292-ui-funds-positions-orders"
);
const evidencePath = path.resolve(
  "..",
  "docs",
  "acceptance",
  "2026-06-16-legacy-acct-demo-19053-ctp025292-ui-acceptance-evidence.json"
);

const forbiddenCommandText =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;

function money(value: number) {
  return `CNY ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

test("direct 025292 route renders funds, positions and orders or fails closed", async ({
  page,
}, testInfo) => {
  const projectionResponse = await page.request.get(`/api/mirror/accounts/${encodeURIComponent(accountId)}`);
  expect(projectionResponse.ok()).toBeTruthy();
  const projection = await projectionResponse.json();

  expect(projection.account_id).toBe(accountId);
  expect(projection.display_alias).toBe("025292");
  expect(projection.boundaries.read_only_projection).toBe(true);
  expect(projection.boundaries.order_action).toBe(false);
  expect(projection.boundaries.broker_truth).toBe(false);

  await page.goto(accountRoute);
  await expect(page.getByTestId("terminal-workbench-shell")).toBeVisible();
  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountId);
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText("025292");
  await expect(page.getByTestId("account-selector")).toContainText(accountId);
  await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
  await expect(page.getByText(forbiddenCommandText)).toHaveCount(0);

  mkdirSync(evidenceDir, { recursive: true });
  const screenshot = path.join(evidenceDir, `${testInfo.project.name}-legacy-acct-demo-19053-ctp025292.png`);

  if (projection.source_health.state === "blocked") {
    await expect(page.getByTestId("account-source-health-panel")).toContainText("typed_blocker");
    await expect(page.getByTestId("account-blocker-row")).toContainText("source unavailable");
    await expect(page.getByTestId("account-summary-cash")).toContainText("missing");
    await expect(page.getByTestId("account-positions-table")).toContainText(
      "No position rows in this fixture projection."
    );
    await expect(page.getByTestId("account-bottom-tape")).toContainText(
      "No open order rows in this mirror projection."
    );
    await page.screenshot({ fullPage: true, path: screenshot });
    if (testInfo.project.name === "desktop") {
      writeFileSync(
        evidencePath,
        JSON.stringify(
          {
            schema: "account-console.legacy-025292-ui-acceptance-evidence.v1",
            status: "blocked_waiting_for_025292_account_source_package",
            ui_url: "http://127.0.0.1:5173/accounts/acct.ctp.live.025292",
            tested_route: accountRoute,
            canonical_account_id: accountId,
            display_alias: "025292",
            source_ref: projection.source_ref,
            source_checksum: projection.source_checksum,
            projection_checkpoint_id: projection.projection_checkpoint_id,
            projection_checksum: projection.projection_checksum,
            blocker_id: projection.blockers[0]?.blocker_id ?? "ctp025292_real_login_source_unavailable",
            next_action: projection.blockers[0]?.next_action,
            required_ready_domains: ["funds", "positions", "orders"],
            browser_evidence: [
              {
                project: testInfo.project.name,
                screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/"),
              },
            ],
            explicit_non_claims: [
              "does_not_use_acct_demo_19053_as_canonical_account_id",
              "does_not_treat_market_data_lineage_as_account_funds",
              "does_not_enable_command_capability",
              "does_not_prove_broker_truth",
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

  expect(projection.source_ref).toBe("output/account_capability/ctp-live-025292/source-package.json");
  expect(projection.source_health.state).toBe("ready");
  expect(projection.balances.length).toBeGreaterThan(0);
  expect(projection.positions.length).toBeGreaterThan(0);
  expect(projection.orders.length).toBeGreaterThan(0);

  const balance = projection.balances[0];
  await expect(page.getByTestId("account-source-health-panel")).toContainText("normalized_read_model");
  await expect(page.getByTestId("account-summary-cash")).toContainText(money(balance.equity));
  await expect(page.getByTestId("account-summary-available-cash")).toContainText(money(balance.available_cash));
  await expect(page.getByTestId("account-summary-buying-power")).toContainText(money(balance.available_cash));
  await expect(page.getByTestId("account-summary-margin")).toContainText(money(balance.margin_used));
  await expect(page.getByTestId("account-summary-position-count")).toContainText(String(projection.positions.length));

  for (const position of projection.positions) {
    await expect(page.getByTestId("account-positions-table")).toContainText(position.instrument);
    await expect(page.getByTestId("account-positions-table")).toContainText(String(position.net_qty));
    await expect(page.getByTestId("account-positions-table")).toContainText(String(position.available_qty));
  }
  for (const order of projection.orders) {
    await expect(page.getByTestId("account-bottom-tape")).toContainText(order.client_order_id);
    await expect(page.getByTestId("account-bottom-tape")).toContainText(order.instrument);
    await expect(page.getByTestId("account-bottom-tape")).toContainText(order.status);
  }
  await expect(page.getByTestId("account-evidence-rail")).toContainText(projection.source_ref);
  await page.screenshot({ fullPage: true, path: screenshot });

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.legacy-025292-ui-acceptance-evidence.v1",
          status: "implementation_browser_evidence",
          ui_url: "http://127.0.0.1:5173/accounts/acct.ctp.live.025292",
          tested_route: accountRoute,
          canonical_account_id: accountId,
          display_alias: "025292",
          source_ref: projection.source_ref,
          source_checksum: projection.source_checksum,
          projection_checkpoint_id: projection.projection_checkpoint_id,
          projection_checksum: projection.projection_checksum,
          source_health_state: projection.source_health.state,
          required_ready_domains: ["funds", "positions", "orders"],
          balances: projection.balances,
          positions: projection.positions,
          orders: projection.orders,
          browser_evidence: [
            {
              project: testInfo.project.name,
              screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/"),
            },
          ],
          explicit_non_claims: [
            "does_not_use_acct_demo_19053_as_canonical_account_id",
            "does_not_enable_command_capability",
            "does_not_prove_broker_truth",
          ],
          verdict: "passed",
        },
        null,
        2
      )
    );
  }
});
