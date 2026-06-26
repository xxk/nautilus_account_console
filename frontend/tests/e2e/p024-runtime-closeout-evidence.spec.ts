import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const runId = "p023-armed-20260621t0748z";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-closeout-ui.json");

test("P024 Web UI renders owner-backed runtime closeout without claiming browser trigger", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/runtime-closeouts/${runId}`
  );
  expect(apiResponse.ok()).toBe(true);
  const closeout = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  await page.goto(`/accounts/${accountId}?p024_runtime_closeout=1`);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-runtime-closeout-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-closeout-run-id")).toHaveText(runId);
  await expect(page.getByTestId("account-runtime-closeout-status")).toHaveText("reconciled");
  await expect(page.getByTestId("account-runtime-closeout-gateway-send")).toHaveText("true");
  await expect(page.getByTestId("account-runtime-closeout-web-trigger")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-closeout-raw-secret")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-closeout-gateway-final")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-closeout-artifact-count")).toHaveText("13");
  await expect(page.getByTestId("account-runtime-closeout-non-claim")).toContainText([
    "does_not_send_broker_order_from_browser_read",
    "does_not_store_raw_ctp_secret_or_endpoint",
    "does_not_claim_live_readiness",
    "does_not_make_gateway_ack_final_state",
    "web_ui_trigger_of_new_runtime_order_still_pending"
  ]);

  await expect(page.getByTestId("account-command-audit-ref")).toContainText("command_audit.json");
  await expect(page.getByTestId("account-command-risk-ref")).toHaveCount(2);
  await expect(page.getByTestId("account-command-approval-ref")).toHaveCount(2);
  await expect(page.getByTestId("account-command-gateway-ref")).toHaveCount(2);
  await expect(page.getByTestId("account-command-readback-ref")).toHaveCount(2);
  await expect(page.getByTestId("account-command-reconciliation-ref")).toContainText("reconciliation_result.json");
  await expect(page.getByTestId("account-command-gateway-final-state")).toHaveText("false");
  await expect(page.getByText(/live ready|live armed|gateway ack final|browser submitted broker order/i)).toHaveCount(0);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-runtime-closeout-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.runtime-closeout-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          run_id: runId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_schema: closeout.schema_version,
          api_status: closeout.status,
          api_mode: closeout.mode,
          closeout_manifest_ref: closeout.closeout_manifest_ref,
          closeout_manifest_checksum: closeout.closeout_manifest_checksum,
          command_audit_ref: closeout.command_audit_ref,
          command_audit_checksum: closeout.command_audit_checksum,
          intent_ref_count: (closeout.intent_refs as unknown[]).length,
          risk_ref_count: (closeout.risk_decision_refs as unknown[]).length,
          approval_ref_count: (closeout.approval_decision_refs as unknown[]).length,
          gateway_ref_count: (closeout.gateway_event_refs as unknown[]).length,
          readback_ref_count: (closeout.readback_refs as unknown[]).length,
          reconciliation_ref: closeout.reconciliation_ref,
          artifact_checksum_count: Object.keys(closeout.artifact_checksums as Record<string, unknown>).length,
          runtime_gateway_send_observed: closeout.runtime_gateway_send_observed,
          broker_order_created: closeout.broker_order_created,
          browser_triggered_broker_order: closeout.browser_triggered_broker_order,
          gateway_ack_is_final_state: closeout.gateway_ack_is_final_state,
          raw_secret_values_recorded: closeout.raw_secret_values_recorded,
          raw_broker_endpoint_recorded: closeout.raw_broker_endpoint_recorded,
          explicit_non_claims: closeout.explicit_non_claims,
          browser_checks: {
            runtime_panel_visible: true,
            command_status_refs_visible: true,
            browser_trigger_displayed_false: true,
            gateway_final_displayed_false: true,
            live_ready_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-runtime-closeout-ui.png"))
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
