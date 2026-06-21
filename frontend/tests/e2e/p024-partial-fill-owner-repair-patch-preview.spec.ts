import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-patch-preview-ui.json");

test("P024 Web UI renders owner repair patch preview", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/partial-fill-owner-repair-patch-preview`
  );
  expect(apiResponse.ok()).toBe(true);
  const preview = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pagePreviewPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-patch-preview`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_patch_preview=1`);
  const pagePreviewResponse = await pagePreviewPromise;
  expect(pagePreviewResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-status")).toHaveText(
    "phase4x_owner_repair_patch_preview_ready"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-verdict")).toHaveText(
    "patch_preview_ready_owner_write_not_authorized"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-baseline")).toHaveCount(2);
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-patch")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-patch")).toContainText([
    "generalize_close_offset_submit_observed",
    "expand_owner_rule_wording",
    "add_close_yesterday_focused_test"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-validator")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-fresh-approval")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-applied")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-patch-preview-full-claimed")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const baseline = preview.owner_baseline as Record<string, any>;
  const gate = preview.post_patch_runtime_gate as Record<string, unknown>;
  const negative = preview.negative_assertions as Record<string, unknown>;
  expect(baseline.owner_repo_write_attempted_by_preview).toBe(false);
  expect(preview.previewed_owner_patch).toHaveLength(3);
  expect(preview.post_patch_required_validators).toHaveLength(3);
  expect(gate.runtime_retry_authorized_by_preview).toBe(false);
  expect(gate.fresh_runtime_retry_approval_required_after_patch).toBe(true);
  expect(negative.owner_patch_applied).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-patch-preview-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-patch-preview-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_patch_preview: {
            schema: preview.schema,
            status: preview.status,
            verdict: preview.verdict,
            baseline_file_count: baseline.baseline_files.length,
            patch_count: preview.previewed_owner_patch.length,
            validator_count: preview.post_patch_required_validators.length,
            owner_repo_write_attempted: baseline.owner_repo_write_attempted_by_preview,
            runtime_retry_authorized: gate.runtime_retry_authorized_by_preview,
            fresh_retry_approval_required: gate.fresh_runtime_retry_approval_required_after_patch,
            owner_patch_applied: negative.owner_patch_applied,
            full_acceptance_claimed: negative.full_acceptance_claimed
          },
          browser_checks: {
            patch_preview_panel_visible: true,
            baseline_files_displayed: true,
            patches_displayed: true,
            validators_displayed: true,
            owner_write_displayed_false: true,
            runtime_retry_displayed_false: true,
            fresh_approval_displayed_true: true,
            patch_applied_displayed_false: true,
            full_acceptance_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-patch-preview-ui.png"))
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
