import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p009-p077-paper-slice-evidence-panel"
);

const forbiddenVisibleText =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;

test.describe("P009 P077 evidence package projection", () => {
  test("renders the E100/E102 read-only evidence package under Account Evidence", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053/evidence");
    await expect(page.getByTestId("account-evidence-panel")).toBeVisible();
    await expect(page.getByTestId("account-evidence-context-bar")).toContainText(
      "Account Workbench / 19053 / Evidence"
    );
    await expect(page.getByTestId("account-evidence-table")).toContainText(
      "evidence.p077.close-yesterday.e100-e102"
    );
    await expect(page.getByTestId("account-evidence-table")).toContainText("nautilus_ctp_adapter");
    await expect(page.getByTestId("account-evidence-table")).toContainText("p077_paper_slice_panel.v1");
    await expect(page.getByTestId("account-evidence-boundary-list")).toContainText(
      "Read-only projection"
    );
    await expect(page.getByTestId("account-evidence-source-ref").first()).toContainText(
      "p077 owner slice projection"
    );
    await expect(page.getByTestId("account-evidence-rejection-rule").last()).toContainText(
      "Reject P077 evidence package display"
    );
    await expect(page.getByRole("link", { name: /Account Workbench/ })).toHaveAttribute(
      "aria-current",
      "page"
    );
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);

    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-p077-e90.png`)
    });
  });
});
