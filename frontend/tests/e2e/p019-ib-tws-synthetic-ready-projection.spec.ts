import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ib.live.u3028269";
const sourceRef = "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_source.synthetic.json";
const sourceChecksum = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const projectionCheckpoint = "mirror.synthetic.u3028269.ready.2026-06-20T00:00:01Z";
const projectionChecksum = "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
const reportBatchRef = "contracts/broker_observation/fixtures/ib_tws_report_batch_sample.json";
const storeReloadRef = "contracts/broker_observation/fixtures/ib_tws_store_complete_reload.json";
const reloadCheckpointId = "broker-observation-store.reload.u3028269.complete.001";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p019-u3028269-synthetic-ready-ui");
const evidencePath = path.resolve(
  "..",
  "docs",
  "acceptance",
  "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json"
);

const readyProjection = {
  schema_version: "account_mirror_projection.v1",
  account_id: accountId,
  display_alias: "U3028269",
  source_kind: "ib_tws_observation",
  source_mode: "live_observation",
  account_domain: "live",
  capabilities: {
    observation: { enabled: true, mirror_state: "ready" },
    command: { enabled: false, mode: "disabled" }
  },
  balances: [
    {
      currency: "USD",
      equity: 100000,
      available_cash: 75000,
      margin_used: 25000,
      position_profit: 123.45,
      unrealized_pnl: 123.45,
      source_ref: sourceRef,
      checksum: "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
    }
  ],
  positions: [
    {
      instrument: "AAPL",
      exchange: "SMART",
      direction: "long",
      net_qty: 10,
      today_qty: 0,
      yesterday_qty: 10,
      available_qty: 10,
      frozen_qty: 0,
      avg_price: 180.25,
      unrealized_pnl: 42,
      source_ref: sourceRef,
      checksum: "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
    }
  ],
  orders: [
    {
      report_id: "report.ib.u3028269.order-status.000001",
      nautilus_report_type: "OrderStatusReport",
      client_order_id: "C-ADR0005-000001",
      venue_order_id: "V-ADR0005-000001",
      instrument_id: "AAPL.NASDAQ",
      side: "BUY",
      order_status: "ACCEPTED",
      quantity: 100,
      filled_quantity: 0,
      remaining_quantity: 100,
      price: 180.5,
      sequence: 1,
      source_ref: "observation-ref://ib-tws/u3028269/reports/000001",
      source_checksum: "sha256:1111111111111111111111111111111111111111111111111111111111111111"
    }
  ],
  fills: [
    {
      report_id: "report.ib.u3028269.fill.000002",
      nautilus_report_type: "FillReport",
      client_order_id: "C-ADR0005-000001",
      venue_order_id: "V-ADR0005-000001",
      instrument_id: "AAPL.NASDAQ",
      side: "BUY",
      order_status: "FILLED",
      quantity: 100,
      filled_quantity: 100,
      remaining_quantity: 0,
      trade_id: "T-ADR0005-000002",
      last_px: 180.45,
      sequence: 2,
      source_ref: "observation-ref://ib-tws/u3028269/reports/000002",
      source_checksum: "sha256:3333333333333333333333333333333333333333333333333333333333333333"
    }
  ],
  source_health: {
    state: "ready",
    account_uid: "ib-live.U3028269",
    observed_at: "2026-06-20T00:00:01Z",
    api_transport: "ib_tws_api",
    screenshot_used_for_values: false,
    raw_secret_values_recorded: false,
    blocker_id: null,
    store_reload: {
      source_ref: storeReloadRef,
      report_batch_ref: reportBatchRef,
      reload_checkpoint_id: reloadCheckpointId,
      records_reloaded_from_store: 2,
      records_loaded_from_live_memory: 0,
      parity_status: "passed"
    }
  },
  blockers: [],
  projection_checkpoint_id: projectionCheckpoint,
  projection_checksum: projectionChecksum,
  source_ref: sourceRef,
  source_checksum: sourceChecksum,
  route_context: {
    route_id: "route.ib.live.u3028269",
    account_truth: "synthetic_contract_guard_not_account_truth",
    execution_adapter: "ib_tws_api.readonly_observation",
    blocker_id: null
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

const readyList = {
  schema_version: "account_mirror_list.v1",
  accounts: [
    {
      account_id: accountId,
      display_alias: "U3028269",
      source_kind: "ib_tws_observation",
      source_mode: "live_observation",
      account_domain: "live",
      route_id: "route.ib.live.u3028269",
      evidence_partition: "account_mirror/ib-live-u3028269/synthetic",
      mirror_state: "ready",
      command_enabled: false,
      command_mode: "disabled",
      balance_count: 1,
      position_count: 1,
      order_count: 1,
      fill_count: 1,
      blocker_count: 0,
      projection_checkpoint_id: projectionCheckpoint,
      projection_checksum: projectionChecksum,
      source_ref: sourceRef,
      source_checksum: sourceChecksum
    }
  ]
};

const readySourceHealth = {
  schema_version: "account_mirror_source_health.v1",
  account_id: accountId,
  state: "ready",
  source_ref: sourceRef,
  source_checksum: sourceChecksum,
  observed_at: "2026-06-20T00:00:01Z",
  projection_checkpoint_id: projectionCheckpoint,
  projection_checksum: projectionChecksum,
  blockers: [],
  boundaries: {
    raw_secret_values_recorded: false,
    screenshot_used_for_funds_positions: false,
    order_action: false,
    broker_truth: false
  }
};

const readyEvidence = {
  schema_version: "account_mirror_evidence.v1",
  account_id: accountId,
  projection_checkpoint_id: projectionCheckpoint,
  projection_checksum: projectionChecksum,
  source_ref: sourceRef,
  source_checksum: sourceChecksum,
  evidence: [
    {
      kind: "synthetic_source_package",
      owner: "account-console-broker-observation-session",
      source_ref: sourceRef,
      checksum: sourceChecksum,
      authority: "synthetic contract guard only; not real U3028269 funds or positions truth"
    },
    {
      kind: "mirror_projection",
      owner: "account-console-backend",
      source_ref: projectionCheckpoint,
      checksum: projectionChecksum,
      authority: "mocked Account Mirror projection for UI contract rendering"
    }
  ],
  blockers: [],
  boundaries: {
    raw_secret_values_recorded: false,
    screenshot_used_for_funds_positions: false,
    order_action: false,
    broker_truth: false
  }
};

test("P019 synthetic ready U3028269 projection renders funds, positions and reports without command drift", async ({
  page
}, testInfo) => {
  expect(readyProjection.boundaries.account_truth).toBe(false);
  expect(readyProjection.boundaries.capital_truth).toBe(false);
  expect(readyProjection.boundaries.broker_truth).toBe(false);
  expect(readyProjection.boundaries.runtime_truth).toBe(false);
  expect(readyProjection.route_context.account_truth).toBe("synthetic_contract_guard_not_account_truth");

  await page.route("**/api/mirror/**", async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname === "/api/mirror/accounts") {
      await route.fulfill({ json: readyList });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}`) {
      await route.fulfill({ json: readyProjection });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/source-health`) {
      await route.fulfill({ json: readySourceHealth });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/evidence`) {
      await route.fulfill({ json: readyEvidence });
      return;
    }
    await route.fallback();
  });

  await page.goto(`/accounts/${accountId}`);
  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText(accountId);
  await expect(page.getByTestId("terminal-top-status-bar")).toContainText("U3028269");
  await expect(page.getByTestId("account-source-health-panel")).toContainText("normalized_read_model");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
  await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
  await expect(page.getByTestId("tws-multi-currency-funds-table")).toContainText("USD");
  await expect(page.getByTestId("tws-multi-currency-funds-table")).toContainText("source currency");
  await expect(page.getByTestId("tws-base-currency-rollup")).toContainText("USD");
  await expect(page.getByTestId("account-summary-position-count")).toContainText("1");
  await expect(page.getByTestId("account-positions-table")).toContainText("AAPL");
  await expect(page.getByTestId("account-position-projection-row")).toContainText("10");
  await expect(page.getByTestId("tws-execution-report-row")).toHaveCount(2);
  await expect(page.getByTestId("tws-execution-report-row").nth(0)).toContainText("OrderStatusReport");
  await expect(page.getByTestId("tws-execution-report-row").nth(0)).toContainText("C-ADR0005-000001");
  await expect(page.getByTestId("tws-execution-report-row").nth(0)).toContainText("ACCEPTED");
  await expect(page.getByTestId("tws-execution-report-row").nth(1)).toContainText("FillReport");
  await expect(page.getByTestId("tws-execution-report-row").nth(1)).toContainText("T-ADR0005-000002");
  await expect(page.getByTestId("tws-execution-report-sequence").nth(0)).toContainText("1");
  await expect(page.getByTestId("tws-execution-report-sequence").nth(1)).toContainText("2");
  await expect(page.getByTestId("tws-execution-report-source-ref").nth(0)).toContainText(
    "observation-ref://ib-tws/u3028269/reports/000001"
  );
  await expect(page.getByTestId("tws-execution-report-source-ref").nth(1)).toContainText(
    "observation-ref://ib-tws/u3028269/reports/000002"
  );
  await expect(page.getByTestId("tws-execution-report-reload-ref")).toHaveCount(2);
  await expect(page.getByTestId("tws-execution-report-reload-ref").nth(0)).toContainText(reloadCheckpointId);
  await expect(page.getByTestId("account-evidence-rail")).toContainText("synthetic source package");
  await expect(page.getByTestId("account-evidence-rail")).toContainText(sourceRef);
  await expect(page.getByTestId("account-blocker-row")).toHaveCount(0);
  await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);
  await expect(page.getByText(/password=|auth_code=|front=tcp:\/\/|api_key=|secret=/i)).toHaveCount(0);

  mkdirSync(evidenceDir, { recursive: true });
  const screenshot = path.join(evidenceDir, `${testInfo.project.name}-acct-ib-live-u3028269-synthetic-ready.png`);
  await page.screenshot({ fullPage: true, path: screenshot });

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p019-u3028269-synthetic-ready-ui-contract-evidence.v1",
          proposal_id: "p019-broker-observation-session-foundation",
          account_id: accountId,
          display_alias: "U3028269",
          route: `/accounts/${accountId}`,
          source_kind: readyProjection.source_kind,
          source_ref: readyProjection.source_ref,
          source_checksum: readyProjection.source_checksum,
          projection_checkpoint_id: readyProjection.projection_checkpoint_id,
          projection_checksum: readyProjection.projection_checksum,
          verdict: "synthetic_contract_only",
          ui_surfaces: {
            funds_table_testid: "tws-multi-currency-funds-table",
            base_currency_rollup_testid: "tws-base-currency-rollup",
            positions_table_testid: "account-positions-table",
            position_row_testid: "account-position-projection-row",
            execution_reports_table_testid: "tws-execution-reports-table",
            execution_report_row_testid: "tws-execution-report-row",
            execution_report_reload_ref_testid: "tws-execution-report-reload-ref",
            command_state_testid: "account-command-capability-state",
            evidence_rail_testid: "account-evidence-rail"
          },
          observed_contract_values: {
            currency: "USD",
            position_instrument: "AAPL",
            execution_report_types: ["OrderStatusReport", "FillReport"],
            execution_report_sequences: [1, 2],
            execution_report_source_refs: [
              "observation-ref://ib-tws/u3028269/reports/000001",
              "observation-ref://ib-tws/u3028269/reports/000002"
            ],
            store_reload_ref: storeReloadRef,
            report_batch_ref: reportBatchRef,
            reload_checkpoint_id: reloadCheckpointId,
            records_reloaded_from_store: 2,
            records_loaded_from_live_memory: 0,
            reload_parity_status: "passed",
            command_enabled: false,
            mirror_state: "ready"
          },
          explicit_non_claims: [
            "does_not_prove_real_u3028269_funds",
            "does_not_prove_real_u3028269_positions",
            "does_not_prove_real_u3028269_order_or_fill_callbacks",
            "does_not_close_real_ui_parity",
            "does_not_accept_adr0005",
            "does_not_satisfy_p018_owner_source_package_acceptance",
            "does_not_open_direct_tws_session",
            "does_not_enable_command_capability",
            "does_not_record_raw_secret_values"
          ],
          required_real_closeout_chain: [
            "local_tws_api_readiness_probe_pass",
            "readonly_tws_api_account_summary_success",
            "readonly_tws_api_positions_success",
            "source_package_built_from_real_query_artifacts",
            "account_mirror_projection_from_real_source_package",
            "ui_parity_against_same_slice_tws_api_source"
          ],
          boundaries: {
            synthetic_contract_only: true,
            raw_secret_values_recorded: false,
            screenshot_used_for_funds_positions: false,
            execution_reports_synthetic_contract_only: true,
            durable_store_synthetic_contract_only: true,
            broker_truth: false,
            order_action: false
          },
          browser_evidence: [
            {
              project: testInfo.project.name,
              screenshot: path.relative(path.resolve(".."), screenshot).replaceAll("\\", "/")
            }
          ]
        },
        null,
        2
      )
    );
  }
});
