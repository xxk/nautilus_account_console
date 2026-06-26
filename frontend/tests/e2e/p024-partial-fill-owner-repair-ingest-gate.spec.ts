import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-ingest-gate-ui.json");

test("P024 Web UI renders owner repair evidence ingest gate", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-owner-repair-evidence-ingest-gate`
  );
  expect(apiResponse.ok()).toBe(true);
  const gate = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageGatePromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-evidence-ingest-gate`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_ingest_gate=1`);
  const pageGateResponse = await pageGatePromise;
  expect(pageGateResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-status")).toHaveText(
    "phase4t_owner_repair_evidence_ingest_gate_ready"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-verdict")).toHaveText(
    "ingest_gate_ready_owner_repair_evidence_missing"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-runtime-evidence")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-required")).toHaveCount(6);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-required")).toContainText([
    "owner_repair_commit",
    "focused_owner_tests_checksum",
    "owner_focus_validator_result"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-update")).toHaveCount(5);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-reject")).toHaveCount(6);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-evidence-recorded")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-gate-full-claimed")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const negative = gate.negative_assertions as Record<string, unknown>;
  expect(negative.owner_repair_evidence_recorded).toBe(false);
  expect(negative.runtime_retry_authorized).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-ingest-gate-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-ingest-gate-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_ingest_gate: {
            schema: gate.schema,
            status: gate.status,
            verdict: gate.verdict,
            required_evidence_count: gate.required_owner_repair_evidence.length,
            update_count: gate.post_ingest_required_account_console_updates.length,
            reject_rule_count: gate.reject_evidence_if.length,
            runtime_retry_allowed: gate.ingest_scope.runtime_retry_allowed_by_ingest_gate,
            runtime_evidence_allowed: gate.ingest_scope.accepts_owner_runtime_partial_fill_evidence,
            owner_repair_evidence_recorded: negative.owner_repair_evidence_recorded,
            full_acceptance_claimed: negative.full_acceptance_claimed
          },
          browser_checks: {
            ingest_gate_panel_visible: true,
            runtime_retry_displayed_false: true,
            runtime_evidence_displayed_false: true,
            required_evidence_displayed: true,
            update_items_displayed: true,
            reject_rules_displayed: true,
            owner_repair_evidence_recorded_displayed_false: true,
            full_acceptance_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-ingest-gate-ui.png"))
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
