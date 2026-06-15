import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p004-account-workbench-orders-panel"
);

const forbiddenVisibleText =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;

test.describe("P004 Account Workbench Orders Panel", () => {
  test("renders read-only orders and order detail fixtures", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053/orders");
    await expect(page.getByTestId("account-orders-panel")).toBeVisible();
    await expect(page.getByTestId("account-orders-context-bar")).toContainText("Account Workbench");
    await expect(page.getByTestId("account-orders-table")).toContainText("p077-e100-rb2610-closeyesterday");
    await expect(page.getByTestId("account-orders-source-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-orders-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-orders-current.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("account-orders-blocker").first()).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-orders-blocked.png`)
    });

    await page.goto("/accounts/acct.demo-19053/orders/p077-e100-rb2610-closeyesterday");
    await expect(page.getByTestId("account-order-detail-panel")).toBeVisible();
    await expect(page.getByTestId("account-order-lifecycle-events")).toContainText("filled_reconciled");
    await expect(page.getByTestId("account-order-report-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-order-detail-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-order-detail-filled.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("account-order-detail-blocked-state")).toBeVisible();
    await expect(page.getByTestId("account-order-detail-blocker").first()).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
  });
});
