# NEXT_STEPS

## Актуални стъпки (2026-11-18 17:34)
1. Потвърди в GitHub UI: callback `http://127.0.0.1:8000/auth/callback`, wildcard callback matching изключен, user-to-server token expiration Opt-out и инсталация върху акаунта/организацията с fork-овете.
2. Потвърди продукционния/proxy access log redaction за callback `code`/`state`; за TLS terminating proxy задай `COOKIE_SECURE=true` или `--proxy-headers`.
3. С валидна OAuth сесия направи само read-only preview проверка; не стартирай реален Sync без изрично одобрение.
4. Commit/push само след изрично одобрение. Преди това повтори пълния pytest, `node --check` за трите JS файла, `scripts/check.ps1` и `git diff --check`.
5. Отделни задачи при публично exposure: CSRF token, shared session store за повече workers, refresh-token support само ако expiration не може да се изключи.

## Предходни стъпки (2026-11-18 04:02)
1. Потвърди в GitHub UI: callback `http://127.0.0.1:8000/auth/callback`, wildcard callback matching изключен, user-to-server token expiration opt-out и инсталация върху акаунта с fork-овете.
2. Ротирай ръчно `GITHUB_TOKEN` и `GITHUB_APP_CLIENT_SECRET` в `.env` (и GitHub App client secret), без отпечатване, копиране или commit на стойности.
3. С валидна OAuth сесия направи само read-only preview проверка; не стартирай реален Sync без изрично одобрение.
4. След одобрение направи commit/push; тестовете вече са изпълнени в локалния `.venv`, но `git diff --check` трябва да се повтори ако има нови промени.
5. Отделни задачи: shared session store, CSRF token, refresh-token support и изясняване на desktop разположението на repo статусните badges.

## Предходни стъпки (2026-11-17 21:36)
1. Ръчна проверка в браузър с валидна OAuth сесия: потвърди `GabrielRules`, малък кръгъл GitHub аватар (`40px` desktop / `36px` mobile), green indicator, `Sign out` без `Sign in`, `SYNC ALL` като единствен бутон без вторичен текст, `Restoring session...` само в status зоната, Disabled tooltip/sheen и гравиран 3D текст без натиснат вид на бутона.
2. Потвърди реалните броячи след успешна проверка: `36 / 34 / 0 / 2`; при неуспешни проверки очаквай `CHECK FAILED / UNVERIFIED` и задържане на крайните числа, не погрешно `34 UNSYNCABLE`. Не стартирай реален Sync по време на тази проверка.
3. В GitHub App settings задай точно `http://127.0.0.1:8000/auth/callback`, изключи wildcard callback matching, потвърди user-to-server token expiration opt-out и инсталацията върху акаунта/организацията с fork-овете.
4. При валидна сесия изпълни smoke test: login → preview на тестов fork → sync само на fork със статус `to be synced` и потвърден диалог → logout → `.\scripts\stop-smoke.ps1`. Не променяй selection/safety логиката.
5. Преди commit/push изпълни `python -m pytest -q`, `node --check web/app.js`, `scripts/check.ps1` и targeted `git diff --check`; commit/push само след изрично одобрение.
6. Отделни последващи задачи: callback access log redaction (без token/code/state), refresh-token support ако expiration не може да се изключи, shared session store за повече workers, CSRF токен при публично exposure и подмяна на остарелия `httpx`/`starlette.testclient` warning.

## Исторически стъпки от 2026-11-15 (запазени, не са актуални)

## Приоритет 1 - Реален GitHub smoke test с loopback callback
- Първо провери в GitHub App settings дали user-to-server token expiration е **Opt-out**; при включен expiration очакваният резултат е Broker `502`, защото `auth_broker/token_policy.py` отхвърля `expires_in`/`refresh_token`.
- Ако expiration е Opt-out и 502 продължава, добави безопасно логване на типа/съобщението на token exchange изключението (без token/code/secret) и повторѝ login-а.
- В GitHub App settings задай точно `http://127.0.0.1:8000/auth/callback` и изключи wildcard callback matching.
- Увери се, че GitHub App е инсталиран на акаунта/организацията, която притежава fork-овете.
- Smoke услугите вече са стартирани (Broker PID 22792, dashboard PID 23492, watchdog PID 22048); при нужда рестартирай с `.\scripts\start-smoke.ps1 -Watchdog -Force`.
- Отвори `http://127.0.0.1:8001`, влез с GitHub, направи preview на тестов fork, sync на fork със статус `behind` и logout.
- Спри услугите с `.\scripts\stop-smoke.ps1`.
- Ако login върне `redirect_uri_mismatch`, callback-ът в GitHub App не съвпада; ако Broker върне `502`, провери дали token expiration е изключен.

## Приоритет 1.5 - Сигурност на логовете
- Uvicorn access log-ът записва пълния `/auth/callback` query string с OAuth code/state; добави redaction или изключи access log за този endpoint, без да логваш token/code/state.

## Приоритет 2 - Commit и CI
- Пълният suite тогава е бил `364 passed, 1 warning`; `node --check web/app.js` и PowerShell parser check минават.
- Commit-ни loopback промените, тестовете, скриптовете и документацията само след изрично одобрение.
- След push провери Windows и Ubuntu CI job-овете, включително `scripts/check.ps1`.

## Приоритет 3 - След успешен реален login
- Ако GitHub token expiration не може да се изключи, добави refresh-token support в Broker и CLI; това е отделна промяна.
- За отдалечен достъп използвай стабилен named HTTPS tunnel/proxy и HTTPS callback; не използвай Quick Tunnel за регистриран callback.
- Ако dashboard-ът ще се пуска с повече от един worker, добави shared session store.
- При публично exposure добави CSRF token; v1 разчита на `SameSite=Lax` и POST-only.
- Вече изпълнено: `httpx2==2.16.0` е инсталиран и проверен с `pip check`.
