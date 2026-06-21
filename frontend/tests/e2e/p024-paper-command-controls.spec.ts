import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "command-controls-ui.json");
const sourceRef = "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/closeout_manifest.json";
const sourceChecksum = "sha256:abababababababababababababababababababababababababababababababab";
const readbackRef = "readback://p024/openctp19053/ui-command-controls/order";

function commandResult(action: "submit" | "cancel", request: Record<string, unknown>) {
  const commandId = `command.p024.${action}.ui-test-001`;
  return {
    schema_version: "account_command.command_api_result.v1",
    proposal_id: "p024-account-console-paper-command-controls",
    account_id: accountId,
    action,
    mode: "paper_armed",
    status: "accepted_for_risk",
    command_id: commandId,
    intent_id: request.intent_id,
    intent_ref: `api://p024/acct-ctp-paper-19053/${action}/${commandId}/intent`,
    idempotency_key: request.idempotency_key,
    idempotency_enforced: true,
    next_required_stage: "risk_decision",
    blockers: [
      {
        blocker_id: `p024_${action}_risk_decision_required`,
        type: "risk_decision_required",
        stage: "risk",
        reason: "intent accepted by API contract gate; risk decision is required before gateway send",
        source_ref: `api://p024/acct-ctp-paper-19053/${action}/${commandId}/intent`,
        next_action: "produce RiskDecision evidence before gateway send"
      },
      {
        blocker_id: `p024_${action}_approval_decision_required`,
        type: "approval_decision_required",
        stage: "approval",
        reason: "intent accepted by API contract gate; approval decision is required before gateway send",
        source_ref: `api://p024/acct-ctp-paper-19053/${action}/${commandId}/intent`,
        next_action: "produce ApprovalDecision evidence before gateway send"
      }
    ],
    gateway_event_refs: [],
    readback_refs: action === "cancel" ? [request.readback_ref] : [],
    gateway_ack_is_final_state: false,
    gateway_send_attempted: false,
    broker_order_created: false,
    runtime_duplicate_send_attempted: false,
    raw_secret_values_recorded: false,
    raw_broker_endpoint_recorded: false
  };
}

function projection(commandEnabled: boolean) {
  return {
    schema_version: "account_mirror_projection.v1",
    account_id: accountId,
    display_alias: "19053",
    source_kind: "ctp_trader_api",
    source_mode: "paper_observation",
    account_domain: "paper",
    capabilities: {
      observation: { enabled: true, mirror_state: "ready" },
      command: commandEnabled
        ? { enabled: true, mode: "paper_armed", allowed_actions: ["submit", "cancel"] }
        : { enabled: false, mode: "disabled", allowed_actions: [] }
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
        report_id: "report.p024.ui.partial.order",
        nautilus_report_type: "OrderStatusReport",
        client_order_id: "p024-ui-rb2610-001",
        venue_order_id: "ctp19053-ui-order-001",
        order_ref: "37",
        front_id: 1,
        session_id: 1,
        instrument_id: "rb2610.SHFE",
        instrument: "rb2610",
        exchange: "SHFE",
        side: "BUY",
        status: "partial",
        order_status: "partial",
        quantity: 10,
        filled_quantity: 4,
        remaining_quantity: 6,
        cancelled_quantity: null,
        limit_price: 24910,
        source_ref: readbackRef,
        report_provenance_ref: readbackRef,
        source_checksum: "sha256:cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd"
      }
    ],
    fills: [
      {
        report_id: "report.p024.ui.fill.001",
        nautilus_report_type: "FillReport",
        client_order_id: "p024-ui-rb2610-001",
        venue_order_id: "ctp19053-ui-order-001",
        instrument_id: "rb2610.SHFE",
        instrument: "rb2610",
        side: "BUY",
        trade_id: "p024-ui-trade-001",
        quantity: 10,
        filled_quantity: 4,
        remaining_quantity: 6,
        last_px: 24910,
        sequence: 2,
        source_ref: "ReqQryTrade://p024/openctp19053/ui-command-controls/fill-001",
        source_checksum: "sha256:efefefefefefefefefefefefefefefefefefefefefefefefefefefefefefefef"
      }
    ],
    source_health: {
      state: "ready",
      observed_at: "2026-06-21T00:00:00Z",
      api_transport: "ctp_trader_api",
      order_action_sent: false,
      cancel_order_sent: false,
      replace_order_sent: false,
      raw_secret_values_recorded: false,
      raw_broker_endpoint_recorded: false
    },
    command_status: null,
    blockers: [],
    projection_checkpoint_id: commandEnabled ? "mirror.p024.command-controls.paper-armed" : "mirror.p024.command-controls.disabled",
    projection_checksum: "sha256:fafafafafafafafafafafafafafafafafafafafafafafafafafafafafafafafa",
    source_ref: sourceRef,
    source_checksum: sourceChecksum,
    route_context: {
      route_id: "route.ctp.paper.19053",
      evidence_partition: "browser-evidence/p024-account-console-paper-command-controls",
      account_truth: "p024_ui_command_controls_contract_fixture_not_runtime_truth"
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

function listForProjection(projectionPayload: Record<string, unknown>) {
  const capabilities = projectionPayload.capabilities as Record<string, Record<string, unknown>>;
  return {
    schema_version: "account_mirror_list.v1",
    accounts: [
      {
        account_id: projectionPayload.account_id,
        display_alias: projectionPayload.display_alias,
        source_kind: projectionPayload.source_kind,
        source_mode: projectionPayload.source_mode,
        account_domain: projectionPayload.account_domain,
        route_id: "route.ctp.paper.19053",
        evidence_partition: "browser-evidence/p024-account-console-paper-command-controls",
        mirror_state: "ready",
        command_enabled: capabilities.command.enabled,
        command_mode: capabilities.command.mode,
        balance_count: 1,
        position_count: 0,
        order_count: 1,
        fill_count: 1,
        blocker_count: 0,
        projection_checkpoint_id: projectionPayload.projection_checkpoint_id,
        projection_checksum: projectionPayload.projection_checksum,
        source_ref: projectionPayload.source_ref,
        source_checksum: projectionPayload.source_checksum
      }
    ]
  };
}

function sourceHealthForProjection(projectionPayload: Record<string, unknown>) {
  return {
    schema_version: "account_mirror_source_health.v1",
    account_id: projectionPayload.account_id,
    state: "ready",
    source_ref: projectionPayload.source_ref,
    source_checksum: projectionPayload.source_checksum,
    observed_at: "2026-06-21T00:00:00Z",
    projection_checkpoint_id: projectionPayload.projection_checkpoint_id,
    projection_checksum: projectionPayload.projection_checksum,
    blockers: [],
    boundaries: projectionPayload.boundaries
  };
}

function evidenceForProjection(projectionPayload: Record<string, unknown>) {
  return {
    schema_version: "account_mirror_evidence.v1",
    account_id: projectionPayload.account_id,
    projection_checkpoint_id: projectionPayload.projection_checkpoint_id,
    projection_checksum: projectionPayload.projection_checksum,
    source_ref: projectionPayload.source_ref,
    source_checksum: projectionPayload.source_checksum,
    evidence: [
      {
        kind: "p024_ui_contract_fixture",
        owner: "account-console-browser-acceptance-tests",
        source_ref: projectionPayload.source_ref,
        checksum: projectionPayload.source_checksum,
        authority: "UI control rendering contract only; broker mutation remains API/gateway owned"
      }
    ],
    blockers: [],
    boundaries: projectionPayload.boundaries
  };
}

test("P024 Web UI gates paper submit and cancel controls on command capability", async ({ page }, testInfo) => {
  let currentProjection: Record<string, unknown> = projection(false);
  const commandRequests: Record<string, unknown>[] = [];

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
      await route.fulfill({ json: sourceHealthForProjection(currentProjection) });
      return;
    }
    if (url.pathname === `/api/mirror/accounts/${accountId}/evidence`) {
      await route.fulfill({ json: evidenceForProjection(currentProjection) });
      return;
    }
    await route.fallback();
  });

  await page.route("**/api/commands/**", async (route) => {
    const request = route.request();
    if (request.method() !== "POST") {
      await route.fallback();
      return;
    }
    const payload = request.postDataJSON() as Record<string, unknown>;
    commandRequests.push(payload);
    const action = request.url().includes("cancel-intents") ? "cancel" : "submit";
    await route.fulfill({ json: commandResult(action, payload), status: 202 });
  });

  mkdirSync(evidenceDir, { recursive: true });

  await page.goto(`/accounts/${accountId}?p024_command_controls=disabled`);
  await expect(page.getByTestId("account-command-mode")).toHaveText("observation only");
  await expect(page.getByTestId("account-command-controls-state")).toHaveText("none mounted");
  await expect(page.getByTestId("account-submit-order-form")).toHaveCount(0);
  await expect(page.getByTestId("account-submit-order-button")).toHaveCount(0);
  await expect(page.getByTestId("account-cancel-order-button")).toHaveCount(0);
  await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);
  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "command-controls-disabled.png") });
  }

  currentProjection = projection(true);
  await page.goto(`/accounts/${accountId}?p024_command_controls=paper_armed`);
  await expect(page.getByTestId("account-command-mode")).toHaveText("paper_armed");
  await expect(page.getByTestId("account-command-controls-state")).toHaveText("mounted");
  await expect(page.getByTestId("account-paper-command-banner")).toBeVisible();
  await expect(page.getByTestId("account-command-preflight-ref")).toContainText(sourceRef);
  await expect(page.getByTestId("account-submit-order-form")).toBeVisible();
  await expect(page.getByTestId("account-submit-idempotency-key")).toContainText("p024-ui-submit-");
  await expect(page.getByTestId("account-cancel-order-identity")).toContainText("ctp19053-ui-order-001");
  await expect(page.getByTestId("account-cancel-order-button")).toBeVisible();
  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "paper-armed-controls.png") });
  }

  await page.getByTestId("account-submit-order-button").click();
  await expect(page.getByTestId("account-command-audit-ref")).toContainText("api://p024/");
  await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("false");
  await expect(page.getByTestId("account-command-blocker").filter({ hasText: "risk_decision_required" })).toHaveCount(1);
  await expect(page.getByTestId("account-command-blocker").filter({ hasText: "approval_decision_required" })).toHaveCount(1);
  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "submit-accepted-for-risk.png") });
  }

  await page.getByTestId("account-cancel-order-button").click();
  await expect(page.getByTestId("account-command-audit-ref")).toContainText("api://p024/");
  await expect(page.getByTestId("account-command-readback-ref")).toContainText(readbackRef);
  await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("false");
  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "cancel-accepted-for-risk.png") });
  }

  const submitRequest = commandRequests.find((request) => request.action === "submit");
  const cancelRequest = commandRequests.find((request) => request.action === "cancel");
  expect(submitRequest).toBeDefined();
  expect(cancelRequest).toBeDefined();
  expect(submitRequest?.raw_secret_values_recorded).toBe(false);
  expect(cancelRequest?.raw_secret_values_recorded).toBe(false);
  expect(cancelRequest?.venue_order_id).toBe("ctp19053-ui-order-001");
  expect(cancelRequest?.readback_ref).toBe(readbackRef);

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.command-controls-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          disabled_controls_absent: true,
          paper_armed_controls_visible: true,
          submit_result_status: "accepted_for_risk",
          cancel_result_status: "accepted_for_risk",
          gateway_send_attempted: false,
          broker_order_created: false,
          gateway_ack_is_final_state: false,
          cancel_uses_readback_identity: true,
          submitted_request: submitRequest,
          cancel_request: cancelRequest,
          explicit_non_claims: [
            "does_not_send_broker_order_from_browser_test",
            "does_not_claim_real_openctp_runtime_command_from_ui",
            "does_not_enable_live_armed",
            "does_not_use_screenshot_as_command_truth"
          ],
          browser_evidence: [
            "command-controls-disabled.png",
            "paper-armed-controls.png",
            "submit-accepted-for-risk.png",
            "cancel-accepted-for-risk.png"
          ].map((screenshot) => ({
            screenshot: path.relative(path.resolve(".."), path.join(evidenceDir, screenshot)).replaceAll("\\", "/")
          }))
        },
        null,
        2
      )
    );
  }
});
