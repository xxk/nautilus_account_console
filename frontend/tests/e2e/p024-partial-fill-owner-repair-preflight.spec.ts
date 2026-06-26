import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-preflight-ui.json");

test("P024 Web UI renders owner repair preflight source audit", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-owner-repair-preflight-source-audit`
  );
  expect(apiResponse.ok()).toBe(true);
  const audit = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageAuditPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-preflight-source-audit`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_preflight=1`);
  const pageAuditResponse = await pageAuditPromise;
  expect(pageAuditResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-status")).toHaveText(
    "phase4v_owner_repair_preflight_source_audited"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-verdict")).toHaveText(
    "owner_repair_still_required_before_runtime_retry"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-owner-path")).toHaveText(
    "D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-source")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-source")).toContainText([
    "scripts/ctp_guarded_paper_order_loop.py",
    "tests/test_guarded_paper_order_loop.py",
    "tests/test_nautilus_integration.py"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-repair-approval")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-retry-approval")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-blind-retry")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-runtime-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-preflight-full-claimed")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const approval = audit.operator_approval_delta as Record<string, unknown>;
  const next = audit.next_required_action as Record<string, unknown>;
  const negative = audit.negative_assertions as Record<string, unknown>;
  expect(approval.sufficient_for_owner_code_repair).toBe(false);
  expect(approval.sufficient_for_post_repair_runtime_retry).toBe(false);
  expect(next.blind_script_retry_rejected).toBe(true);
  expect(negative.owner_runtime_invocation_attempted).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-preflight-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-preflight-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_preflight: {
            schema: audit.schema,
            status: audit.status,
            verdict: audit.verdict,
            source_check_count: audit.source_checks.length,
            owner_repo_write_attempted: audit.owner_repo.write_attempted_by_audit,
            repair_approval_sufficient: approval.sufficient_for_owner_code_repair,
            retry_approval_sufficient: approval.sufficient_for_post_repair_runtime_retry,
            blind_script_retry_rejected: next.blind_script_retry_rejected,
            runtime_invocation_attempted: negative.owner_runtime_invocation_attempted,
            full_acceptance_claimed: negative.full_acceptance_claimed
          },
          browser_checks: {
            preflight_panel_visible: true,
            source_checks_displayed: true,
            owner_write_displayed_false: true,
            repair_approval_displayed_false: true,
            retry_approval_displayed_false: true,
            blind_retry_displayed_true: true,
            runtime_invoked_displayed_false: true,
            full_acceptance_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-preflight-ui.png"))
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
