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
  return {
    detail: "command_capability_not_mounted",
    action,
    request
  };
}

function runtimeRunRequest(action: "submit" | "cancel", request: Record<string, unknown>) {
  const commandId = `command.p024.${action}.ui-test-001`;
  const intentRef = `api://p024/acct-ctp-paper-19053/${action}/${commandId}/intent`;
  return {
    schema_version: "account_command.owner_runtime_run_request.v1",
    proposal_id: "p024-account-console-paper-command-controls",
    account_id: accountId,
    action,
    mode: "paper_armed",
    status: "blocked_until_owner_runtime_invocation",
    command_id: commandId,
    intent_id: request.intent_id,
    intent_ref: intentRef,
    idempotency_key: request.idempotency_key,
    owner_runtime_owner_ref: "owner://nautilus_ctp_adapter",
    owner_runtime_repo_ref: "owner-repo://nautilus_ctp_adapter",
    owner_runtime_entrypoint_ref:
      action === "cancel" ? "scripts/ctp_guarded_paper_cancel_loop.py" : "scripts/ctp_guarded_paper_order_loop.py",
    owner_runtime_config_ref: "cfgs/local/ctp.openctp.tts.7x24.local.json",
    source_preflight_ref: action === "cancel" ? request.readback_ref : request.preflight_ref,
    readback_ref: action === "cancel" ? request.readback_ref : null,
    expected_output_root_ref: `output/account_command/ctp-paper-19053/p024-ui-${action}-${commandId}`,
    runtime_invocation_attempted: false,
    browser_triggered_broker_order: false,
    gateway_send_attempted: false,
    broker_order_created: false,
    raw_secret_values_recorded: false,
    raw_broker_endpoint_recorded: false,
    external_write_approval_required: true,
    blockers: [
      {
        blocker_id: `p024_${action}_owner_runtime_invocation_required`,
        type: "owner_runtime_invocation_required",
        stage: "owner_runtime",
        reason: "handoff test fixture",
        source_ref: intentRef,
        next_action: "invoke owner runtime"
      },
      {
        blocker_id: `p024_${action}_external_write_approval_required`,
        type: "external_write_approval_required",
        stage: "owner_runtime",
        reason: "handoff test fixture",
        source_ref: intentRef,
        next_action: "approve owner writes"
      },
      {
        blocker_id: `p024_${action}_post_run_ingest_required`,
        type: "post_run_ingest_required",
        stage: "readback",
        reason: "handoff test fixture",
        source_ref: intentRef,
        next_action: "ingest owner artifacts"
      }
    ],
    explicit_non_claims: [
      "does_not_invoke_owner_runtime",
      "does_not_send_broker_order_from_browser",
      "does_not_store_raw_ctp_secret_or_endpoint",
      "does_not_claim_live_readiness",
      "does_not_make_gateway_ack_final_state"
    ],
    run_request_checksum: "sha256:2424242424242424242424242424242424242424242424242424242424242424"
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
        ? {
            enabled: true,
            mode: "paper_armed",
            allowed_actions: ["submit", "cancel"],
            authority_ref: null,
            capability_checksum: sourceChecksum
          }
        : {
            enabled: false,
            mode: "disabled",
            allowed_actions: [],
            authority_ref: null,
            capability_checksum: sourceChecksum
          }
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

  await page.route("**/api/mirror/accounts**", async (route) => {
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
    if (request.url().includes("runtime-run-requests")) {
      const action = request.url().includes("/cancel") ? "cancel" : "submit";
      await route.fulfill({ json: runtimeRunRequest(action, payload), status: 202 });
      return;
    }
    commandRequests.push(payload);
    const action = request.url().includes("cancel-intents") ? "cancel" : "submit";
    await route.fulfill({ json: commandResult(action, payload), status: 403 });
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
  await expect(page.getByTestId("account-command-mode")).toHaveText("observation only");
  await expect(page.getByTestId("account-command-controls-state")).toHaveText("none mounted");
  await expect(page.getByTestId("account-paper-command-banner")).toHaveCount(0);
  await expect(page.getByTestId("account-submit-order-form")).toHaveCount(0);
  await expect(page.getByTestId("account-cancel-order-button")).toHaveCount(0);
  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "paper-armed-controls.png") });
  }

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "submit-accepted-for-risk.png") });
  }

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "cancel-accepted-for-risk.png") });
  }

  const submitRequest = commandRequests.find((request) => request.action === "submit");
  const cancelRequest = commandRequests.find((request) => request.action === "cancel");
  expect(submitRequest).toBeUndefined();
  expect(cancelRequest).toBeUndefined();

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
          paper_armed_controls_visible: false,
          submit_result_status: "command_capability_not_mounted",
          cancel_result_status: "command_capability_not_mounted",
          gateway_send_attempted: false,
          broker_order_created: false,
          gateway_ack_is_final_state: false,
          cancel_uses_readback_identity: false,
          submitted_request: null,
          cancel_request: null,
          explicit_non_claims: [
            "does_not_send_broker_order_from_browser_test",
            "does_not_claim_real_openctp_runtime_command_from_ui",
            "does_not_enable_live_armed",
            "does_not_use_screenshot_as_command_truth",
            "does_not_treat_paper_armed_ui_projection_as_authority"
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
