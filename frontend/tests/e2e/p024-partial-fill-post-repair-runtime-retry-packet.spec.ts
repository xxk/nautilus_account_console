import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-post-repair-runtime-retry-packet-ui.json");

test("P024 Web UI renders post-repair runtime retry approval packet", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-post-repair-runtime-retry-approval-packet`
  );
  expect(apiResponse.ok()).toBe(true);
  const packet = (await apiResponse.json()) as Record<string, any>;

  mkdirSync(evidenceDir, { recursive: true });
  const pagePacketPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-post-repair-runtime-retry-approval-packet`)
  );
  await page.goto(`/accounts/${accountId}?p024_post_repair_retry_packet=1`);
  const pagePacketResponse = await pagePacketPromise;
  expect(pagePacketResponse.status()).toBe(200);

  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-status")).toHaveText(
    "phase4ze_post_repair_runtime_retry_approval_packet_ready"
  );
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-verdict")).toHaveText(
    "one_guarded_post_repair_paper_attempt_authorized"
  );
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-authorized")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-max-attempts")).toHaveText("1");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-exposure-reduction")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-required")).toHaveCount(7);
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-post-repair-runtime-retry-packet-real-partial")).toHaveText("false");
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);

  const guard = packet.runtime_retry_guard as Record<string, unknown>;
  const negative = packet.negative_assertions_before_runtime as Record<string, unknown>;
  expect(guard.runtime_retry_authorized_by_packet).toBe(true);
  expect(guard.maximum_attempts).toBe(1);
  expect(guard.exposure_reduction_only).toBe(true);
  expect(negative.owner_runtime_invocation_attempted_by_packet).toBe(false);
  expect(negative.real_partial_fill_claimed).toBe(false);
  expect(negative.full_acceptance_claimed).toBe(false);

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-partial-fill-post-repair-runtime-retry-packet-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-post-repair-runtime-retry-packet-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_post_repair_runtime_retry_packet: {
            schema: packet.schema,
            status: packet.status,
            verdict: packet.verdict,
            runtime_retry_authorized_by_packet: guard.runtime_retry_authorized_by_packet,
            maximum_attempts: guard.maximum_attempts,
            exposure_reduction_only: guard.exposure_reduction_only,
            required_runtime_evidence_count: packet.required_runtime_evidence.length,
            owner_runtime_invocation_attempted_by_packet: negative.owner_runtime_invocation_attempted_by_packet,
            real_partial_fill_claimed: negative.real_partial_fill_claimed
          },
          browser_checks: {
            retry_packet_panel_visible: true,
            authorized_displayed_true: true,
            max_attempts_displayed_one: true,
            exposure_reduction_displayed_true: true,
            runtime_requirements_displayed: true,
            runtime_invoked_displayed_false: true,
            real_partial_fill_displayed_false: true,
            sensitive_endpoint_wording_absent: true
          },
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-post-repair-runtime-retry-packet-ui.png"))
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
