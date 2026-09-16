# Lightweight Threat Model

| Risk | Example | Demo control | Production consideration |
|---|---|---|---|
| Accidental data disclosure | User pastes a password | Pattern scanner + BLOCK | Enterprise DLP and secret scanning |
| Shadow AI | User selects an unapproved tool | Approved-tool policy | CASB/SSE, DNS/proxy controls, procurement governance |
| Excess privilege | Agent receives unnecessary access | Policy guidance | OAuth scopes, RBAC/ABAC, short-lived credentials |
| Unsafe autonomous action | Agent sends/deletes/updates | REVIEW concept | Transaction approval, action allowlists, rollback |
| Weak traceability | No record of why access was allowed | Audit metadata | Central immutable logs + SIEM |
| False confidence | Scanner misses sensitive content | Explicit starter-kit limitation | Layered detection, classification labels, security review |

This document is a teaching aid, not a complete threat model for a specific organization.
