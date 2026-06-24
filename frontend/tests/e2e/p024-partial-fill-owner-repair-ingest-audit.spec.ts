import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-ingest-audit-ui.json");

test("P024 Web UI renders owner repair evidence ingest audit", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-owner-repair-evidence-ingest-audit`
  );
  expect(apiResponse.ok()).toBe(true);
  const audit = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pageAuditPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-evidence-ingest-audit`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_ingest_audit=1`);
  const pageAuditResponse = await pageAuditPromise;
  expect(pageAuditResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-status")).toHaveText(
    "phase4zd_owner_repair_evidence_ingested"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-verdict")).toHaveText(
    "owner_repair_evidence_recorded_runtime_retry_packet_required"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-commit")).toContainText("01db0f8");
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-checksum")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-validator")).toHaveCount(2);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-validator")).toContainText([
    "57 passed",
    "88 passed"
  ]);
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-evidence-recorded")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-ingest-audit-real-partial")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const decision = audit.ingest_decision as Record<string, unknown>;
  const negative = audit.negative_assertions as Record<string, unknown>;
  expect(decision.owner_repair_evidence_recorded).toBe(true);
  expect(decision.owner_validators_passed).toBe(true);
  expect(decision.runtime_retry_authorized).toBe(false);
  expect(negative.real_partial_fill_claimed).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-ingest-audit-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-ingest-audit-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_ingest_audit: {
            schema: audit.schema,
            status: audit.status,
            verdict: audit.verdict,
            owner_repair_commit_ref: audit.owner_repair_evidence.owner_repair_commit_ref,
            source_checksum_count: audit.post_repair_source_checksums.length,
            validator_count: audit.owner_validator_refs.length,
            owner_repair_evidence_recorded: decision.owner_repair_evidence_recorded,
            runtime_retry_authorized: decision.runtime_retry_authorized,
            real_partial_fill_claimed: negative.real_partial_fill_claimed
          },
          browser_checks: {
            ingest_audit_panel_visible: true,
            commit_ref_displayed: true,
            checksums_displayed: true,
            validators_displayed: true,
            owner_repair_evidence_recorded_displayed_true: true,
            runtime_retry_displayed_false: true,
            real_partial_fill_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-ingest-audit-ui.png"))
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
