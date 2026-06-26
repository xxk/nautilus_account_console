import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-handoff-bundle-ui.json");

test("P024 Web UI renders owner-runtime execution handoff bundle without allowing execution", async ({
  page
}, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/runtime-execution-handoff-bundle`
  );
  expect(apiResponse.ok()).toBe(true);
  const bundle = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageBundlePromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/runtime-execution-handoff-bundle`)
  );
  await page.goto(`/accounts/${accountId}?p024_runtime_handoff_bundle=1`);
  const pageBundleResponse = await pageBundlePromise;
  expect(pageBundleResponse.status()).toBe(200);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-runtime-handoff-bundle-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-handoff-bundle-status")).toHaveText(
    "phase4c_owner_runtime_execution_handoff_bundle_ready"
  );
  await expect(page.getByTestId("account-runtime-handoff-bundle-verdict")).toHaveText(
    "handoff_bundle_ready_runtime_not_invoked"
  );
  await expect(page.getByTestId("account-runtime-handoff-bundle-execution-allowed")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-bundle-approval-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-bundle-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-bundle-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-bundle-broker-order")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-handoff-bundle-input")).toHaveCount(7);
  await expect(page.getByTestId("account-runtime-handoff-bundle-input")).toContainText([
    "owner_pre_snapshot_ref",
    "readback_order_identity"
  ]);
  await expect(page.getByTestId("account-runtime-handoff-bundle-step")).toHaveCount(7);
  await expect(page.getByTestId("account-runtime-handoff-bundle-step")).toContainText([
    "pre_approval_gate",
    "submit_runtime",
    "cancel_runtime",
    "browser_closeout"
  ]);
  await expect(page.getByTestId("account-runtime-handoff-bundle-step")).toContainText([
    "--arm-paper-send",
    "--arm-cancel-send"
  ]);
  await expect(page.getByTestId("account-runtime-handoff-bundle-artifact-count")).toHaveText("14");
  await expect(page.getByTestId("account-runtime-handoff-bundle-gate-count")).toHaveText("6");
  await expect(page.getByTestId("account-runtime-handoff-bundle-blocker")).toHaveCount(3);
  await expect(page.getByTestId("account-runtime-handoff-bundle-blocker")).toContainText([
    "external_write_approval_required",
    "runtime_inputs_required",
    "owner_runtime_artifacts_missing"
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
  expect(negative.browser_triggered_broker_order).toBe(false);
  expect(negative.gateway_send_attempted).toBe(false);
  expect(negative.broker_order_created).toBe(false);
  expect(negative.raw_secret_values_recorded).toBe(false);
  expect(negative.raw_broker_endpoint_recorded).toBe(false);
  expect(bundle.explicit_non_claims).toContain("does_not_guess_runtime_inputs");
  expect(bundle.explicit_non_claims).toContain("does_not_close_real_runtime_execution");

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-runtime-handoff-bundle-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.runtime-handoff-bundle-ui.v1",
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
            required_owner_artifact_count: (bundle.required_owner_artifacts as unknown[]).length,
            post_handoff_gate_count: (bundle.post_handoff_gates as unknown[]).length,
            blocker_count: (bundle.blockers as unknown[]).length,
            runtime_invocation_attempted: negative.runtime_invocation_attempted,
            owner_repo_write_attempted: negative.owner_repo_write_attempted,
            browser_triggered_broker_order: negative.browser_triggered_broker_order,
            gateway_send_attempted: negative.gateway_send_attempted,
            broker_order_created: negative.broker_order_created,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            handoff_bundle_panel_visible: true,
            execution_allowed_displayed_false: true,
            approval_obtained_displayed_false: true,
            runtime_invocation_displayed_false: true,
            owner_write_displayed_false: true,
            broker_order_displayed_false: true,
            runtime_inputs_displayed: true,
            operator_sequence_displayed: true,
            required_artifact_count_displayed: true,
            post_handoff_gate_count_displayed: true,
            blockers_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          explicit_non_claims: bundle.explicit_non_claims,
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-runtime-handoff-bundle-ui.png"))
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
