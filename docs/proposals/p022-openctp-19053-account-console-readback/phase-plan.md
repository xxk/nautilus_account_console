# P022 Phase Plan / OpenCTP 19053

- Proposal ID: `p022-openctp-19053-account-console-readback`
- Status: implementation_gate_passed
- Updated: 2026-06-20

| Phase | Goal | Evidence | Status |
| --- | --- | --- | --- |
| Phase 0 | ADR-0005 alignment | Proposal docs and no-command boundary | completed |
| Phase 1 | Owner artifact ingestion | `build_ctp19053_source_package_from_real_login.py --owner-session-label ...` | completed |
| Phase 2 | Account Mirror projection | `validate_ctp19053_consistency.py`, `validate_account_mirror_api.py` | completed |
| Phase 3 | UI readback | `ctp19053-ui-funds-positions.spec.ts` | completed |
| Phase 4 | Closeout gates | `validate_p022_openctp_19053_readback.py`, build, pytest, Playwright | completed |

## Acceptance Exit

P022 can close only when:

1. funds render from numeric owner account query values;
2. positions render from owner readonly snapshot records;
3. open orders render as rows or a typed empty state from owner order evidence;
4. command capability remains disabled;
5. raw secrets and raw broker endpoint values are absent from Account Console artifacts;
6. proposal docs and validators pass.
