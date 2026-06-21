import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const sourceRef = "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/command_audit.json";
const sourceChecksum = "sha256:9ae6f852d20f24f516766a0aeaa11ee3a9c97e9ea29fd9aa282d2ccaabfc6837";
const projectionChecksum = "sha256:6969696969696969696969696969696969696969696969696969696969696969";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p023-openctp-19053-command");
const evidencePath = path.join(evidenceDir, "ui-status-evidence.json");

type StatusStageId = "reconciled" | "gateway_ack_only_blocked";

interface StatusStage {
  id: StatusStageId;
  label: string;
  screenshot: string;
  commandStatus: Record<string, unknown>;
}

const refs = {
  audit: "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/command_audit.json",
  risk: "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/submit_risk_decision.json",
  approval: "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/submit_approval_decision.json",
  gateway: "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/submit_gateway_event.json",
  readback: "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json",
  reconcile: "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/reconciliation_result.json"
};

const stages: StatusStage[] = [
  {
    id: "reconciled",
    label: "audit/readback/reconcile complete",
    screenshot: "command-status-reconciled.png",
    commandStatus: {
      schema_version: "account_command.ui_status_projection.v1",
      status: "reconciled",
      command_audit_ref: refs.audit,
      risk_decision_refs: [refs.risk],
      approval_decision_refs: [refs.approval],
      gateway_event_refs: [refs.gateway],
      readback_refs: [refs.readback],
      reconciliation_ref: refs.reconcile,
      gateway_ack_is_final_state: false,
      readback_required: true,
      reconciliation_required: true,
      blockers: []
    }
  },
  {
    id: "gateway_ack_only_blocked",
    label: "gateway ack without readback is blocked",
    screenshot: "command-status-blocked.png",
    commandStatus: {
      schema_version: "account_command.ui_status_projection.v1",
      status: "blocked",
      command_audit_ref: refs.audit,
      risk_decision_refs: [refs.risk],
      approval_decision_refs: [refs.approval],
      gateway_event_refs: [refs.gateway],
      readback_refs: [],
      reconciliation_ref: null,
      gateway_ack_is_final_state: true,
      readback_required: true,
      reconciliation_required: true,
      blockers: [
        {
          stage: "post_submit_readback",
          reason: "gateway ack cannot finalize command status without readback and reconciliation",
          source_ref: refs.gateway
        }
      ]
    }
  }
];

function projectionForStage(stage: StatusStage) {
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
        source_ref: sourceRef,
        checksum: sourceChecksum
      }
    ],
    positions: [],
    orders: [
      {
        report_id: "report.ctp19053.p023.status.order",
        nautilus_report_type: "OrderStatusReport",
        client_order_id: "p023-rb2610-close-20260621t0748z",
        venue_order_id: "2",
        instrument_id: "rb2610.SHFE",
        instrument: "rb2610",
        side: "SELL",
        status: "canceled",
        order_status: "canceled",
        quantity: 1,
        filled_quantity: 0,
        remaining_quantity: 0,
        cancelled_quantity: 1,
        limit_price: 3300,
        source_ref: refs.readback,
        source_checksum: "sha256:0108e2cad1619b775bab7d9765b4486d044fe0ac0bc95621897d739348320475"
      }
    ],
    fills: [],
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
    command_status: stage.commandStatus,
    blockers: [],
    projection_checkpoint_id: `mirror.p023.openctp19053.command-status.${stage.id}`,
    projection_checksum: projectionChecksum,
    source_ref: sourceRef,
    source_checksum: sourceChecksum,
    route_context: {
      route_id: "route.ctp.paper.19053",
      evidence_partition: "browser-evidence/p023-openctp-19053-command",
      account_truth: "command_status_ui_contract_fixture_not_runtime_truth"
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
        fill_count: 0,
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
        kind: "command_audit",
        owner: "account-console-browser-acceptance-tests",
        source_ref: refs.audit,
        checksum: sourceChecksum,
        authority: "UI status display contract only; command state remains artifact/readback owned"
      }
    ],
    blockers: [],
    boundaries: projection.boundaries
  };
}

test("P023 Web UI displays command status only from audit readback and reconciliation", async ({ page }, testInfo) => {
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
    await page.goto(`/accounts/${accountId}?p023_command_status=${stage.id}`);

    await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
    await expect(page.getByText(/submit order|place order|cancel order|replace order|can trade/i)).toHaveCount(0);
    await expect(page.getByTestId("account-command-status-panel")).toBeVisible();
    await expect(page.getByTestId("account-command-audit-ref")).toContainText(refs.audit);
    await expect(page.getByTestId("account-command-risk-ref")).toContainText(refs.risk);
    await expect(page.getByTestId("account-command-approval-ref")).toContainText(refs.approval);
    await expect(page.getByTestId("account-command-gateway-ref")).toContainText(refs.gateway);

    if (stage.id === "reconciled") {
      await expect(page.getByTestId("account-command-readback-ref")).toContainText(refs.readback);
      await expect(page.getByTestId("account-command-reconciliation-ref")).toContainText(refs.reconcile);
      await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("false");
      await expect(page.getByTestId("account-command-blocker")).toHaveCount(0);
    } else {
      await expect(page.getByTestId("account-command-readback-ref")).toHaveCount(0);
      await expect(page.getByTestId("account-command-reconciliation-ref")).toHaveCount(0);
      await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("invalid");
      await expect(page.getByTestId("account-command-blocker").filter({ hasText: "gateway ack is not final" })).toHaveCount(1);
      await expect(page.getByTestId("account-command-blocker").filter({ hasText: "missing readback refs" })).toHaveCount(1);
      await expect(page.getByTestId("account-command-blocker").filter({ hasText: "missing reconciliation ref" })).toHaveCount(1);
    }

    const screenshotPath =
      testInfo.project.name === "desktop"
        ? path.join(evidenceDir, stage.screenshot)
        : path.join(evidenceDir, `${testInfo.project.name}-${stage.screenshot}`);
    await page.screenshot({ fullPage: true, path: screenshotPath });

    observedStages.push({
      stage: stage.id,
      label: stage.label,
      browser: {
        audit_ref_seen: await page.getByTestId("account-command-audit-ref").textContent(),
        gateway_ref_seen: await page.getByTestId("account-command-gateway-ref").textContent(),
        gateway_final_state: await page.getByTestId("account-command-gateway-final-state").textContent(),
        readback_ref_count: await page.getByTestId("account-command-readback-ref").count(),
        reconciliation_ref_count: await page.getByTestId("account-command-reconciliation-ref").count(),
        blocker_count: await page.getByTestId("account-command-blocker").count()
      },
      api: {
        status: stage.commandStatus.status,
        command_audit_ref: stage.commandStatus.command_audit_ref,
        gateway_event_refs: stage.commandStatus.gateway_event_refs,
        readback_refs: stage.commandStatus.readback_refs,
        reconciliation_ref: stage.commandStatus.reconciliation_ref,
        gateway_ack_is_final_state: stage.commandStatus.gateway_ack_is_final_state
      },
      verdict: "pass"
    });
  }

  if (testInfo.project.name === "desktop") {
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p023.ui-status-evidence.v1",
          proposal_id: "p023-openctp-19053-paper-command-capability",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          ui09_status_evidence_verdict: "pass",
          gateway_ack_final_state_rejected: true,
          command_controls_enabled: false,
          command_mode: "disabled",
          stages: observedStages,
          explicit_non_claims: [
            "does_not_submit_orders",
            "does_not_cancel_orders",
            "does_not_enable_command_controls",
            "does_not_treat_gateway_ack_as_final_state",
            "does_not_use_screenshot_as_command_truth"
          ],
          browser_evidence: stages.map((stage) => ({
            stage: stage.id,
            screenshot: path.relative(path.resolve(".."), path.join(evidenceDir, stage.screenshot)).replaceAll("\\", "/")
          }))
        },
        null,
        2
      )
    );
  }
});
