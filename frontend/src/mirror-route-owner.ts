import type { MirrorAccountSummary } from "./types";

export const mirrorRouteAliases: Record<string, string> = {
  "acct.demo-19053": "simulated-001",
};

export function resolveMirrorRouteAccountId(routeAccountId: string, accounts: MirrorAccountSummary[]) {
  const canonicalRouteAccountId = mirrorRouteAliases[routeAccountId] ?? routeAccountId;
  if (accounts.some((account) => account.account_id === canonicalRouteAccountId)) {
    return canonicalRouteAccountId;
  }
  return accounts[0]?.account_id;
}
