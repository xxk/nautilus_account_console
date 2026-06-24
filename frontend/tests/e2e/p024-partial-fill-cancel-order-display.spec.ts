import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const sourceRef = "owner-approved-fixture://p024/openctp19053/partial-fill-cancel-ui-contract";
const sourceChecksum = "sha256:2424242424242424242424242424242424242424242424242424242424242424";
const projectionChecksum = "sha256:4646464646464646464646464646464646464646464646464646464646464646";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const orderDisplayEvidencePath = path.join(evidenceDir, "partial-fill-cancel-order-display.json");

type StageId = "S1" | "S2" | "S3" | "S4";

interface StageExpectation {
  id: StageId;
  label: string;
  status: string;
  submitted: number;
  filled: number;
  remaining: number;
  cancelled: number | null;
  fillRows: number;
  screenshot: string;
}

interface ObservedStage {
  stage: StageId;
  label: string;
  browser: {
    identity: string | null;
    status: string | null;
    submitted_quantity: string | null;
    filled_quantity: string | null;
    remaining_quantity: string | null;
    cancelled_quantity: string | null;
    remaining_cancel_quantity: string | null;
    cancel_pending_ref: string | null;
  };
  browser_fill_rows: Array<{
    trade_id: string | null;
    filled_quantity: number | null;
    price: number | null;
    source_ref: string | null;
  }>;
  browser_fill_total: number;
  api: {
    identity: string;
    status: string;
    submitted_quantity: number;
    filled_quantity: number;
    remaining_quantity: number;
    cancelled_quantity: number | null;
  };
  api_fill_rows: Array<{
    trade_id: string;
    filled_quantity: number;
    price: number;
    source_ref: string;
  }>;
  api_fill_total: number;
  order_artifact_ref: unknown;
  fill_artifact_refs: string[];
  command_status_refs: {
    audit: string | null;
    risk: string[];
    approval: string[];
    gateway: string[];
    readback: string[];
    reconciliation: string | null;
    gateway_ack_is_final_state: boolean;
  };
  formula: string;
  verdict: "pass";
}

const stages: StageExpectation[] = [
  {
    id: "S1",
    label: "submitted/working",
    status: "working",
    submitted: 10,
    filled: 0,
    remaining: 10,
    cancelled: null,
    fillRows: 0,
    screenshot: "p024-working-order-display.png"
  },
  {
    id: "S2",
    label: "partially filled",
    status: "partial",
    submitted: 10,
    filled: 4,
    remaining: 6,
    cancelled: null,
    fillRows: 2,
    screenshot: "p024-partial-fill-display.png"
  },
  {
    id: "S3",
    label: "cancel pending",
    status: "cancel_pending",
    submitted: 10,
    filled: 4,
    remaining: 6,
    cancelled: null,
    fillRows: 2,
    screenshot: "p024-cancel-pending-display.png"
  },
  {
    id: "S4",
    label: "remaining cancelled",
    status: "canceled",
    submitted: 10,
    filled: 4,
    remaining: 0,
    cancelled: 6,
    fillRows: 2,
    screenshot: "p024-cancelled-display.png"
  }
];

function orderSourceRef(stage: StageExpectation) {
  if (stage.id === "S3") {
    return "readback://p024/openctp19053/partial-fill-cancel/s2/order";
  }
  if (stage.id === "S4") {
    return "readback://p024/openctp19053/partial-fill-cancel/s4/cancel-readback/order";
  }
  return `readback://p024/openctp19053/partial-fill-cancel/${stage.id.toLowerCase()}/order`;
}

function orderForStage(stage: StageExpectation) {
  const source = orderSourceRef(stage);
  return {
    report_id: `report.p024.partial.${stage.id.toLowerCase()}.order-status`,
    nautilus_report_type: "OrderStatusReport",
    client_order_id: "p024-partial-rb2610-001",
    venue_order_id: "ctp19053-p024-partial-order-001",
    order_ref: "37",
    front_id: 1,
    session_id: 1,
    instrument_id: "rb2610.SHFE",
    instrument: "rb2610",
    exchange: "SHFE",
    side: "SELL",
    status: stage.status,
    order_status: stage.status,
    order_type: "LIMIT",
    quantity: stage.submitted,
    filled_quantity: stage.filled,
    remaining_quantity: stage.remaining,
    cancelled_quantity: stage.cancelled,
    price: 3300,
    limit_price: 3300,
    sequence: stage.id === "S1" ? 1 : stage.id === "S2" ? 3 : stage.id === "S3" ? 4 : 5,
    report_provenance_ref:
      stage.id === "S3"
        ? "command-audit://p024/openctp19053/partial-fill-cancel/cancel-pending"
        : source,
    source_ref: source,
    source_checksum: `sha256:${stage.id.toLowerCase().repeat(32).slice(0, 64)}`
  };
}

function fillsForStage(stage: StageExpectation) {
  if (stage.fillRows === 0) {
    return [];
  }
  return [
    {
      report_id: "report.p024.partial.s2.fill.001",
      nautilus_report_type: "FillReport",
      client_order_id: "p024-partial-rb2610-001",
      venue_order_id: "ctp19053-p024-partial-order-001",
      instrument_id: "rb2610.SHFE",
      instrument: "rb2610",
      side: "SELL",
      order_status: "PARTIALLY_FILLED",
      quantity: 10,
      filled_quantity: 2,
      remaining_quantity: 8,
      trade_id: "ctp19053-p024-partial-trade-001",
      last_px: 3299,
      sequence: 2,
      source_ref: "ReqQryTrade://p024/openctp19053/partial-fill-cancel/s2/trade-001",
      source_checksum: "sha256:0101010101010101010101010101010101010101010101010101010101010101"
    },
    {
      report_id: "report.p024.partial.s2.fill.002",
      nautilus_report_type: "FillReport",
      client_order_id: "p024-partial-rb2610-001",
      venue_order_id: "ctp19053-p024-partial-order-001",
      instrument_id: "rb2610.SHFE",
      instrument: "rb2610",
      side: "SELL",
      order_status: "PARTIALLY_FILLED",
      quantity: 10,
      filled_quantity: 2,
      remaining_quantity: 6,
      trade_id: "ctp19053-p024-partial-trade-002",
      last_px: 3298,
      sequence: 3,
      source_ref: "ReqQryTrade://p024/openctp19053/partial-fill-cancel/s2/trade-002",
      source_checksum: "sha256:0202020202020202020202020202020202020202020202020202020202020202"
    }
  ];
}

function commandStatusForStage(stage: StageExpectation) {
  if (stage.id === "S3") {
    return {
      schema_version: "account_command.ui_status_projection.v1",
      status: "cancel_pending",
      command_audit_ref: "command-audit://p024/openctp19053/partial-fill-cancel/cancel-intent",
      risk_decision_refs: ["risk://p024/openctp19053/partial-fill-cancel/cancel-risk-pass"],
      approval_decision_refs: ["approval://p024/openctp19053/partial-fill-cancel/cancel-paper-approval"],
      gateway_event_refs: ["gateway://p024/openctp19053/partial-fill-cancel/cancel-requested"],
      readback_refs: [],
      reconciliation_ref: null,
      gateway_ack_is_final_state: false,
      readback_required: true,
      reconciliation_required: true,
      blockers: [
        {
          blocker_id: "p024_cancel_readback_required",
          type: "readback_required",
          stage: "readback",
          reason: "cancel pending cannot be terminal until Account Mirror observes post-cancel order state",
          source_ref: "gateway://p024/openctp19053/partial-fill-cancel/cancel-requested",
          next_action: "wait for ReqQryOrder readback and reconciliation"
        }
      ]
    };
  }
  if (stage.id === "S4") {
    return {
      schema_version: "account_command.ui_status_projection.v1",
      status: "canceled",
      command_audit_ref: "command-audit://p024/openctp19053/partial-fill-cancel/cancel-intent",
      risk_decision_refs: ["risk://p024/openctp19053/partial-fill-cancel/cancel-risk-pass"],
      approval_decision_refs: ["approval://p024/openctp19053/partial-fill-cancel/cancel-paper-approval"],
      gateway_event_refs: ["gateway://p024/openctp19053/partial-fill-cancel/cancel-requested"],
      readback_refs: [orderSourceRef(stage)],
      reconciliation_ref: "reconcile://p024/openctp19053/partial-fill-cancel/s4-cancelled",
      gateway_ack_is_final_state: false,
      readback_required: true,
      reconciliation_required: true,
      blockers: []
    };
  }
  return null;
}

function parseBrowserInt(value: string | null): number | null {
  if (value === null) {
    return null;
  }
  const text = value.trim();
  if (text === "" || text === "missing") {
    return null;
  }
  return Number.parseInt(text, 10);
}

function projectionForStage(stage: StageExpectation) {
  const fills = fillsForStage(stage);
  return {
    schema_version: "account_mirror_projection.v1",
    account_id: accountId,
    display_alias: "19053",
    source_kind: "ctp_trader_api",
    source_mode: "paper_observation",
    account_domain: "paper",
    capabilities: {
      observation: { enabled: true, mirror_state: "ready" },
      command: {
        enabled: true,
        mode: "paper_armed",
        allowed_actions: ["submit", "cancel"],
        authority_ref: "owner-repo://nautilus_ctp_adapter",
        capability_checksum: "sha256:5656565656565656565656565656565656565656565656565656565656565656"
      }
    },
    balances: [
      {
        currency: "CNY",
        equity: 1000000,
        available_cash: 950000,
        margin_used: 50000,
        position_profit: 0,
        source_ref: sourceRef,
        checksum: sourceChecksum
      }
    ],
    positions: [],
    orders: [orderForStage(stage)],
    fills,
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
      fills_state: fills.length > 0 ? "available" : "empty",
      fill_rows: fills.length,
      readonly_api_calls: ["ReqQryOrder", "ReqQryTrade"],
      complete_trade_history_claimed: false,
      order_action_sent: false,
      cancel_order_sent: false,
      replace_order_sent: false,
      raw_secret_values_recorded: false,
      raw_broker_endpoint_recorded: false
    },
    command_status: commandStatusForStage(stage),
    blockers: [],
    projection_checkpoint_id: `mirror.p024.openctp19053.partial-fill-cancel.${stage.id.toLowerCase()}`,
    projection_checksum: projectionChecksum,
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

function commandResult(request: Record<string, unknown>) {
  return {
    schema_version: "account_command.command_api_result.v1",
    proposal_id: "p024-account-console-paper-command-controls",
    account_id: accountId,
    action: "cancel",
    mode: "paper_armed",
    status: "risk_gate_pending",
    command_id: "command.p024.partial-fill-cancel.ui-test-001",
    intent_id: request.intent_id,
    intent_ref: "api://p024/acct-ctp-paper-19053/cancel/partial-fill-cancel-ui-test/intent",
    idempotency_key: request.idempotency_key,
    idempotency_enforced: true,
    next_required_stage: "risk_decision",
    blockers: [
      {
        blocker_id: "p024_partial_cancel_risk_decision_required",
        type: "risk_decision_required",
        stage: "risk",
        reason: "cancel intent accepted by API contract gate; risk decision is required before gateway send",
        source_ref: "api://p024/acct-ctp-paper-19053/cancel/partial-fill-cancel-ui-test/intent",
        next_action: "produce RiskDecision evidence before gateway send"
      },
      {
        blocker_id: "p024_partial_cancel_approval_decision_required",
        type: "approval_decision_required",
        stage: "approval",
        reason: "cancel intent accepted by API contract gate; approval decision is required before gateway send",
        source_ref: "api://p024/acct-ctp-paper-19053/cancel/partial-fill-cancel-ui-test/intent",
        next_action: "produce ApprovalDecision evidence before gateway send"
      }
    ],
    gateway_event_refs: [],
    readback_refs: [request.readback_ref],
    gateway_ack_is_final_state: false,
    gateway_send_attempted: false,
    broker_order_created: false,
    runtime_duplicate_send_attempted: false,
    raw_secret_values_recorded: false,
    raw_broker_endpoint_recorded: false
  };
}

function runtimeRunRequest(request: Record<string, unknown>) {
  const intentRef = "api://p024/acct-ctp-paper-19053/cancel/partial-fill-cancel-ui-test/intent";
  return {
    schema_version: "account_command.owner_runtime_run_request.v1",
    proposal_id: "p024-account-console-paper-command-controls",
    account_id: accountId,
    action: "cancel",
    mode: "paper_armed",
    status: "blocked_until_owner_runtime_invocation",
    command_id: "command.p024.partial-fill-cancel.ui-test-001",
    intent_id: request.intent_id,
    intent_ref: intentRef,
    idempotency_key: request.idempotency_key,
    owner_runtime_owner_ref: "owner://nautilus_ctp_adapter",
    owner_runtime_repo_ref: "owner-repo://nautilus_ctp_adapter",
    owner_runtime_entrypoint_ref: "scripts/ctp_guarded_paper_cancel_loop.py",
    owner_runtime_config_ref: "cfgs/local/ctp.openctp.tts.7x24.local.json",
    source_preflight_ref: request.readback_ref,
    readback_ref: request.readback_ref,
    expected_output_root_ref:
      "output/account_command/ctp-paper-19053/p024-ui-cancel-command.p024.partial-fill-cancel.ui-test-001",
    runtime_invocation_attempted: false,
    browser_triggered_broker_order: false,
    gateway_send_attempted: false,
    broker_order_created: false,
    raw_secret_values_recorded: false,
    raw_broker_endpoint_recorded: false,
    external_write_approval_required: true,
    blockers: [
      {
        blocker_id: "p024_cancel_owner_runtime_invocation_required",
        type: "owner_runtime_invocation_required",
        stage: "owner_runtime",
        reason: "handoff test fixture",
        source_ref: intentRef,
        next_action: "invoke owner runtime"
      },
      {
        blocker_id: "p024_cancel_external_write_approval_required",
        type: "external_write_approval_required",
        stage: "owner_runtime",
        reason: "handoff test fixture",
        source_ref: intentRef,
        next_action: "approve owner writes"
      },
      {
        blocker_id: "p024_cancel_post_run_ingest_required",
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

function listForProjection(projection: Record<string, unknown>) {
  const capabilities = projection.capabilities as Record<string, Record<string, unknown>>;
  return {
    schema_version: "account_mirror_list.v1",
    accounts: [
      {
        account_id: projection.account_id,
        display_alias: projection.display_alias,
        source_kind: projection.source_kind,
        source_mode: projection.source_mode,
        account_domain: projection.account_domain,
        route_id: "route.ctp.paper.19053",
        evidence_partition: "browser-evidence/p024-account-console-paper-command-controls",
        mirror_state: "ready",
        command_enabled: capabilities.command.enabled,
        command_mode: capabilities.command.mode,
        balance_count: 1,
        position_count: 0,
        order_count: 1,
        fill_count: (projection.fills as unknown[]).length,
        blocker_count: 0,
        projection_checkpoint_id: projection.projection_checkpoint_id,
        projection_checksum: projection.projection_checksum,
        source_ref: projection.source_ref,
        source_checksum: projection.source_checksum
      }
    ]
  };
}

function sourceHealthForProjection(projection: Record<string, unknown>) {
  return {
    schema_version: "account_mirror_source_health.v1",
    account_id: projection.account_id,
    state: "ready",
    source_ref: projection.source_ref,
    source_checksum: projection.source_checksum,
    observed_at: "2026-06-21T00:00:00Z",
    projection_checkpoint_id: projection.projection_checkpoint_id,
    projection_checksum: projection.projection_checksum,
    blockers: [],
    boundaries: projection.boundaries
  };
}

function evidenceForProjection(projection: Record<string, unknown>) {
  return {
    schema_version: "account_mirror_evidence.v1",
    account_id: projection.account_id,
    projection_checkpoint_id: projection.projection_checkpoint_id,
    projection_checksum: projection.projection_checksum,
    source_ref: projection.source_ref,
    source_checksum: projection.source_checksum,
    evidence: [
      {
        kind: "owner_approved_ui_contract_fixture",
        owner: "account-console-browser-acceptance-tests",
        source_ref: projection.source_ref,
        checksum: projection.source_checksum,
        authority: "UI display contract only; not OpenCTP runtime truth"
      },
      {
        kind: "mirror_projection",
        owner: "account-console-frontend-test",
        source_ref: projection.projection_checkpoint_id,
        checksum: projection.projection_checksum,
        authority: "mocked Account Mirror projection for browser display validation"
      }
    ],
    blockers: [],
    boundaries: projection.boundaries
  };
}

test("P024 Web UI displays partial-fill then cancel order lifecycle correctly", async ({ page }, testInfo) => {
  let currentProjection: Record<string, unknown> = projectionForStage(stages[0]);
  const cancelRequests: Record<string, unknown>[] = [];

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
    if (request.url().includes("runtime-run-requests")) {
      await route.fulfill({ json: runtimeRunRequest(payload), status: 202 });
      return;
    }
    cancelRequests.push(payload);
    await route.fulfill({ json: commandResult(payload), status: 202 });
  });

  mkdirSync(evidenceDir, { recursive: true });
  const observedStages: ObservedStage[] = [];

  for (const stage of stages) {
    currentProjection = projectionForStage(stage);
    await page.goto(`/accounts/${accountId}?p024_partial_stage=${stage.id}`);

    await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
    await expect(page.getByTestId("account-command-mode")).toHaveText("paper_armed");
    await expect(page.getByTestId("account-command-controls-state")).toHaveText("mounted");

    const row = page.getByTestId("tws-open-order-row").first();
    await expect(page.getByTestId("tws-open-order-row")).toHaveCount(1);
    await expect(row.getByTestId("account-order-identity")).toContainText("ctp19053-p024-partial-order-001");
    await expect(row.getByTestId("account-order-status")).toContainText(stage.status.replaceAll("_", " "));
    await expect(row.getByTestId("account-order-submitted-quantity")).toHaveText(String(stage.submitted));
    await expect(row.getByTestId("account-order-filled-quantity")).toHaveText(String(stage.filled));
    await expect(row.getByTestId("account-order-remaining-quantity")).toContainText(String(stage.remaining));
    await expect(row.getByTestId("account-order-cancelled-quantity")).toHaveText(
      stage.cancelled === null ? "missing" : String(stage.cancelled)
    );

    if (stage.id === "S2") {
      await expect(row.getByTestId("account-order-partial-fill-row")).toContainText("partial");
      await expect(row.getByTestId("account-remaining-cancel-quantity")).toHaveText(String(stage.remaining));
      await expect(page.getByTestId("account-cancel-order-identity")).toContainText("ctp19053-p024-partial-order-001");
      await expect(page.getByTestId("account-cancel-order-button")).toBeVisible();
      expect(stage.filled + stage.remaining).toBe(stage.submitted);
    }
    if (stage.id === "S3") {
      await expect(row.getByTestId("account-cancel-pending-ref")).toContainText("command-audit://");
      await expect(row.getByTestId("account-remaining-cancel-quantity")).toHaveCount(0);
      await expect(page.getByTestId("account-cancel-order-button")).toHaveCount(0);
      await expect(page.getByTestId("account-command-status-panel")).toBeVisible();
      await expect(page.getByTestId("account-command-audit-ref")).toContainText("command-audit://");
      await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("false");
    }
    if (stage.id === "S4") {
      expect(stage.filled + (stage.cancelled ?? 0)).toBe(stage.submitted);
      expect(stage.remaining).toBe(0);
      await expect(row.getByTestId("account-remaining-cancel-quantity")).toHaveCount(0);
      await expect(page.getByTestId("account-cancel-order-button")).toHaveCount(0);
      await expect(page.getByTestId("account-command-readback-ref")).toContainText(orderSourceRef(stage));
      await expect(page.getByTestId("account-command-reconciliation-ref")).toContainText("reconcile://");
      await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("false");
    }

    await expect(page.getByTestId("tws-fill-row")).toHaveCount(stage.fillRows);
    if (stage.fillRows === 0) {
      await expect(page.getByTestId("tws-fill-empty-state")).toContainText("No fill rows");
    } else {
      const fillRows = page.getByTestId("tws-fill-row");
      await expect(fillRows.nth(0).getByTestId("account-fill-quantity")).toHaveText("2");
      await expect(fillRows.nth(0).getByTestId("account-fill-price")).toHaveText("3299");
      await expect(fillRows.nth(0).getByTestId("account-fill-source-ref")).toContainText("ReqQryTrade");
      await expect(fillRows.nth(1).getByTestId("account-fill-quantity")).toHaveText("2");
      await expect(fillRows.nth(1).getByTestId("account-fill-price")).toHaveText("3298");
      await expect(fillRows.nth(1).getByTestId("account-fill-source-ref")).toContainText("ReqQryTrade");
    }

    if (testInfo.project.name === "desktop") {
      await page.screenshot({ fullPage: true, path: path.join(evidenceDir, stage.screenshot) });
    }

    const remainingCancelQuantity =
      (await row.getByTestId("account-remaining-cancel-quantity").count()) > 0
        ? await row.getByTestId("account-remaining-cancel-quantity").textContent()
        : null;
    const cancelPendingRef =
      (await row.getByTestId("account-cancel-pending-ref").count()) > 0
        ? await row.getByTestId("account-cancel-pending-ref").textContent()
        : null;
    const commandStatus = commandStatusForStage(stage);

    const orderBrowser = {
      identity: await row.getByTestId("account-order-identity").textContent(),
      status: await row.getByTestId("account-order-status").textContent(),
      submitted_quantity: await row.getByTestId("account-order-submitted-quantity").textContent(),
      filled_quantity: await row.getByTestId("account-order-filled-quantity").textContent(),
      remaining_quantity: await row.getByTestId("account-order-remaining-quantity").textContent(),
      cancelled_quantity: await row.getByTestId("account-order-cancelled-quantity").textContent(),
      remaining_cancel_quantity: remainingCancelQuantity,
      cancel_pending_ref: cancelPendingRef
    };
    const browserFillRows = [];
    const fillRows = page.getByTestId("tws-fill-row");
    for (let index = 0; index < stage.fillRows; index += 1) {
      const fillRow = fillRows.nth(index);
      const filledQuantity = parseBrowserInt(await fillRow.getByTestId("account-fill-quantity").textContent());
      browserFillRows.push({
        trade_id: await fillRow.getByTestId("tws-fill-status-or-trade").textContent(),
        filled_quantity: filledQuantity,
        price: parseBrowserInt(await fillRow.getByTestId("account-fill-price").textContent()),
        source_ref: await fillRow.getByTestId("account-fill-source-ref").textContent()
      });
    }
    const browserFillTotal = browserFillRows.reduce((total, fill) => total + (fill.filled_quantity ?? 0), 0);
    const apiFillRows = fillsForStage(stage).map((fill) => ({
      trade_id: fill.trade_id,
      filled_quantity: fill.filled_quantity,
      price: fill.last_px,
      source_ref: fill.source_ref
    }));
    const apiFillTotal = apiFillRows.reduce((total, fill) => total + fill.filled_quantity, 0);
    if (stage.fillRows > 0) {
      expect(browserFillTotal).toBe(stage.filled);
      expect(apiFillTotal).toBe(stage.filled);
    }

    observedStages.push({
      stage: stage.id,
      label: stage.label,
      browser: orderBrowser,
      browser_fill_rows: browserFillRows,
      browser_fill_total: browserFillTotal,
      api: {
        identity: "ctp19053-p024-partial-order-001",
        status: stage.status,
        submitted_quantity: stage.submitted,
        filled_quantity: stage.filled,
        remaining_quantity: stage.remaining,
        cancelled_quantity: stage.cancelled
      },
      api_fill_rows: apiFillRows,
      api_fill_total: apiFillTotal,
      order_artifact_ref: (currentProjection.orders as Record<string, unknown>[])[0].source_ref,
      fill_artifact_refs: fillsForStage(stage).map((fill) => fill.source_ref),
      command_status_refs: {
        audit: commandStatus?.command_audit_ref ?? null,
        risk: commandStatus?.risk_decision_refs ?? [],
        approval: commandStatus?.approval_decision_refs ?? [],
        gateway: commandStatus?.gateway_event_refs ?? [],
        readback: commandStatus?.readback_refs ?? [],
        reconciliation: commandStatus?.reconciliation_ref ?? null,
        gateway_ack_is_final_state: commandStatus?.gateway_ack_is_final_state === true
      },
      formula:
        stage.id === "S4"
          ? "filled_quantity + cancelled_quantity == submitted_quantity"
          : "filled_quantity + remaining_quantity == submitted_quantity",
      verdict: "pass"
    });

    if (stage.id === "S2") {
      await page.getByTestId("account-cancel-order-button").click();
      await expect(page.getByTestId("account-command-intent-receipt-panel")).toBeVisible();
      await expect(page.getByTestId("account-command-intent-ref")).toContainText("api://p024/");
      await expect(page.getByTestId("account-command-intent-status")).toHaveText("risk_gate_pending");
      await expect(page.getByTestId("account-command-intent-next-stage")).toHaveText("risk_decision");
      await expect(page.getByTestId("account-command-intent-gateway-final-state")).toHaveText("false");
      if (testInfo.project.name === "desktop") {
        await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-cancel-intent-accepted.png") });
      }
    }
  }

  const observedByStage = new Map(observedStages.map((stage) => [stage.stage, stage]));
  const s2 = observedByStage.get("S2");
  const s3 = observedByStage.get("S3");
  const s4 = observedByStage.get("S4");
  expect(s2).toBeDefined();
  expect(s3).toBeDefined();
  expect(s4).toBeDefined();
  const partialCancelDisplayChecks = {
    same_order_identity_across_stages: new Set(observedStages.map((stage) => stage.browser.identity)).size === 1,
    s2_browser_fill_sum_equals_order_filled_quantity: s2?.browser_fill_total === s2?.api.filled_quantity,
    s2_trade_refs_match_api_projection:
      JSON.stringify(s2?.browser_fill_rows.map((fill) => fill.source_ref)) ===
      JSON.stringify(s2?.api_fill_rows.map((fill) => fill.source_ref)),
    s2_cancel_target_equals_s2_remaining_quantity:
      parseBrowserInt(s2?.browser.remaining_cancel_quantity ?? null) === s2?.api.remaining_quantity,
    s3_quantities_unchanged_until_cancel_readback:
      s3?.api.filled_quantity === s2?.api.filled_quantity &&
      s3?.api.remaining_quantity === s2?.api.remaining_quantity &&
      s3?.browser_fill_total === s2?.browser_fill_total,
    s3_no_remaining_cancel_quantity_visible: s3?.browser.remaining_cancel_quantity === null,
    s3_cancel_pending_is_not_terminal: s3?.command_status_refs.gateway_ack_is_final_state === false,
    s4_filled_quantity_preserved_after_cancel:
      parseBrowserInt(s4?.browser.filled_quantity ?? null) === s2?.api.filled_quantity &&
      s4?.browser_fill_total === s2?.browser_fill_total,
    s4_cancelled_quantity_equals_s2_remaining_quantity:
      parseBrowserInt(s4?.browser.cancelled_quantity ?? null) === s2?.api.remaining_quantity,
    s4_remaining_quantity_zero: parseBrowserInt(s4?.browser.remaining_quantity ?? null) === 0,
    s4_no_remaining_cancel_quantity_visible: s4?.browser.remaining_cancel_quantity === null,
    fill_trade_identities_stable_after_cancel:
      JSON.stringify(s4?.browser_fill_rows.map((fill) => fill.trade_id)) ===
      JSON.stringify(s2?.browser_fill_rows.map((fill) => fill.trade_id))
  };
  expect(Object.values(partialCancelDisplayChecks).every(Boolean)).toBe(true);

  const cancelRequest = cancelRequests.find((request) => request.action === "cancel");
  expect(cancelRequest).toBeDefined();
  expect(cancelRequest?.venue_order_id).toBe("ctp19053-p024-partial-order-001");
  expect(cancelRequest?.readback_ref).toBe(orderSourceRef(stages[1]));
  expect(cancelRequest?.raw_secret_values_recorded).toBe(false);
  expect(cancelRequest?.raw_broker_endpoint_recorded).toBe(false);

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      orderDisplayEvidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-cancel-ui-acceptance.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          source_ref: sourceRef,
          source_checksum: sourceChecksum,
          projection_checksum: projectionChecksum,
          verdict: "browser_order_display_contract_pass_runtime_partial_fill_blocked",
          ui_order_display_verdict: "pass",
          partial_cancel_display_verdict: "pass",
          ui_command_control_verdict: "historical_fixture_governed_cancel_intent_display_only",
          runtime_partial_fill_verdict: "historical_fixture_governed_blocked_until_owner_evidence",
          stages: observedStages,
          partial_cancel_display_checks: partialCancelDisplayChecks,
          cancel_request: cancelRequest,
          command_artifacts: {
            cancel_intent_ref: "api://p024/acct-ctp-paper-19053/cancel/partial-fill-cancel-ui-test/intent",
            risk_decision_ref: "risk://p024/openctp19053/partial-fill-cancel/cancel-risk-pass",
            approval_decision_ref: "approval://p024/openctp19053/partial-fill-cancel/cancel-paper-approval",
            gateway_event_ref: "gateway://p024/openctp19053/partial-fill-cancel/cancel-requested",
            s3_cancel_pending_ref: "command-audit://p024/openctp19053/partial-fill-cancel/cancel-pending",
            s4_readback_ref: orderSourceRef(stages[3]),
            s4_reconciliation_ref: "reconcile://p024/openctp19053/partial-fill-cancel/s4-cancelled",
            gateway_ack_is_final_state: false,
            gateway_send_attempted_from_browser_test: false,
            broker_order_created_from_browser_test: false
          },
          raw_secret_values_recorded: false,
          raw_broker_endpoint_recorded: false,
          explicit_non_claims: [
            "does_not_prove_real_openctp_partial_fill_runtime",
            "does_not_use_screenshot_as_order_truth",
            "does_not_claim_live_readiness",
            "gateway_ack_is_not_final_state",
            "browser_test_does_not_send_broker_cancel",
            "typed_owner_approved_fixture_is_not_broker_truth"
          ],
          browser_evidence: [
            ...stages.map((stage) => ({
              stage: stage.id,
              screenshot: path.relative(path.resolve(".."), path.join(evidenceDir, stage.screenshot)).replaceAll("\\", "/")
            })),
            {
              stage: "S2_CANCEL_INTENT",
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-cancel-intent-accepted.png"))
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
