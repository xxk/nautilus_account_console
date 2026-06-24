from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class P021GovernanceError(AssertionError):
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P021GovernanceError(message)


def validate_route_context_owner() -> None:
    route_context = ROOT / "backend" / "src" / "nautilus_account_console" / "route_context.py"
    source_bridge = ROOT / "backend" / "src" / "nautilus_account_console" / "source_bridge.py"
    account_mirror = ROOT / "backend" / "src" / "nautilus_account_console" / "account_mirror.py"
    require(route_context.exists(), "P021-I1: canonical route_context.py is missing")
    source_text = read(source_bridge)
    mirror_text = read(account_mirror)
    require("route_context_from_source_artifact" in source_text, "P021-I1: source_bridge must use canonical source route resolver")
    require("blocked_route_context" in source_text, "P021-I1: source_bridge must use canonical blocked route resolver")
    require("route_context_from_capability_bundle" in mirror_text, "P021-I1: account_mirror must use canonical bundle route resolver")
    require("_fallback_route_context" not in source_text, "P021-I1: source_bridge must not define fallback route_context")
    require("_fallback_route_context" not in mirror_text, "P021-I1: account_mirror must not define fallback route_context")
    require("_validate_route_context_impl" in source_text, "P021-I1: source_bridge must delegate validation to canonical route_context")
    require("RouteContextError" in source_text and "SourceBridgeError" in source_text, "P021-I1: source_bridge compatibility wrapper must preserve SourceBridgeError")
    require("def validate_route_context" not in mirror_text, "P021-I1: account_mirror must not duplicate route_context validation")


def validate_source_package_boundary() -> None:
    source_bridge = ROOT / "backend" / "src" / "nautilus_account_console" / "source_bridge.py"
    issue_list = ROOT / "docs" / "proposals" / "p021-account-console-owner-fork-governance" / "issue-list.md"
    owner_map = ROOT / "docs" / "ownership" / "account-console-owner-map.md"
    source_text = read(source_bridge)
    issue_text = read(issue_list)
    owner_text = read(owner_map)
    for name in [
        "CTP19053_REAL_SOURCE_PACKAGE",
        "CTP025292_REAL_SOURCE_PACKAGE",
        "IB_U3028269_SOURCE_PACKAGE",
    ]:
        require(name in source_text, f"P021-I2: expected source package ref {name} is missing")
    require("source_ref" in source_text and "checksum" in source_text, "P021-I2: source package refs must preserve source_ref and checksum")
    require("not Account Console-owned truth" in issue_text, "P021-I2: issue ledger must reject Account Console source ownership")
    require("external strategy/runtime owner" in owner_text, "P021-I2: owner map must anchor external source owner boundary")


def validate_synthetic_test_boundary() -> None:
    spec = ROOT / "frontend" / "tests" / "e2e" / "p019-ib-tws-synthetic-ready-projection.spec.ts"
    evidence = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json"
    text = read(spec)
    require("synthetic_contract_guard_not_account_truth" in text, "P021-I3: synthetic route context must not claim account truth")
    forbidden_truth_claims = [
        "capital_truth: true",
        "account_truth: true",
        "broker_truth: true",
        "runtime_truth: true",
    ]
    present = [claim for claim in forbidden_truth_claims if claim in text]
    require(not present, f"P021-I3: synthetic test has authority leakage {present}")
    require("expect(readyProjection.boundaries.account_truth).toBe(false)" in text, "P021-I3: synthetic test needs account_truth false assertion")
    require("expect(readyProjection.boundaries.capital_truth).toBe(false)" in text, "P021-I3: synthetic test needs capital_truth false assertion")
    if evidence.exists():
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        require(payload.get("verdict") == "synthetic_contract_only", "P021-I3: synthetic evidence verdict must stay synthetic-only")
        boundaries = payload.get("boundaries", {})
        require(boundaries.get("synthetic_contract_only") is True, "P021-I3: synthetic evidence must mark synthetic_contract_only")
        require(boundaries.get("broker_truth") is False, "P021-I3: synthetic evidence must not claim broker truth")


def validate_frontend_registry_boundary() -> None:
    tests_dir = ROOT / "frontend" / "tests"
    src_dir = ROOT / "frontend" / "src"
    app = src_dir / "App.tsx"
    registry = src_dir / "app-registry.ts"
    readme = ROOT / "frontend" / "tests" / "README.md"
    readme_text = read(readme)
    require("No test file creates a second route registry" in readme_text, "P021-I4: frontend tests README must ban second route registry")
    require(registry.exists(), "P021-I4: canonical frontend registry module app-registry.ts must exist")
    production_text = "\n".join(read(path) for path in src_dir.glob("*.tsx"))
    require("frontend/tests" not in production_text, "P021-I4: production frontend must not import frontend/tests")
    app_text = read(app)
    registry_text = read(registry)
    require("from \"./fixture-registry\"" in registry_text, "P021-I4: app-registry must delegate fixture ownership to fixture-registry")
    require("from \"./app-shell-registry\"" in registry_text, "P021-I4: app-registry must delegate shell ownership to app-shell-registry")
    require("from \"./mirror-route-owner\"" in registry_text, "P021-I4: app-registry must delegate mirror route ownership to mirror-route-owner")
    require("function commandResultToStatus" not in app_text, "P021-I5: frontend must not synthesize command_status from command result")
    require("function runtimeCloseoutToStatus" not in app_text, "P021-I5: frontend must not synthesize command_status from runtime closeout")
    require(
        "const commandStatus = mirrorReadback?.selected.command_status ?? null;" in app_text,
        "P021-I5: command status must come from mirror canonical projection only",
    )
    forbidden_test_registry = re.compile(r"\b(createBrowserRouter|RouterProvider|routes\s*=|routeRegistry)\b")
    offenders = []
    for path in tests_dir.rglob("*.ts"):
        text = read(path)
        if forbidden_test_registry.search(text):
            offenders.append(str(path.relative_to(ROOT)))
    require(not offenders, f"P021-I4: tests must not create route registries: {offenders}")


def validate_backend_command_plane_owner_split() -> None:
    command_actions = ROOT / "backend" / "src" / "nautilus_account_console" / "command_actions.py"
    command_api = ROOT / "backend" / "src" / "nautilus_account_console" / "command_api.py"
    main = ROOT / "backend" / "src" / "nautilus_account_console" / "main.py"
    api_text = read(command_api)
    actions_text = read(command_actions)
    main_text = read(main)
    require(command_actions.exists(), "P021-I6: command_actions.py must exist as action-intake owner")
    require("def accept_submit_intent" in actions_text, "P021-I6: command_actions must own submit intent acceptance")
    require("def accept_cancel_intent" in actions_text, "P021-I6: command_actions must own cancel intent acceptance")
    require(
        "def prepare_submit_runtime_run_request" in actions_text,
        "P021-I6: command_actions must own submit runtime handoff preparation",
    )
    require(
        "def prepare_cancel_runtime_run_request" in actions_text,
        "P021-I6: command_actions must own cancel runtime handoff preparation",
    )
    require("def load_command_plane_projection" in api_text, "P021-I6: command_api must own canonical command-plane projection")
    require(
        'projection_owner="account-console-backend.mirror_projection"' in api_text,
        "P021-I6: command-plane projection must declare mirror projection as canonical owner",
    )
    require(
        'canonical_source="/api/mirror/accounts/{account_id}"' in api_text,
        "P021-I6: command-plane projection must point at mirror canonical source",
    )
    require(
        'legacy_read_surface_state="legacy_read_only_until_mirror_convergence"' in api_text,
        "P021-I6: command-plane projection must mark legacy reads as retirement-bound",
    )
    require("RETIRED_ARCHIVE_COMMAND_SURFACES" in api_text, "P021-I6: command api must inventory retired archive-only surfaces")
    require("LEGACY_COMMAND_RETIREMENT_SLICES" in api_text, "P021-I6: command api must carry retirement slicing inventory")
    require(
        'category="retain_blocker_projection"' in api_text and 'category="retire_when_panels_removed"' in api_text,
        "P021-I6: command-plane retirement slicing must classify legacy read surfaces",
    )
    require(
        'execution_state="active_blocker_projection"' in api_text and 'execution_state="retired_archive_only"' in api_text,
        "P021-I6: command-plane retirement slicing must declare current lifecycle state",
    )
    require("panel_ids=" in api_text, "P021-I6: retirement slicing must map legacy read surfaces to panels")
    require("LEGACY_COMMAND_RETIREMENT_BATCHES" in api_text, "P021-I6: command api must define retirement execution batches")
    require("def register_legacy_command_read_routes" in api_text, "P021-I6: command api must own legacy read route registration")
    require(
        "/api/commands/accounts/{account_id}/projection" in main_text,
        "P021-I6: main must expose canonical command-plane projection route",
    )
    require("load_command_plane_projection" in main_text, "P021-I6: main must wire read projection owner explicitly")
    require("accept_submit_intent" in main_text and "accept_cancel_intent" in main_text, "P021-I6: main must wire action owner explicitly")
    require(
        "register_legacy_command_read_routes(app)" in main_text,
        "P021-I6: main must delegate legacy read route exposure to command_api registration",
    )
    for path in [
        "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}",
        "/api/commands/accounts/{account_id}/runtime-invocation-readiness",
        "/api/commands/accounts/{account_id}/runtime-execution-approval-packet",
        "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle",
        "/api/commands/accounts/{account_id}/runtime-execution-gap-audit",
    ]:
        require(
            main_text.count(path) <= 1,
            f"P021-I6: main must not hand-maintain duplicate legacy read route registration for {path}",
        )


def validate_frontend_legacy_command_read_entrypoint() -> None:
    api = ROOT / "frontend" / "src" / "api.ts"
    app = ROOT / "frontend" / "src" / "App.tsx"
    command_plane = ROOT / "frontend" / "src" / "command-plane.ts"
    command_plane_panels = ROOT / "frontend" / "src" / "command-plane-panels.tsx"
    command_surface_panels = ROOT / "frontend" / "src" / "command-surface-panels.tsx"
    account_workbench_adapters = ROOT / "frontend" / "src" / "account-workbench-adapters.ts"
    account_workbench_routing = ROOT / "frontend" / "src" / "account-workbench-routing.ts"
    fixture_selection = ROOT / "frontend" / "src" / "fixture-selection.ts"
    fixture_registry = ROOT / "frontend" / "src" / "fixture-registry.ts"
    app_shell_registry = ROOT / "frontend" / "src" / "app-shell-registry.ts"
    mirror_route_owner = ROOT / "frontend" / "src" / "mirror-route-owner.ts"
    account_workbench_panels = ROOT / "frontend" / "src" / "account-workbench-panels.tsx"
    account_workbench_terminal = ROOT / "frontend" / "src" / "account-workbench-terminal.tsx"
    account_health_panels = ROOT / "frontend" / "src" / "account-health-panels.tsx"
    intraday_monitor_panels = ROOT / "frontend" / "src" / "intraday-monitor-panels.tsx"
    panel_shared = ROOT / "frontend" / "src" / "panel-shared.tsx"
    ui_primitives = ROOT / "frontend" / "src" / "ui-primitives.tsx"
    api_text = read(api)
    app_text = read(app)
    command_plane_text = read(command_plane)
    panel_text = read(command_plane_panels)
    command_surface_text = read(command_surface_panels)
    account_workbench_adapters_text = read(account_workbench_adapters)
    account_workbench_routing_text = read(account_workbench_routing)
    fixture_selection_text = read(fixture_selection)
    fixture_registry_text = read(fixture_registry)
    app_shell_registry_text = read(app_shell_registry)
    mirror_route_owner_text = read(mirror_route_owner)
    account_workbench_text = read(account_workbench_panels)
    account_workbench_terminal_text = read(account_workbench_terminal)
    account_health_text = read(account_health_panels)
    intraday_monitor_text = read(intraday_monitor_panels)
    panel_shared_text = read(panel_shared)
    ui_primitives_text = read(ui_primitives)
    require(
        "const LEGACY_COMMAND_READ_DESCRIPTOR" in api_text,
        "P021-I6: frontend api must declare legacy command read descriptor",
    )
    require(
        'owner: "account-console-backend.command-plane-retirement-registry"' in api_text,
        "P021-I6: frontend legacy loader must defer retirement authority to backend registry",
    )
    require(
        "async function fetchLegacyCommandReadSuite" in api_text,
        "P021-I6: frontend api must centralize legacy command read suite",
    )
    require(
        "LEGACY_COMMAND_READ_REGISTRY" in api_text,
        "P021-I6: frontend api must map legacy routes through one registry",
    )
    require(command_plane.exists(), "P021-I6: frontend command-plane owner module command-plane.ts must exist")
    require(command_plane_panels.exists(), "P021-I6: command-plane panel owner module command-plane-panels.tsx must exist")
    require(command_surface_panels.exists(), "P021-I6: command-surface panel owner module command-surface-panels.tsx must exist")
    require(account_workbench_adapters.exists(), "P021-I4: account workbench adapter owner module account-workbench-adapters.ts must exist")
    require(account_workbench_routing.exists(), "P021-I4: account workbench routing owner module account-workbench-routing.ts must exist")
    require(fixture_selection.exists(), "P021-I4: fixture selection owner module fixture-selection.ts must exist")
    require(fixture_registry.exists(), "P021-I4: fixture registry owner module fixture-registry.ts must exist")
    require(app_shell_registry.exists(), "P021-I4: app shell registry owner module app-shell-registry.ts must exist")
    require(mirror_route_owner.exists(), "P021-I4: mirror route owner module mirror-route-owner.ts must exist")
    require(account_workbench_panels.exists(), "P021-I4: account workbench panel owner module account-workbench-panels.tsx must exist")
    require(account_workbench_terminal.exists(), "P021-I4: account workbench terminal owner module account-workbench-terminal.tsx must exist")
    require(account_health_panels.exists(), "P021-I4: account health panel owner module account-health-panels.tsx must exist")
    require(intraday_monitor_panels.exists(), "P021-I4: intraday monitor panel owner module intraday-monitor-panels.tsx must exist")
    require(panel_shared.exists(), "P021-I4: shared panel helper module panel-shared.tsx must exist")
    require(ui_primitives.exists(), "P021-I6: shared ui primitive module ui-primitives.tsx must exist")
    require(
        "export function useCommandPlaneGovernance" in command_plane_text,
        "P021-I6: command-plane.ts must own command-plane governance loading",
    )
    require(
        "summarizeCommandPlaneProjection" in command_plane_text,
        "P021-I6: command-plane.ts must own command-plane retirement summary derivation",
    )
    require(
        "export function CommandPlaneOwnerPanel" in panel_text
        and "export function CommandRuntimeCloseoutPanel" in panel_text,
        "P021-I6: command-plane-panels.tsx must own command-plane governance panel rendering",
    )
    require(
        "export function CommandRuntimeRunRequestPanel" in command_surface_text
        and "export function CommandStatusPanel" in command_surface_text,
        "P021-I6: command-surface-panels.tsx must own command action/read panel rendering",
    )
    require(
        "export function useFixtureSelection" in fixture_selection_text,
        "P021-I4: fixture-selection.ts must own canonical fixture selection state and lookup",
    )
    require(
        "accountWorkbench" in fixture_selection_text and "setAccountWorkbenchFallback" in fixture_selection_text,
        "P021-I4: fixture-selection.ts must converge workbench fallback state under one owner",
    )
    require(
        "healthFixtureMap" in fixture_registry_text
        and "accountSummaryFixtureMap" in fixture_registry_text
        and "intradayMonitorFixtureMap" in fixture_registry_text,
        "P021-I4: fixture-registry.ts must own canonical fixture maps and labels",
    )
    require(
        "workbenches" in app_shell_registry_text and "portfolioOwnerConsoleUrl" in app_shell_registry_text,
        "P021-I4: app-shell-registry.ts must own shell navigation and external handoff config",
    )
    require(
        "resolveMirrorRouteAccountId" in mirror_route_owner_text and "mirrorRouteAliases" in mirror_route_owner_text,
        "P021-I4: mirror-route-owner.ts must own mirror route alias resolution",
    )
    require(
        "export function classifyAppRoute" in account_workbench_routing_text
        and "export function resolveAccountWorkbenchView" in account_workbench_routing_text
        and "export function isMirrorWorkbenchEligibleRoute" in account_workbench_routing_text,
        "P021-I4: account-workbench-routing.ts must own account workbench route classification and mirror eligibility",
    )
    require(
        "export function mirrorSummaryReadModel" in account_workbench_adapters_text
        and "export function mirrorPositionsReadModel" in account_workbench_adapters_text
        and "export function mirrorOrdersReadModel" in account_workbench_adapters_text,
        "P021-I4: account-workbench-adapters.ts must own mirror read-model derivation for account workbench surfaces",
    )
    require(
        "export function mirrorWorkbenchProjection" in account_workbench_adapters_text,
        "P021-I4: account-workbench-adapters.ts must own unified mirror workbench projection derivation",
    )
    require(
        "export function AccountOrdersPanel" in account_workbench_text
        and "export function AccountPositionsPanel" in account_workbench_text
        and "export function AccountSettlementPanel" in account_workbench_text
        and "export function AccountEquityPanel" in account_workbench_text
        and "export function AccountReconcilePanel" in account_workbench_text
        and "export function AccountIncidentsPanel" in account_workbench_text
        and "export function AccountEvidencePanel" in account_workbench_text
        and "export function AccountOrderDetailPanel" in account_workbench_text,
        "P021-I4: account-workbench-panels.tsx must own the extracted account workbench domain panel rendering",
    )
    require(
        "export function AccountWorkbenchTerminalPanel" in account_workbench_terminal_text,
        "P021-I4: account-workbench-terminal.tsx must own the account workbench terminal rendering",
    )
    require(
        "export function AccountHealthPanel" in account_health_text,
        "P021-I4: account-health-panels.tsx must own the daily closeout health panel rendering",
    )
    require(
        "export function IntradayMonitorPanel" in intraday_monitor_text,
        "P021-I4: intraday-monitor-panels.tsx must own the intraday monitor panel rendering",
    )
    require(
        "export function SourceRefsList" in panel_shared_text
        and "export function BlockerList" in panel_shared_text
        and "export function Ref" in panel_shared_text
        and "export function Metric" in panel_shared_text
        and "export function accountBoundaryRows" in panel_shared_text,
        "P021-I4: panel-shared.tsx must own cross-domain panel helpers",
    )
    require(
        "export function StateBadge" in ui_primitives_text and "export function CopyableCode" in ui_primitives_text,
        "P021-I6: ui-primitives.tsx must own shared badge/copy primitives",
    )
    require(
        "projection.retirement_slices" in api_text,
        "P021-I6: legacy read loader must be driven by backend retirement slices",
    )
    require(
        "retired_archive_surfaces" in panel_text,
        "P021-I6: canonical command-plane panel owner must render retired archive inventory separately from legacy live-read inventory",
    )
    require(
        "type LegacyCommandPanelResult" in api_text and "function toLegacyCommandPanelResult" in api_text,
        "P021-I6: frontend legacy loader must normalize projection-registered panel results in one place",
    )
    require(
        "export type LegacyCommandReadSuite" in api_text,
        "P021-I6: frontend legacy governance suite must have an explicit contract type",
    )
    require(
        "useCommandPlaneGovernance(summary.account.account_id)" in app_text,
        "P021-I6: App must consume canonical command-plane governance through the frontend owner module",
    )
    require(
        "const mirrorProjection = useMemo(" in app_text
        and "mirrorWorkbenchProjection(mirrorReadback, routeState.routeOrderId)" in app_text,
        "P021-I4: App must derive a unified mirror workbench projection before rendering account panels",
    )
    require(
        'from "./account-workbench-panels"' in app_text
        and 'from "./account-workbench-adapters"' in app_text
        and 'from "./account-workbench-routing"' in app_text
        and 'from "./fixture-selection"' in app_text
        and 'from "./app-shell-registry"' in app_text
        and 'from "./mirror-route-owner"' in app_text
        and 'from "./account-workbench-terminal"' in app_text
        and 'from "./account-health-panels"' in app_text
        and 'from "./intraday-monitor-panels"' in app_text
        and 'from "./panel-shared"' in app_text
        and 'from "./ui-primitives"' in app_text,
        "P021: App must consume domain panels, terminal owner, and shared primitives through canonical frontend owner modules",
    )
    require(
        "fetchLegacyCommandReadSuite(accountId, commandPlaneProjectionResult)" in command_plane_text,
        "P021-I6: command-plane.ts must load legacy reads through the canonical command-plane projection",
    )
    require(
        "useState<LegacyCommandReadSuite | null>(null)" in command_plane_text
        and "Awaited<ReturnType<typeof fetchLegacyCommandReadSuite>>" not in command_plane_text,
        "P021-I6: command-plane.ts must depend on the explicit legacy governance suite contract, not an inferred return type",
    )
    for legacy_panel in [
        "function CommandRuntimeInvocationReadinessPanel",
        "function CommandRuntimeExecutionApprovalPacketPanel",
        "function CommandRuntimeExecutionHandoffBundlePanel",
        "function CommandRuntimeExecutionGapAuditPanel",
        "function CommandRuntimeCloseoutPanel",
        "function CommandRuntimeRunRequestPanel",
        "function CommandIntentReceiptPanel",
        "function CommandStatusPanel",
        "function AccountOrdersPanel",
        "function AccountPositionsPanel",
        "function AccountSettlementPanel",
        "function AccountEquityPanel",
        "function AccountReconcilePanel",
        "function AccountIncidentsPanel",
        "function AccountEvidencePanel",
        "function AccountOrderDetailPanel",
        "function AccountHealthPanel",
        "function IntradayMonitorPanel",
        "function AccountWorkbenchTerminalPanel",
    ]:
        require(
            legacy_panel not in app_text,
            f"P021-I6: App must not retain command-plane governance panel owner implementation: {legacy_panel}",
        )
    for helper in [
        "export interface FixtureSelectionState",
        "export function useFixtureSelection",
    ]:
        require(
            helper in fixture_selection_text,
            f"P021-I4: fixture-selection.ts must declare canonical fixture selection contract helper {helper}",
        )
    require(
        "export type AccountHealthFixtureId" in fixture_registry_text,
        "P021-I4: fixture-registry.ts must carry the canonical health fixture type owner",
    )
    for helper in [
        "function classifyAppRoute",
        "function resolveAccountWorkbenchView",
        "function isMirrorWorkbenchEligibleRoute",
    ]:
        require(
            helper in account_workbench_routing_text and helper not in app_text,
            f"P021-I4: account-workbench-routing.ts must own extracted workbench route helper {helper}",
        )
    for helper in [
        "function blockerSeverity",
        "function mirrorBlockers",
        "function mirrorEvidenceRefs",
        "function mirrorContext",
        "function mirrorBoundaries",
        "function mirrorWorkbenchProjection",
        "function mirrorSummaryReadModel",
        "function mirrorPositionsReadModel",
        "function mirrorOrdersReadModel",
    ]:
        require(
            helper in account_workbench_adapters_text and helper not in app_text,
            f"P021-I4: account-workbench-adapters.ts must own extracted mirror adapter helper {helper}",
        )
    for helper in [
        "export function resolveMirrorRouteAccountId",
        "export const mirrorRouteAliases",
    ]:
        require(
            helper in mirror_route_owner_text and helper not in app_text,
            f"P021-I4: mirror-route-owner.ts must own extracted mirror route helper {helper}",
        )
    for branch in [
        'fixture={mirrorProjection?.orderDetail ?? accountOrderDetailFixture}',
        'fixture={mirrorProjection?.orders ?? accountOrdersFixture}',
        'fixture={mirrorProjection?.positions ?? accountPositionsFixture}',
        'fixture={mirrorProjection?.settlement ?? accountSettlementFixture}',
        'fixture={mirrorProjection?.equity ?? accountEquityFixture}',
        'fixture={mirrorProjection?.reconcile ?? accountReconcileFixture}',
        'fixture={mirrorProjection?.incidents ?? accountIncidentsFixture}',
        'fixture={mirrorProjection?.evidence ?? accountEvidenceFixture}',
    ]:
        require(
            branch in app_text,
            f"P021-I4: mirror-eligible account workbench routes must render through unified projection branch {branch}",
        )
    for helper in [
        "function formatMoney",
        "function numberTone",
    ]:
        require(
            helper in account_workbench_terminal_text and helper not in app_text,
            f"P021-I4: account-workbench-terminal.tsx must own extracted helper {helper}",
        )
    for helper in [
        "function formatMaybeValue",
        "function ReconcileItemCard",
        "function IncidentRowCard",
        "function EvidencePackageCard",
    ]:
        require(
            helper in account_workbench_text and helper not in app_text,
            f"P021-I4: account-workbench-panels.tsx must own extracted helper {helper}",
        )
    for helper in [
        "function SourceRefsList",
        "function RejectionRuleList",
        "function accountBoundaryRows",
        "function BlockerList",
        "function Ref",
        "function Metric",
    ]:
        require(
            helper in panel_shared_text and helper not in app_text,
            f"P021-I4: panel-shared.tsx must own cross-domain helper {helper}",
        )
    for helper in ["function AccountDetail", "function SelectFilter"]:
        require(
            helper in account_health_text and helper not in app_text,
            f"P021-I4: account-health-panels.tsx must own extracted helper {helper}",
        )
    for helper in [
        "function formatLag",
        "function IntradayExceptionCard",
        "function IntradayStreamCard",
        "function IntradayIncidentCard",
    ]:
        require(
            helper in intraday_monitor_text and helper not in app_text,
            f"P021-I4: intraday-monitor-panels.tsx must own extracted helper {helper}",
        )
    require(
        "status === \"fulfilled\"" not in app_text and "not scheduled by command-plane retirement registry" not in app_text,
        "P021-I6: App must not interpret settled-result retirement semantics directly",
    )
    require(
        "const [runtimeReadiness, setRuntimeReadiness]" not in app_text
        and "const [runtimeApprovalPacket, setRuntimeApprovalPacket]" not in app_text
        and "const [partialFillOwnerRepairPlan, setPartialFillOwnerRepairPlan]" not in app_text,
        "P021-I6: App must not own per-panel legacy governance state as scattered hooks",
    )
    for helper in [
        "function mirrorExecutionReportRows",
        "function isP024PaperArmed",
        "function defaultSubmitIntent",
        "function cancelIntentForOrder",
        "const isAccountWorkbenchRoute = currentPath.startsWith(\"/accounts/\")",
        "const isAccountOrderDetailRoute =",
        "const isAccountOrdersRoute =",
        "const isAccountPositionsRoute =",
        "const isAccountSettlementRoute =",
        "const isAccountEquityRoute =",
        "const isAccountReconcileRoute =",
        "const isAccountIncidentsRoute =",
        "const isAccountEvidenceRoute =",
    ]:
        require(
            helper not in app_text,
            f"P021-I4: App must not retain terminal adapter/control helper implementation: {helper}",
        )
    for helper in [
        "const [fixtureState, setFixtureState]",
        "const [accountSummaryFixtureState, setAccountSummaryFixtureState]",
        "const [accountOrdersFixtureState, setAccountOrdersFixtureState]",
        "const [accountOrderDetailFixtureState, setAccountOrderDetailFixtureState]",
        "const [accountPositionsFixtureState, setAccountPositionsFixtureState]",
        "const [accountSettlementFixtureState, setAccountSettlementFixtureState]",
        "const [accountEquityFixtureState, setAccountEquityFixtureState]",
        "const [accountReconcileFixtureState, setAccountReconcileFixtureState]",
        "const [accountIncidentsFixtureState, setAccountIncidentsFixtureState]",
        "const [accountEvidenceFixtureState, setAccountEvidenceFixtureState]",
        "const [intradayMonitorFixtureState, setIntradayMonitorFixtureState]",
        "const fixture = healthFixtureMap[fixtureState]",
        "const accountSummaryFixture = accountSummaryFixtureMap[accountSummaryFixtureState]",
        "const accountOrdersFixture = accountOrdersFixtureMap[accountOrdersFixtureState]",
        "const accountOrderDetailFixture = accountOrderDetailFixtureMap[accountOrderDetailFixtureState]",
        "const accountPositionsFixture = accountPositionsFixtureMap[accountPositionsFixtureState]",
        "const accountSettlementFixture = accountSettlementFixtureMap[accountSettlementFixtureState]",
        "const accountEquityFixture = accountEquityFixtureMap[accountEquityFixtureState]",
        "const accountReconcileFixture = accountReconcileFixtureMap[accountReconcileFixtureState]",
        "const accountIncidentsFixture = accountIncidentsFixtureMap[accountIncidentsFixtureState]",
        "const accountEvidenceFixture = accountEvidenceFixtureMap[accountEvidenceFixtureState]",
        "const intradayMonitorFixture = intradayMonitorFixtureMap[intradayMonitorFixtureState]",
    ]:
        require(
            helper not in app_text,
            f"P021-I4: App must not retain fixture selection implementation: {helper}",
        )
    for helper in [
        "const workbenchFallback = fixtures.accountWorkbench",
        "const showWorkbenchFixtureSelectors = !mirrorProjection;",
    ]:
        require(
            helper in app_text,
            f"P021-I4: App must consume converged workbench fallback owner helper {helper}",
        )
    forbidden_inline_calls = [
        "fetchCommandRuntimeCloseout(summary.account.account_id)",
        "fetchCommandRuntimeInvocationReadiness(summary.account.account_id)",
        "fetchCommandRuntimeExecutionApprovalPacket(summary.account.account_id)",
        "fetchCommandRuntimeExecutionHandoffBundle(summary.account.account_id)",
        "fetchCommandPartialFillRuntimeExecutionApprovalPacket(summary.account.account_id)",
        "fetchCommandPartialFillRuntimeExecutionHandoffBundle(summary.account.account_id)",
        "fetchCommandRuntimeExecutionGapAudit(summary.account.account_id)",
    ]
    offenders = [call for call in forbidden_inline_calls if call in app_text]
    require(
        not offenders,
        f"P021-I6: App must not scatter legacy command read calls outside centralized suite: {offenders}",
    )


def validate_p021_docs_closed() -> None:
    proposal = ROOT / "docs" / "proposals" / "p021-account-console-owner-fork-governance"
    for name in ["README.md", "phase-plan.md", "acceptance.md", "issue-list.md"]:
        require((proposal / name).exists(), f"P021 docs missing {name}")
    issue_text = read(proposal / "issue-list.md")
    require("Status | `closed`" in issue_text or "Status | `accepted_with_guardrails`" in issue_text, "P021 issues must include closed or guarded rows")
    require("Status | `open`" not in issue_text, "P021 issue-list must not retain open issues at closeout")
    require(issue_text.count("### P021-I") >= 6, "P021 issue-list must carry forward all six current owner/fork issues")
    readme_text = read(proposal / "README.md")
    phase_text = read(proposal / "phase-plan.md")
    acceptance_text = read(proposal / "acceptance.md")
    for text, label in [
        (readme_text, "README"),
        (phase_text, "phase plan"),
        (acceptance_text, "acceptance"),
    ]:
        require("P021-I5" in text, f"P021 {label} must include I5")
        require("P021-I6" in text, f"P021 {label} must include I6")
    require("six concrete risk lanes" in readme_text, "P021 README must describe six risk lanes")
    require("Phase 5" in phase_text and "Phase 6" in phase_text, "P021 phase plan must include Phase 5 and Phase 6")
    require("A8" in acceptance_text and "A9" in acceptance_text, "P021 acceptance must add scenarios for I5/I6")


def main() -> int:
    validate_route_context_owner()
    validate_source_package_boundary()
    validate_synthetic_test_boundary()
    validate_frontend_registry_boundary()
    validate_backend_command_plane_owner_split()
    validate_frontend_legacy_command_read_entrypoint()
    validate_p021_docs_closed()
    print("P021_OWNER_FORK_GOVERNANCE_OK: issues=6 route_context=canonical synthetic=guarded registry=single_owner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
