import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "partial-fill-runtime-approval-packet-ui.json");

test("P024 Web UI renders partial-fill runtime approval packet without invoking runtime", async ({
  page
}, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8875/api/commands/accounts/${accountId}/partial-fill-runtime-execution-approval-packet`
  );
  expect(apiResponse.ok()).toBe(true);
  const packet = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  const pagePacketPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/partial-fill-runtime-execution-approval-packet`)
  );
  await page.goto(`/accounts/${accountId}?p024_partial_fill_runtime_approval_packet=1`);
  const pagePacketResponse = await pagePacketPromise;
  expect(pagePacketResponse.status()).toBe(200);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-panel")).toBeVisible();
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-status")).toHaveText(
    "phase4j_partial_fill_runtime_execution_approval_packet_ready"
  );
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-verdict")).toHaveText(
    "approval_packet_ready_runtime_not_invoked"
  );
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-owner-path")).toHaveText(
    "D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-required")).toHaveText("true");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-new-order")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-cancel-sent")).toHaveText("false");
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-exact-text")).toContainText(
    "P024 partial-fill acceptance"
  );
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-formula")).toContainText([
    "0 < filled_quantity < submitted_quantity",
    "filled_quantity + cancelled_quantity == submitted_quantity",
    "remaining_quantity == 0"
  ]);
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-entrypoint")).toHaveCount(2);
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-blocker")).toHaveCount(2);
  await expect(page.getByTestId("account-partial-fill-runtime-approval-packet-blocker")).toContainText([
    "external_write_approval_required",
    "owner_runtime_partial_fill_state_missing"
  ]);
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);
  await expect(page.getByText(/live ready|browser submitted broker order/i)).toHaveCount(0);

  const approval = packet.required_operator_approval as Record<string, unknown>;
  const planned = packet.planned_execution as Record<string, unknown>;
  const negative = packet.negative_assertions as Record<string, unknown>;
  expect(approval.required).toBe(true);
  expect(approval.obtained).toBe(false);
  expect(String(approval.exact_approval_text)).toContain("P024 partial-fill acceptance");
  expect(planned.runtime_invocation_attempted).toBe(false);
  expect(planned.owner_repo_write_attempted).toBe(false);
  expect(planned.new_order_submitted).toBe(false);
  expect(planned.cancel_sent).toBe(false);
  expect(negative.runtime_invocation_attempted).toBe(false);
  expect(negative.owner_repo_write_attempted).toBe(false);
  expect(negative.new_order_submitted).toBe(false);
  expect(negative.cancel_sent).toBe(false);
  expect(negative.browser_triggered_broker_order).toBe(false);
  expect(negative.gateway_send_attempted).toBe(false);
  expect(negative.broker_order_created).toBe(false);
  expect(negative.raw_secret_values_recorded).toBe(false);
  expect(negative.raw_broker_endpoint_recorded).toBe(false);
  expect(packet.explicit_non_claims).toContain("does_not_claim_real_partial_fill_runtime");

  if (testInfo.project.name === "desktop") {
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, "p024-partial-fill-runtime-approval-packet-ui.png")
    });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.partial-fill-runtime-approval-packet-ui.v1",
          proposal_id: "p024-account-console-paper-command-controls",
          account_id: accountId,
          route: `/accounts/${accountId}`,
          verdict: "pass",
          api_approval_packet: {
            schema: packet.schema,
            status: packet.status,
            verdict: packet.verdict,
            approval_required: approval.required,
            approval_obtained: approval.obtained,
            exact_approval_text_present: String(approval.exact_approval_text).includes(
              "P024 partial-fill acceptance"
            ),
            entrypoint_count: (packet.entrypoints as unknown[]).length,
            blocker_count: (packet.blockers as unknown[]).length,
            runtime_invocation_attempted: negative.runtime_invocation_attempted,
            owner_repo_write_attempted: negative.owner_repo_write_attempted,
            new_order_submitted: negative.new_order_submitted,
            cancel_sent: negative.cancel_sent,
            browser_triggered_broker_order: negative.browser_triggered_broker_order,
            gateway_send_attempted: negative.gateway_send_attempted,
            broker_order_created: negative.broker_order_created,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            approval_packet_panel_visible: true,
            exact_approval_text_displayed: true,
            approval_obtained_displayed_false: true,
            runtime_invocation_displayed_false: true,
            owner_write_displayed_false: true,
            new_order_displayed_false: true,
            cancel_sent_displayed_false: true,
            formulas_displayed: true,
            entrypoints_displayed: true,
            blockers_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          explicit_non_claims: packet.explicit_non_claims,
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-partial-fill-runtime-approval-packet-ui.png"))
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
