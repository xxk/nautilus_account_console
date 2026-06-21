import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const sourceRef = "owner-approved-fixture://p024/openctp19053/runtime-handoff";
const sourceChecksum = "sha256:5151515151515151515151515151515151515151515151515151515151515151";
const readbackRef = "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-handoff-ui.json");

function projection() {
  return {
    schema_version: "account_mirror_projection.v1",
    account_id: accountId,
    display_alias: "19053",
    source_kind: "ctp_trader_api",
    source_mode: "paper_observation",
    account_domain: "paper",
    capabilities: {
      observation: { enabled: true, mirror_state: "ready" },
      command: { enabled: true, mode: "paper_armed", allowed_actions: ["submit", "cancel"] }
    },
    balances: [
      {
        currency: "CNY",
        equity: 1000000,
        available_cash: 950000,
        margin_used: 50000,
        source_ref: sourceRef,
        checksum: sourceChecksum
      }
    ],
    positions: [],
    orders: [
      {
        report_id: "report.p024.runtime-handoff.order",
        nautilus_report_type: "OrderStatusReport",
        client_order_id: "p024-runtime-handoff-rb2610-001",
        venue_order_id: "ctp19053-runtime-handoff-order-001",
        order_ref: "37",
        front_id: 1,
        session_id: 1,
        instrument_id: "rb2610.SHFE",
        instrument: "rb2610",
        exchange: "SHFE",
        side: "BUY",
        status: "working",
        order_status: "working",
        order_type: "LIMIT",
        quantity: 1,
        filled_quantity: 0,
        remaining_quantity: 1,
        price: 24910,
        limit_price: 24910,
        sequence: 1,
        report_provenance_ref: readbackRef,
        source_ref: readbackRef,
        source_checksum: sourceChecksum
      }
    ],
    fills: [],
    source_health: {
      state: "ready",
      observed_at: "2026-06-21T00:00:00Z",
      api_transport: "ctp_trader_api",
      source_authority: "owner_approved_ui_contract_fixture",
      order_trade_query_success: true,
      order_trade_query_login_success: true,
      order_trade_query_ready: true,
      open_orders_state: "available",
      open_order_rows: 1,
      fills_state: "empty",
      fill_rows: 0,
      readonly_api_calls: ["ReqQryOrder", "ReqQryTrade"],
      complete_trade_history_claimed: false,
      order_action_sent: false,
      cancel_order_sent: false,
      replace_order_sent: false,
      raw_secret_values_recorded: false,
      raw_broker_endpoint_recorded: false
    },
    command_status: null,
    blockers: [],
    projection_checkpoint_id: "mirror.p024.runtime-handoff.001",
    projection_checksum: sourceChecksum,
    source_ref: sourceRef,
    source_checksum: sourceChecksum,
    route_context: {
      route_id: "route.ctp.paper.19053",
      evidence_partition: "browser-evidence/p024-account-console-paper-command-controls",
      account_truth: "owner_approved_ui_contract_fixture_not_runtime_truth"
    },
    boundaries: {
      read_only_projection: true,
      runtime_truth: false,
      account_truth: false,
      broker_truth: false,
      order_truth: false,
      order_action: false,
      raw_secret_values_recorded: false
    }
  };
}

function listForProjection(currentProjection: Record<string, unknown>) {
  const capabilities = currentProjection.capabilities as Record<string, Record<string, unknown>>;
  return {
    schema_version: "account_mirror_list.v1",
    accounts: [
      {
        account_id: currentProjection.account_id,
        display_alias: currentProjection.display_alias,
        source_kind: currentProjection.source_kind,
        source_mode: currentProjection.source_mode,
        account_domain: currentProjection.account_domain,
        route_id: "route.ctp.paper.19053",
        evidence_partition: "browser-evidence/p024-account-console-paper-command-controls",
        mirror_state: "ready",
        command_enabled: capabilities.command.enabled,
        command_mode: capabilities.command.mode,
        balance_count: 1,
        position_count: 0,
        order_count: 1,
        fill_count: 0,
        blocker_count: 0,
        projection_checkpoint_id: currentProjection.projection_checkpoint_id,
        projection_checksum: currentProjection.projection_checksum,
        source_ref: currentProjection.source_ref,
        source_checksum: currentProjection.source_checksum
      }
    ]
  };
}

test("P024 Web UI prepares owner-runtime handoff request without invoking broker runtime", async ({ page }, testInfo) => {
  const currentProjection = projection();

  await page.route("**/api/mirror/**", async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname === "/api/mirror/accounts") {
      await route.fulfill({ json: listForProjection(currentProjection) });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}`) {
      await route.fulfill({ json: currentProjection });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/source-health`) {
      await route.fulfill({
        json: {
          schema_version: "account_mirror_source_health.v1",
          account_id: accountId,
          state: "ready",
          source_ref: sourceRef,
          source_checksum: sourceChecksum,
          observed_at: "2026-06-21T00:00:00Z",
          projection_checkpoint_id: currentProjection.projection_checkpoint_id,
          projection_checksum: currentProjection.projection_checksum,
          blockers: [],
          boundaries: currentProjection.boundaries
        }
      });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/evidence`) {
      await route.fulfill({
        json: {
          schema_version: "account_mirror_evidence.v1",
          account_id: accountId,
          projection_checkpoint_id: currentProjection.projection_checkpoint_id,
          projection_checksum: currentProjection.projection_checksum,
          source_ref: sourceRef,
          source_checksum: sourceChecksum,
          evidence: [
            {
              kind: "owner_approved_ui_contract_fixture",
              owner: "account-console-browser-acceptance-tests",
              source_ref: sourceRef,
              checksum: sourceChecksum,
              authority: "UI handoff display contract only"
            }
          ],
          blockers: [],
          boundaries: currentProjection.boundaries
        }
      });
      return;
    }
    await route.fallback();
  });

  mkdirSync(evidenceDir, { recursive: true });
  await page.goto(`/accounts/${accountId}?p024_runtime_handoff=1`);

  await expect(page.getByTestId("account-command-controls-state")).toHaveText("mounted");

  const submitHandoffPromise = page.waitForResponse((response) =>
    response.url().includes("/api/commands/accounts/acct.ctp.paper.19053/runtime-run-requests/submit")
  );
  await page.getByTestId("account-submit-order-button").click();
  const submitHandoffResponse = await submitHandoffPromise;
  expect(submitHandoffResponse.status()).toBe(202);
  const submitHandoff = await submitHandoffResponse.json();

  await expect(page.getByTestId("account-runtime-handoff-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-handoff-action")).toHaveText("submit");
  await expect(page.getByTestId("account-runtime-handoff-status")).toHaveText("blocked_until_owner_runtime_invocation");
  await expect(page.getByTestId("account-runtime-handoff-entrypoint")).toContainText("ctp_guarded_paper_order_loop.py");
  await expect(page.getByTestId("account-runtime-handoff-config-ref")).toHaveText(
    "cfgs/local/ctp.openctp.tts.7x24.local.json"
  );
  await expect(page.getByTestId("account-runtime-handoff-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-web-trigger")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-raw-secret")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-blocker")).toHaveCount(3);
  await expect(page.getByTestId("account-runtime-handoff-non-claim")).toContainText([
    "does_not_invoke_owner_runtime",
    "does_not_send_broker_order_from_browser"
  ]);

  const cancelHandoffPromise = page.waitForResponse((response) =>
    response.url().includes("/api/commands/accounts/acct.ctp.paper.19053/runtime-run-requests/cancel")
  );
  await page.getByTestId("account-cancel-order-button").click();
  const cancelHandoffResponse = await cancelHandoffPromise;
  expect(cancelHandoffResponse.status()).toBe(202);
  const cancelHandoff = await cancelHandoffResponse.json();

  await expect(page.getByTestId("account-runtime-handoff-action")).toHaveText("cancel");
  await expect(page.getByTestId("account-runtime-handoff-entrypoint")).toContainText("ctp_guarded_paper_cancel_loop.py");
  await expect(page.getByTestId("account-runtime-handoff-readback-ref")).toContainText(readbackRef);
  await expect(page.getByTestId("account-runtime-handoff-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-web-trigger")).toHaveText("false");
  await expect(page.getByText(/live ready|gateway ack final|browser submitted broker order/i)).toHaveCount(0);

  expect(submitHandoff.runtime_invocation_attempted).toBe(false);
  expect(submitHandoff.browser_triggered_broker_order).toBe(false);
  expect(cancelHandoff.runtime_invocation_attempted).toBe(false);
  expect(cancelHandoff.browser_triggered_broker_order).toBe(false);
  expect(cancelHandoff.readback_ref).toBe(readbackRef);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-runtime-handoff-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.runtime-handoff-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          submit_handoff: submitHandoff,
          cancel_handoff: cancelHandoff,
          browser_checks: {
            handoff_panel_visible: true,
            submit_handoff_displayed: true,
            cancel_handoff_displayed: true,
            runtime_invocation_displayed_false: true,
            browser_trigger_displayed_false: true,
            live_ready_wording_absent: true
          },
          explicit_non_claims: [
            "does_not_invoke_owner_runtime",
            "does_not_send_broker_order_from_browser",
            "does_not_claim_live_readiness",
            "does_not_use_screenshot_as_command_truth"
          ],
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-runtime-handoff-ui.png"))
                .replaceAll("\\", "/")
            }
          ]
        },
        null,
        2
      )
    );
  }
});
