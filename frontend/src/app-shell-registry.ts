export const portfolioOwnerConsoleUrl =
  "http://127.0.0.1:4185/console/portfolios/CTA-CORE-001?view=portfolio-owner&origin=account-console&portfolio_uid=CTA-CORE-001";

export const workbenches = [
  { label: "Daily Closeout", path: "/closeout", icon: "Gauge" },
  { label: "Intraday Monitor", path: "/monitor", icon: "Radio" },
  { label: "Account Workbench", path: "/accounts/acct.demo-19053", icon: "Database" },
  { label: "Allocation Admin", path: "/management/accounts", icon: "Layers" },
  { label: "Risk And Reconcile", path: "/risk-reconcile", icon: "ShieldAlert" },
  { label: "Evidence Explorer", path: "/evidence", icon: "FileSearch" },
  { label: "Stream Ops", path: "/ops/stream", icon: "Waypoints" },
] as const;
