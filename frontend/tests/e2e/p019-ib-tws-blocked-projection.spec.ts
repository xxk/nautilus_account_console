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
const accountId = "acct.ib.live.u3028269";
const sourceRef = "contract://p019/u3028269/blocked-projection.synthetic.v1";
const readinessRef = "output/debug/p019-tws-api-readiness/tws-api-readiness-probe.json";
const sourceChecksum = "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";
const projectionChecksum = "sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff";
const projectionCheckpoint = "mirror.blocked.u3028269.tws-api-readiness-missing.001";

const blockedProjection = {
  schema_version: "account_mirror_projection.v1",
  account_id: accountId,
  display_alias: "U3028269",
  source_kind: "ib_tws_observation",
  source_mode: "live_observation",
  account_domain: "live",
  capabilities: {
    observation: { enabled: true, mirror_state: "blocked" },
    command: { enabled: false, mode: "disabled" }
  },
  balances: [],
  positions: [],
  orders: [],
  fills: [],
  source_health: {
    state: "blocked",
    api_transport: "ib_tws_api",
    blocker_id: "tws_api_readiness_missing",
    raw_secret_values_recorded: false,
    screenshot_used_for_values: false,
    direct_session_allowed: false,
    readiness_probe_ref: readinessRef
  },
  blockers: [
    {
      type: "source_unavailable",
      blocker_id: "tws_api_readiness_missing",
      source_ref: readinessRef,
      message: "source unavailable until TWS API readiness probe and source package pass"
    }
  ],
  projection_checkpoint_id: projectionCheckpoint,
  projection_checksum: projectionChecksum,
  source_ref: sourceRef,
  source_checksum: sourceChecksum,
  route_context: {
    route_id: "route.ib.live.u3028269.account-readonly",
    account_truth: "blocked_until_tws_api_source_package",
    blocker_id: "tws_api_readiness_missing"
  },
  boundaries: {
    read_only_projection: true,
    runtime_truth: false,
    capital_truth: false,
    broker_truth: false,
    order_action: false,
    account_truth: false,
    raw_secret_values_recorded: false,
    screenshot_used_for_funds_positions: false
  }
};

const blockedList = {
  schema_version: "account_mirror_list.v1",
  accounts: [
    {
      account_id: accountId,
      display_alias: "U3028269",
      source_kind: "ib_tws_observation",
      source_mode: "live_observation",
      account_domain: "live",
      route_id: "route.ib.live.u3028269.account-readonly",
      evidence_partition: "account_mirror/ib-live-u3028269/blocked",
      mirror_state: "blocked",
      command_enabled: false,
      command_mode: "disabled",
      balance_count: 0,
      position_count: 0,
      order_count: 0,
      fill_count: 0,
      blocker_count: 1,
      projection_checkpoint_id: projectionCheckpoint,
      projection_checksum: projectionChecksum,
      source_ref: sourceRef,
      source_checksum: sourceChecksum
    }
  ]
};

const blockedSourceHealth = {
  schema_version: "account_mirror_source_health.v1",
  account_id: accountId,
  state: "blocked",
  source_ref: sourceRef,
  source_checksum: sourceChecksum,
  projection_checkpoint_id: projectionCheckpoint,
  projection_checksum: projectionChecksum,
  blockers: blockedProjection.blockers,
  boundaries: {
    raw_secret_values_recorded: false,
    screenshot_used_for_funds_positions: false,
    order_action: false,
    broker_truth: false
  }
};

const blockedEvidence = {
  schema_version: "account_mirror_evidence.v1",
  account_id: accountId,
  projection_checkpoint_id: projectionCheckpoint,
  projection_checksum: projectionChecksum,
  source_ref: sourceRef,
  source_checksum: sourceChecksum,
  evidence: [
    {
      kind: "typed_blocker",
      owner: "account-console-broker-observation-session",
      source_ref: readinessRef,
      checksum: sourceChecksum,
      authority: "blocked Account Mirror projection; not broker/account/order truth"
    }
  ],
  blockers: blockedProjection.blockers,
  boundaries: {
    raw_secret_values_recorded: false,
    screenshot_used_for_funds_positions: false,
    order_action: false,
    broker_truth: false
  }
};

test("P019 U3028269 route renders Account Mirror TWS API readiness blocker without command drift", async ({ page }, testInfo) => {
  await page.route("**/api/mirror/**", async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname === "/api/mirror/accounts") {
      await route.fulfill({ json: blockedList });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}`) {
      await route.fulfill({ json: blockedProjection });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/source-health`) {
      await route.fulfill({ json: blockedSourceHealth });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/evidence`) {
      await route.fulfill({ json: blockedEvidence });
      return;
    }
    await route.fallback();
  });

  const projection = blockedProjection;

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
  await expect(page.getByTestId("account-bottom-tape")).toContainText("No open order rows in this mirror projection.");
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
