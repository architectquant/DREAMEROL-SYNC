# AI Development Changelog

## 2026-11-21 21:38 - Подредба по състояние в Dashboard

- **Извършена задача:** Добавена е постоянна подредба на репозиторитите: `READY TO SYNC` → `UP TO DATE` → `UNSYNCABLE/непроверени`, като в рамките на групата се пази първоначалният ред. След Sync репото автоматично слиза при `UP TO DATE`, ако новата проверка потвърди това състояние.
- **Променени файлове:** `DASHBOARD/utils.js`, `DASHBOARD/app.js`, `DASHBOARD/index.html`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** След успешния Sync `GabrielRules/TEST2` остана на първа позиция, а останалите `READY TO SYNC` редове бяха след него; потребителят поиска групиране по състояние.
- **Изпълнени тестове:** `node --check DASHBOARD\app.js`; `node --check DASHBOARD\utils.js`; `python -m pytest -q -p no:cacheprovider`; едно одобрено презареждане на съществуващия Dashboard таб с CDP проверка на реда, scripts, write заявки и JS грешки.
- **Резултат:** `501 passed, 1 warning in 6.05s`. Живо: 3 `READY TO SYNC`, после 34 `UP TO DATE`, после 2 `UNSYNCABLE`; `app.js?v=20261121h`, `utils.js?v=20261121d`, URL `/dashboard`, `dry_run:false` заявки `[]`, JS грешки `[]`. Backup: `%TEMP%\opencode\repo-order-backup-20261121-2132`. Няма commit или push.
- **Оставащи проблеми:** При refresh броячите започват от `0/0/0/0` и се попълват след проверката — очаквано поведение при пълен reload. След refresh `GabrielRules/TEST2` е отново `READY TO SYNC`, защото прясна `dry_run` проверка връща `behind_by:1`, въпреки че Sync операцията от 21:29 е записана с `success:1`. Причината не е доказана; нужен е отделен read-only анализ, без нов Sync без одобрение.

## 2026-11-21 21:29 - Реален Sync на GabrielRules/TEST2

- **Извършена задача:** След изрично одобрение от потребителя е изпълнен реален Sync само на `GabrielRules/TEST2`. Първоначалната проверка спря, защото в избора имаше и `GabrielRules/TEST3`; то беше премахнато само от UI след допълнително потвърждение. Код не е променян в тази стъпка.
- **Променени файлове:** `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Завършена е подготовката от 21:24 (валидна сесия, стабилен Dashboard, успешен preflight за 1 репо) и потребителят изрично потвърди реален Sync.
- **Изпълнени тестове:** CDP проверка на съществуващия Dashboard таб без reload; `/api/auth/status`; `SYNC CHOSEN` с потвърден диалог; `/api/history`; проверка на DOM статуса, броячите и записаните заявки.
- **Резултат:** Едно `{"dry_run":true,"repositories":["GabrielRules/TEST2"]}`, едно `{"dry_run":false,"confirmation":"SYNC","repositories":["GabrielRules/TEST2"]}` и `GET /api/history`. Статус `SYNC CHOSEN: 1 synchronized, 0 skipped, 0 failed, 0 need attention. Background checks continue.`; `stat-*`/`summary*` = `39/35/2/2`; `TEST2` е `UP TO DATE (0 ahead, 0 behind) - Synced 2 upstream commits.` с `Last successful sync 21/11/2026, 21:29:36`. История: операция `99d31057-d500-4c95-a03b-3b5859c81b97`, `created_at 2026-11-21T19:29:36Z`, `success:1`. URL остана `/dashboard`, JS грешки `[]`, изборът е изчистен. Няма commit, push или допълнителни GitHub writes.
- **Оставащи проблеми:** Очаква се визуална проверка от потребителя и евентуален reload, за да се потвърди запазването на `39/35/2/2` и историята. Без нов Sync без отделно одобрение.

## 2026-11-21 21:24 - Успешен preflight за 1 репозитори преди реален Sync

- **Извършена задача:** След одобрение е увеличен само timeout-ът на `preflightSelected()` до `PREFLIGHT_TIMEOUT_MS = 30000`; batch проверките остават на `CHECK_TIMEOUT_MS = 8000`. Проверени са git diff/статус, пълният test suite, валидността на сесията, изборът на точно едно `READY TO SYNC` репо и preflightът за `GabrielRules/TEST2`.
- **Променени файлове:** `DASHBOARD/app.js`, `DASHBOARD/index.html`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Първоначалният preflight за 1 репо връщаше HTTP `200` за около 16.8s, но 8-секундният checking timeout го прекратяваше с `Could not reach the server.`; това блокираше безопасното потвърждение преди Sync.
- **Изпълнени тестове:** `node --check DASHBOARD\app.js`; `python -m pytest -q -p no:cacheprovider`; `git status --short`; `git diff --stat`; `git diff --check` за кодовите файлове; жива CDP проверка на съществуващия Dashboard таб без нови reload-и; `SYNC CHOSEN` с прехванат `window.confirm → false`.
- **Резултат:** `node --check` OK; `500 passed, 1 warning in 7.73s`. Първоначално имаше `1 failed, 499 passed` заради source-assert, очакващ `CHECK_TIMEOUT_MS)` вместо реалното `CHECK_TIMEOUT_MS * activeNames.length)`; assert-ът е коригиран и повторният suite мина изцяло. `git diff --check` за кодовите файлове показва само съществуващи CRLF предупреждения. Сесия `200 AUTHENTICATED` за `GabrielRules`; избран е self `GabrielRules/TEST2`; preflight изпрати само `{"dry_run":true,"repositories":["GabrielRules/TEST2"]}`, без `dry_run:false`, и диалогът съдържаше точно 1 репозитори. `window.confirm` беше отказан, значи реален Sync, GitHub write, commit и push НЕ са изпълнени. Backup: `%TEMP%\opencode\preflight-timeout-backup-20261121-2115`.
- **Оставащи проблеми:** Чака се изрично потребителско потвърждение за реален Sync на `GabrielRules/TEST2`. По-ранните „рестартирания“ на Dashboard идваха от собствените CDP навигации/reload-и на агента, не от приложението или sign out. Welcome на `127.0.0.1` (`web/index.html`) остава извън обхвата на theme guard.

## 2026-11-21 21:11 - Theme guard и стабилна работа с Dashboard проверки/сесия

- **Извършена задача:** Добавен е защитен слой срещу инжектираното от Chrome разширение `dark_1.css` (`DASHBOARD/theme_guard.js` + `@layer dreamerol-guard`) и е стабилизирана работата с чекбокси при проверки и изтичане на сесия. Чекбоксите се блокират само докато текат проверки, изборът се пази в `sessionStorage` по акаунт, при 401 по check път се показва `SESSION EXPIRED — PLEASE SIGN IN` без redirect, а SYNC бутоните остават изключени до валидна сесия и завършени проверки.
- **Променени файлове:** `DASHBOARD/theme_guard.js`, `DASHBOARD/dashboard.css`, `DASHBOARD/index.html`, `DASHBOARD/app.js`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Външното разширение правеше Dashboard/Welcome сиви; освен това при избор на репо по време на проверка или изтичане на сесия се наблюдаваха прекъсване на избора и навигация към `/healthz`. Клиентският код не съдържа преход към `healthz`; контролният таб беше създаден от агента и вече е затворен.
- **Изпълнени тестове:** `node --check DASHBOARD\theme_guard.js`; `node --check DASHBOARD\app.js`; `python -m pytest -q -p no:cacheprovider`; жива CDP проверка с валидна сесия за `GabrielRules`; CDP симулация на 401 и batch заявки с коригиран async wait.
- **Резултат:** `node --check` OK; пълен suite `499 passed, 1 warning in 8.09s`. Живо: `/api/auth/status 200 AUTHENTICATED`, 1 list + 4 batch `/api/sync` HTTP `200`, `Check complete: 39 forks checked...`, броячи `39/34/3/2` в `stat-*` и `summary-*`, `guard="on"`, `cleaned="110"`, JS грешки `[]`. Клик върху 1 и 2 `READY TO SYNC` репо не смени URL-а от `/dashboard` и не създаде нови `/api/sync` заявки; изборът се записа и възстанови от `sessionStorage`. Backup-и: `%TEMP%\opencode\theme-guard-backup-20261121-201828`, `...\checkbox-guard-backup-20261121-204650`, `...\checkbox-spec-backup-20261121-204939`, `...\dashboard-stability-backup-20261121-210130`. Няма commit, push, merge, реален Sync или GitHub write.
- **Оставащи проблеми:** Реален Sync не е изпълван — изисква отделно одобрение и успешен preflight за избраните 1–2 репозиторити. Welcome на `127.0.0.1` ползва `web/index.html` и остава извън обхвата на guard. Ако `/healthz` redirect се появи отново, трябва да се улови navigation history на конкретния таб.

## 2026-11-21 18:27 - BFCache рестарт на batch проверката

- **Извършена задача:** Поправен е рестартът на вече завършена или активна batch проверка при връщане от BFCache/back-forward в `DASHBOARD/app.js`. Новият `handlePageShowRestore()` запазва текущите броячи и резултати и не стартира паралелни `/api/sync` заявки.
- **Променени файлове:** `DASHBOARD/app.js`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Старият `pageshow persisted:true` handler винаги извикваше `invalidatePendingOperations()` и `initDashboard({force:true})`, което нулираше броячите (`39/34/3/2 → 39/0/0/0`) и стартираше нова серия от четири batch проверки при навигация назад/напред.
- **Изпълнени тестове:** `node --check DASHBOARD\app.js`; targeted `python -m pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py`; пълен `python -m pytest -q -p no:cacheprovider`; жива read-only CDP проверка с BFCache restore при завършена и активна batch.
- **Резултат:** `node --check` OK; targeted `69 passed, 1 warning in 2.37s`; пълен suite `492 passed, 1 warning in 6.17s`. При завършена проверка Back/Forward не създаде нови list/batch заявки и броячите останаха `39/34/3/2`. При активна проверка restore-ът не нулира `39/0/0/0` и не добави нова серия; текущата проверка завърши с общо 1 list + 4 batch и `39/34/3/2`. Backup: `%TEMP%\opencode\dreamerol-bfcache-backup-20261121-182227`. Няма commit, push, merge, реален Sync, GitHub write, OAuth/hosts/Chrome промени.
- **Оставащи проблеми:** Постоянното премахване на сивия UI от Chrome разширението `pjbgfifennfhnbkhoidkdchbflppjncb` чака отделно одобрение за hosts/Chrome промени; backup и точен план вече съществуват. `.env`/`BROKER_DASHBOARD_URL` не може да се пренасочи към `dreamerol.local` без кодова промяна във валидацията на `auth_broker/config.py`.

## 2026-11-21 16:07 - Batch проверка на background fork заявките

- **Извършена задача:** След изрично одобрение `runBackgroundChecks()` в `DASHBOARD/app.js` изпраща fork-овете на партиди по 10 с `{dry_run:true, repositories:[...]}` и мапва всеки резултат по `repository`, вместо да изпраща 35 отделни заявки. Проверката на Git историята и snapshot-ите от 19–20.11 показа, че TOTAL вече се изчислява от пълния дедупликиран масив; дефектът е в многократните `get_forks()` повиквания и 8-секундния timeout, не в `computeDashboardCounts()`.
- **Променени файлове:** `DASHBOARD/app.js`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Симптомът `35/35 complete ... 35 unverified` и броячи `35/0/0/0` се появява след преминаването от последователно обхождане към фонови проверки. Всяка от 35-те заявки викаше отново `get_forks()` (`api/routes.py:372`), което при паралелизъм 3 и timeout 8s водеше до масови `preview_error`/`unknown`.
- **Изпълнени тестове:** `node --check DASHBOARD\app.js`; `node --check DASHBOARD\utils.js`; targeted `pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py`; пълен `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1`; `git diff --check`.
- **Резултат:** `node --check` OK; targeted `61 passed, 1 warning`; пълен suite `484 passed, 1 warning in 8.07s`. Добавени са регресионни проверки за 4 партиди от 10 и за 35 fork-а с `:1 READY TO SYNC / 34 UP TO DATE / 0 check errors`. `git diff --check` има само предишни whitespace/CRLF предупреждения извън променения код. Backup: `%TEMP%\opencode\dreamerol-batch-backup-*`. Няма commit, push, merge, реален Sync, GitHub write или промяна в `.env`/credentials/history.
- **Оставащи проблеми:** Нужна е браузърна проверка с валидна OAuth сесия, за да се потвърди, че реалните броячи вече са попълнени. UNSYNCABLE и проверката за грешки умишлено остават непроменени; евентуално включване на errors+divergents там е отделна промяна на модела.

## 2026-11-20 00:27 - Инстант избиране на forkове и background проверки в Dashboard

- **Извършена задача:** След изолиран mock smoke test (9/9) и изрично одобрение е интегрирана новата последователност: бърз list отговор, checkbox-и веднага, активен `SYNC CHOSEN` преди проверките, прогресивни броячи, независими background проверки, разбираема 403 грешка, generation guard и запазен задължителен preflight.
- **Променени файлове:** `DASHBOARD/app.js`, `DASHBOARD/index.html`, `DASHBOARD/utils.js`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_20-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Потребителят поиска спиране на `CHECKING` като предпоставка за избор и синхронизация, както и коректни броячи/грешки при list fail. Предишната одобрена counter snapshot логика трябваше да остане непокътната.
- **Изпълнени тестове:** Изолиран headless Chrome/CDP smoke с mocks за 9 сценария; `node --check DASHBOARD\app.js`; `node --check DASHBOARD\utils.js`; targeted `pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py`; пълен `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1`; HTTP проверки на локалния стек.
- **Резултат:** Smoke `9/9 PASS` без реални GitHub заявки (`liveCalls=0`); `node --check` OK; targeted `58 passed, 1 warning`; пълен suite `481 passed, 1 warning in 7.85s`. `/healthz` `200 {"status":"ok"}`, `/dashboard` `200`, `/dashboard/static/app.js?v=20261120a` съдържа новия код, CSS `200`. Backup: `%TEMP%\opencode\dreamerol-original-before-instant-20261120-002624`. Няма commit, push, merge, реален Sync, GitHub write или промяна в `.env`/credentials/history.
- **Оставащи проблеми:** Няма автоматичен browser E2E в основния repo; визуалната проверка с валидна OAuth сесия остава ръчна. След reload без сесия `/api/auth/status` връща очаквано `401`.

## 2026-11-19 23:24 - Поправка: Sync counters и състояние след reload

- **Извършена задача:** След визуална проверка на новия Dashboard е поправен пропускът при успешен Sync: `SYNC RESULTS` показваше `2 synchronized`, но горните четири брояча не се обновяваха, а след reload се връщаха на `0/0/0/0`.
- **Променени файлове:** `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `DASHBOARD/index.html`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_19-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Потребителят очакваше броячите да отразят завършения Sync веднага и да запазят състоянието си при презареждане. Предишната логика обновяваше само секцията със SYNC резултати, а не `stat-*` counters.
- **Изпълнени тестове:** `node --check DASHBOARD\app.js` и `node --check DASHBOARD\utils.js`; targeted `pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py`; пълен `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1`; HTTP проверки на локалния стек.
- **Резултат:** `node --check` без грешки; targeted suite `53 passed`; пълен suite `476 passed in 7.50s`; broker `/healthz` `200 {"status":"ok"}`, `/dashboard` `200`, версираните JS/CSS се обслужват с новия код. Добавени са `operationCountsAfter`, `mergeOperationResults`, `counts_before`, както и version query `?v=20261119c` срещу стар browser cache. Локалното приложение е рестартирано. Агентът не е правил commit, push, merge, реален Sync или GitHub write операция; `data/sync_history.json` отразява единствено реалния Sync на потребителя от визуалната проверка (`TEST2`/`TEST3`).
- **Оставащи проблеми:** Нужна е визуална потвърдителна проверка от потребителя след нов Sync и reload. Няма browser E2E автоматизация; старите localStorage записи без `counts_before` не възстановяват snapshot преди нова проверка.

## 2026-11-18 22:58 - PR #1 е merge-нат в architectquant/DREAMEROL-SYNC

- **Извършена задача:** Поправката за web auth/403 от `GabrielRules:feature/github-app-auth` е прехвърлена в `architectquant/DREAMEROL-SYNC:main` чрез PR #1.
- **Променени файлове:** `README.md` от merge resolve; `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Потребителят изрично одобри PR към своя fork и последващ merge. Първоначалният опит с `GabrielRules` credential върна `404` защото правата бяха само `pull`; повторен с наличния `architectquant` credential (`admin/push`) беше успешен.
- **Изпълнени тестове:** targeted pytest `72 passed`; пълен pytest `461 passed, 1 warning`; `scripts/check.ps1` → `All checks passed`; live dry-run `HTTP 200 behind_by:3`; реален Sync `HTTP 200 synced`; финален preview `37` репозитория `35/0/2`; локален `git merge-tree` без конфликти; GitHub API потвърди `merged:true`.
- **Резултат:** PR #1 е `closed/merged`, `merge_commit_sha:b16c977776793c92bef7681c297e8e322974be9a`; `architectquant/main` сочи същия SHA. Няма push извън този PR, нов реален Sync или промени в GitHub App настройките.
- **Оставащи проблеми:** In-memory сесиите, липсата на автоматичен refresh/rotation на токени и евентуален PR към `Dreamerol` остават извън тази задача. Реалният preview показва 2 diverged fork-а, които съзнателно не се синхронизират автоматично.

- **Извършена задача:** Финализирана е визуалната група `SYNC CHOSEN` / `SYNC ALL`, извършен е read-only release preparation review и са приложени одобрените document-only корекции.
- **Променени файлове:** `DASHBOARD/dashboard.css`, `DASHBOARD/index.html`, `tests/test_dashboard_progress.py`, `README.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** да се придаде завършен, ясен и поддържан вид на двете sync действия и да се синхронизира документацията с реалното състояние на release кандидата.
- **Изпълнени тестове:** `.\.venv\Scripts\python.exe -m pytest -q`; `scripts/check.ps1`; `compileall`; `node --check` за `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `web/app.js`; PowerShell Parser; `pip check`; `git diff --check`; smoke стек `scripts/stop-smoke.ps1` + `scripts/start-smoke.ps1 -Force`; headless Chrome/CDP при 1440×1200 и 390×844.
- **Резултат:** pytest `457 passed` (в `scripts/check.ps1`: `457 passed, 1 warning` – StarletteDeprecationWarning); всички syntax/parse/package checks OK; `git diff --check` exit 0 само с CRLF предупреждения; Broker `/healthz` 200, dashboard `/` 200, `/auth/callback` без state 400, `/api/auth/status` без сесия 401; CDP потвърди цветовете `#C93BFF`/`#10EFA2`, размерите 70/62px, desktop side-by-side и mobile stacked без horizontal overflow. Конзолата показва само очаквани 401 и benign 404 за `favicon.ico`.
- **Оставащи проблеми:** Няма валидна OAuth сесия и реален GitHub smoke test; GitHub App token expiration Opt-out, callback/wildcard/installation и продукционният access-log redaction трябва да се потвърдят от GitHub UI/инфраструктурата. Остават in-memory сесиите, липсата на отделен CSRF token и cookie Secure зад TLS proxy. Реален Sync, push и промени в GitHub App настройки не са извършвани.

## 2026-11-13 17:14 - Web dashboard Auth Broker интеграция

- **Извършена задача:** Добавен е server-side Auth Broker login към web dashboard-а, с HTTP-only session cookie, автоматично preview след вход и запазен ръчен PAT fallback.
- **Променени файлове:** `.env.example`, `README.md`, `api/app.py`, `api/routes.py`, `auth_broker/routes.py`, `web/app.js`, `web/index.html`, `web/style.css`; нови `api/auth.py`, `tests/test_web_auth.py`.
- **Причина:** Браузърът не трябва да получава GitHub token, а интеграцията трябва да запази съществуващия preview/sync workflow и ръчния token fallback.
- **Изпълнени тестове:** `node --check web/app.js`; `python -m pytest -q`; `git diff --check`.
- **Резултат:** `node --check` успешен; pytest `339 passed, 1 warning`; `git diff --check` само CRLF/LF предупреждения без whitespace грешки.
- **Оставащи проблеми:** Реалният GitHub login не е тестван; сесиите са в паметта на един процес и не се споделят между workers; промените не са commit-нати.

## 2026-11-13 17:27 - Локален smoke test на Broker и dashboard

- **Извършена задача:** Стартирани са Broker на порт 8000 и dashboard на порт 8001 и е проверен локалният auth flow без завършване на реален GitHub login.
- **Променени файлове:** `LOG_13-11-26.md` (само лог).
- **Причина:** Да се провери реалната връзка между двете услуги, cookie session-а и logout поведението извън unit тестовете.
- **Изпълнени тестове:** Ръчен smoke test с `Invoke-WebRequest`: начална страница, `POST /api/auth/start`, `GET /api/auth/status`, `POST /api/auth/logout`, повторен status след logout.
- **Резултат:** Началната страница се зарежда; auth start връща 200 и authorization URL; статусът е `PENDING`; logout връща `SIGNED_OUT`; след logout status връща 401; двата сървъра стартират без грешки.
- **Оставащи проблеми:** Реалният GitHub login е блокиран от placeholder стойности за GitHub App client ID/secret и callback URL `broker.example.com`.

## 2026-11-13 17:36 - AI development logging и checkpoint документация

- **Извършена задача:** Добавени са правилата за AI development logging и са създадени/обновени файловете за changelog, текущ статус, следващи стъпки и архитектурни решения.
- **Променени файлове:** `AGENTS.md`, `docs/development/CHANGELOG_AI.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `LOG_13-11-26.md`.
- **Причина:** Да има постоянна, точна и проверяема история на разработката, включително checkpoint при прекъсване.
- **Изпълнени тестове:** Няма изпълнени тестове; промяната е само в документация и правила.
- **Резултат:** Документацията е създадена/обновена; не се твърди успешен тест за тази стъпка.
- **Оставащи проблеми:** Реалният GitHub login остава за тест с валидни credentials и публичен HTTPS callback.

## 2026-11-13 17:39 - Финален test gate преди commit

- **Извършена задача:** Изпълнен е финалният пълен test suite преди евентуален commit на Auth Broker интеграцията.
- **Променени файлове:** `CURRENT_STATUS.md`, `docs/development/CHANGELOG_AI.md`, `LOG_13-11-26.md` (само статус и логове).
- **Причина:** Да се потвърди, че текущото състояние на кода е стабилно преди commit.
- **Изпълнени тестове:** `python -m pytest -q`.
- **Резултат:** `339 passed, 1 warning in 1.20s`.
- **Оставащи проблеми:** Има един `StarletteDeprecationWarning` за `httpx`/`starlette.testclient`; реален GitHub login не е тестван. Промените не са commit-нати.

## 2026-11-14 02:55 - Проверка на текущото състояние

- **Извършена задача:** Потвърдено е текущото състояние на клона и работното дърво преди следваща стъпка.
- **Променени файлове:** `LOG_14-11-26.md`, `docs/development/CHANGELOG_AI.md` (само логове).
- **Причина:** Да се установи дали неcommit-натата Auth Broker web интеграция е стабилна и какви са реалните следващи стъпки.
- **Изпълнени тестове:** `python -m pytest -q -p no:cacheprovider`.
- **Резултат:** `339 passed, 1 warning in 2.11s`; няма нови кодови промени.
- **Оставащи проблеми:** Промените не са commit-нати; реален GitHub login не е тестван; сесиите на dashboard-а са само в паметта на един процес.

## 2026-11-14 03:02 - Одит на Keyring retry и regression test

- **Извършена задача:** Направен е одит на Keyring retry поведението на CLI и е добавен regression тест за многократен retry без повторен Broker poll.
- **Променени файлове:** `tests/test_auth_cli.py`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Да се потвърди, че при Keyring грешка CLI-ят не излиза веднага и не праща ACK, а позволява безопасен повторен опит в същата транзакция, както изисква спецификацията.
- **Изпълнени тестове:** `python -m pytest tests/test_auth_cli.py -q -k "keyring or login_stores"`; `python -m pytest -q -p no:cacheprovider`.
- **Резултат:** Целевите тестове `5 passed`; пълният suite `340 passed, 1 warning in 1.26s`.
- **Оставащи проблеми:** Реалният GitHub login остава блокиран от placeholder credentials; промените не са commit-нати. Keyring retry не е пречка за smoke test.

## 2026-11-14 03:05 - Одит на .env и GitHub App конфигурацията

- **Извършена задача:** Проверени са `.env`, `.gitignore`, Broker конфигурацията и callback route-ът преди реален GitHub smoke test.
- **Променени файлове:** `LOG_14-11-26.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md` (само документация и статус).
- **Причина:** Да се установи какво липсва за реален login и да не се стартира тест с невалидна конфигурация.
- **Изпълнени тестове:** Няма изпълнени тестове; направени са статични проверки на конфигурацията и `.gitignore`.
- **Резултат:** `.env` е игнориран от Git; GitHub App credentials и callback URL са placeholder; изисква се фиксиран HTTPS URL без wildcard/query/fragment и път `/auth/callback`.
- **Оставащи проблеми:** Нужни са реални GitHub App credentials и публичен HTTPS callback; локален `127.0.0.1` не може да се използва директно от GitHub.

## 2026-11-14 03:13 - Commit на Auth Broker web интеграцията

- **Извършена задача:** Прегледан е diff-ът и Auth Broker web интеграцията е commit-ната.
- **Променени файлове:** Всички файлове от интеграцията, документацията и тестовете; commit `92f5581`.
- **Причина:** Да се фиксира стабилен checkpoint преди реален GitHub smoke test с външни credentials.
- **Изпълнени тестове:** `python -m pytest -q -p no:cacheprovider` преди commit-а.
- **Резултат:** `340 passed, 1 warning`; commit `92f5581` с 18 файла и 1336 insertions. `.env` не е включен.
- **Оставащи проблеми:** Реалният GitHub login остава блокиран от placeholder credentials; последващите лог/статус записи са неcommit-нати.

## 2026-11-14 03:16 - Автоматично зареждане на .env в Broker

- **Извършена задача:** `create_app()` вече зарежда `.env` автоматично, когато не е подаден явен `BrokerConfig`.
- **Променени файлове:** `auth_broker/app.py`, `tests/test_auth_broker_api.py`, `README.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Стартирането с `uvicorn auth_broker.app:create_app --factory` да работи директно с локалния `.env` без ръчно експортиране на променливи.
- **Изпълнени тестове:** `python -m pytest tests/test_auth_broker_api.py -q -k dotenv`; `python -m pytest -q -p no:cacheprovider`.
- **Резултат:** Целевите тестове `2 passed`; пълният suite `342 passed, 1 warning in 1.60s`.
- **Оставащи проблеми:** Промяната не е commit-ната; реален GitHub login остава блокиран от placeholder credentials.

## 2026-11-14 03:21 - Security преглед на web auth сесията

- **Извършена задача:** Направен е security преглед на web auth flow и са добавени `no-store` headers и regression тестове.
- **Променени файлове:** `api/app.py`, `tests/test_web_auth.py`, `README.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Да се намалят CSRF, cache leakage и session fixation рисковете около browser сесията и credential източниците.
- **Изпълнени тестове:** `python -m pytest tests/test_web_auth.py -q -p no:cacheprovider`; `python -m pytest -q -p no:cacheprovider`.
- **Резултат:** `30 passed` за web auth тестовете; пълният suite `349 passed, 1 warning in 1.65s`.
- **Оставащи проблеми:** Няма отделен CSRF token — v1 разчита на `SameSite=Lax` и POST-only. Зад HTTPS proxy е нужен `--proxy-headers` за `Secure` cookie. Реален GitHub login остава блокиран от placeholder credentials.

## 2026-11-14 03:29 - Commit на security промените

- **Извършена задача:** Commit на security hardening промените след изрично одобрение.
- **Променени файлове:** `api/app.py`, `tests/test_web_auth.py`, `README.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Запазване на прегледаните и тествани промени в Git историята.
- **Изпълнени тестове:** Няма нови промени по код; последният пълен suite е `349 passed, 1 warning`.
- **Резултат:** Commit `be41a0b`.
- **Оставащи проблеми:** Реален GitHub login остава блокиран от placeholder credentials; няма отделен CSRF token.

## 2026-11-14 03:42 - cloudflared и HTTPS tunnel за smoke test

- **Извършена задача:** Инсталиран е `cloudflared` и е стартиран временен HTTPS tunnel към Broker за GitHub callback.
- **Променени файлове:** `.env` (gitignored), `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** GitHub не може да извика `127.0.0.1`; нужен е публичен HTTPS callback за реален OAuth test.
- **Изпълнени тестове:** `GET https://volt-mechanisms-shirts-routine.trycloudflare.com/auth/callback` → 400 (очаквано без state); `GET http://127.0.0.1:8001/` → 200; `/auth/start` връща `redirect_uri` с новия tunnel URL.
- **Резултат:** `cloudflared 2026.11.0` инсталиран; Broker, dashboard и tunnel работят. Няма промяна по код и не е пускан нов pytest suite.
- **Оставащи проблеми:** `.env` все още съдържа placeholder `GITHUB_APP_CLIENT_ID` и `GITHUB_APP_CLIENT_SECRET`; quick tunnel URL се променя при рестарт. Документацията от тази стъпка е неcommit-ната.

## 2026-11-14 03:51 - Скриптове за стартиране и спиране на smoke test

- **Извършена задача:** Добавени са PowerShell скриптове за автоматизиран локален smoke test с Broker, dashboard и cloudflared.
- **Променени файлове:** `scripts/start-smoke.ps1`, `scripts/stop-smoke.ps1`, `README.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Да се намали ръчната работа и да се избегне разминаване между ephemeral tunnel URL и `BROKER_CALLBACK_URL`.
- **Изпълнени тестове:** PowerShell syntax check; `start-smoke.ps1 -DryRun`; реален старт с cloudflared; `GET /auth/callback` през тунела → 400; `GET http://127.0.0.1:8001/` → 200; `/auth/start` → правилен `redirect_uri`; `stop-smoke.ps1` спря всички процеси; `python -m pytest -q -p no:cacheprovider` → `349 passed, 1 warning`.
- **Резултат:** Скриптовете работят end-to-end; активен tunnel `https://sealed-arguments-quality-stays.trycloudflare.com`, Broker PID 18608, dashboard PID 15192, cloudflared PID 14768.
- **Оставащи проблеми:** Скриптовете и документацията са неcommit-нати; реален GitHub login остава блокиран от placeholder credentials.

## 2026-11-14 03:55 - Broker hardening и trusted proxy

- **Извършена задача:** Добавени са security headers за всички `/auth/` отговори и trusted proxy конфигурация за cloudflared.
- **Променени файлове:** `auth_broker/app.py`, `tests/test_auth_broker_api.py`, `.env` (gitignored), `.env.example`, `README.md`, `scripts/start-smoke.ps1`, `DECISIONS.md`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Да не се кешират auth отговори и rate limiting-ът да ползва реалния клиентски IP зад локалния тунел.
- **Изпълнени тестове:** `python -m pytest tests/test_auth_broker_api.py -q -p no:cacheprovider` → `17 passed`; `python -m pytest -q -p no:cacheprovider` → `350 passed, 1 warning`; ръчни проверки на 401, 404 и тунел 400 за четирите headers.
- **Резултат:** Broker е рестартиран с новата конфигурация (PID 10640); `RateLimitConfig.from_env().trusted_proxies` е `('127.0.0.1', '::1')`.
- **Оставащи проблеми:** Промените по код и скриптове са commit-нати като `23f1226`; логите като `fa4a135`. Реален GitHub login остава блокиран от placeholder credentials.

## 2026-11-14 04:04 - Commit на smoke-test и Broker hardening

- **Извършена задача:** Commit на smoke-test скриптовете, Broker hardening промените и документацията.
- **Променени файлове:** `auth_broker/app.py`, `tests/test_auth_broker_api.py`, `.env.example`, `README.md`, `scripts/start-smoke.ps1`, `scripts/stop-smoke.ps1`, `CURRENT_STATUS.md`, `DECISIONS.md`, `NEXT_STEPS.md`, `LOG_14-11-26.md`.
- **Причина:** Запазване на тестваните промени в Git историята след изрично одобрение.
- **Изпълнени тестове:** Последен пълен suite `350 passed, 1 warning`; няма нови кодови промени след него.
- **Резултат:** Commit `23f1226` за код и скриптове; commit `fa4a135` за логи; последващ logging commit за тази бележка.
- **Оставащи проблеми:** Реален GitHub login остава блокиран от placeholder credentials.

## 2026-11-14 04:06 - Възстановяване на Broker процеса

- **Извършена задача:** Открито е, че Broker PID 10640 е спрял, и процесът е стартиран отново на същия порт и тунел.
- **Променени файлове:** `CURRENT_STATUS.md`, `LOG_14-11-26.md`, `docs/development/CHANGELOG_AI.md` (само документация).
- **Причина:** Тунелът връщаше 502, защото на порт 8000 нямаше listener.
- **Изпълнени тестове:** `python -m pytest -q -p no:cacheprovider` → `350 passed, 1 warning`; `curl` към `/auth/unknown` → 404 с `no-store`, `Pragma`, `Referrer-Policy` и `nosniff`; тунелът към `/auth/callback` → 400.
- **Резултат:** Broker работи като PID 24436; state файлът е обновен; dashboard PID 15192 и cloudflared PID 14768 продължават да работят.
- **Оставащи проблеми:** Причината за спирането на PID 10640 не е установена; документацията от тази стъпка е неcommit-ната.

## 2026-11-14 04:12 - Mock GitHub OAuth E2E и Broker health endpoint

- **Извършена задача:** Добавен е fake GitHub OAuth provider за пълен E2E тест и `GET /healthz` към Broker.
- **Променени файлове:** `tests/test_auth_mock_oauth_e2e.py`, `auth_broker/app.py`, `tests/test_auth_broker_api.py`.
- **Причина:** Да се тества целият OAuth flow с PKCE без реални GitHub credentials и да има health endpoint за watchdog.
- **Изпълнени тестове:** `python -m pytest tests/test_auth_mock_oauth_e2e.py tests/test_auth_broker_api.py -q -p no:cacheprovider` → `21 passed`; `python -m pytest -q -p no:cacheprovider` → `354 passed, 1 warning`.
- **Резултат:** Успешният flow, `access_denied` и token exchange failure са покрити; `/healthz` връща `{"status":"ok"}` с `no-store`.
- **Оставащи проблеми:** Fake provider-ът не замества реален GitHub smoke test; промените не са commit-нати.

## 2026-11-14 04:17 - Broker watchdog и smoke скриптове

- **Извършена задача:** Добавен е `watch-smoke.ps1`, `-Watchdog` в `start-smoke.ps1` и спиране на watchdog-а в `stop-smoke.ps1`.
- **Променени файлове:** `scripts/watch-smoke.ps1`, `scripts/start-smoke.ps1`, `scripts/stop-smoke.ps1`, `README.md`, `DECISIONS.md`.
- **Причина:** Broker може да спре неочаквано и да остави тунела с 502; рестартът на cloudflared би сменил callback URL.
- **Изпълнени тестове:** PowerShell parser check; `watch-smoke.ps1 -Once` при здрав Broker → exit 0; kill на Broker → watchdog го рестартира; `stop-smoke.ps1` спря watchdog, cloudflared, dashboard и Broker.
- **Резултат:** Watchdog-ът рестартира само Broker-а на същия порт и тунел; `start-smoke.ps1` чака `/healthz` и до 90 секунди за тунела.
- **Оставащи проблеми:** Dashboard и cloudflared не се рестартират автоматично; при техен проблем е нужен ръчен `start-smoke.ps1`. Промените не са commit-нати.

## 2026-11-14 04:26 - Lifecycle проверка с нов тунел

- **Извършена задача:** Тестван е пълният lifecycle `start-smoke.ps1 -Watchdog` → `stop-smoke.ps1` → нов старт с watchdog.
- **Променени файлове:** `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `LOG_14-11-26.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Да се потвърди, че новите health/watchdog промени работят с реални процеси и cloudflared.
- **Изпълнени тестове:** `GET http://127.0.0.1:8000/healthz` → 200 `{"status":"ok"}`; dashboard → 200; тунел `/auth/callback` → 400; kill на Broker → watchdog рестарт в рамките на 5 секунди; `stop-smoke.ps1` → всички процеси спрени.
- **Резултат:** Активен тунел `https://female-sender-lenders-usr.trycloudflare.com`; Broker PID 23424, dashboard PID 15884, cloudflared PID 20656, watchdog PID 19892.
- **Оставащи проблеми:** Реален GitHub login остава блокиран от placeholder credentials; документацията и кодът от 04:12-04:26 са неcommit-нати.

## 2026-11-14 04:41 - Разширен CI и локален check скрипт

- **Извършена задача:** CI вече проверява Ubuntu и Windows, Python/JS/PowerShell синтаксис и `pip check`; добавен е локален `scripts/check.ps1`.
- **Променени файлове:** `.github/workflows/tests.yml`, `scripts/check.ps1`, `LOG_14-11-26.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Да се хващат проблеми в скриптовете и на Windows още в CI и да има една локална команда за проверка.
- **Изпълнени тестове:** `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\check.ps1` → `All checks passed`; pytest `354 passed, 1 warning`.
- **Резултат:** Локалните и CI проверките са синхронизирани; Windows job-ът покрива PowerShell скриптовете.
- **Оставащи проблеми:** Промените не са commit-нати; Windows CI job-ът ще се потвърди при push.

## 2026-11-15 03:24 - Локален loopback callback вместо Quick Tunnel

- **Извършена задача:** GitHub App callback-ът е преминат към фиксиран `http://127.0.0.1:8000/auth/callback`; HTTP се допуска само за loopback hosts, а smoke скриптовете вече не стартират cloudflared.
- **Променени файлове:** `auth_broker/config.py`, `tests/test_auth_oauth.py`, `tests/test_auth_broker_api.py`, `tests/test_auth_mock_oauth_e2e.py`, `.env` (gitignored), `.env.example`, `README.md`, `docs/GITHUB_APP_AUTH_SPEC.md`, `DECISIONS.md`, `scripts/start-smoke.ps1`, `scripts/stop-smoke.ps1`, `scripts/watch-smoke.ps1`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_15-11-26.md`.
- **Причина:** Quick Tunnel URL-ът се сменя при всеки рестарт и изисква ръчна промяна в GitHub App; фиксираният loopback callback премахва `redirect_uri_mismatch` и dead callback проблема без rewrite на OAuth логиката.
- **Изпълнени тестове:** `python -m pytest tests/test_auth_broker_api.py tests/test_auth_mock_oauth_e2e.py -q -p no:cacheprovider` → `21 passed, 1 warning`; `python -m pytest -q -p no:cacheprovider` → `364 passed, 1 warning`; `node --check web/app.js`; PowerShell parser check; `scripts/check.ps1` → `All checks passed`; `start-smoke.ps1 -DryRun`; start/stop без watchdog; start с watchdog и kill на Broker → автоматичен рестарт; `/healthz` 200, dashboard 200, `/auth/callback` без state 400.
- **Резултат:** Loopback config-ът, E2E mock flow-ът и smoke lifecycle-ът работят. Първият targeted run хвана стар assert за `https` callback; тестът беше коригиран да сравнява с конфигурирания `CALLBACK_URL`, след което мина. `git diff --check` показва само CRLF предупреждения и съществуващ празен ред в края на `.gitignore`, който не е променян в тази задача.
- **Оставащи проблеми:** Реалният GitHub login не е изпълнен; GitHub App callback/wildcard/token expiration/installation настройките са ръчни. Ако token expiration не е opted out, login ще върне `502`. Промените не са commit-нати.

## 2026-11-15 03:52 - Проверка на GitHub callback и smoke тест

- **Извършена задача:** Проверен е GitHub authorization URL-ът, който dashboard-ът генерира, и е изпълнен smoke check на стартираните услуги.
- **Променени файлове:** `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_15-11-26.md`, `docs/development/CHANGELOG_AI.md` (само документация).
- **Причина:** Да се потвърди, че Broker използва точния loopback callback и че услугите са здрави преди реален login.
- **Изпълнени тестове:** `POST http://127.0.0.1:8001/api/auth/start` → authorization URL с `redirect_uri=http://127.0.0.1:8000/auth/callback`; GitHub authorize endpoint → `302` към login; контролна заявка с грешен callback → също `302`, т.е. pre-login проверката не е достатъчна; `watch-smoke.ps1 -Once` → Broker PID 22792 и dashboard PID 23492 здрави, exit 0; `scripts/check.ps1` → `364 passed, 1 warning`, `All checks passed`.
- **Резултат:** Локалната OAuth конфигурация и услугите са коректни. GitHub App callback настройката не може да се потвърди без реален sign-in.
- **Оставащи проблеми:** Нужен е ръчен GitHub login, preview, sync и logout; услугите продължават да работят.

## 2026-11-15 04:03 - Диагностика на 502 при /auth/callback

- **Извършена задача:** Проверен е реалният callback след GitHub authorize и е локализиран етапът на грешката.
- **Променени файлове:** `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `LOG_15-11-26.md`, `docs/development/CHANGELOG_AI.md` (само документация).
- **Причина:** Broker логът показва callback с code/state → `502 Bad Gateway`; state-ът е обработен и е стигнало до token exchange. Широкият `except Exception` в `auth_broker/routes.py` скрива точния тип на изключението. Контролен token request с dummy code върна `bad_verification_code`, което показва, че client ID/secret и redirect URI се приемат.
- **Изпълнени тестове:** `POST /api/auth/start` + контролиран callback с dummy code → 502 страница с 160-байтов HTML; `/api/auth/status` за същата сесия → `FAILED`; headless Chrome на dashboard-а → без console errors; `curl` на callback без валиден state → 400 HTML.
- **Резултат:** Няма грешка при redirect към dashboard; callback-ът връща HTML статус страница, а dashboard получава терминално `FAILED`. Най-вероятната конкретна причина е включен user-to-server token expiration, при който token response съдържа `expires_in`/`refresh_token` и се отхвърля от token policy.
- **Оставащи проблеми:** Нужно е потвърждение на GitHub App expiration настройката или безопасно логване на token exchange изключението; uvicorn access log-ът записва пълния callback query string с code/state и трябва да се редактира; не са променяни конфигурации, код или Git.

## 2026-11-17 18:10 - Редизайн на Dashboard и строги fork counters

- **Извършена задача:** Реализиран е одобреният frontend редизайн с тъмна адаптивна тема, бранд/акаунт/connection state, точни бутони `CHECK FORKED REPOS` и `SYNC`, прогрес индикатори, четири counters, търсене/филтри, финално резюме, sync резюме и сгъваеми results/history. Добавени са строги helper-и за неизвестни състояния, upstream metadata и sync резултати.
- **Променени файлове:** `DASHBOARD/index.html`, `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `DASHBOARD/dashboard.css`, `tests/test_api.py`, нов `tests/test_dashboard_strict_counts.py`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Да се премахне остарелият визуален стил и да се запазят само одобрените термини и надеждното броене само на реални fork-ове, без промяна в auth, discovery, класификация или synchronization логиката.
- **Изпълнени тестове:** `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; `python -m pytest tests/test_api.py tests/test_dashboard_strict_counts.py -q`; `python -m pytest -q --ignore=tests/test_dashboard_progress.py`.
- **Резултат:** Първоначалният targeted run хвана 2 пропуска (`up_to_date = 0`) поради липсваща изрична `synced` ветка; след поправката targeted тестовете са `23 passed, 1 warning`, а широкият suite е `395 passed, 1 warning` (StarletteDeprecationWarning). Node syntax checks минаха. Няма реален sync, merge, commit или push; предходните uncommitted промени са запазени.
- **Оставащи проблеми:** Визуална проверка в браузър и live OAuth сесия не са извършени. `tests/test_dashboard_progress.py` остава блокиран от предходен `SyntaxError` на ред 223 и не е пипан. Upstream/parent данни се показват само ако вече са в API отговора; няма нови backend промени.

## 2026-11-17 18:18 - Фаза 3: строги числови fork counters

- **Извършена задача:** Доведена е до краен вид логиката за броене само на реални GitHub fork-ове. `computeDashboardCounts()` използва `fork === true`, изключва `fork === false`, третира липсващ/невалиден fork флаг като data грешка, дедублира по repository name и класифицира чрез `ahead_by`/`behind_by`: `0/0` → UP TO DATE, `0/>0` → TO BE SYNCED, `>0/>0` и `>0/0` → UNSYNCABLE, грешките при инспекция също са UNSYNCABLE. Четирите counters винаги се събират до TOTAL FORKS.
- **Променени файлове:** `api/routes.py`, `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `tests/test_api.py`, `tests/test_web_auth.py`, `tests/test_dashboard_strict_counts.py`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Предишният API отговор не излъчваше `ahead_by`, макар че синхронизаторът го изчислява; без него не можеха да се докажат числовите дефиниции. Добавено е само read-only поле в отговора, а липсващ/невалиден fork флаг вече не се превръща принудително в `false`, за да може да се докладва като data грешка. Няма промяна в discovery, класификация, synchronization safety, OAuth или PAT конфигурацията.
- **Изпълнени тестове:** `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; `python -m pytest tests/test_api.py tests/test_dashboard_strict_counts.py -q`; `python -m pytest -q --ignore=tests/test_dashboard_progress.py`; `python -m compileall -q api/routes.py`; `git diff --check`.
- **Резултат:** Targeted тестовете са `35 passed, 1 warning`, широкият suite е `407 passed, 1 warning` (StarletteDeprecationWarning), compileall мина, `git diff --check` дава само CRLF предупреждения. Първоначалният широк run хвана остарял expected response shape в `tests/test_web_auth.py`; след добавяне на `ahead_by` в очакването всички тестове минаха. Mock проверките за акаунтите дават architectquant `34 / 30 / 4 / 0` и GabrielRules `36 / 34 / 0 / 2`.
- **Оставащи проблеми:** Реална live проверка не е извършена: broker/dashboard отговарят 200, но `/api/auth/status` е 401, т.е. липсва наличен OAuth сесионен контекст. Не е използван PAT и не е стартиран login. `tests/test_dashboard_progress.py` остава блокиран от предходен `SyntaxError` на ред 223. Няма реален sync, merge, commit или push.

## 2026-11-17 18:31 - Фаза 4: визуална корекция на Dashboard
- **Извършена задача:** Dashboard-ът е доведен до завършен космически визуален стил: хедърът съдържа sky с crescent moon и звезди, акаунтът и connection статусът са под заглавието, основните бутони са в action bar под тях, статистическите карти са по-големи, а repo списъкът и адаптивните правила са преработени за 1440px, 1024px и 390px. Генерирани са реални screenshot-и на статичния shell в трите ширини.
- **Променени файлове:** `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `DASHBOARD/app.js`, `docs/screenshots/dashboard-1440.png`, `docs/screenshots/dashboard-1024.png`, `docs/screenshots/dashboard-390.png`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Да се отстрани остарелият и претрупан визуален вид без промяна в одобрената логика за броене, auth, discovery, класификация или synchronization. Снимките са направени с блокиран `app.js` само за да се избегне неавторизираното пренасочване; не са добавени fake данни.
- **Изпълнени тестове:** `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; `python -m compileall -q api/routes.py`; `python -m pytest tests/test_api.py tests/test_dashboard_strict_counts.py tests/test_web_auth.py -q`; `python -m pytest -q --ignore=tests/test_dashboard_progress.py`; `git diff --check`; headless Chrome/CDP screenshot и layout метрики при 1440px, 1024px и 390px.
- **Резултат:** Node syntax checks и compileall минаха; targeted тестовете са `68 passed, 1 warning`, широкият suite е `407 passed, 1 warning` (StarletteDeprecationWarning), `git diff --check` дава само CRLF предупреждения. Screenshot-ите са създадени; метриките показват `scrollWidth = innerWidth` и `4/4/2` колонки за counters съответно при 1440/1024/390px. Няма реален sync, merge, commit или push.
- **Оставащи проблеми:** Screenshot-ите покриват статичния shell, не авторизирани редове с реални данни. Live проверката остава блокирана от липсваща OAuth сесия (`/api/auth/status` → 401); не е използван PAT. `tests/test_dashboard_progress.py` остава блокиран от предходен `SyntaxError` на ред 223.

## 2026-11-17 20:01 - Критичен fork флаг и финален SYNC UI

- **Извършена задача:** Диагностициран и отстранен е дефектът, при който Dashboard-ът получаваше 36 записа, но отхвърляше всички като `missing/invalid fork flag` и показваше `0/0/0/0`. Коренната причина беше стар dashboard API процес (PID 22768, стартиран 16:00), докато текущият `api/routes.py` вече излъчва реалното GitHub булево поле `fork`; фронтендът правилно изисква `fork === true`. Рестартиран е само процесът на порт 8001 (нов PID 11000). Добавен е regression тест, който минава през реалния `ForkSynchronizer` и потвърждава, че fork редовете носят `fork: true`, а оригиналите се изключват. Финалният UI е проверен: само един `SYNC` бутон в hero банера, без `CHECK FORKED REPOS`, с автоматична проверка след вход и запазени safety проверки.
- **Променени файлове:** `tests/test_api.py`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`; рестартиран dashboard процесът на 8001. Предходните `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `DASHBOARD/app.js` и `DASHBOARD/dreamerol-sync-hero.png` са запазени без нови UI промени.
- **Причина:** Старият зареден Python код не съдържаше сериализацията на `fork`, а новият frontend вече третира липсващия флаг като data грешка. Не е направен fallback или предположение, който да скрие проблема; използва се само реалното GitHub метаполе.
- **Изпълнени тестове:** `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; `python -m compileall -q api/routes.py fork_sync/synchronizer.py tests/test_api.py`; focused `python -m pytest tests/test_api.py::test_dry_run_list_serializes_github_fork_flag_from_discovery tests/test_api.py::test_dry_run_list_exposes_existing_fork_property tests/test_api.py::test_dry_run_list_keeps_missing_or_invalid_fork_flags_reportable tests/test_api.py::test_dry_run_list_36_unique_repositories_total_36 tests/test_dashboard_strict_counts.py -q`; `python -m pytest -q --ignore=tests/test_dashboard_progress.py`; read-only TestClient Preview; headless Chrome/CDP layout проверки при 1440/1024/390px.
- **Резултат:** Node syntax checks и compileall минаха. Focused тестовете са `19 passed, 1 warning`; широкият suite е `408 passed, 1 warning` (StarletteDeprecationWarning). Read-only Preview върна HTTP 200 с ключове `account`, `total`, `results`, `diagnostics`; 36 реда, всички с `fork: true`, diagnostics `36/36/36/0`; frontend helper-ите дадоха 0 fork flag грешки и reconcile `36 = 34 + 0 + 2` за проверения статусен сценарий. Публичните GitHub метаданни за GabrielRules показват 36 репозитории, 36 с `fork: true` и 36 с валиден `parent`. CDP проверките потвърдиха един `SYNC` бутон, нулеви `CHECK FORKED REPOS`, центриране в hero и липса на horizontal overflow при трите ширини. Няма реален sync, merge, commit или push.
- **Оставащи проблеми:** Няма валидна OAuth сесия (`/api/auth/status` → 401), затова не е уловен реален авторизиран Network payload; проверката е чрез публични GitHub метаданни и read-only TestClient Preview. По-ранната бележка за 34 fork-а и 2 оригинала не е потвърдена от текущите публични метаданни. `tests/test_dashboard_progress.py` остава блокиран от предходен `SyntaxError` на ред 223.

## 2026-11-17 20:30 - Корекция: failed checks не са UNSYNCABLE

- **Извършена задача:** Отстранена е причината за обратния вид на GabrielRules броячите (`2 UP TO DATE / 34 UNSYNCABLE` вместо очакваните `34 / 2`). Неуспешните или непотвърдените per-repo проверки вече са отделно състояние `CHECK FAILED / UNVERIFIED`, не се влагат в потвърдено `UNSYNCABLE`, и не позволяват показване на финалните четири числа. Последното известно успешно състояние остава видимо като `(LAST KNOWN)`, но също маркира числата като непълни.
- **Променени файлове:** `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `DASHBOARD/dashboard.css`, `tests/test_dashboard_strict_counts.py`, `tests/test_dashboard_progress.py`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Коренната причина не беше разместена асиметрия в `ahead_by`/`behind_by` или обърнат aggregation, а това, че list режимът връща `pending` без сравнителни данни, а последващите `preview_error`/`unknown`/`error` проверки се влагаха в `UNSYNCABLE`. Това превръщаше временни проверки/permissions/rate-limit грешки в погрешно потвърдени UNSYNCABLE fork-ове.
- **Изпълнени тестове:** `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; `git diff --check -- DASHBOARD/app.js DASHBOARD/dashboard.css DASHBOARD/utils.js tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py`; `python -m pytest -q`; inline `node --input-type=module` helper проверка за пълни данни и за 34 неуспешни проверки.
- **Резултат:** Node syntax checks и `git diff --check` минаха. `python -m pytest -q` → `428 passed, 1 warning` (StarletteDeprecationWarning); предходният SyntaxError в `tests/test_dashboard_progress.py` е отстранен и целият suite вече се изпълнява. Inline проверката даде `36 / 34 UP TO DATE / 0 TO BE SYNCED / 2 UNSYNCABLE, complete=true` при пълни числови данни и `36 / 0 / 0 / 2` с `34 check errors, complete=false` при масови неуспешни проверки. Няма промени в OAuth, API contract, discovery, Compare/Merge или synchronization логиката; няма реален Sync, commit или push.
- **Оставащи проблеми:** Реална авторизирана проверка все още не е извършена — `/api/auth/status` връща 401, затова историческото `34/2` не е потвърдено срещу live per-repo comparison payload в тази сесия. Нужна е ръчна браузърна проверка с валидна OAuth сесия; при timeout/401/429/502 редовете трябва да са `CHECK FAILED / UNVERIFIED`, не `UNSYNCABLE`.

## 2026-11-18 03:11 - Security hardening преди публичен release

- **Извършена задача:** Приложен е одобреният minimal release-hardening пакет след Phase 2 security audit: конфигурируем `COOKIE_SECURE`, CSRF Origin/Referer проверка за state-changing `/api/*` POST заявки, redaction на OAuth callback `code`/`state` в uvicorn access логовете, periodic cleanup на изтекли Broker транзакции, `openapi_url=None`, browser security headers и премахване на hardcoded `http://127.0.0.1:8001` URL-и от frontend-а.
- **Променени файлове:** `api/app.py`, `api/routes.py`, `auth_broker/app.py`, `web/app.js`, `DASHBOARD/app.js`, `DASHBOARD/index.html`, `.env.example`, `tests/test_web_auth.py`, `tests/test_auth_broker_api.py`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `DECISIONS.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Audit-ът установи публично-достъпни слаби места в cookie Secure логиката, липсваща CSRF проверка, HTTP downgrade и експозиция на callback secrets в access логовете; целта беше минимална корекция без промяна на одобрения Dashboard и безrewrite на OAuth/sync логиката.
- **Изпълнени тестове:** `python -m pytest -q`; `node --check web/app.js`; `node --check DASHBOARD/app.js`; `git diff --check`; CDP `verify-dropdown-result.cjs`, `verify-brand-link.cjs`, `verify-branding.cjs`, `measure-status-alignment.cjs`.
- **Резултат:** `python -m pytest -q` → `434 passed, 1 warning` (StarletteDeprecationWarning); node syntax checks → OK; `git diff --check` → само LF→CRLF warnings; CDP проверките → всички checks `true`, включително `signInHrefOriginRelative`. Няма реален Sync, commit или push.
- **Оставащи проблеми:** Няма валидна OAuth сесия (`/api/auth/status` → 401), затова live browser flow не е повторен след hardening-а. Реалните GitHub App permissions, callback и installation трябва да се потвърдят в GitHub UI; Phase 3 synchronization safety review остава неизпълнен.

## 2026-11-18 04:02 - Phase 6 Release readiness корекции

- **Извършена задача:** Приложени са одобрените release readiness корекции: стандартен MIT `LICENSE` без не-мит лицензионен текст, неутрализиран текст за собственост в `COPYRIGHT.md`, Python 3.11 минимум в README/`scripts/check.ps1` и CI matrix 3.11/3.12, разширени JS syntax checks в CI и премахнати подвеждащи PAT fallback инструкции за браузъра от README.
- **Променени файлове:** `LICENSE`, `COPYRIGHT.md`, `README.md`, `.github/workflows/tests.yml`, `scripts/check.ps1`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `docs/WORKLOG/WORKLOG.md`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/development/CHANGELOG_AI.md`. Локално е създаден само игнорираният `.venv`.
- **Причина:** Публичният release изисква MIT-only лиценз, съвместимост с `httpx2==2.16.0`, последователни проверки и коректна документация без втора браузърна authentication mechanism.
- **Изпълнени тестове:** `.venv\Scripts\python.exe -m pip check`; `.venv\Scripts\python.exe -c "import httpx2; print(...)"`; `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`; tokenize-aware Python compile на 39 файла; `node --check web/app.js`; `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; PowerShell AST parse на `scripts/*.ps1`; `git diff --check`.
- **Резултат:** `pip check` → `No broken requirements found`; `httpx2==2.16.0` → импортиран успешно; pytest → `453 passed in 5.40s` без warnings; Python compile → OK за 39 файла; JS checks → OK; PowerShell parse → OK; `git diff --check` → само LF→CRLF предупреждения, без whitespace грешки. Няма commit, push или реален Sync.
- **Оставащи проблеми:** Няма валидна OAuth сесия; реални GitHub App callback/permissions/installation и реален Sync остават непроверени. `.env` съдържа credential типове, които изискват ръчна ротация без показване на стойности. Сесиите са in-memory, липсва отделен CSRF token, token expiration изисква потвърден opt-out или refresh-token работа.

## 2026-11-18 05:12 - Две sync действия в Dashboard

- **Извършена задача:** Добавени са green `SYNC CHOSEN` и red `SYNC ALL` в компактна responsive група. `SYNC ALL` е с възстановени оригинален текст и размер (32px desktop / 26px mobile); добавени са брояч на `READY TO SYNC` forks, отделни потвърждения, празни selection guard-и и блокиране на двата бутона по време на preview/sync.
- **Променени файлове:** `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `DASHBOARD/app.js`, `tests/test_dashboard_progress.py`, `docs/WORKLOG/END_OF_DAY_2026-11-18.md`, `docs/WORKLOG/WORKLOG.md`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Потребителят поиска отделни действия за избрани и за всички eligible fork-ове, с по-compakt подредба и запазени съществуващи sync safeguards.
- **Изпълнени тестове:** `python -m pytest tests/test_dashboard_progress.py -q`; `python -m pytest -q`; `node --check DASHBOARD/app.js`; `node --check DASHBOARD/utils.js`; `git diff --check`; CDP `verify-sync-action-group.cjs` при 1440×1200 и 390×844.
- **Резултат:** targeted `23 passed`; пълен pytest `457 passed, 1 warning in 5.71s`; JS syntax OK; `scripts/check.ps1 -SkipTests` → `All checks passed`; `git diff --check` без whitespace грешки (само CRLF предупреждения). CDP проверките за етикети, ред, брояч, 32/26px, еднакви височини, 12px desktop gap, mobile stacking, green/red палитри, 7-слоен текст-сянка, липса на stroke и липса на overflow са `true`. Няма реален Sync, commit или push.
- **Оставащи проблеми:** Няма валидна OAuth сесия; реалният OAuth поток, read-only preview и реален Sync остават непроверени. Моделът не може визуално да инспектира screenshot-ите; потребителят трябва да потвърди крайния вид на око. `.env`, GitHub App настройките и credentials не са променяни.

## 2026-11-18 20:00 - Минимална поправка на сесията и 403 при `/api/sync`

- **Извършена задача:** Премахнато е излишното `GET /user` при всяко `/api/sync`; използва се вече валидираният акаунт от сесията. Сесията и browser cookie-то се удължават при активност, а GitHub 401 изчиства сървърната сесия/cookie и връща `REAUTH_REQUIRED` чрез структурирана грешка.
- **Променени файлове:** `api/auth.py`, `api/routes.py`, `tests/test_web_auth.py`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** След валиден OAuth login targeted dry-run за `GabrielRules/TEST` връщаше 403 именно от `GET /user` преди сравнението, въпреки че акаунтът вече е потвърден при login. Целта беше най-малката безопасна промяна без GitHub App настройки, нови credentials или реален Sync.
- **Изпълнени тестове:** targeted `python -m pytest -q -p no:cacheprovider tests/test_web_auth.py tests/test_api.py`; пълен `python -m pytest -q -p no:cacheprovider`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check.ps1`; `git status`, `git diff --check`, `git diff --stat`.
- **Резултат:** targeted `72 passed`; пълен pytest `461 passed in 4.62s`; `scripts/check.ps1` → `All checks passed` с `461 passed, 1 warning` (StarletteDeprecationWarning); `git diff --check` → само LF→CRLF предупреждения. Няма commit, push, реален Sync или промяна в GitHub App/credentials.
- **Оставащи проблеми:** Live ефектът върху 403 не е проверен след промяната — нужен е нов targeted `dry_run:true` през контролирания Chrome. Ако 403 остане при сравнението, следващата стъпка са Installation Access Tokens с App private key, което изисква отделно одобрение.

## 2026-11-18 20:11 - Live потвърждение на поправката за 403

- **Извършена задача:** Рестартиран е smoke стекът с `-Force`, стартиран е контролираният Chrome на CDP порт `9224`, направен е нов OAuth login и е изпълнен само read-only targeted `dry_run:true` за `GabrielRules/TEST`.
- **Променени файлове:** `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Да се потвърди на живо, че премахнатото `GET /user` в `/api/sync` е решило 403, наблюдаван след валиден OAuth login.
- **Изпълнени тестове:** `verify-login.mjs`; `targeted-test-preview.mjs`; `check-test-current-state.mjs`. По-рано в същата задача: targeted pytest `72 passed`, пълен pytest `461 passed`, `scripts/check.ps1` → `All checks passed`.
- **Резултат:** `/api/auth/status` → `200 AUTHENTICATED` с очакван акаунт; targeted preview → HTTP `200`, `status: behind`, `message: 3 upstream commit(s) available.`, `behind_by: 3`, `ahead_by: 0`. Commit-ите остават `0c82ac0` (original) и `42212b1` (fork). Няма реален Sync, commit, push или GitHub App промени.
- **Оставащи проблеми:** Реалният Sync (`dry_run:false`) не е изпълван и изисква отделно изрично одобрение. Installation Access Tokens не са нужни за този конкретен 403, но остават опция при future token expiration/401.

## 2026-11-18 20:14 - Реален Sync за GabrielRules/TEST

- **Извършена задача:** След изрично одобрение е изпълнен реален Sync (`dry_run:false`) само за избрания fork `GabrielRules/TEST`, с валидна OAuth сесия.
- **Променени файлове:** `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`.
- **Причина:** Да се потвърди, че поправката в `/api/sync` работи не само за read-only preview, но и за одобрения мутиращ Sync път.
- **Изпълнени тестове:** `live-sync-test.mjs` (guard за `AUTHENTICATED` + `account === 'GabrielRules'`), `check-test-current-state.mjs`, преглед на `broker.err.log` и `dashboard.err.log`.
- **Резултат:** API върна HTTP `200`, `status: synced`, `message: Synced 3 upstream commits.`, `behind_by: 3`, `ahead_by: 0`, `last_successful_sync: 2026-11-18T18:13:46Z`. GitHub UI показва fork-а на `0c82ac0` и `This branch is up to date with architectquant/TEST:main.`; originalът остава `0c82ac0`. Няма локален commit, push или GitHub App промени; логовете са без грешки.
- **Оставащи проблеми:** Локално остават 6 uncommitted файла от поправката и документацията. Commit/push изискват отделно одобрение; допълнителен Sync — само след нов одобрен dry-run.

