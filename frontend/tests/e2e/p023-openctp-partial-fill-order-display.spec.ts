import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const sourceRef = "owner-approved-fixture://p023/openctp19053/partial-fill-ui-contract";
const sourceChecksum = "sha256:2323232323232323232323232323232323232323232323232323232323232323";
const projectionChecksum = "sha256:4545454545454545454545454545454545454545454545454545454545454545";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p023-openctp-19053-command");
const orderDisplayEvidencePath = path.join(evidenceDir, "partial-fill-order-display.json");
const closeoutPath = path.join(evidenceDir, "closeout.json");

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
    screenshot: "submit-readback.png"
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
    screenshot: "partial-fill-readback.png"
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
    screenshot: "blocker-state.png"
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
    screenshot: "cancel-readback.png"
  }
];

function orderForStage(stage: StageExpectation) {
  return {
    report_id: `report.ctp19053.partial.${stage.id.toLowerCase()}.order-status`,
    nautilus_report_type: "OrderStatusReport",
    client_order_id: "p023-partial-rb2610-001",
    venue_order_id: "ctp19053-partial-order-001",
    instrument_id: "rb2610.SHFE",
    instrument: "rb2610",
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
        ? "command-audit://p023/openctp19053/partial-fill/cancel-pending"
        : `readback://p023/openctp19053/partial-fill/${stage.id.toLowerCase()}/order`,
    source_ref: `readback://p023/openctp19053/partial-fill/${stage.id.toLowerCase()}/order`,
    source_checksum: `sha256:${stage.id.toLowerCase().repeat(32).slice(0, 64)}`
  };
}

function fillsForStage(stage: StageExpectation) {
  if (stage.fillRows === 0) {
    return [];
  }
  return [
    {
      report_id: "report.ctp19053.partial.s2.fill.001",
      nautilus_report_type: "FillReport",
      client_order_id: "p023-partial-rb2610-001",
      venue_order_id: "ctp19053-partial-order-001",
      instrument_id: "rb2610.SHFE",
      instrument: "rb2610",
      side: "SELL",
      order_status: "PARTIALLY_FILLED",
      quantity: 10,
      filled_quantity: 2,
      remaining_quantity: 8,
      trade_id: "ctp19053-partial-trade-001",
      last_px: 3299,
      sequence: 2,
      source_ref: "ReqQryTrade://p023/openctp19053/partial-fill/s2/trade-001",
      source_checksum: "sha256:0101010101010101010101010101010101010101010101010101010101010101"
    },
    {
      report_id: "report.ctp19053.partial.s2.fill.002",
      nautilus_report_type: "FillReport",
      client_order_id: "p023-partial-rb2610-001",
      venue_order_id: "ctp19053-partial-order-001",
      instrument_id: "rb2610.SHFE",
      instrument: "rb2610",
      side: "SELL",
      order_status: "PARTIALLY_FILLED",
      quantity: 10,
      filled_quantity: 2,
      remaining_quantity: 6,
      trade_id: "ctp19053-partial-trade-002",
      last_px: 3298,
      sequence: 3,
      source_ref: "ReqQryTrade://p023/openctp19053/partial-fill/s2/trade-002",
      source_checksum: "sha256:0202020202020202020202020202020202020202020202020202020202020202"
    }
  ];
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
      command: { enabled: false, mode: "disabled" }
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
    blockers: [],
    projection_checkpoint_id: `mirror.p023.openctp19053.partial-fill.${stage.id.toLowerCase()}`,
    projection_checksum: projectionChecksum,
    source_ref: sourceRef,
    source_checksum: sourceChecksum,
    route_context: {
      route_id: "route.ctp.paper.19053",
      evidence_partition: "browser-evidence/p023-openctp-19053-command",
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

function listForProjection(projection: Record<string, unknown>) {
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
        evidence_partition: "browser-evidence/p023-openctp-19053-command",
        mirror_state: "ready",
        command_enabled: false,
        command_mode: "disabled",
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

test("P023 Web UI displays partial-fill order lifecycle without using UI as truth", async ({ page }, testInfo) => {
  let currentProjection: Record<string, unknown> = projectionForStage(stages[0]);

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

  mkdirSync(evidenceDir, { recursive: true });
  const observedStages = [];

  for (const stage of stages) {
    currentProjection = projectionForStage(stage);
    await page.goto(`/accounts/${accountId}?p023_stage=${stage.id}`);

    await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
    await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);

    const row = page.getByTestId("tws-open-order-row").first();
    await expect(page.getByTestId("tws-open-order-row")).toHaveCount(1);
    await expect(row.getByTestId("account-order-identity")).toContainText("ctp19053-partial-order-001");
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
      expect(stage.filled + stage.remaining).toBe(stage.submitted);
    }
    if (stage.id === "S3") {
      await expect(row.getByTestId("account-cancel-pending-ref")).toContainText("command-audit://");
    }
    if (stage.id === "S4") {
      expect(stage.filled + (stage.cancelled ?? 0)).toBe(stage.submitted);
      expect(stage.remaining).toBe(0);
    }

    await expect(page.getByTestId("tws-fill-row")).toHaveCount(stage.fillRows);
    if (stage.fillRows === 0) {
      await expect(page.getByTestId("tws-fill-empty-state")).toContainText("No fill rows");
    } else {
      const fillRows = page.getByTestId("tws-fill-row");
      await expect(fillRows.nth(0).getByTestId("account-fill-quantity")).toHaveText("2");
      await expect(fillRows.nth(0).getByTestId("account-fill-price")).toHaveText("3299");
      await expect(fillRows.nth(0).getByTestId("account-fill-source-ref")).toContainText("ReqQryTrade");
    }

    const stageScreenshot =
      testInfo.project.name === "desktop"
        ? path.join(evidenceDir, stage.screenshot)
        : path.join(evidenceDir, `${testInfo.project.name}-${stage.screenshot}`);
    await page.screenshot({ fullPage: true, path: stageScreenshot });
    if (stage.id === "S1" && testInfo.project.name === "desktop") {
      await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "disabled-state.png") });
    }

    const orderBrowser = {
      identity: await row.getByTestId("account-order-identity").textContent(),
      status: await row.getByTestId("account-order-status").textContent(),
      submitted_quantity: await row.getByTestId("account-order-submitted-quantity").textContent(),
      filled_quantity: await row.getByTestId("account-order-filled-quantity").textContent(),
      remaining_quantity: await row.getByTestId("account-order-remaining-quantity").textContent(),
      cancelled_quantity: await row.getByTestId("account-order-cancelled-quantity").textContent()
    };

    observedStages.push({
      stage: stage.id,
      label: stage.label,
      browser: orderBrowser,
      api: {
        identity: "ctp19053-partial-order-001",
        status: stage.status,
        submitted_quantity: stage.submitted,
        filled_quantity: stage.filled,
        remaining_quantity: stage.remaining,
        cancelled_quantity: stage.cancelled
      },
      artifact_ref: (currentProjection.orders as Record<string, unknown>[])[0].source_ref,
      fill_artifact_refs: fillsForStage(stage).map((fill) => fill.source_ref),
      formula:
        stage.id === "S4"
          ? "filled_quantity + cancelled_quantity == submitted_quantity"
          : "filled_quantity + remaining_quantity == submitted_quantity",
      verdict: "pass"
    });
  }

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      orderDisplayEvidencePath,
      JSON.stringify(
        {
          schema: "account-console.p023.partial-fill-order-display.v1",
          proposal_id: "p023-openctp-19053-paper-command-capability",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          source_ref: sourceRef,
          source_checksum: sourceChecksum,
          projection_checksum: projectionChecksum,
          ui13_order_display_verdict: "pass",
          ui13_action_control_verdict: "typed_blocker_command_controls_disabled",
          runtime_partial_fill_verdict: "typed_blocker_until_real_or_owner_approved_partial_fill_state",
          stages: observedStages,
          explicit_non_claims: [
            "does_not_submit_orders",
            "does_not_cancel_orders",
            "does_not_prove_real_openctp_partial_fill_runtime",
            "does_not_use_screenshot_as_order_truth",
            "does_not_enable_command_capability"
          ],
          browser_evidence: stages.map((stage) => ({
            stage: stage.id,
            screenshot: path.relative(path.resolve(".."), path.join(evidenceDir, stage.screenshot)).replaceAll("\\", "/")
          })),
          disabled_state_screenshot: path
            .relative(path.resolve(".."), path.join(evidenceDir, "disabled-state.png"))
            .replaceAll("\\", "/")
        },
        null,
        2
      )
    );
    writeFileSync(
      closeoutPath,
      JSON.stringify(
        {
          schema: "account-console.p023.browser-closeout.v1",
          proposal_id: "p023-openctp-19053-paper-command-capability",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "browser_order_display_contract_pass_runtime_partial_fill_blocked",
          order_display_evidence: path
            .relative(path.resolve(".."), orderDisplayEvidencePath)
            .replaceAll("\\", "/"),
          command_enabled: false,
          command_mode: "disabled",
          runtime_partial_fill: "blocked_until_real_or_owner_approved_partial_fill_state",
          explicit_non_claims: [
            "does_not_submit_orders",
            "does_not_cancel_orders",
            "does_not_claim_live_readiness"
          ]
        },
        null,
        2
      )
    );
  }
});
