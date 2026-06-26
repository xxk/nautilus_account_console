import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-post-repair-runtime-attempt-ui.json");

test("P024 Web UI renders post-repair runtime attempt audit", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/partial-fill-post-repair-runtime-attempt-audit`
  );
  expect(apiResponse.ok()).toBe(true);
  const audit = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageAuditPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-post-repair-runtime-attempt-audit`)
  );
  await page.goto(`/accounts/${accountId}?p024_post_repair_runtime_attempt=1`);
  const pageAuditResponse = await pageAuditPromise;
  expect(pageAuditResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-status")).toHaveText(
    "phase4zf_post_repair_runtime_attempt_full_fill_blocker_recorded"
  );
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-verdict")).toHaveText(
    "real_paper_order_filled_not_partial_fill_no_cancel_remainder"
  );
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-order")).toContainText(
    "p024-post-repair-20260621T2355-rb2610"
  );
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-filled")).toHaveText("1");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-remaining")).toHaveText("0");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-partial")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-position-delta")).toHaveText("-1");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-attempt-artifact")).toHaveCount(3);
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const observation = audit.runtime_observation as Record<string, unknown>;
  const decision = audit.acceptance_decision as Record<string, unknown>;
  const negative = audit.negative_assertions as Record<string, unknown>;
  expect(observation.filled_quantity).toBe(1);
  expect(observation.remaining_quantity).toBe(0);
  expect(observation.partial_fill_formula_satisfied).toBe(false);
  expect(decision.real_paper_order_created).toBe(true);
  expect(decision.partial_fill_then_cancel_acceptance_satisfied).toBe(false);
  expect(negative.additional_runtime_retry_authorized).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-post-repair-runtime-attempt-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-post-repair-runtime-attempt-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_post_repair_runtime_attempt: {
            schema: audit.schema,
            status: audit.status,
            verdict: audit.verdict,
            filled_quantity: observation.filled_quantity,
            remaining_quantity: observation.remaining_quantity,
            partial_fill_formula_satisfied: observation.partial_fill_formula_satisfied,
            real_paper_order_created: decision.real_paper_order_created,
            partial_fill_then_cancel_acceptance_satisfied: decision.partial_fill_then_cancel_acceptance_satisfied,
            additional_runtime_retry_authorized: negative.additional_runtime_retry_authorized
          },
          browser_checks: {
            attempt_panel_visible: true,
            full_fill_displayed: true,
            partial_fill_displayed_false: true,
            retry_displayed_false: true,
            position_delta_displayed: true,
            artifacts_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-post-repair-runtime-attempt-ui.png"))
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
