import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-plan-ui.json");

test("P024 Web UI renders owner repair plan without allowing retry", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-owner-repair-implementation-plan`
  );
  expect(apiResponse.ok()).toBe(true);
  const plan = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pagePlanPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-implementation-plan`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_plan=1`);
  const pagePlanResponse = await pagePlanPromise;
  expect(pagePlanResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-status")).toHaveText(
    "phase4r_owner_close_offset_repair_implementation_plan_ready"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-verdict")).toHaveText(
    "owner_repair_plan_ready_no_owner_write_attempted"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-owner-path")).toHaveText(
    "D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-fresh-approval")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-success-formula")).toHaveText(
    "0 < filled_quantity < submitted_quantity"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-source")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-source")).toContainText([
    "CLOSEYESTERDAY -> 4"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-change")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-change")).toContainText([
    "CLOSEYESTERDAY expected/submit offset 4"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-validator")).toHaveCount(4);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-validator")).toContainText([
    "python -m pytest tests/test_guarded_paper_order_loop.py -q",
    "python -m pytest tests/test_nautilus_integration.py -q"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-forbidden")).toHaveCount(5);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-forbidden")).toContainText([
    "do not treat rejected OnRspOrderInsert offset 1 as submit truth",
    "do not run another paper order before owner repair approval"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-partial-claimed")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-plan-full-claimed")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);
  await expect(page.getByText(/full acceptance complete|runtime retry authorized/i)).toHaveCount(0);

  const negative = plan.negative_assertions as Record<string, unknown>;
  expect(negative.owner_repo_write_attempted_by_this_plan).toBe(false);
  expect(negative.owner_runtime_invocation_attempted).toBe(false);
  expect(negative.runtime_retry_authorized).toBe(false);
  expect(negative.partial_fill_claimed).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-plan-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-plan-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_plan: {
            schema: plan.schema,
            status: plan.status,
            verdict: plan.verdict,
            source_ref_count: plan.owner_read_context.source_refs.length,
            planned_change_count: plan.planned_owner_changes_after_exact_approval.length,
            validator_count: plan.post_repair_validator_sequence.length,
            forbidden_shape_count: plan.forbidden_repair_shapes.length,
            owner_repo_write_attempted: plan.owner_read_context.owner_repo_write_attempted,
            runtime_attempt_allowed: plan.post_repair_runtime_attempt_gate.runtime_attempt_allowed_by_this_plan,
            fresh_approval_required: plan.post_repair_runtime_attempt_gate.fresh_approval_required,
            partial_fill_claimed: negative.partial_fill_claimed,
            full_acceptance_claimed: negative.full_acceptance_claimed,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            repair_plan_panel_visible: true,
            status_displayed: true,
            owner_path_displayed: true,
            owner_write_displayed_false: true,
            runtime_retry_displayed_false: true,
            fresh_approval_displayed_true: true,
            close_yesterday_source_displayed: true,
            planned_changes_displayed: true,
            validators_displayed: true,
            forbidden_shapes_displayed: true,
            partial_fill_claimed_displayed_false: true,
            full_acceptance_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-plan-ui.png"))
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
