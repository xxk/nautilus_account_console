import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-remaining-acceptance-state-ui.json");

test("P024 Web UI renders remaining acceptance state", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/partial-fill-remaining-acceptance-current-state`
  );
  expect(apiResponse.ok()).toBe(true);
  const state = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageStatePromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-remaining-acceptance-current-state`)
  );
  await page.goto(`/accounts/${accountId}?p024_remaining_acceptance=1`);
  const pageStateResponse = await pageStatePromise;
  expect(pageStateResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-status")).toHaveText(
    "phase4q_remaining_acceptance_current_state_audited"
  );
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-verdict")).toHaveText(
    "not_fully_accepted_pending_owner_repair_and_real_partial_fill"
  );
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-full-claimed")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-owner-repair-allowed")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-requirement")).toHaveCount(5);
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-evidence-group")).toHaveCount(4);
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-real-partial-claimed")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-remaining-acceptance-web-ui-claimed")).toHaveText("false");
  await expect(page.getByText(/R5_web_ui_real_partial_fill_projection/i)).toBeVisible();
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const requirements = state.remaining_acceptance_requirements as Array<Record<string, unknown>>;
  const negative = state.negative_assertions as Record<string, unknown>;
  const next = state.next_authorized_action as Record<string, unknown>;
  expect(requirements).toHaveLength(5);
  expect(requirements.map((item) => item.requirement_id).sort()).toEqual([
    "R1_owner_repair_approval",
    "R2_owner_close_offset_repair",
    "R3_owner_validators",
    "R4_post_repair_partial_fill_runtime",
    "R5_web_ui_real_partial_fill_projection"
  ]);
  for (const requirement of requirements) {
    expect(requirement.current_status).toBe("missing");
  }
  expect(next.owner_code_repair_allowed).toBe(false);
  expect(next.owner_runtime_retry_allowed).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);
  expect(negative.real_partial_fill_claimed).toBe(false);
  expect(negative.web_ui_real_partial_fill_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-remaining-acceptance-state-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-remaining-acceptance-state-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_remaining_acceptance_state: {
            schema: state.schema,
            status: state.status,
            verdict: state.verdict,
            requirement_count: requirements.length,
            missing_requirement_ids: requirements.map((item) => item.requirement_id),
            accepted_evidence_group_count: state.accepted_evidence_groups.length,
            owner_code_repair_allowed: next.owner_code_repair_allowed,
            owner_runtime_retry_allowed: next.owner_runtime_retry_allowed,
            full_acceptance_claimed: negative.full_acceptance_claimed,
            real_partial_fill_claimed: negative.real_partial_fill_claimed,
            web_ui_real_partial_fill_claimed: negative.web_ui_real_partial_fill_claimed
          },
          browser_checks: {
            remaining_panel_visible: true,
            r1_to_r5_displayed: true,
            all_requirements_displayed_missing: true,
            evidence_groups_displayed: true,
            owner_repair_allowed_displayed_false: true,
            runtime_retry_displayed_false: true,
            full_acceptance_displayed_false: true,
            real_partial_fill_claimed_displayed_false: true,
            web_ui_real_partial_fill_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-remaining-acceptance-state-ui.png"))
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
