import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p004-account-workbench-settlement-equity-panel"
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

test.describe("P004 Account Workbench Settlement And Equity Panels", () => {
  test("renders read-only settlement fixtures under Account Workbench", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053/settlement");
    await expect(page.getByTestId("account-settlement-panel")).toBeVisible();
    await expect(page.getByTestId("account-settlement-context-bar")).toContainText("Account Workbench");
    await expect(page.getByTestId("account-settlement-table")).toContainText("Current settlement ref");
    await expect(page.getByTestId("account-settlement-source-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-settlement-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-settlement-current.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("account-settlement-blocker").first()).toBeVisible();
    await expect(page.getByTestId("account-settlement-row")).toContainText("missing");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-settlement-blocked.png`)
    });

    await page.getByLabel("Fixture").selectOption("partial");
    await expect(page.getByTestId("account-settlement-blocker").first()).toBeVisible();
    await expect(page.getByTestId("account-settlement-row")).toContainText("Position carryover ref");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-settlement-partial.png`)
    });

    await page.getByLabel("Fixture").selectOption("stale");
    await expect(page.getByTestId("account-settlement-stale-state")).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
  });

  test("renders read-only equity fixtures under Account Workbench", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053/equity");
    await expect(page.getByTestId("account-equity-panel")).toBeVisible();
    await expect(page.getByTestId("account-equity-context-bar")).toContainText("Account Workbench");
    await expect(page.getByTestId("account-equity-table")).toContainText("Equity Points");
    await expect(page.getByTestId("account-equity-point-row").first()).toContainText("Ledger ref");
    await expect(page.getByTestId("account-equity-source-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-equity-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-equity-current.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("account-equity-blocker").first()).toBeVisible();
    await expect(page.getByTestId("account-equity-point-row").first()).toContainText("missing");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-equity-blocked.png`)
    });

    await page.getByLabel("Fixture").selectOption("partial");
    await expect(page.getByTestId("account-equity-blocker").first()).toBeVisible();
    await expect(page.getByTestId("account-equity-point-row").first()).toContainText("Curve ref");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-equity-partial.png`)
    });

    await page.getByLabel("Fixture").selectOption("stale");
    await expect(page.getByTestId("account-equity-stale-state")).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
  });
});
