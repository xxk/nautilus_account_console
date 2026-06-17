import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "simulated-001";
const accountUid = "sandbox-paper.simulated-001";
const legacyRoute = "/accounts/acct.demo-19053";
const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "legacy-simulated-001-ag2612"
);
const evidencePath = path.resolve(
  "..",
  "docs",
  "acceptance",
  "2026-06-16-legacy-acct-demo-19053-simulated-001-ag2612-ui-acceptance-evidence.json"
);

const forbiddenCommandText =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;

function money(value: number) {
  return `CNY ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

test("legacy acct.demo-19053 route renders Simulated 001 ag2612 buy-one projection", async ({
  page,
}, testInfo) => {
  const projectionResponse = await page.request.get(`/api/mirror/accounts/${encodeURIComponent(accountId)}`);
  expect(projectionResponse.ok()).toBeTruthy();
  const projection = await projectionResponse.json();

  expect(projection.account_id).toBe(accountId);
  expect(projection.display_alias).toBe("Simulated 001");
  expect(projection.source_kind).toBe("nautilus_sandbox_paper");
  expect(projection.source_health.account_uid).toBe(accountUid);
  expect(projection.source_health.ledger_type).toBe("simulated_sandbox_ledger");
  expect(projection.source_health.broker_order_submission).toBe(false);
  expect(projection.boundaries.read_only_projection).toBe(true);
  expect(projection.boundaries.order_action).toBe(false);
  expect(projection.boundaries.broker_truth).toBe(false);
  expect(projection.balances.length).toBeGreaterThan(0);
  expect(projection.positions.length).toBeGreaterThan(0);
  expect(projection.orders.length).toBeGreaterThan(0);

  const balance = projection.balances[0];
  const position = projection.positions.find((row: Record<string, unknown>) => row.instrument === "ag2612");
  const order = projection.orders.find(
    (row: Record<string, unknown>) => row.client_order_id === "simulated-001-ag2612-buy-1-001"
  );
  expect(position).toBeTruthy();
  expect(order).toBeTruthy();
  expect(position.net_qty).toBe(1);
  expect(position.available_qty).toBe(1);
  expect(order.side).toBe("buy");
  expect(order.quantity).toBe(1);
  expect(order.filled_quantity).toBe(1);
  expect(order.status).toBe("filled");

  await page.goto(legacyRoute);
  await expect(page.getByTestId("terminal-workbench-shell")).toBeVisible();
  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountId);
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText("Simulated 001");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountUid);
  await expect(page.getByTestId("account-source-health-panel")).toContainText("Nautilus Sandbox Paper");
  await expect(page.getByTestId("account-source-health-panel")).toContainText("simulated ledger only");
  await expect(page.getByTestId("account-source-health-panel")).toContainText("disabled");
  await expect(page.getByTestId("account-summary-cash")).toContainText(money(balance.equity));
  await expect(page.getByTestId("account-summary-available-cash")).toContainText(money(balance.available_cash));
  await expect(page.getByTestId("account-summary-margin")).toContainText(money(balance.margin_used));
  await expect(page.getByTestId("account-summary-position-count")).toContainText("1");
  await expect(page.getByTestId("account-positions-table")).toContainText("ag2612");
  await expect(page.getByTestId("account-positions-table")).toContainText("LONG");
  await expect(page.getByTestId("account-positions-table")).toContainText("1");
  await expect(page.getByTestId("account-bottom-tape")).toContainText("simulated-001-ag2612-buy-1-001");
  await expect(page.getByTestId("account-bottom-tape")).toContainText("ag2612");
  await expect(page.getByTestId("account-bottom-tape")).toContainText("BUY");
  await expect(page.getByTestId("account-bottom-tape")).toContainText("filled");
  await expect(page.getByTestId("account-order-execution-report")).toContainText(
    "simulated-001-ag2612-buy-1-001"
  );
  await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
  await expect(page.getByText(forbiddenCommandText)).toHaveCount(0);

  mkdirSync(evidenceDir, { recursive: true });
  const screenshot = path.join(evidenceDir, `${testInfo.project.name}-legacy-simulated-001-ag2612.png`);
  await page.screenshot({ fullPage: true, path: screenshot });

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.legacy-simulated-001-ag2612-ui-acceptance-evidence.v1",
          status: "implementation_browser_evidence",
          legacy_url: "http://127.0.0.1:5173/accounts/acct.demo-19053",
          tested_route: legacyRoute,
          canonical_account_id: accountId,
          account_uid: accountUid,
          display_alias: "Simulated 001",
          scenario: "sandbox_paper_buy_one_ag2612",
          source_ref: projection.source_ref,
          source_checksum: projection.source_checksum,
          projection_checkpoint_id: projection.projection_checkpoint_id,
          projection_checksum: projection.projection_checksum,
          balance,
          position,
          order,
          browser_evidence: [
            {
              project: testInfo.project.name,
              screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/"),
            },
          ],
          explicit_non_claims: [
            "ui_does_not_submit_order",
            "ui_does_not_write_sandbox_ledger_truth",
            "ui_does_not_enable_command_capability",
            "sandbox_projection_does_not_prove_broker_truth",
          ],
          verdict: "passed",
        },
        null,
        2
      )
    );
  }
});
