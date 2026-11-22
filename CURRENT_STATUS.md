# CURRENT_STATUS

## Актуално състояние (2026-11-18 18:23)
- **Клон/HEAD:** `feature/github-app-auth @ b15c9a7`, проверено чрез `git status` и `git rev-parse --short HEAD`. Локалният commit `Finalize sync action styling and release documentation` е направен; push няма, клонът е `ahead 16`.
- **Последна завършена задача:** Реален GitHub OAuth login и read-only Sync preview smoke test. Потвърдени са `/auth/start` → `/auth/callback` 303 → `/auth/poll` 200 → `/auth/ack` 200 и `/api/auth/status` 200 със `state: AUTHENTICATED`. Preview: `36 / 36` (`34` UP TO DATE, `0` READY TO SYNC, `2` UNSYNCABLE, `0` check failures), без промяна на репозитории. Commit `b15c9a7` е създаден.
- **Запазване:** Няма кодови промени в auth/OAuth, API, backend, sync логика или counters. Няма мутиращ Sync, credential rotation, смяна на GitHub App настройки или push. Credentials, token, `code`, `state` и account не са извеждани. След commit са променени само 3 документа: `CURRENT_STATUS.md`, `docs/WORKLOG/WORKLOG.md`, `docs/WORKLOG/LOG_18-11-26.md`.
- **Тестове:** `.\.venv\Scripts\python.exe -m pytest -q` → `457 passed in 6.13s`; `scripts/check.ps1` → `All checks passed` и pytest `457 passed, 1 warning` (StarletteDeprecationWarning); `compileall`, `node --check` за `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `web/app.js`, PowerShell Parser и `pip check` → OK; `git diff --check` → exit 0, само LF→CRLF предупреждения. Реален OAuth smoke потвърден: callback 303, poll/ack/status 200; 0 secret-like записа в логовете. Preview `36/36`, `34` UP TO DATE, `0` READY TO SYNC, `2` UNSYNCABLE, `0` check failures; `sync-progress` и `sync-summary` скрити. Callback `code`/`state` са `[REDACTED]` в логовете. CDP desktop/mobile без overflow.
- **Ограничения / release blockers:** Живият OAuth/callback и read-only preview са потвърдени, включително redaction в smoke логовете. Остават: GitHub App UI проверка за callback/wildcard, permissions/installation и token expiration Opt-out; `Secure` cookie зад TLS proxy (`COOKIE_SECURE=true` или `--proxy-headers`); отделен CSRF token; in-memory сесии/транзакции; потвърждение на продукционния logger redaction извън smoke стека. Мутиращ Sync не е тестван по избрания read-only обхват.
- **Следваща стъпка:** потвърждаване в GitHub App UI на callback/wildcard, permissions/installation, token expiration Opt-out и продукционния logger redaction; по одобрение – CSRF/`Secure` cookie и по-ясно `dry_run` логиране; мутиращ Sync само с disposable fork и ново одобрение; push не се прави без изрично одобрение.

## Предходно състояние (2026-11-18 04:02)
- **Клон/HEAD:** `feature/github-app-auth @ 629afbb`, проверено чрез `git status` и `git rev-parse`. Няма commit или push.
- **Последна завършена задача:** Phase 6 release readiness корекции: `LICENSE` е стандартен MIT; премахнати са не-мит лицензионният текст и неподкрепеното твърдение за собственост в `COPYRIGHT.md`; минималната поддържана версия е Python 3.11; CI matrix-ът проверява 3.11 и 3.12, а environment проверката изисква >=3.11; CI проверява `web/app.js`, `DASHBOARD/app.js` и `DASHBOARD/utils.js`; премахнати са подвеждащите PAT fallback инструкции за браузъра.
- **Запазване:** Всички съществуващи tracked/untracked промени са непокътнати; `.env` не е променян или commit-ван; локалният `.venv` е игнориран от Git.
- **Зависимости:** Създаден е локален `.venv` без глобални инсталации; `httpx2==2.16.0` е инсталиран и проверен; `pip check` → `No broken requirements found`.
- **Тестове:** `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` → `453 passed in 5.40s` (тогава записано без warnings; по-късно в този файл е отбелязан `StarletteDeprecationWarning`); tokenize-aware Python compile на 39 файла → OK; `node --check` за трите JS файла → OK; PowerShell parse → OK; `git diff --check` → само LF→CRLF предупреждения, без whitespace грешки.
- **Ограничения:** Няма валидна OAuth сесия; реален callback/permissions/installation, реален Sync, in-memory сесии, липсващ CSRF token и token expiration остават непотвърдени или нерешени. Credentials в `.env` изискват ръчна ротация на `GITHUB_TOKEN` и `GITHUB_APP_CLIENT_SECRET`; стойностите не са показвани.
- **Следваща стъпка:** Потвърждение на GitHub App настройки и валидна OAuth сесия; commit/push само след изрично одобрение; без реален Sync без одобрение.

## Актуално състояние (2026-11-17 21:36)
- **Клон/HEAD:** `feature/github-app-auth @ 629afbb`, проверено преди тази промяна. Няма commit или push.
- **Последна завършена задача:** Финална visual polish на `SYNC ALL` бутона само в CSS: по-ярък наситен emerald gradient (`#3BEE7E → #16D46A → #079447`) с фина green glow, по-голям bold white текст (`22px` desktop / `20px` mobile), по-голям SYNC икон (`28px` / `24px`), леко по-широк бутон (`560px` desktop / `328px` налична ширина mobile) и запазен гравиран 3D ефект.
- **Запазване на логиката:** Няма промени в HTML, JS, authentication, OAuth, API, counters, repository classification, confirmation, safety checks или synchronization поведение. Hero artwork и account navigation не са променяни.
- **Проверки:** CDP desktop 1440×1200 и mobile 390×844: `verify-final-button-cleanup.cjs` и `verify-premium-button-states.cjs` → всички checks `true`, включително `largerLettering`, `largerIcon`, `brighterBorder`, `emeraldGradient`, `greenGlow`, `disabledNotPale`, `greenPreserved`, `raisedWhenDisabled`, `checkingSheen`, `tooltipVisible` и `engravedTextDisabled`. `verify-final-nav-button.cjs` и `verify-avatar-size.cjs` → `true`. `node --check DASHBOARD/app.js`, `node --check DASHBOARD/utils.js`, targeted `git diff --check -- DASHBOARD/dashboard.css` → OK. `python -m pytest -q tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `35 passed`.
- **Ограничения:** Няма валидна OAuth сесия; реален avatar URL, авторизиран payload, реални counters и реален Sync остават непотвърдени. Пълният pytest suite и `scripts/check.ps1` не са повторени след тази CSS-only промяна.

## Предишно състояние (2026-11-17 21:29)
- **Клон/HEAD:** `feature/github-app-auth @ 629afbb`, проверено чрез `git status` и `git rev-parse`. Няма commit или push.
- **Последна завършена задача:** Завършена е серия presentation-only refinement-а на `DASHBOARD`: тънка горна лента, компактен акаунт панел, малък кръгъл GitHub аватар (`40px` desktop / `36px` mobile), единствено `SYNC ALL` в основния бутон, преместен статус извън бутона, подобрено disabled състояние с tooltip/sheen и гравиран 3D текст.
- **Запазване на работата:** Прегледани са `git status --short --untracked-files=all`. Всички 27 променени tracked файла, 2 изтрити root `LOG_13-11-26.md`/`LOG_14-11-26.md` и 24 untracked файла са оставени непокътнати. Копията на двата лога съществуват в `docs/WORKLOG/`; не е извършено възстановяване, изчистване, stash, reset или checkout.
- **Запазена логика:** Няма промени в authentication, OAuth, Auth Broker, API contract, synchronization scope, repository selection, confirmation dialog, safety checks, counters classification или hero artwork. Реален Sync не е извършван.
- **Последни реални проверки:** `python -m pytest -q` → `428 passed, 1 warning` (2026-11-17 20:30, преди последните presentation-only стъпки). След тях: targeted `python -m pytest -q tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `35 passed` (21:22); CDP headless проверки при 1440×1200 и 390×844 за button enabled/disabled, tooltip/sheen, engraved text, avatar size/alignment, top strip, hero и layout → всички проверки `true`; `node --check DASHBOARD/app.js`, `node --check DASHBOARD/utils.js` и targeted `git diff --check -- DASHBOARD/index.html DASHBOARD/dashboard.css` → OK.
- **Известни ограничения:** Няма валидна OAuth сесия: `/api/auth/status` връща 401, затова реалният avatar URL, авторизираният GabrielRules payload и реалните `36 / 34 / 0 / 2` числа не са потвърдени в браузър. Реален GitHub login/callback, preview и sync не са изпълнени в тази сесия.
- **Отстоящи въпроси:** GitHub App настройките (callback `http://127.0.0.1:8000/auth/callback`, wildcard off, token expiration opt-out, installation) остават за потвърждение. Uvicorn access log-ът за `/auth/callback` все още може да записва OAuth code/state. Пълният pytest suite и `scripts/check.ps1` не са повторени след последните presentation-only промени.

## Следващи стъпки от състоянието на 2026-11-18 04:02 (запазено)
1. Ръчна браузърна проверка с валидна OAuth сесия: малък кръгъл avatar, подравняване с username/`Sign out`, `SYNC ALL` без вторичен текст, disabled tooltip/sheen, гравиран текст, `Restoring session...` в status зоната и реални fork counters.
2. Потвърди GitHub App settings: точен loopback callback, wildcard callback изключен, user-to-server token expiration opt-out и инсталация върху акаунта/организацията с fork-овете.
3. Изпълни реален smoke test: login → preview на тестов fork → sync само на fork със статус `to be synced` → logout; след това спри услугите.
4. Преди всякакъв commit: `python -m pytest -q`, `node --check web/app.js`, `node --check DASHBOARD/app.js`, `node --check DASHBOARD/utils.js`, `scripts/check.ps1` и targeted `git diff --check`; едва след изрично одобрение commit/push.
5. Отделни последващи задачи: redaction на OAuth callback access log, refresh-token support ако expiration не може да се изключи, shared session store за повече workers и CSRF токен при публично exposure.

## Историческо състояние от 2026-11-15 (запазено, не е актуално)
- 2026-11-15 03:24: GitHub App callback-ът е преминат от ephemeral Quick Tunnel към фиксиран локален loopback `http://127.0.0.1:8000/auth/callback`; Broker и dashboard слушат само на `127.0.0.1`, а smoke скриптовете вече не стартират cloudflared.
- Преди това: mock GitHub OAuth E2E тестове, Broker `/healthz` и watchdog (2026-11-14 04:26).

## Историческо състояние от 2026-11-15 (запазено, не е актуално)
- Клон: `feature/github-app-auth`; последни commit-и: `23f1226`, `fa4a135`, `629afbb`.
- `BROKER_CALLBACK_URL` в `.env` е `http://127.0.0.1:8000/auth/callback`; GitHub App credentials са непразни и не са очевидни placeholder стойности, но не са отпечатвани.
- `auth_broker/config.py` допуска HTTPS навсякъде и HTTP само за loopback hosts (`127.0.0.1`, `::1`, `localhost`); публичен HTTP, LAN IP, `0.0.0.0`, wildcard, query, fragment и userinfo се отхвърлят.
- `.env.example` и документацията описват loopback callback-а; wildcard callback matching трябва да е изключен.
- `scripts/start-smoke.ps1` стартира Broker на `127.0.0.1:8000` и dashboard на `127.0.0.1:8001`, чака `/healthz`, проверява dashboard-а и не стартира/не пренаписва тунел.
- `scripts/watch-smoke.ps1` рестартира Broker или dashboard на loopback портовете; `scripts/stop-smoke.ps1` спира watchdog-а, dashboard-а и Broker-а. Няма cloudflared зависимост.
- `python -m pytest -q -p no:cacheprovider`: `364 passed, 1 warning` (2026-11-15 03:19).
- `node --check web/app.js`: успешен.
- `scripts/check.ps1`: `All checks passed`.
- PowerShell parser check: всички скриптове са синтактично валидни.
- Smoke lifecycle: старт без watchdog → `/healthz` 200, dashboard 200, `/auth/callback` без state 400; старт с watchdog → kill на Broker → автоматичен рестарт с нов PID; `stop-smoke.ps1` спря всички процеси и изчисти state файла.
- Текущо (2026-11-15 03:52): smoke услугите са стартирани — Broker PID 22792, dashboard PID 23492, watchdog PID 22048; `watch-smoke.ps1 -Once` ги отчита като здрави. `scripts/check.ps1` мина с `364 passed, 1 warning` и `All checks passed`.
- Dashboard `/api/auth/start` генерира GitHub authorization URL с `redirect_uri=http://127.0.0.1:8000/auth/callback`; това съвпада с `BROKER_CALLBACK_URL`. GitHub authorize endpoint не валидира callback-а преди login (правилен и грешен callback връщат еднакъв `302` към login), затова GitHub App настройката остава за потвърждение при реален sign-in.
- Реален callback на 2026-11-15 04:00 е получил code/state, но Broker е върнал `502 Bad Gateway` от token exchange. Контролен token request с dummy code върна `bad_verification_code`, т.е. client credentials и redirect URI се приемат; точната причина за 502 е скрита от широкия `except Exception` в callback handler-а. Най-вероятна причина: включен user-to-server token expiration, при който GitHub връща `expires_in`/`refresh_token`, а `auth_broker/token_policy.py` ги отхвърля.
- Broker връща `Cache-Control: no-store`, `Pragma: no-cache`, `Referrer-Policy: no-referrer` и `X-Content-Type-Options: nosniff` за `/auth/` отговорите.
- Mock OAuth E2E тестовете вече използват loopback callback и покриват success, `access_denied` и token exchange failure.

## Исторически незавършени промени (2026-11-15; виж актуалния checkpoint по-горе)
- Промените по `auth_broker/config.py`, тестовете, `.env`, скриптовете и документацията са неcommit-нати.
- Не е извършен реален GitHub login след смяната на callback-а.
- GitHub App настройките (callback, wildcard, token expiration, installation) не могат да се проверят от repository-то.

## Исторически известни грешки (2026-11-15; част от тях са актуални – виж checkpoint-а по-горе)
- Има един `StarletteDeprecationWarning` за `httpx`/`starlette.testclient`; тестовете минават.
- Сесиите са в паметта на един процес и не се споделят между workers.
- GitHub user-to-server tokens изтичат по подразбиране; `auth_broker/token_policy.py` отхвърля отговори с `expires_in`/`refresh_token`. Ако expiration не е opted out, реален login ще върне Broker `502`.
- Ако GitHub App callback-ът не е точно loopback URL-ът, login ще върне `redirect_uri_mismatch`.
- Исторически Broker access log-ът записваше пълния `/auth/callback` query string, включително OAuth code/state; в текущия код `auth_broker/app.py` добавя redaction за `uvicorn.access`, но продукционният/proxy logger трябва да се потвърди отделно.
- Няма поддръжка за отдалечен достъп; за него е нужен стабилен named HTTPS tunnel/proxy.

## Историческа следваща стъпка (2026-11-15)
1. В GitHub App settings задай callback `http://127.0.0.1:8000/auth/callback`, изключи wildcard callback matching и потвърди/opt-out на user-to-server token expiration.
2. Увери се, че GitHub App е инсталиран на акаунта/организацията, която притежава fork-овете.
3. Пусни `.\scripts\start-smoke.ps1 -Watchdog` и отвори `http://127.0.0.1:8001`.
4. Изпълни реален login, preview на тестов fork, sync на fork със статус `behind` и logout.
5. Спри услугите с `.\scripts\stop-smoke.ps1`; при успех commit-ни промените след изрично одобрение.
