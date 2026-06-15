import { readFileSync, readdirSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..", "..");
const panelContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_health_panel.contract.json"
);
const p077PanelContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "p077_paper_slice_panel.contract.json"
);
const accountSummaryContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_summary_panel.contract.json"
);
const accountOrdersContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_orders_panel.contract.json"
);
const accountOrderDetailContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_order_detail_panel.contract.json"
);
const accountPositionsContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_positions_panel.contract.json"
);
const accountSettlementContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_settlement_panel.contract.json"
);
const accountEquityContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_equity_panel.contract.json"
);
const accountReconcileContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_reconcile_panel.contract.json"
);
const accountIncidentsContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_incidents_panel.contract.json"
);
const accountEvidenceContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "account_evidence_panel.contract.json"
);
const intradayMonitorContractPath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "panels",
  "intraday_monitor_panel.contract.json"
);
const fixtureDir = path.join(repoRoot, "contracts", "ui", "fixtures", "daily_closeout");
const accountWorkbenchFixtureDir = path.join(
  repoRoot,
  "contracts",
  "ui",
  "fixtures",
  "account_workbench"
);
const intradayMonitorFixtureDir = path.join(
  repoRoot,
  "contracts",
  "ui",
  "fixtures",
  "intraday_monitor"
);
const p077FixturePath = path.join(
  repoRoot,
  "contracts",
  "ui",
  "fixtures",
  "p077_paper_slice",
  "e100_close_yesterday_filled_e102_closeout.json"
);
const requiredFixtureFiles = new Set([
  "account_health_happy_path.json",
  "account_health_adr0044_foundation_closeout.json",
  "account_health_empty.json",
  "account_health_blocked_settlement.json",
  "account_health_stale_stream.json",
  "account_health_partial_evidence.json"
]);
const requiredAccountSummaryFixtureFiles = new Set([
  "account_summary_happy_path.json",
  "account_summary_empty.json",
  "account_summary_blocked.json",
  "account_summary_stale_stream.json",
  "account_summary_partial_evidence.json"
]);
const requiredAccountOrdersFixtureFiles = new Set([
  "account_orders_current_e100.json",
  "account_orders_empty.json",
  "account_orders_blocked_missing_lifecycle.json",
  "account_orders_stale_stream.json",
  "account_order_detail_e100_filled_lifecycle.json",
  "account_order_detail_blocked_missing_events.json"
]);
const requiredAccountPositionsFixtureFiles = new Set([
  "account_positions_current_e100.json",
  "account_positions_empty.json",
  "account_positions_blocked_missing_carryover.json",
  "account_positions_stale_stream.json",
  "account_positions_partial_missing_settlement.json"
]);
const requiredAccountSettlementFixtureFiles = new Set([
  "account_settlement_current.json",
  "account_settlement_empty.json",
  "account_settlement_blocked_missing_current.json",
  "account_settlement_stale_stream.json",
  "account_settlement_partial_missing_carryover.json"
]);
const requiredAccountEquityFixtureFiles = new Set([
  "account_equity_current.json",
  "account_equity_empty.json",
  "account_equity_blocked_missing_ledger.json",
  "account_equity_stale_stream.json",
  "account_equity_partial_missing_curve.json"
]);
const requiredAccountReconcileFixtureFiles = new Set([
  "account_reconcile_matched.json",
  "account_reconcile_empty.json",
  "account_reconcile_mismatch.json",
  "account_reconcile_stale_stream.json",
  "account_reconcile_partial_missing_tolerance.json"
]);
const requiredAccountIncidentsFixtureFiles = new Set([
  "account_incidents_active.json",
  "account_incidents_empty.json",
  "account_incidents_blocked_source.json",
  "account_incidents_stale_stream.json",
  "account_incidents_partial_missing_repair.json"
]);
const requiredAccountEvidenceFixtureFiles = new Set([
  "account_evidence_current.json",
  "account_evidence_empty.json",
  "account_evidence_blocked_missing_schema.json",
  "account_evidence_stale_stream.json",
  "account_evidence_partial_missing_raw_payload.json"
]);
const requiredIntradayMonitorFixtureFiles = new Set([
  "intraday_monitor_current.json",
  "intraday_monitor_empty.json",
  "intraday_monitor_blocked.json",
  "intraday_monitor_stale.json",
  "intraday_monitor_partial.json"
]);
const forbiddenPattern =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;
const checksumPattern = /^sha256:[a-f0-9]{64}$/;

function readJson(filePath) {
  return JSON.parse(readFileSync(filePath, "utf8"));
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function collectFiles(dir, files = []) {
  for (const item of readdirSync(dir)) {
    const fullPath = path.join(dir, item);
    if (statSync(fullPath).isDirectory()) {
      collectFiles(fullPath, files);
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

function scanForbiddenTerms() {
  const scanRoots = [
    path.join(repoRoot, "frontend", "src"),
    fixtureDir,
    accountWorkbenchFixtureDir,
    intradayMonitorFixtureDir
  ];
  for (const root of scanRoots) {
    for (const filePath of collectFiles(root)) {
      const content = readFileSync(filePath, "utf8");
      const match = content.match(forbiddenPattern);
      assert(!match, `forbidden UI wording/action "${match?.[0]}" found in ${filePath}`);
    }
  }
}

function validateAccountSummaryFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_summary_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.workbench === "Account Workbench", `${fileName}: workbench mismatch`);
  assert(fixture.panel === "Account Summary Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}", `${fileName}: route mismatch`);
  assert(
    ["happy_path", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state),
    `${fileName}: fixture_state mismatch`
  );
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assert(fixture.context.source_authority, `${fileName}: source authority missing`);
  assert(fixture.account.account_id, `${fileName}: account_id missing`);
  assert(fixture.account.account_alias, `${fileName}: account_alias missing`);
  assert(Array.isArray(fixture.positions), `${fileName}: positions must be an array`);
  assert(Array.isArray(fixture.blockers), `${fileName}: blockers must be an array`);
  assert(Array.isArray(fixture.source_refs), `${fileName}: source_refs must be an array`);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);

  for (const key of [
    "read_only_projection",
    "runtime_truth",
    "ledger_truth",
    "ui_truth",
    "paper_ready",
    "live_ready",
    "broker_tradable",
    "admission_truth",
    "capital_truth",
    "action_controls"
  ]) {
    const expected = key === "read_only_projection";
    assert(fixture.boundaries[key] === expected, `${fileName}: boundary ${key} mismatch`);
  }

  if (fixture.fixture_state === "empty") {
    assert(fixture.positions.length === 0, `${fileName}: empty fixture should not include positions`);
    assert(fixture.blockers.length === 0, `${fileName}: empty fixture should not include blockers`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked fixture requires a blocker`);
    assert(fixture.account.display_state === "blocked", `${fileName}: blocked fixture display_state mismatch`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale fixture stream_state mismatch`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial fixture requires a blocker`);
  }

  for (const source of fixture.source_refs) {
    assert(source.source_ref, `${fileName}: source_ref missing`);
    assert(checksumPattern.test(source.checksum), `${fileName}: source checksum must be sha256`);
    assert(source.authority, `${fileName}: source authority missing`);
  }
  for (const position of fixture.positions) {
    assert(position.source_ref, `${fileName}: position source_ref missing`);
    assert(checksumPattern.test(position.checksum), `${fileName}: position checksum must be sha256`);
  }
  for (const blocker of fixture.blockers) {
    assert(blocker.blocker_id, `${fileName}: blocker_id missing`);
    assert(blocker.next_action, `${fileName}: blocker next_action missing`);
    assert(blocker.source_ref, `${fileName}: blocker source_ref missing`);
    assert(checksumPattern.test(blocker.checksum), `${fileName}: blocker checksum must be sha256`);
  }
}

function assertReadOnlyOrderBoundaries(fixture, fileName) {
  assert(fixture.boundaries.read_only_projection === true, `${fileName}: read_only_projection mismatch`);
  for (const key of [
    "runtime_truth",
    "account_truth",
    "order_truth",
    "ledger_truth",
    "ui_truth",
    "paper_ready",
    "live_ready",
    "broker_tradable",
    "admission_truth",
    "capital_truth",
    "action_controls"
  ]) {
    assert(fixture.boundaries[key] === false, `${fileName}: boundary ${key} must be false`);
  }
}

function validateOrderRow(order, fileName) {
  assert(order.account_id, `${fileName}: order account_id missing`);
  assert(order.client_order_id, `${fileName}: client_order_id missing`);
  assert(order.instrument, `${fileName}: instrument missing`);
  assert(order.source_ref, `${fileName}: order source_ref missing`);
  assert(checksumPattern.test(order.checksum), `${fileName}: order checksum must be sha256`);
  if (order.status === "filled") {
    assert(order.lifecycle_ref, `${fileName}: filled order requires lifecycle_ref`);
    assert(order.report_provenance_ref, `${fileName}: filled order requires report_provenance_ref`);
    assert(order.filled_quantity === order.quantity, `${fileName}: filled quantity must equal order quantity`);
  }
}

function validateAccountOrdersFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_orders_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.workbench === "Account Workbench", `${fileName}: workbench mismatch`);
  assert(fixture.panel === "Account Orders Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/orders", `${fileName}: route mismatch`);
  assert(["current_orders", "empty", "blocked", "stale"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assert(Array.isArray(fixture.orders), `${fileName}: orders must be an array`);
  assert(Array.isArray(fixture.blockers), `${fileName}: blockers must be an array`);
  assert(Array.isArray(fixture.source_refs), `${fileName}: source_refs must be an array`);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  if (fixture.fixture_state === "current_orders") {
    assert(fixture.orders.length > 0, `${fileName}: current_orders requires at least one order`);
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.orders.length === 0, `${fileName}: empty orders fixture should not include orders`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked orders fixture requires blocker`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale orders fixture stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale orders fixture requires blocker`);
  }
  for (const order of fixture.orders) {
    validateOrderRow(order, fileName);
  }
  for (const source of fixture.source_refs) {
    assert(source.source_ref, `${fileName}: source_ref missing`);
    assert(checksumPattern.test(source.checksum), `${fileName}: source checksum must be sha256`);
    assert(source.authority, `${fileName}: source authority missing`);
  }
}

function validateAccountOrderDetailFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_order_detail_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.workbench === "Account Workbench", `${fileName}: workbench mismatch`);
  assert(fixture.panel === "Account Order Detail Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/orders/{client_order_id}", `${fileName}: route mismatch`);
  assert(["filled_lifecycle", "blocked", "stale"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  validateOrderRow(fixture.order, fileName);
  assert(Array.isArray(fixture.events), `${fileName}: events must be an array`);
  assert(Array.isArray(fixture.report_provenance), `${fileName}: report_provenance must be an array`);
  assert(Array.isArray(fixture.blockers), `${fileName}: blockers must be an array`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  if (fixture.fixture_state === "filled_lifecycle") {
    assert(fixture.events.length >= 2, `${fileName}: filled lifecycle requires official event sequence`);
    assert(fixture.report_provenance.length > 0, `${fileName}: filled lifecycle requires report provenance`);
    const eventSeq = fixture.events.map((event) => event.event_seq).join(",");
    assert(eventSeq === "0,1", `${fileName}: event sequence must be stable and ordered`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.events.length === 0, `${fileName}: blocked detail should not invent events`);
    assert(fixture.blockers.length > 0, `${fileName}: blocked detail requires blocker`);
  }
  for (const event of fixture.events) {
    assert(event.event_id, `${fileName}: event_id missing`);
    assert(Number.isInteger(event.event_seq), `${fileName}: event_seq must be integer`);
    assert(event.source_ref, `${fileName}: event source_ref missing`);
    assert(checksumPattern.test(event.checksum), `${fileName}: event checksum must be sha256`);
    assert(event.authority, `${fileName}: event authority missing`);
  }
}

function validatePositionRow(position, fileName) {
  assert(position.account_id, `${fileName}: position account_id missing`);
  assert(position.instrument, `${fileName}: position instrument missing`);
  assert(["LONG", "SHORT", "NET", "UNKNOWN"].includes(position.direction), `${fileName}: position direction mismatch`);
  assert(position.source_ref, `${fileName}: position source_ref missing`);
  assert(checksumPattern.test(position.checksum), `${fileName}: position checksum must be sha256`);
}

function validateAccountPositionsFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_positions_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.workbench === "Account Workbench", `${fileName}: workbench mismatch`);
  assert(fixture.panel === "Account Positions Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/positions", `${fileName}: route mismatch`);
  assert(["current_positions", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assert(fixture.account.account_id, `${fileName}: account_id missing`);
  assert(fixture.account.account_alias, `${fileName}: account_alias missing`);
  assert(Array.isArray(fixture.positions), `${fileName}: positions must be an array`);
  assert(Array.isArray(fixture.blockers), `${fileName}: blockers must be an array`);
  assert(Array.isArray(fixture.source_refs), `${fileName}: source_refs must be an array`);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  if (fixture.fixture_state === "current_positions") {
    assert(fixture.positions.length > 0, `${fileName}: current_positions requires at least one position`);
    for (const position of fixture.positions) {
      assert(position.carryover_ref, `${fileName}: current position requires carryover_ref`);
      assert(position.settlement_ref, `${fileName}: current position requires settlement_ref`);
    }
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.positions.length === 0, `${fileName}: empty positions fixture should not include positions`);
    assert(fixture.blockers.length === 0, `${fileName}: empty positions fixture should not include blockers`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked positions fixture requires blocker`);
    assert(fixture.positions.some((position) => position.carryover_ref === null), `${fileName}: blocked fixture should expose missing carryover`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale positions fixture stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale positions fixture requires blocker`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial positions fixture requires blocker`);
    assert(fixture.positions.some((position) => position.settlement_ref === null), `${fileName}: partial fixture should expose missing settlement`);
  }
  for (const position of fixture.positions) {
    validatePositionRow(position, fileName);
  }
  for (const source of fixture.source_refs) {
    assert(source.source_ref, `${fileName}: source_ref missing`);
    assert(checksumPattern.test(source.checksum), `${fileName}: source checksum must be sha256`);
    assert(source.authority, `${fileName}: source authority missing`);
  }
  for (const blocker of fixture.blockers) {
    assert(blocker.blocker_id, `${fileName}: blocker_id missing`);
    assert(blocker.next_action, `${fileName}: blocker next_action missing`);
    assert(blocker.source_ref, `${fileName}: blocker source_ref missing`);
    assert(checksumPattern.test(blocker.checksum), `${fileName}: blocker checksum must be sha256`);
  }
}

function validateAccountSettlementFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_settlement_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.panel === "Account Settlement Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/settlement", `${fileName}: route mismatch`);
  assert(["current_settlement", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  assert(fixture.settlement.source_ref, `${fileName}: settlement source_ref missing`);
  assert(checksumPattern.test(fixture.settlement.checksum), `${fileName}: settlement checksum must be sha256`);
  if (fixture.fixture_state === "current_settlement") {
    assert(fixture.settlement.current_settlement_ref, `${fileName}: current settlement requires current_settlement_ref`);
    assert(fixture.settlement.position_carryover_ref, `${fileName}: current settlement requires position_carryover_ref`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked settlement requires blocker`);
    assert(fixture.settlement.current_settlement_ref === null, `${fileName}: blocked fixture should expose missing current settlement`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale settlement stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale settlement requires blocker`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial settlement requires blocker`);
    assert(fixture.settlement.position_carryover_ref === null, `${fileName}: partial fixture should expose missing carryover`);
  }
}

function validateAccountEquityFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_equity_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.panel === "Account Equity Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/equity", `${fileName}: route mismatch`);
  assert(["current_equity", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  if (fixture.fixture_state === "current_equity") {
    assert(fixture.equity_points.length > 0, `${fileName}: current equity requires points`);
    for (const point of fixture.equity_points) {
      assert(point.ledger_ref, `${fileName}: current equity point requires ledger_ref`);
      assert(point.curve_ref, `${fileName}: current equity point requires curve_ref`);
    }
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.equity_points.length === 0, `${fileName}: empty equity should not include points`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked equity requires blocker`);
    assert(fixture.equity_points.some((point) => point.ledger_ref === null), `${fileName}: blocked fixture should expose missing ledger_ref`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale equity stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale equity requires blocker`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial equity requires blocker`);
    assert(fixture.equity_points.some((point) => point.curve_ref === null), `${fileName}: partial fixture should expose missing curve_ref`);
  }
  for (const point of fixture.equity_points) {
    assert(point.source_ref, `${fileName}: equity point source_ref missing`);
    assert(checksumPattern.test(point.checksum), `${fileName}: equity point checksum must be sha256`);
  }
}

function validateAccountReconcileFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_reconcile_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.panel === "Account Reconcile Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/reconcile", `${fileName}: route mismatch`);
  assert(["matched", "empty", "mismatch", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  if (fixture.fixture_state === "matched") {
    assert(fixture.reconcile_items.length > 0, `${fileName}: matched reconcile requires items`);
    assert(fixture.reconcile_items.every((item) => item.status === "matched"), `${fileName}: matched fixture should only include matched rows`);
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.reconcile_items.length === 0, `${fileName}: empty reconcile should not include items`);
    assert(fixture.blockers.length === 0, `${fileName}: empty reconcile should not include blockers`);
  }
  if (fixture.fixture_state === "mismatch") {
    assert(fixture.blockers.length > 0, `${fileName}: mismatch reconcile requires blocker`);
    assert(fixture.reconcile_items.some((item) => item.status === "mismatch" && item.mismatch_ref), `${fileName}: mismatch fixture should expose mismatch_ref`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale reconcile stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale reconcile requires blocker`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial reconcile requires blocker`);
    assert(fixture.reconcile_items.some((item) => item.tolerance_ref === null), `${fileName}: partial fixture should expose missing tolerance_ref`);
  }
  for (const item of fixture.reconcile_items) {
    assert(item.item_id, `${fileName}: reconcile item_id missing`);
    assert(item.owner, `${fileName}: reconcile owner missing`);
    assert(item.next_action, `${fileName}: reconcile next_action missing`);
    assert(item.source_ref, `${fileName}: reconcile source_ref missing`);
    assert(checksumPattern.test(item.checksum), `${fileName}: reconcile checksum must be sha256`);
  }
}

function validateAccountIncidentsFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_incidents_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.panel === "Account Incidents Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/incidents", `${fileName}: route mismatch`);
  assert(["active_incidents", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  if (fixture.fixture_state === "active_incidents") {
    assert(fixture.incidents.length > 0, `${fileName}: active incidents requires rows`);
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.incidents.length === 0, `${fileName}: empty incidents should not include rows`);
    assert(fixture.blockers.length === 0, `${fileName}: empty incidents should not include blockers`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked incidents requires blocker`);
    assert(fixture.incidents.some((incident) => incident.repair_ref === null), `${fileName}: blocked fixture should expose missing repair_ref`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale incidents stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale incidents requires blocker`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial incidents requires blocker`);
    assert(fixture.incidents.some((incident) => incident.repair_ref === null), `${fileName}: partial fixture should expose missing repair_ref`);
  }
  for (const incident of fixture.incidents) {
    assert(incident.incident_id, `${fileName}: incident_id missing`);
    assert(incident.owner, `${fileName}: incident owner missing`);
    assert(incident.next_action, `${fileName}: incident next_action missing`);
    assert(incident.source_ref, `${fileName}: incident source_ref missing`);
    assert(checksumPattern.test(incident.checksum), `${fileName}: incident checksum must be sha256`);
  }
}

function validateAccountEvidenceFixture(fileName) {
  const filePath = path.join(accountWorkbenchFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_evidence_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.panel === "Account Evidence Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/accounts/{account_id}/evidence", `${fileName}: route mismatch`);
  assert(["current_evidence", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  if (fixture.fixture_state === "current_evidence") {
    assert(fixture.evidence_packages.length > 0, `${fileName}: current evidence requires packages`);
    assert(fixture.evidence_packages.every((pkg) => pkg.status === "current"), `${fileName}: current fixture should only include current packages`);
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.evidence_packages.length === 0, `${fileName}: empty evidence should not include packages`);
    assert(fixture.blockers.length === 0, `${fileName}: empty evidence should not include blockers`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked evidence requires blocker`);
    assert(fixture.evidence_packages.some((pkg) => pkg.schema_ref === "missing"), `${fileName}: blocked fixture should expose missing schema_ref`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale evidence stream mismatch`);
    assert(fixture.blockers.length > 0, `${fileName}: stale evidence requires blocker`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.blockers.length > 0, `${fileName}: partial evidence requires blocker`);
    assert(fixture.evidence_packages.some((pkg) => pkg.raw_payload_ref === null), `${fileName}: partial fixture should expose missing raw_payload_ref`);
  }
  for (const pkg of fixture.evidence_packages) {
    assert(pkg.package_id, `${fileName}: package_id missing`);
    assert(pkg.owner, `${fileName}: evidence owner missing`);
    assert(pkg.schema_ref, `${fileName}: schema_ref missing`);
    assert(pkg.schema_version_ref, `${fileName}: schema_version_ref missing`);
    assert(pkg.source_ref, `${fileName}: evidence source_ref missing`);
    assert(pkg.next_action, `${fileName}: evidence next_action missing`);
    assert(checksumPattern.test(pkg.checksum), `${fileName}: evidence checksum must be sha256`);
    if (pkg.raw_payload_ref) {
      assert(pkg.normalized_ref, `${fileName}: raw_payload_ref requires normalized_ref`);
    }
  }
}

function validateP077PaperSliceFixture() {
  const contract = readJson(p077PanelContractPath);
  assert(contract.title === "P077 Paper Slice Evidence Read Model", "P077 panel contract title mismatch");
  const fixture = readJson(p077FixturePath);
  assert(fixture.schema_version === "p077_paper_slice_panel.v1", "P077 fixture schema_version mismatch");
  assert(fixture.panel === "P077 Paper Slice Evidence Panel", "P077 fixture panel mismatch");
  assert(fixture.context.projection_owner === "account-console-contracts", "P077 projection owner mismatch");
  assert(fixture.context.producer_owner === "nautilus_ctp_adapter", "P077 producer owner mismatch");
  assert(checksumPattern.test(fixture.context.checksum), "P077 context checksum must be sha256");
  assert(fixture.slice.account_alias === "19053", "P077 account alias mismatch");
  assert(fixture.slice.instrument === "rb2610", "P077 instrument mismatch");
  assert(fixture.slice.disposition === "filled", "P077 disposition mismatch");
  assert(fixture.slice.fill_volume === 1, "P077 fill volume mismatch");
  assert(fixture.slice.authorization_consumed === true, "P077 authorization consumption mismatch");
  assert(fixture.slice.active_authorization === false, "P077 active authorization must be false");
  assert(fixture.boundaries.read_only_projection === true, "P077 read-only projection boundary mismatch");
  for (const key of [
    "runtime_truth",
    "ledger_truth",
    "ui_truth",
    "paper_ready",
    "live_ready",
    "broker_tradable",
    "admission_truth",
    "capital_truth"
  ]) {
    assert(fixture.boundaries[key] === false, `P077 boundary ${key} must be false`);
  }
  for (const evidence of fixture.evidence) {
    assert(evidence.source_ref, `P077 evidence ${evidence.kind} source_ref missing`);
    assert(checksumPattern.test(evidence.checksum), `P077 evidence ${evidence.kind} checksum must be sha256`);
    assert(evidence.authority, `P077 evidence ${evidence.kind} authority missing`);
  }
}

function validateIntradayMonitorFixture(fileName) {
  const filePath = path.join(intradayMonitorFixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "intraday_monitor_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.workbench === "Intraday Monitor", `${fileName}: workbench mismatch`);
  assert(fixture.panel === "Intraday Monitor Exception Queue Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/monitor", `${fileName}: route mismatch`);
  assert(["current", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state), `${fileName}: state mismatch`);
  assert(fixture.context.projection_owner === "account-console-contracts", `${fileName}: projection owner mismatch`);
  assertReadOnlyOrderBoundaries(fixture, fileName);
  assert(Array.isArray(fixture.exceptions), `${fileName}: exceptions must be an array`);
  assert(Array.isArray(fixture.streams), `${fileName}: streams must be an array`);
  assert(Array.isArray(fixture.incidents), `${fileName}: incidents must be an array`);
  assert(Array.isArray(fixture.blockers), `${fileName}: blockers must be an array`);
  assert(fixture.source_refs.length > 0, `${fileName}: source_refs missing`);
  assert(Number.isInteger(fixture.lag_summary.stale_stream_count), `${fileName}: stale_stream_count missing`);
  assert(Number.isInteger(fixture.lag_summary.open_incident_count), `${fileName}: open_incident_count missing`);
  assert(Number.isInteger(fixture.lag_summary.blocked_source_count), `${fileName}: blocked_source_count missing`);

  if (fixture.fixture_state === "current") {
    assert(fixture.exceptions.length > 0, `${fileName}: current fixture requires exception rows`);
    assert(fixture.streams.length > 0, `${fileName}: current fixture requires stream rows`);
  }
  if (fixture.fixture_state === "empty") {
    assert(fixture.exceptions.length === 0, `${fileName}: empty fixture should not include exceptions`);
    assert(fixture.streams.length === 0, `${fileName}: empty fixture should not include streams`);
    assert(fixture.incidents.length === 0, `${fileName}: empty fixture should not include incidents`);
    assert(fixture.blockers.length === 0, `${fileName}: empty fixture should not include blockers`);
  }
  if (fixture.fixture_state === "blocked") {
    assert(fixture.blockers.length > 0, `${fileName}: blocked fixture requires blockers`);
    assert(fixture.lag_summary.blocked_source_count > 0, `${fileName}: blocked fixture requires blocked source count`);
  }
  if (fixture.fixture_state === "stale") {
    assert(fixture.context.stream_state === "stale", `${fileName}: stale fixture stream mismatch`);
    assert(fixture.lag_summary.stale_stream_count > 0, `${fileName}: stale fixture requires stale streams`);
  }
  if (fixture.fixture_state === "partial") {
    assert(fixture.context.stream_state === "partial", `${fileName}: partial fixture stream mismatch`);
    assert(fixture.streams.some((stream) => stream.lag_ms === null), `${fileName}: partial fixture should expose missing lag`);
  }

  for (const exception of fixture.exceptions) {
    assert(exception.exception_id, `${fileName}: exception_id missing`);
    assert(exception.owner, `${fileName}: exception owner missing`);
    assert(exception.next_action, `${fileName}: exception next_action missing`);
    assert(exception.source_ref, `${fileName}: exception source_ref missing`);
    assert(checksumPattern.test(exception.checksum), `${fileName}: exception checksum must be sha256`);
  }
  for (const stream of fixture.streams) {
    assert(stream.stream_id, `${fileName}: stream_id missing`);
    assert(stream.source_ref, `${fileName}: stream source_ref missing`);
    assert(checksumPattern.test(stream.checksum), `${fileName}: stream checksum must be sha256`);
  }
  for (const incident of fixture.incidents) {
    assert(incident.incident_id, `${fileName}: incident_id missing`);
    assert(incident.owner, `${fileName}: incident owner missing`);
    assert(incident.next_action, `${fileName}: incident next_action missing`);
    assert(incident.source_ref, `${fileName}: incident source_ref missing`);
    assert(checksumPattern.test(incident.checksum), `${fileName}: incident checksum must be sha256`);
  }
}

function validateFixture(fileName) {
  const filePath = path.join(fixtureDir, fileName);
  const fixture = readJson(filePath);
  assert(fixture.schema_version === "account_health_panel.v1", `${fileName}: schema_version mismatch`);
  assert(fixture.workbench === "Daily Closeout", `${fileName}: workbench mismatch`);
  assert(fixture.panel === "Account Health Panel", `${fileName}: panel mismatch`);
  assert(fixture.route === "/closeout", `${fileName}: route mismatch`);
  assert(
    ["happy_path", "empty", "blocked", "stale", "partial"].includes(fixture.fixture_state),
    `${fileName}: fixture_state mismatch`
  );
  assert(checksumPattern.test(fixture.context.checksum), `${fileName}: context checksum must be sha256`);
  assert(Array.isArray(fixture.accounts), `${fileName}: accounts must be an array`);

  const totalAccounts = fixture.accounts.length;
  const closeoutCompleted = fixture.accounts.filter((row) => row.closeout_state === "complete").length;
  const closeoutBlocked = fixture.accounts.filter((row) => row.closeout_state === "blocked").length;
  const settlementBlocked = fixture.accounts.filter((row) => row.settlement_state === "blocked").length;
  const staleOrPartial = fixture.accounts.filter((row) =>
    ["stale", "partial"].includes(row.closeout_state) ||
    ["stale", "partial"].includes(row.settlement_state) ||
    ["stale", "partial"].includes(row.equity_continuity)
  ).length;
  const openBlockers = fixture.accounts.reduce((count, row) => count + row.blockers.length, 0);

  assert(fixture.summary.total_accounts === totalAccounts, `${fileName}: total_accounts mismatch`);
  assert(fixture.summary.closeout_completed === closeoutCompleted, `${fileName}: completed count mismatch`);
  assert(fixture.summary.closeout_blocked === closeoutBlocked, `${fileName}: blocked count mismatch`);
  assert(fixture.summary.settlement_blocked === settlementBlocked, `${fileName}: settlement count mismatch`);
  assert(fixture.summary.stale_or_partial === staleOrPartial, `${fileName}: stale/partial count mismatch`);
  assert(fixture.summary.open_blockers === openBlockers, `${fileName}: blocker count mismatch`);

  for (const row of fixture.accounts) {
    assert(row.account_id, `${fileName}: row account_id missing`);
    assert(row.source_ref, `${fileName}: ${row.account_id} source_ref missing`);
    assert(checksumPattern.test(row.checksum), `${fileName}: ${row.account_id} checksum must be sha256`);
    assert(row.blocker_count === row.blockers.length, `${fileName}: ${row.account_id} blocker_count mismatch`);
    assert(row.closeout_run_id, `${fileName}: ${row.account_id} closeout_run_id missing`);
    assert(row.settlement_run_id, `${fileName}: ${row.account_id} settlement_run_id missing`);
    assert(row.equity_curve_artifact_id, `${fileName}: ${row.account_id} equity artifact missing`);
    for (const blocker of row.blockers) {
      assert(blocker.source_ref, `${fileName}: ${row.account_id} blocker source_ref missing`);
      assert(blocker.next_diagnostic_ref, `${fileName}: ${row.account_id} diagnostic ref missing`);
    }
  }
}

function main() {
  const contract = readJson(panelContractPath);
  assert(contract.title === "Account Health Panel Read Model", "panel contract title mismatch");
  const accountSummaryContract = readJson(accountSummaryContractPath);
  assert(
    accountSummaryContract.title === "Account Summary Panel Read Model",
    "account summary panel contract title mismatch"
  );
  const accountOrdersContract = readJson(accountOrdersContractPath);
  assert(accountOrdersContract.title === "Account Orders Panel Read Model", "account orders contract title mismatch");
  const accountOrderDetailContract = readJson(accountOrderDetailContractPath);
  assert(
    accountOrderDetailContract.title === "Account Order Detail Panel Read Model",
    "account order detail contract title mismatch"
  );
  const accountPositionsContract = readJson(accountPositionsContractPath);
  assert(
    accountPositionsContract.title === "Account Positions Panel Read Model",
    "account positions contract title mismatch"
  );
  const accountSettlementContract = readJson(accountSettlementContractPath);
  assert(
    accountSettlementContract.title === "Account Settlement Panel Read Model",
    "account settlement contract title mismatch"
  );
  const accountEquityContract = readJson(accountEquityContractPath);
  assert(accountEquityContract.title === "Account Equity Panel Read Model", "account equity contract title mismatch");
  const accountReconcileContract = readJson(accountReconcileContractPath);
  assert(
    accountReconcileContract.title === "Account Reconcile Panel Read Model",
    "account reconcile contract title mismatch"
  );
  const accountIncidentsContract = readJson(accountIncidentsContractPath);
  assert(
    accountIncidentsContract.title === "Account Incidents Panel Read Model",
    "account incidents contract title mismatch"
  );
  const accountEvidenceContract = readJson(accountEvidenceContractPath);
  assert(
    accountEvidenceContract.title === "Account Evidence Panel Read Model",
    "account evidence contract title mismatch"
  );
  const intradayMonitorContract = readJson(intradayMonitorContractPath);
  assert(
    intradayMonitorContract.title === "Intraday Monitor Panel Read Model",
    "intraday monitor contract title mismatch"
  );
  const fixtureFiles = readdirSync(fixtureDir).filter((fileName) => fileName.startsWith("account_health_"));
  for (const required of requiredFixtureFiles) {
    assert(fixtureFiles.includes(required), `missing required fixture ${required}`);
  }
  for (const fileName of fixtureFiles) {
    validateFixture(fileName);
  }
  const accountSummaryFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_summary_")
  );
  for (const required of requiredAccountSummaryFixtureFiles) {
    assert(accountSummaryFixtureFiles.includes(required), `missing required account summary fixture ${required}`);
  }
  for (const fileName of accountSummaryFixtureFiles) {
    validateAccountSummaryFixture(fileName);
  }
  const accountOrdersFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter(
    (fileName) => fileName.startsWith("account_orders_") || fileName.startsWith("account_order_detail_")
  );
  for (const required of requiredAccountOrdersFixtureFiles) {
    assert(accountOrdersFixtureFiles.includes(required), `missing required account orders fixture ${required}`);
  }
  for (const fileName of accountOrdersFixtureFiles) {
    if (fileName.startsWith("account_orders_")) {
      validateAccountOrdersFixture(fileName);
    } else {
      validateAccountOrderDetailFixture(fileName);
    }
  }
  const accountPositionsFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_positions_")
  );
  for (const required of requiredAccountPositionsFixtureFiles) {
    assert(accountPositionsFixtureFiles.includes(required), `missing required account positions fixture ${required}`);
  }
  for (const fileName of accountPositionsFixtureFiles) {
    validateAccountPositionsFixture(fileName);
  }
  const accountSettlementFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_settlement_")
  );
  for (const required of requiredAccountSettlementFixtureFiles) {
    assert(accountSettlementFixtureFiles.includes(required), `missing required account settlement fixture ${required}`);
  }
  for (const fileName of accountSettlementFixtureFiles) {
    validateAccountSettlementFixture(fileName);
  }
  const accountEquityFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_equity_")
  );
  for (const required of requiredAccountEquityFixtureFiles) {
    assert(accountEquityFixtureFiles.includes(required), `missing required account equity fixture ${required}`);
  }
  for (const fileName of accountEquityFixtureFiles) {
    validateAccountEquityFixture(fileName);
  }
  const accountReconcileFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_reconcile_")
  );
  for (const required of requiredAccountReconcileFixtureFiles) {
    assert(accountReconcileFixtureFiles.includes(required), `missing required account reconcile fixture ${required}`);
  }
  for (const fileName of accountReconcileFixtureFiles) {
    validateAccountReconcileFixture(fileName);
  }
  const accountIncidentsFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_incidents_")
  );
  for (const required of requiredAccountIncidentsFixtureFiles) {
    assert(accountIncidentsFixtureFiles.includes(required), `missing required account incidents fixture ${required}`);
  }
  for (const fileName of accountIncidentsFixtureFiles) {
    validateAccountIncidentsFixture(fileName);
  }
  const accountEvidenceFixtureFiles = readdirSync(accountWorkbenchFixtureDir).filter((fileName) =>
    fileName.startsWith("account_evidence_")
  );
  for (const required of requiredAccountEvidenceFixtureFiles) {
    assert(accountEvidenceFixtureFiles.includes(required), `missing required account evidence fixture ${required}`);
  }
  for (const fileName of accountEvidenceFixtureFiles) {
    validateAccountEvidenceFixture(fileName);
  }
  const intradayMonitorFixtureFiles = readdirSync(intradayMonitorFixtureDir).filter((fileName) =>
    fileName.startsWith("intraday_monitor_")
  );
  for (const required of requiredIntradayMonitorFixtureFiles) {
    assert(intradayMonitorFixtureFiles.includes(required), `missing required intraday monitor fixture ${required}`);
  }
  for (const fileName of intradayMonitorFixtureFiles) {
    validateIntradayMonitorFixture(fileName);
  }
  validateP077PaperSliceFixture();
  scanForbiddenTerms();
  console.log("account health, account summary, account orders, account positions, account settlement, account equity, account reconcile, account incidents, account evidence, intraday monitor and P077 paper slice fixtures plus forbidden scan passed");
}

main();
