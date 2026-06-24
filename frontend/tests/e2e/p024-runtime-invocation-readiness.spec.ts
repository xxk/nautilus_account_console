import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-readiness-ui.json");

test("P024 Web UI renders owner-runtime readiness blocker without invoking runtime", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/runtime-invocation-readiness`
  );
  expect(apiResponse.ok()).toBe(true);
  const readiness = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageReadinessPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/runtime-invocation-readiness`)
  );
  await page.goto(`/accounts/${accountId}?p024_runtime_readiness=1`);
  const pageReadinessResponse = await pageReadinessPromise;
  expect(pageReadinessResponse.status()).toBe(200);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-runtime-readiness-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-readiness-status")).toHaveText(
    "blocked_waiting_for_external_owner_runtime_write_approval"
  );
  await expect(page.getByTestId("account-runtime-readiness-owner")).toHaveText("owner://nautilus_ctp_adapter");
  await expect(page.getByTestId("account-runtime-readiness-owner-path")).toContainText(
    "D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-runtime-readiness-config-ref")).toHaveText(
    "cfgs/local/ctp.openctp.tts.7x24.local.json"
  );
  await expect(page.getByTestId("account-runtime-readiness-config-raw")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-readiness-approval-required")).toHaveText("true");
  await expect(page.getByTestId("account-runtime-readiness-approval-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-readiness-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-readiness-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-readiness-browser-trigger")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-readiness-raw-secret")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-readiness-entrypoint")).toHaveCount(2);
  await expect(page.getByTestId("account-runtime-readiness-entrypoint")).toContainText([
    "scripts/ctp_guarded_paper_order_loop.py",
    "scripts/ctp_guarded_paper_cancel_loop.py"
  ]);
  await expect(page.getByTestId("account-runtime-readiness-entrypoint")).toContainText([
    "--arm-paper-send",
    "--arm-cancel-send"
  ]);
  await expect(page.getByTestId("account-runtime-readiness-blocker")).toHaveCount(2);
  await expect(page.getByTestId("account-runtime-readiness-blocker")).toContainText([
    "external_write_approval_required",
    "owner_runtime_artifacts_missing"
  ]);
  await expect(page.getByTestId("account-runtime-readiness-non-claim")).toContainText([
    "does_not_invoke_owner_runtime",
    "does_not_write_owner_repo",
    "does_not_close_phase_3_runtime_execution"
  ]);
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);
  await expect(page.getByText(/live ready|browser submitted broker order/i)).toHaveCount(0);

  const ownerRuntime = readiness.owner_runtime as Record<string, unknown>;
  const externalApproval = readiness.external_write_approval_request as Record<string, unknown>;
  const negative = readiness.negative_assertions as Record<string, unknown>;
  expect(ownerRuntime.config_raw_content_read).toBe(false);
  expect(ownerRuntime.raw_secret_values_recorded).toBe(false);
  expect(ownerRuntime.raw_broker_endpoint_recorded).toBe(false);
  expect(externalApproval.required).toBe(true);
  expect(externalApproval.obtained).toBe(false);
  expect(negative.runtime_invocation_attempted).toBe(false);
  expect(negative.owner_repo_write_attempted).toBe(false);
  expect(negative.browser_triggered_broker_order).toBe(false);
  expect(negative.gateway_send_attempted).toBe(false);
  expect(negative.broker_order_created).toBe(false);
  expect(negative.raw_secret_values_recorded).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-runtime-readiness-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.runtime-readiness-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_readiness: {
            schema: readiness.schema,
            status: readiness.status,
            verdict: readiness.verdict,
            owner_ref: ownerRuntime.owner_ref,
            owner_repo_path: ownerRuntime.owner_repo_path,
            config_ref: ownerRuntime.config_ref,
            config_raw_content_read: ownerRuntime.config_raw_content_read,
            approval_required: externalApproval.required,
            approval_obtained: externalApproval.obtained,
            entrypoint_count: (readiness.entrypoints as unknown[]).length,
            blocker_count: (readiness.blockers as unknown[]).length,
            runtime_invocation_attempted: negative.runtime_invocation_attempted,
            owner_repo_write_attempted: negative.owner_repo_write_attempted,
            browser_triggered_broker_order: negative.browser_triggered_broker_order,
            gateway_send_attempted: negative.gateway_send_attempted,
            broker_order_created: negative.broker_order_created,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            readiness_panel_visible: true,
            owner_ref_displayed: true,
            owner_path_displayed: true,
            config_ref_displayed_without_raw_endpoint: true,
            approval_required_displayed_true: true,
            approval_obtained_displayed_false: true,
            runtime_invocation_displayed_false: true,
            owner_write_displayed_false: true,
            browser_trigger_displayed_false: true,
            raw_secret_displayed_false: true,
            entrypoints_displayed: true,
            blockers_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          explicit_non_claims: readiness.explicit_non_claims,
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-runtime-readiness-ui.png"))
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
