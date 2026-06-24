export type AccountWorkbenchView =
  | "summary"
  | "order_detail"
  | "orders"
  | "positions"
  | "settlement"
  | "equity"
  | "reconcile"
  | "incidents"
  | "evidence";

export interface AccountWorkbenchRouteState {
  currentPath: string;
  isIntradayMonitorRoute: boolean;
  isAccountWorkbenchRoute: boolean;
  accountWorkbenchView: AccountWorkbenchView | null;
  routeAccountId: string;
  routeOrderId: string;
}

export function classifyAppRoute(currentPath: string): AccountWorkbenchRouteState {
  const isIntradayMonitorRoute = currentPath === "/monitor";
  const pathSegments = currentPath.split("/");
  const routeAccountId = decodeURIComponent(pathSegments[2] ?? "");
  const routeOrderId = decodeURIComponent(pathSegments[4] ?? "");

  if (!currentPath.startsWith("/accounts/")) {
    return {
      currentPath,
      isIntradayMonitorRoute,
      isAccountWorkbenchRoute: false,
      accountWorkbenchView: null,
      routeAccountId,
      routeOrderId
    };
  }

  const accountWorkbenchView = resolveAccountWorkbenchView(currentPath);
  return {
      currentPath,
      isIntradayMonitorRoute,
      isAccountWorkbenchRoute: true,
      accountWorkbenchView,
      routeAccountId,
      routeOrderId
  };
}

export function resolveAccountWorkbenchView(currentPath: string): AccountWorkbenchView {
  if (/^\/accounts\/[^/]+\/orders\/[^/]+/.test(currentPath)) {
    return "order_detail";
  }
  if (/^\/accounts\/[^/]+\/orders\/?$/.test(currentPath)) {
    return "orders";
  }
  if (/^\/accounts\/[^/]+\/positions\/?$/.test(currentPath)) {
    return "positions";
  }
  if (/^\/accounts\/[^/]+\/settlement\/?$/.test(currentPath)) {
    return "settlement";
  }
  if (/^\/accounts\/[^/]+\/equity\/?$/.test(currentPath)) {
    return "equity";
  }
  if (/^\/accounts\/[^/]+\/reconcile\/?$/.test(currentPath)) {
    return "reconcile";
  }
  if (/^\/accounts\/[^/]+\/incidents\/?$/.test(currentPath)) {
    return "incidents";
  }
  if (/^\/accounts\/[^/]+\/evidence\/?$/.test(currentPath)) {
    return "evidence";
  }
  return "summary";
}

export function isMirrorWorkbenchEligibleRoute(route: AccountWorkbenchRouteState): boolean {
  return (
    route.isAccountWorkbenchRoute &&
    (route.routeAccountId.startsWith("acct.") || route.routeAccountId === "simulated-001")
  );
}
