import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const runId = "p023-armed-20260621t0748z";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-closeout-ui.json");

test("P024 Web UI renders owner-backed runtime closeout without claiming browser trigger", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/runtime-closeouts/${runId}`
  );
  expect(apiResponse.status()).toBe(409);
  const closeout = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  await page.goto(`/accounts/${accountId}?p024_runtime_closeout=1`);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-runtime-closeout-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-closeout-error")).toContainText("runtime closeout request failed: 409");
  await expect(page.getByTestId("account-runtime-closeout-run-id")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-status")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-gateway-send")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-web-trigger")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-raw-secret")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-gateway-final")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-artifact-count")).toHaveCount(0);
  await expect(page.getByTestId("account-runtime-closeout-non-claim")).toHaveCount(0);

  await expect(page.getByTestId("account-command-status-panel")).toBeVisible();
  await expect(page.getByTestId("account-command-risk-ref")).toHaveCount(0);
  await expect(page.getByTestId("account-command-approval-ref")).toHaveCount(0);
  await expect(page.getByTestId("account-command-gateway-ref")).toHaveCount(0);
  await expect(page.getByTestId("account-command-readback-ref")).toHaveCount(0);
  await expect(page.getByText("No command audit evidence in this read-only projection.")).toBeVisible();
  await expect(page.getByTestId("account-command-audit-ref")).toHaveCount(0);
  await expect(page.getByTestId("account-command-reconciliation-ref")).toHaveCount(0);
  await expect(page.getByTestId("account-command-gateway-final-state")).toHaveCount(0);
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
          verdict: "blocked_pending_owner_runtime_evidence",
          api_status_code: apiResponse.status(),
          api_blocker: closeout.detail,
          runtime_gateway_send_observed: false,
          broker_order_created: false,
          browser_triggered_broker_order: false,
          gateway_ack_is_final_state: false,
          raw_secret_values_recorded: false,
          raw_broker_endpoint_recorded: false,
          explicit_non_claims: [
            "does_not_send_broker_order_from_browser_read",
            "does_not_store_raw_ctp_secret_or_endpoint",
            "does_not_claim_live_readiness",
            "does_not_make_gateway_ack_final_state",
            "does_not_promote_repo_local_output_to_runtime_truth",
            "owner_runtime_evidence_required_before_positive_claim"
          ],
          browser_checks: {
            runtime_panel_visible: true,
            owner_evidence_blocker_visible: true,
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
