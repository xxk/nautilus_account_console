import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p019-u3028269-blocked-ui");
const evidencePath = path.resolve(
  "..",
  "docs",
  "acceptance",
  "2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json"
);

test("P019 U3028269 route renders Account Mirror TWS API readiness blocker without command drift", async ({ page }, testInfo) => {
  const accountId = "acct.ib.live.u3028269";
  const projectionResponse = await page.request.get(
    `http://127.0.0.1:8775/api/mirror/accounts/${encodeURIComponent(accountId)}`
  );
  expect(projectionResponse.ok()).toBeTruthy();
  const projection = await projectionResponse.json();

  expect(projection.account_id).toBe(accountId);
  expect(projection.display_alias).toBe("U3028269");
  expect(projection.source_kind).toBe("ib_tws_observation");
  expect(projection.capabilities.command.enabled).toBe(false);
  expect(projection.capabilities.observation.mirror_state).toBe("blocked");
  expect(projection.source_health.blocker_id).toBe("tws_api_readiness_missing");
  expect(projection.source_health.raw_secret_values_recorded).toBe(false);
  expect(projection.balances).toEqual([]);
  expect(projection.positions).toEqual([]);
  expect(projection.orders).toEqual([]);
  expect(projection.fills).toEqual([]);
  expect(projection.boundaries.broker_truth).toBe(false);
  expect(projection.boundaries.order_action).toBe(false);

  await page.goto(`/accounts/${accountId}`);
  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountId);
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText("U3028269");
  await expect(page.getByTestId("account-source-health-panel")).toContainText("typed_blocker");
  await expect(page.getByTestId("account-source-health-panel")).toContainText("ib_tws_observation");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
  await expect(page.getByTestId("tws-multi-currency-funds-table")).toBeVisible();
  await expect(page.getByTestId("tws-multi-currency-funds-table")).toContainText("Currency");
  await expect(page.getByTestId("tws-multi-currency-funds-table")).toContainText("Buying power");
  await expect(page.getByTestId("tws-multi-currency-funds-table")).toContainText("Equity/net liq");
  await expect(page.getByTestId("tws-funds-blocker")).toContainText("source unavailable");
  await expect(page.getByTestId("tws-funds-blocker")).toContainText("tws-api-readiness-probe.json");
  await expect(page.getByTestId("tws-fx-provenance")).toContainText("source unavailable");
  await expect(page.getByTestId("tws-base-currency-rollup")).toContainText("blocked until source package");
  await expect(page.getByTestId("account-positions-table")).toContainText(
    "No position rows in this fixture projection."
  );
  await expect(page.getByTestId("account-bottom-tape")).toContainText("No order rows in this fixture projection.");
  await expect(page.getByTestId("tws-execution-reports-table")).toBeVisible();
  await expect(page.getByTestId("tws-execution-reports-table")).toContainText("Report type");
  await expect(page.getByTestId("tws-execution-reports-table")).toContainText("Client order");
  await expect(page.getByTestId("tws-execution-reports-table")).toContainText("Venue order");
  await expect(page.getByTestId("tws-execution-reports-table")).toContainText("Sequence");
  await expect(page.getByTestId("tws-execution-report-blocker")).toContainText("tws_api_readiness_missing");
  await expect(page.getByTestId("tws-execution-report-blocker")).toContainText("source unavailable");
  await expect(page.getByTestId("account-evidence-rail")).toContainText("typed blocker");
  await expect(page.getByTestId("account-evidence-rail")).toContainText("tws-api-readiness-probe.json");
  await expect(page.getByText("acct.demo-19053")).toHaveCount(0);
  await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);
  await expect(page.getByText(/password=|auth_code=|front=tcp:\/\/|api_key=|secret=/i)).toHaveCount(0);

  mkdirSync(evidenceDir, { recursive: true });
  const screenshot = path.join(evidenceDir, `${testInfo.project.name}-acct-ib-live-u3028269-blocked.png`);
  await page.screenshot({ fullPage: true, path: screenshot });

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p019-u3028269-blocked-ui-parity-evidence.v1",
          proposal_id: "p019-broker-observation-session-foundation",
          status: "blocked_waiting_for_tws_api_readiness_and_real_source_package",
          account_id: accountId,
          display_alias: "U3028269",
          route: `/accounts/${accountId}`,
          source_kind: projection.source_kind,
          source_ref: projection.source_ref,
          source_checksum: projection.source_checksum,
          projection_checkpoint_id: projection.projection_checkpoint_id,
          projection_checksum: projection.projection_checksum,
          blocker_id: projection.blockers[0]?.blocker_id ?? "tws_api_readiness_missing",
          blocker_kind: projection.blockers[0]?.type ?? "runtime_blocker",
          parity: {
            funds_parity: "blocked",
            positions_parity: "blocked",
            orders_fills_parity: "blocked",
            execution_reports_table_parity: "blocked",
            execution_reports_persistence_parity: "blocked"
          },
          ui_surfaces: {
            funds_table_testid: "tws-multi-currency-funds-table",
            funds_blocker_testid: "tws-funds-blocker",
            fx_provenance_testid: "tws-fx-provenance",
            positions_table_testid: "account-positions-table",
            orders_table_testid: "account-bottom-tape",
            execution_reports_table_testid: "tws-execution-reports-table",
            execution_reports_blocker_testid: "tws-execution-report-blocker"
          },
          browser_evidence: [
            {
              project: testInfo.project.name,
              screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/")
            }
          ],
          explicit_non_claims: [
            "does_not_accept_adr0005",
            "does_not_open_direct_tws_session",
            "does_not_prove_tws_api_funds_parity",
            "does_not_prove_tws_api_positions_parity",
            "does_not_prove_order_or_fill_truth",
            "does_not_enable_command_capability",
            "does_not_record_raw_secret_values"
          ],
          boundaries: {
            raw_secret_values_recorded: false,
            direct_session_allowed: projection.source_health.direct_session_allowed ?? false,
            broker_truth: projection.boundaries.broker_truth,
            order_action: projection.boundaries.order_action
          },
          verdict: "blocked"
        },
        null,
        2
      )
    );
  }
});
