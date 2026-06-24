import { useMemo, useState } from "react";

import {
  accountEvidenceFixtureMap,
  accountEquityFixtureMap,
  accountIncidentsFixtureMap,
  accountOrderDetailFixtureMap,
  accountOrdersFixtureMap,
  accountPositionsFixtureMap,
  accountReconcileFixtureMap,
  accountSettlementFixtureMap,
  accountSummaryFixtureMap,
  healthFixtureMap,
  intradayMonitorFixtureMap,
  type AccountHealthFixtureId
} from "./fixture-registry";
import type {
  AccountEquityFixtureState,
  AccountEvidenceFixtureState,
  AccountIncidentsFixtureState,
  AccountOrderDetailFixtureState,
  AccountOrdersFixtureState,
  AccountPositionsFixtureState,
  AccountReconcileFixtureState,
  AccountSettlementFixtureState,
  AccountSummaryFixtureState,
  IntradayMonitorFixtureState
} from "./types";

export interface FixtureSelectionState {
  health: {
    fixtureState: AccountHealthFixtureId;
    setFixtureState: (value: AccountHealthFixtureId) => void;
    fixture: (typeof healthFixtureMap)[AccountHealthFixtureId];
  };
  accountWorkbench: {
    summary: {
      fixtureState: AccountSummaryFixtureState;
      setFixtureState: (value: AccountSummaryFixtureState) => void;
      fixture: (typeof accountSummaryFixtureMap)[AccountSummaryFixtureState];
    };
    orders: {
      fixtureState: AccountOrdersFixtureState;
      setFixtureState: (value: AccountOrdersFixtureState) => void;
      fixture: (typeof accountOrdersFixtureMap)[AccountOrdersFixtureState];
    };
    orderDetail: {
      fixtureState: AccountOrderDetailFixtureState;
      setFixtureState: (value: AccountOrderDetailFixtureState) => void;
      fixture: (typeof accountOrderDetailFixtureMap)[AccountOrderDetailFixtureState];
    };
    positions: {
      fixtureState: AccountPositionsFixtureState;
      setFixtureState: (value: AccountPositionsFixtureState) => void;
      fixture: (typeof accountPositionsFixtureMap)[AccountPositionsFixtureState];
    };
    settlement: {
      fixtureState: AccountSettlementFixtureState;
      setFixtureState: (value: AccountSettlementFixtureState) => void;
      fixture: (typeof accountSettlementFixtureMap)[AccountSettlementFixtureState];
    };
    equity: {
      fixtureState: AccountEquityFixtureState;
      setFixtureState: (value: AccountEquityFixtureState) => void;
      fixture: (typeof accountEquityFixtureMap)[AccountEquityFixtureState];
    };
    reconcile: {
      fixtureState: AccountReconcileFixtureState;
      setFixtureState: (value: AccountReconcileFixtureState) => void;
      fixture: (typeof accountReconcileFixtureMap)[AccountReconcileFixtureState];
    };
    incidents: {
      fixtureState: AccountIncidentsFixtureState;
      setFixtureState: (value: AccountIncidentsFixtureState) => void;
      fixture: (typeof accountIncidentsFixtureMap)[AccountIncidentsFixtureState];
    };
    evidence: {
      fixtureState: AccountEvidenceFixtureState;
      setFixtureState: (value: AccountEvidenceFixtureState) => void;
      fixture: (typeof accountEvidenceFixtureMap)[AccountEvidenceFixtureState];
    };
  };
  intradayMonitor: {
    fixtureState: IntradayMonitorFixtureState;
    setFixtureState: (value: IntradayMonitorFixtureState) => void;
    fixture: (typeof intradayMonitorFixtureMap)[IntradayMonitorFixtureState];
  };
}

export function useFixtureSelection(): FixtureSelectionState {
  const [healthFixtureState, setHealthFixtureState] = useState<AccountHealthFixtureId>("happy_path");
  const [accountWorkbenchFallback, setAccountWorkbenchFallback] = useState({
    summary: "happy_path" as AccountSummaryFixtureState,
    orders: "current_orders" as AccountOrdersFixtureState,
    orderDetail: "filled_lifecycle" as AccountOrderDetailFixtureState,
    positions: "current_positions" as AccountPositionsFixtureState,
    settlement: "current_settlement" as AccountSettlementFixtureState,
    equity: "current_equity" as AccountEquityFixtureState,
    reconcile: "mismatch" as AccountReconcileFixtureState,
    incidents: "active_incidents" as AccountIncidentsFixtureState,
    evidence: "current_evidence" as AccountEvidenceFixtureState
  });
  const [intradayMonitorFixtureState, setIntradayMonitorFixtureState] =
    useState<IntradayMonitorFixtureState>("current");

  const accountWorkbench = useMemo(
    () => ({
      summary: {
        fixtureState: accountWorkbenchFallback.summary,
        setFixtureState: (value: AccountSummaryFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, summary: value })),
        fixture: accountSummaryFixtureMap[accountWorkbenchFallback.summary]
      },
      orders: {
        fixtureState: accountWorkbenchFallback.orders,
        setFixtureState: (value: AccountOrdersFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, orders: value })),
        fixture: accountOrdersFixtureMap[accountWorkbenchFallback.orders]
      },
      orderDetail: {
        fixtureState: accountWorkbenchFallback.orderDetail,
        setFixtureState: (value: AccountOrderDetailFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, orderDetail: value })),
        fixture: accountOrderDetailFixtureMap[accountWorkbenchFallback.orderDetail]
      },
      positions: {
        fixtureState: accountWorkbenchFallback.positions,
        setFixtureState: (value: AccountPositionsFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, positions: value })),
        fixture: accountPositionsFixtureMap[accountWorkbenchFallback.positions]
      },
      settlement: {
        fixtureState: accountWorkbenchFallback.settlement,
        setFixtureState: (value: AccountSettlementFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, settlement: value })),
        fixture: accountSettlementFixtureMap[accountWorkbenchFallback.settlement]
      },
      equity: {
        fixtureState: accountWorkbenchFallback.equity,
        setFixtureState: (value: AccountEquityFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, equity: value })),
        fixture: accountEquityFixtureMap[accountWorkbenchFallback.equity]
      },
      reconcile: {
        fixtureState: accountWorkbenchFallback.reconcile,
        setFixtureState: (value: AccountReconcileFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, reconcile: value })),
        fixture: accountReconcileFixtureMap[accountWorkbenchFallback.reconcile]
      },
      incidents: {
        fixtureState: accountWorkbenchFallback.incidents,
        setFixtureState: (value: AccountIncidentsFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, incidents: value })),
        fixture: accountIncidentsFixtureMap[accountWorkbenchFallback.incidents]
      },
      evidence: {
        fixtureState: accountWorkbenchFallback.evidence,
        setFixtureState: (value: AccountEvidenceFixtureState) =>
          setAccountWorkbenchFallback((current) => ({ ...current, evidence: value })),
        fixture: accountEvidenceFixtureMap[accountWorkbenchFallback.evidence]
      }
    }),
    [accountWorkbenchFallback]
  );

  return {
    health: {
      fixtureState: healthFixtureState,
      setFixtureState: setHealthFixtureState,
      fixture: healthFixtureMap[healthFixtureState]
    },
    accountWorkbench,
    intradayMonitor: {
      fixtureState: intradayMonitorFixtureState,
      setFixtureState: setIntradayMonitorFixtureState,
      fixture: intradayMonitorFixtureMap[intradayMonitorFixtureState]
    }
  };
}
