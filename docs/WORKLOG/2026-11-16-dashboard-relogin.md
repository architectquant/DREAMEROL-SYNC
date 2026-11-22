# Dashboard fix after re-login — 2026-11-16

## Changes
- DASHBOARD/app.js: added robust session restoration/init flow (initDashboard, esetDashboardState, loading/initialized guards), automatic repository preview reload on every successful authenticated session restore/login (preview({auto:true})), history rendering/reset, avatar/state cleanup, and pageshow re-init for persisted/bfcache returns. Sign out now clears dashboard state before redirect.

## Verified
- 
ode --check DASHBOARD/app.js: OK.
- python -m pytest tests/test_api.py tests/test_web_auth.py -q: **32 passed, 1 warning** (auth status/logout/session-token and sync API flows; confirms backend session clear + re-auth paths remain functional).

## Repeated Sign out → Sign in cycles
- **Automated:** backend auth/logout/status and session-based sync flows covered by existing tests (passed); frontend init logic now re-runs auth check + auto-preview on each dashboard load/restore. 
- **Manual/browser:** not executed in this environment (requires running dashboard with valid GitHub OAuth and real UI cycles). Needs live verification: perform repeated Sign out → Sign in and confirm account, repositories, synchronization results, and history repopulate each time.

## Notes
- History/results are in-session UI state (not persisted server-side); after each successful login/session restore repositories are auto-reloaded and a history entry is recorded. No security checks weakened.
