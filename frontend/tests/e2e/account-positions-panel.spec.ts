import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p004-account-workbench-positions-panel"
);

const forbiddenVisibleText = new RegExp(
  [
    ["Paper", "ready"].join(" "),
    ["Live", "ready"].join(" "),
    "admit" + "ted",
    ["production", "ready"].join(" "),
    ["capital", "allocated"].join(" "),
    ["can", "trade"].join(" "),
    ["submit", "order"].join(" "),
    ["place", "order"].join(" "),
    ["cancel", "order"].join(" "),
    ["replace", "order"].join(" ")
  ].join("|"),
  "i"
);

test.describe("P004 Account Workbench Positions Panel", () => {
  test("renders read-only position fixtures under Account Workbench", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053/positions");
    await expect(page.getByTestId("account-positions-panel")).toBeVisible();
    await expect(page.getByTestId("account-positions-context-bar")).toContainText("Account Workbench");
    await expect(page.getByTestId("account-positions-table")).toContainText("rb2610");
    await expect(page.getByTestId("account-position-row").first()).toContainText("Carryover ref");
    await expect(page.getByTestId("account-positions-source-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-positions-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-positions-current.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("account-positions-blocker").first()).toBeVisible();
    await expect(page.getByTestId("account-position-row").first()).toContainText("missing");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-positions-blocked.png`)
    });

    await page.getByLabel("Fixture").selectOption("partial");
    await expect(page.getByTestId("account-positions-blocker").first()).toBeVisible();
    await expect(page.getByTestId("account-position-row").first()).toContainText("Settlement ref");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-positions-partial.png`)
    });

    await page.getByLabel("Fixture").selectOption("stale");
    await expect(page.getByTestId("account-positions-stale-state")).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
  });
});
