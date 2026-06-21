import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-execution-handoff-ui.json");

test("P024 Web UI renders owner repair execution handoff", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/partial-fill-owner-repair-execution-handoff-bundle`
  );
  expect(apiResponse.ok()).toBe(true);
  const bundle = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageBundlePromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-execution-handoff-bundle`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_execution_handoff=1`);
  const pageBundleResponse = await pageBundlePromise;
  expect(pageBundleResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-status")).toHaveText(
    "phase4z_owner_repair_execution_handoff_bundle_ready"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-verdict")).toHaveText(
    "handoff_bundle_ready_owner_write_not_invoked"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-execution")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-approval")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-step")).toHaveCount(7);
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-artifact")).toHaveCount(7);
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-patch-applied")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-execution-handoff-full-claimed")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const guard = bundle.execution_guard as Record<string, unknown>;
  const negative = bundle.negative_assertions as Record<string, unknown>;
  expect(guard.execution_allowed).toBe(false);
  expect(guard.owner_repo_write_allowed_by_this_bundle).toBe(false);
  expect(guard.runtime_retry_authorized_by_this_bundle).toBe(false);
  expect(bundle.operator_sequence_after_exact_approval).toHaveLength(7);
  expect(bundle.required_post_handoff_artifacts).toHaveLength(7);
  expect(negative.owner_patch_applied).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-execution-handoff-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-execution-handoff-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_execution_handoff: {
            schema: bundle.schema,
            status: bundle.status,
            verdict: bundle.verdict,
            step_count: bundle.operator_sequence_after_exact_approval.length,
            artifact_count: bundle.required_post_handoff_artifacts.length,
            execution_allowed: guard.execution_allowed,
            owner_repo_write_allowed: guard.owner_repo_write_allowed_by_this_bundle,
            runtime_retry_authorized: guard.runtime_retry_authorized_by_this_bundle,
            exact_approval_required: guard.requires_exact_owner_repair_approval,
            owner_patch_applied: negative.owner_patch_applied,
            full_acceptance_claimed: negative.full_acceptance_claimed
          },
          browser_checks: {
            handoff_panel_visible: true,
            steps_displayed: true,
            artifacts_displayed: true,
            execution_displayed_false: true,
            owner_write_displayed_false: true,
            runtime_retry_displayed_false: true,
            exact_approval_displayed_true: true,
            patch_applied_displayed_false: true,
            full_acceptance_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-execution-handoff-ui.png"))
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
