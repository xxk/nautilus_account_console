import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const accountId = "acct.ctp.paper.19053";
const evidenceDir = path.resolve("..", "docs", "acceptance", "browser-evidence", "p024-account-console-paper-command-controls");
const evidencePath = path.join(evidenceDir, "runtime-approval-packet-ui.json");

test("P024 Web UI renders owner-runtime execution approval packet without invoking runtime", async ({ page }, testInfo) => {
  const apiResponse = await page.request.get(
    `http://127.0.0.1:8775/api/commands/accounts/${accountId}/runtime-execution-approval-packet`
  );
  expect(apiResponse.ok()).toBe(true);
  const packet = (await apiResponse.json()) as Record<string, unknown>;

  mkdirSync(evidenceDir, { recursive: true });
  const pagePacketPromise = page.waitForResponse((response) =>
    response.url().includes(`/api/commands/accounts/${accountId}/runtime-execution-approval-packet`)
  );
  await page.goto(`/accounts/${accountId}?p024_runtime_approval_packet=1`);
  const pagePacketResponse = await pagePacketPromise;
  expect(pagePacketResponse.status()).toBe(200);

  await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
  await expect(page.getByTestId("account-runtime-approval-packet-panel")).toBeVisible();
  await expect(page.getByTestId("account-runtime-approval-packet-status")).toHaveText(
    "phase4a_owner_runtime_execution_approval_packet_ready"
  );
  await expect(page.getByTestId("account-runtime-approval-packet-verdict")).toHaveText(
    "approval_packet_ready_runtime_not_invoked"
  );
  await expect(page.getByTestId("account-runtime-approval-packet-owner-path")).toHaveText(
    "D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-runtime-approval-packet-required")).toHaveText("true");
  await expect(page.getByTestId("account-runtime-approval-packet-obtained")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-approval-packet-invoked")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-approval-packet-owner-write")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-approval-packet-broker-order")).toHaveText("false");
  await expect(page.getByTestId("account-runtime-approval-packet-exact-text")).toContainText(
    "I approve writes to D:/Nautilus/nautilus_ctp_adapter"
  );
  await expect(page.getByTestId("account-runtime-approval-packet-entrypoint")).toHaveCount(2);
  await expect(page.getByTestId("account-runtime-approval-packet-entrypoint")).toContainText([
    "scripts/ctp_guarded_paper_order_loop.py",
    "scripts/ctp_guarded_paper_cancel_loop.py"
  ]);
  await expect(page.getByTestId("account-runtime-approval-packet-entrypoint")).toContainText([
    "--arm-paper-send",
    "--arm-cancel-send"
  ]);
  await expect(page.getByTestId("account-runtime-approval-packet-blocker")).toHaveCount(2);
  await expect(page.getByTestId("account-runtime-approval-packet-blocker")).toContainText([
    "external_write_approval_required",
    "owner_runtime_artifacts_missing"
  ]);
  await expect(page.getByText(/tcp:\/\//i)).toHaveCount(0);
  await expect(page.getByText(/trading\.openctp/i)).toHaveCount(0);
  await expect(page.getByText(/live ready|browser submitted broker order/i)).toHaveCount(0);

  const approval = packet.required_operator_approval as Record<string, unknown>;
  const planned = packet.planned_execution as Record<string, unknown>;
  const negative = packet.negative_assertions as Record<string, unknown>;
  expect(approval.required).toBe(true);
  expect(approval.obtained).toBe(false);
  expect(approval.approval_path).toBe("D:/Nautilus/nautilus_ctp_adapter");
  expect(String(approval.exact_approval_text)).toContain("I approve writes to D:/Nautilus/nautilus_ctp_adapter");
  expect(planned.runtime_invocation_attempted).toBe(false);
  expect(planned.owner_repo_write_attempted).toBe(false);
  expect(negative.runtime_invocation_attempted).toBe(false);
  expect(negative.owner_repo_write_attempted).toBe(false);
  expect(negative.browser_triggered_broker_order).toBe(false);
  expect(negative.gateway_send_attempted).toBe(false);
  expect(negative.broker_order_created).toBe(false);
  expect(negative.raw_secret_values_recorded).toBe(false);
  expect(negative.raw_broker_endpoint_recorded).toBe(false);
  expect(packet.explicit_non_claims).toContain("does_not_close_real_runtime_execution");

  if (testInfo.project.name === "desktop") {
    await page.screenshot({ fullPage: true, path: path.join(evidenceDir, "p024-runtime-approval-packet-ui.png") });
    writeFileSync(
      evidencePath,
      JSON.stringify(
        {
          schema: "account-console.p024.runtime-approval-packet-ui.v1",
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
            approval_path: approval.approval_path,
            exact_approval_text_present: String(approval.exact_approval_text).includes(
              "I approve writes to D:/Nautilus/nautilus_ctp_adapter"
            ),
            entrypoint_count: (packet.entrypoints as unknown[]).length,
            blocker_count: (packet.blockers as unknown[]).length,
            runtime_invocation_attempted: negative.runtime_invocation_attempted,
            owner_repo_write_attempted: negative.owner_repo_write_attempted,
            browser_triggered_broker_order: negative.browser_triggered_broker_order,
            gateway_send_attempted: negative.gateway_send_attempted,
            broker_order_created: negative.broker_order_created,
            raw_secret_values_recorded: negative.raw_secret_values_recorded,
            raw_broker_endpoint_recorded: negative.raw_broker_endpoint_recorded
          },
          browser_checks: {
            approval_packet_panel_visible: true,
            owner_path_displayed: true,
            exact_approval_text_displayed: true,
            approval_required_displayed_true: true,
            approval_obtained_displayed_false: true,
            runtime_invocation_displayed_false: true,
            owner_write_displayed_false: true,
            broker_order_displayed_false: true,
            entrypoints_displayed: true,
            blockers_displayed: true,
            sensitive_endpoint_wording_absent: true
          },
          explicit_non_claims: packet.explicit_non_claims,
          browser_evidence: [
            {
              screenshot: path
                .relative(path.resolve(".."), path.join(evidenceDir, "p024-runtime-approval-packet-ui.png"))
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
