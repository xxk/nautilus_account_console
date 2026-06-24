import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-owner-repair-approval-packet-ui.json");

test("P024 Web UI renders owner repair approval packet", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-owner-repair-approval-packet`
  );
  expect(apiResponse.ok()).toBe(true);
  const packet = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pagePacketPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-owner-repair-approval-packet`)
  );
  await page.goto(`/accounts/${accountId}?p024_owner_repair_approval_packet=1`);
  const pagePacketResponse = await pagePacketPromise;
  expect(pagePacketResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-status")).toHaveText(
    "phase4p_owner_close_offset_repair_approval_packet_ready"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-verdict")).toHaveText(
    "owner_repair_approval_required_before_retry"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-current-matches")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-runtime-retry")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-exact-text")).toContainText(
    "repair owner close-offset semantics for P024"
  );
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-change")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-validator")).toHaveCount(2);
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-blocker")).toHaveCount(3);
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-additional-order")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-partial-claimed")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-owner-repair-approval-packet-full-claimed")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const assessment = packet.current_thread_approval_assessment as Record<string, unknown>;
  const approval = packet.required_owner_repair_approval as Record<string, unknown>;
  const retryGate = packet.retry_gate as Record<string, unknown>;
  const negative = packet.negative_assertions as Record<string, unknown>;
  expect(assessment.matches_current_next_action).toBe(false);
  expect(approval.obtained).toBe(false);
  expect(String(approval.exact_approval_text_required)).toContain("repair owner close-offset semantics for P024");
  expect(retryGate.runtime_invocation_allowed).toBe(false);
  expect(retryGate.additional_partial_fill_order_authorized).toBe(false);
  expect(negative.owner_repo_write_attempted_by_this_packet).toBe(false);
  expect(negative.additional_order_authorized).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-owner-repair-approval-packet-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-owner-repair-approval-packet-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_owner_repair_approval_packet: {
            schema: packet.schema,
            status: packet.status,
            verdict: packet.verdict,
            approval_obtained: approval.obtained,
            current_approval_matches_next_action: assessment.matches_current_next_action,
            exact_approval_text_present: String(approval.exact_approval_text_required).includes(
              "repair owner close-offset semantics for P024"
            ),
            owner_change_count: packet.required_owner_repair_scope.expected_owner_changes.length,
            owner_validator_count: packet.required_owner_repair_scope.required_owner_validators_before_retry.length,
            blocker_count: packet.residual_blockers.length,
            runtime_retry_allowed: retryGate.runtime_invocation_allowed,
            additional_order_authorized: retryGate.additional_partial_fill_order_authorized,
            owner_repo_write_attempted: negative.owner_repo_write_attempted_by_this_packet,
            partial_fill_claimed: negative.partial_fill_claimed,
            full_acceptance_claimed: negative.full_acceptance_claimed
          },
          browser_checks: {
            approval_packet_panel_visible: true,
            exact_approval_text_displayed: true,
            owner_changes_displayed: true,
            validators_displayed: true,
            blockers_displayed: true,
            approval_obtained_displayed_false: true,
            current_approval_matches_displayed_false: true,
            runtime_retry_displayed_false: true,
            owner_write_displayed_false: true,
            additional_order_displayed_false: true,
            partial_fill_claimed_displayed_false: true,
            full_acceptance_claimed_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-owner-repair-approval-packet-ui.png"))
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
