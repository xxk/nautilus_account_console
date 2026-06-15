import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p004-account-workbench-summary-panel"
);

const forbiddenVisibleText =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;

test.describe("P004 Account Workbench Summary Panel", () => {
  test("renders Account Summary fixtures under Account Workbench", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053");
    await expect(page.getByTestId("account-workbench-summary-panel")).toBeVisible();
    await expect(page.getByTestId("account-workbench-context-bar")).toContainText("Account Workbench");
    await expect(page.getByTestId("account-summary-metric-strip")).toContainText("Cash");
    await expect(page.getByTestId("account-summary-source-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-summary-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByRole("link", { name: /Account Workbench/ })).toHaveAttribute(
      "aria-current",
      "page"
    );
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);

    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-summary-happy.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("account-summary-blocker").first()).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-summary-blocked.png`)
    });

    await page.getByLabel("Fixture").selectOption("stale");
    await expect(page.getByTestId("account-summary-stale-state")).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-summary-stale.png`)
    });

    await page.getByLabel("Fixture").selectOption("empty");
    await expect(page.getByTestId("account-summary-empty-state")).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
  });
});
