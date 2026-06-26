import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-execution-gap-audit-ui.json");

test("P024 Web UI renders final runtime execution gap without claiming full acceptance", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/runtime-execution-gap-audit`
  );
  expect(apiResponse.ok()).toBe(true);
  const audit = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageAuditPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/runtime-execution-gap-audit`)
  );
  await page.goto(`/accounts/${accountId}?p024_runtime_execution_gap=1`);
  const pageAuditResponse = await pageAuditPromise;
  expect(pageAuditResponse.status()).toBe(200);

  await expect(page.getByTestId("account-runtime-execution-gap-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-execution-gap-status")).toHaveText(
    "phase4e_final_runtime_execution_gap_audited"
  );
  await expect(page.getByTestId("account-runtime-execution-gap-verdict")).toHaveText(
    "blocked_pending_owner_runtime_execution"
  );
  await expect(page.getByTestId("account-runtime-execution-gap-final-claimed")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-execution-gap-accepted-count")).toHaveText("14");
  await expect(page.getByTestId("account-runtime-execution-gap-not-accepted")).toContainText("A4");
  await expect(page.getByTestId("account-runtime-execution-gap-not-accepted")).toContainText(
    "blocked_pending_owner_runtime_execution"
  );
  await expect(page.getByTestId("account-runtime-execution-gap-not-accepted")).toContainText(
    "approved owner-runtime execution artifacts"
  );
  await expect(page.getByTestId("account-runtime-execution-gap-approval-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-execution-gap-approval-path")).toHaveText(
    "D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-runtime-execution-gap-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-execution-gap-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-execution-gap-broker-order")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-execution-gap-artifact-count")).toHaveText("14");
  await expect(page.getByTestId("account-runtime-execution-gap-required")).toHaveCount(8);
  await expect(page.getByTestId("account-runtime-execution-gap-blocker")).toHaveCount(3);
  await expect(page.getByTestId("account-runtime-execution-gap-blocker")).toContainText([
    "external_write_approval_required",
    "owner_runtime_artifacts_missing",
    "owner_runtime_partial_fill_state_missing"
  ]);
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);
  await expect(page.getByText(/full acceptance complete|broker order created/i)).toHaveCount(0);

  const negative = audit.negative_assertions as Record<string, unknown>;
  expect(negative.final_acceptance_claimed).toBe(false);
  expect(negative.runtime_invocation_attempted).toBe(false);
  expect(negative.owner_repo_write_attempted).toBe(false);
  expect(negative.broker_order_created).toBe(false);
  expect(audit.explicit_non_claims).toContain("does_not_claim_all_acceptance_complete");

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-runtime-execution-gap-audit-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.runtime-execution-gap-audit-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_gap_audit: {
            schema: audit.schema,
            status: audit.status,
            verdict: audit.verdict,
            accepted_scenario_count: (audit.accepted_scenarios as unknown[]).length,
            not_accepted_scenario_count: (audit.not_accepted_scenarios as unknown[]).length,
            required_before_goal_complete_count: (audit.required_before_goal_complete as unknown[]).length,
            required_owner_artifact_count: (audit.required_owner_artifacts as unknown[]).length,
            blocker_count: (audit.residual_blockers as unknown[]).length,
            final_acceptance_claimed: negative.final_acceptance_claimed,
            runtime_invocation_attempted: negative.runtime_invocation_attempted,
            owner_repo_write_attempted: negative.owner_repo_write_attempted,
            browser_triggered_broker_order: negative.browser_triggered_broker_order,
            broker_order_created: negative.broker_order_created,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            gap_panel_visible: true,
            verdict_displayed_blocked: true,
            final_acceptance_claimed_displayed_false: true,
            a4_not_accepted_displayed: true,
            approval_obtained_displayed_false: true,
            runtime_invocation_displayed_false: true,
            owner_write_displayed_false: true,
            broker_order_displayed_false: true,
            required_items_displayed: true,
            blocker_items_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          explicit_non_claims: audit.explicit_non_claims,
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-runtime-execution-gap-audit-ui.png"))
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
