import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-runtime-handoff-bundle-ui.json");

test("P024 Web UI renders partial-fill runtime handoff bundle without allowing execution", async ({
  page
}, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-runtime-execution-handoff-bundle`
  );
  expect(apiResponse.ok()).toBe(true);
  const bundle = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageBundlePromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-runtime-execution-handoff-bundle`)
  );
  await page.goto(`/accounts/${accountId}?p024_partial_fill_runtime_handoff_bundle=1`);
  const pageBundleResponse = await pageBundlePromise;
  expect(pageBundleResponse.status()).toBe(200);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-status")).toHaveText(
    "phase4k_partial_fill_runtime_execution_handoff_bundle_ready"
  );
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-verdict")).toHaveText(
    "handoff_bundle_ready_runtime_not_invoked"
  );
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-execution-allowed")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-approval-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-new-order")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-cancel-sent")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-input")).toHaveCount(4);
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-input")).toContainText([
    "fresh_owner_pre_snapshot_ref",
    "quantity",
    "risk_reviewed_limit_price",
    "owner_post_submit_order_identity"
  ]);
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-step")).toHaveCount(7);
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-step")).toContainText([
    "pre_approval_gate",
    "submit_partial_fill_attempt",
    "cancel_remaining_if_identity_available",
    "ingest_or_preserve_blocker"
  ]);
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-success")).toContainText([
    "0 < filled_quantity < submitted_quantity",
    "filled_quantity + cancelled_quantity == submitted_quantity",
    "remaining_quantity == 0",
    "Web UI order identity matches owner native identity refs"
  ]);
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-fallback")).toHaveCount(4);
  await expect(page.getByTestId("account-partial-fill-runtime-handoff-bundle-fallback")).toContainText([
    "fully_filled_not_partial_fill_then_cancel",
    "cancelled_without_fill_not_partial_fill",
    "rejected_or_timeout_not_partial_fill",
    "owner_runtime_artifact_incomplete"
  ]);
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);
  await expect(page.getByText(/live ready|browser submitted broker order/i)).toHaveCount(0);

  const guard = bundle.execution_guard as Record<string, unknown>;
  const negative = bundle.negative_assertions as Record<string, unknown>;
  expect(guard.execution_allowed).toBe(false);
  expect(guard.approval_obtained).toBe(false);
  expect(negative.runtime_invocation_attempted).toBe(false);
  expect(negative.owner_repo_write_attempted).toBe(false);
  expect(negative.new_order_submitted).toBe(false);
  expect(negative.cancel_sent).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);
  expect(negative.browser_fixture_promoted_to_runtime_truth).toBe(false);
  expect(negative.raw_secret_values_recorded).toBe(false);
  expect(negative.raw_broker_endpoint_recorded).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, "p024-partial-fill-runtime-handoff-bundle-ui.png")
    });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-runtime-handoff-bundle-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_handoff_bundle: {
            schema: bundle.schema,
            status: bundle.status,
            verdict: bundle.verdict,
            execution_allowed: guard.execution_allowed,
            approval_required: guard.approval_required,
            approval_obtained: guard.approval_obtained,
            runtime_input_count: (bundle.runtime_input_requirements as unknown[]).length,
            operator_step_count: (bundle.operator_sequence as unknown[]).length,
            non_ui_success_count: ((bundle.success_criteria as Record<string, unknown>).non_ui_runtime as unknown[])
              .length,
            web_ui_success_count: ((bundle.success_criteria as Record<string, unknown>).web_ui_runtime as unknown[])
              .length,
            fallback_count: (bundle.fallback_classifications as unknown[]).length,
            runtime_invocation_attempted: negative.runtime_invocation_attempted,
            owner_repo_write_attempted: negative.owner_repo_write_attempted,
            new_order_submitted: negative.new_order_submitted,
            cancel_sent: negative.cancel_sent,
            full_acceptance_claimed: negative.full_acceptance_claimed,
            browser_fixture_promoted_to_runtime_truth: negative.browser_fixture_promoted_to_runtime_truth,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            handoff_bundle_panel_visible: true,
            execution_allowed_displayed_false: true,
            approval_obtained_displayed_false: true,
            runtime_invocation_displayed_false: true,
            owner_write_displayed_false: true,
            new_order_displayed_false: true,
            cancel_sent_displayed_false: true,
            runtime_inputs_displayed: true,
            operator_sequence_displayed: true,
            success_criteria_displayed: true,
            fallback_classifications_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-runtime-handoff-bundle-ui.png"))
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
