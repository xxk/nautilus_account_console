import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p001-daily-closeout-account-health-panel"
);

test.describe("P001 Daily Closeout Account Health Panel", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/closeout");
    await expect(page.getByTestId("daily-closeout-account-health-panel")).toBeVisible();
  });

  test("renders fixture-backed account health states", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await expect(page.getByTestId("daily-closeout-metric-strip")).toContainText("Total accounts");
    await expect(page.getByTestId("daily-closeout-account-health-row").first()).toBeVisible();
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-happy.png`)
    });

    await page.getByLabel("Fixture").selectOption("adr0044_foundation");
    await expect(
      page.getByTestId("daily-closeout-account-health-row").filter({ hasText: "paper-account-alpha" })
    ).toBeVisible();
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-adr0044-source-backed.png`)
    });

    await page.getByLabel("Fixture").selectOption("blocked");
    await expect(page.getByTestId("daily-closeout-blocker").first()).toBeVisible();
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-blocked.png`)
    });

    await page.getByLabel("Fixture").selectOption("stale");
    await expect(page.getByTestId("daily-closeout-stale-state")).toBeVisible();
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-stale.png`)
    });

    await page.getByLabel("Fixture").selectOption("empty");
    await expect(page.getByTestId("daily-closeout-empty-state").first()).toBeVisible();
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-empty.png`)
    });

    await page.getByLabel("Fixture").selectOption("partial");
    await expect(page.getByText("partial").first()).toBeVisible();
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-partial.png`)
    });
  });
});
