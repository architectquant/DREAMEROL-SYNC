# DECISIONS

## Съществуващи архитектурни решения

### 2026-11-13 - Server-side Auth Broker сесии
- **Решение:** `WebAuthManager` пази Broker polling secret-а и GitHub credential-а в паметта на API процеса.
- **Причина:** Браузърът не трябва да получава GitHub token; cookie-то съдържа само непрозрачен session ID.
- **Последица:** Сесиите не се споделят между workers и се губят при рестарт.

### 2026-11-13 - HttpOnly session cookie
- **Решение:** Браузърът получава `dreamerol_session` с `HttpOnly`, `SameSite=Lax`, `Path=/`, `Max-Age=600` и `Secure` при HTTPS.
- **Причина:** Намалява риска от кражба на сесията чрез JavaScript и ограничава CSRF векторите.
- **Последица:** Session TTL е 10 минути; при нужда от по-дълги сесии TTL трябва да се промени съзнателно.

### 2026-11-13 - Валидация преди Broker ACK
- **Решение:** Credential-ът от Broker се валидира чрез `GitHubClient.get_authenticated_user()` преди да бъде запазен; Broker ACK е best-effort след успешна валидация.
- **Причина:** Невалиден GitHub credential не трябва да се приема или потвърждава.
- **Последица:** При неуспешен ACK credential-ът може да остане валиден в сесията, но Broker транзакцията не е потвърдена.

### 2026-11-13 - Bearer token с приоритет пред cookie
- **Решение:** `/api/sync` приема `Authorization: Bearer <token>` или session cookie; при наличие на Bearer той има приоритет.
- **Причина:** Запазва съвместимостта с ръчния PAT fallback и позволява явно избиране на credential.
- **Последица:** Клиент с невалиден Bearer не fallback-ва автоматично към cookie.

### 2026-11-13 - Ръчен PAT fallback
- **Решение:** Dashboard-ът запазва форма за ръчен GitHub PAT, когато Broker не е достъпен.
- **Причина:** Локалната разработка и среди без GitHub App не трябва да остават без вход.
- **Последица:** PAT се пази само в паметта на браузъра и се изпраща към локалния API.

## Нови решения в текущия етап

### 2026-11-14 - Broker зарежда `.env` при фабрично стартиране
- **Решение:** `create_app()` вика `load_dotenv()` само когато не е подаден явен `BrokerConfig`.
- **Причина:** `uvicorn auth_broker.app:create_app --factory` да работи директно с локален `.env`, без ръчно експортиране на променливите.
- **Последица:** При явен конфиг `.env` не се чете; тестовете и вграждането с собствен конфиг остават изолирани.

### 2026-11-14 - Security baseline за web auth API
- **Решение:** Всички `/api/` отговори са `Cache-Control: no-store`; state-changing endpoints приемат само `POST`; сесийната cookie е `HttpOnly`, `SameSite=Lax`, `Secure` при HTTPS; невалиден Bearer token не fallback-ва към cookie.
- **Причина:** Намалява CSRF, cache leakage и случайно смесване на credential източници.
- **Последица:** Няма отделен CSRF token във v1; защитата разчита на `SameSite=Lax` и POST-only. При публично exposure може да се добави token. Зад HTTPS proxy е нужен `--proxy-headers`, за да се маркира cookie-то като `Secure`.

### 2026-11-14 - Broker зад локален cloudflared
- **Решение:** `BROKER_TRUSTED_PROXIES=127.0.0.1,::1` за локален cloudflared tunnel; всички `/auth/` отговори получават `no-store`, `Pragma: no-cache`, `Referrer-Policy: no-referrer` и `X-Content-Type-Options: nosniff`.
- **Причина:** Правилен client IP за rate limiting и предотвратява caching на auth отговори.
- **Последица:** `X-Forwarded-For` се доверява само от localhost; при друг proxy адресът трябва да се обнови.
- **Статус:** Заменено от решението от 2026-11-15 за локален loopback callback.

### 2026-11-14 - Mock GitHub OAuth provider за E2E тестове
- **Решение:** Тестовете използват локален fake GitHub OAuth provider, който валидира PKCE S256, client credentials и code exchange.
- **Причина:** Пълният flow може да се тества без реални GitHub App credentials и без външна зависимост.
- **Последица:** Fake provider-ът не замества реален GitHub smoke test; той покрива само протокола и Broker логиката.

### 2026-11-14 - Broker health endpoint и watchdog
- **Решение:** Broker има `GET /healthz`; `watch-smoke.ps1` проверява health и рестартира само Broker-а на същия порт и тунел. Dashboard и cloudflared само се докладват.
- **Причина:** Broker може да спре неочаквано и да остави тунела с 502; рестартът на cloudflared би сменил публичния callback URL.
- **Последица:** Watchdog-ът не възстановява dashboard/cloudflared автоматично; при техен проблем е нужен ръчен рестарт през `start-smoke.ps1`.
- **Статус:** Заменено от решението от 2026-11-15; watchdog-ът вече рестартира Broker и dashboard на loopback портове, без тунел.

### 2026-11-15 - Локален loopback callback вместо Quick Tunnel
- **Решение:** За локална single-user инсталация GitHub App callback-ът е фиксиран на `http://127.0.0.1:8000/auth/callback`; Broker и dashboard слушат само на `127.0.0.1`. HTTP се допуска само за loopback hosts (`127.0.0.1`, `::1`, `localhost`), а всички други deployment-и изискват HTTPS.
- **Причина:** Quick Tunnel URL-ът е ephemeral и всяко рестартиране изисква ръчна промяна в GitHub App, което причинява `redirect_uri_mismatch` или мъртъв callback. GitHub поддържа loopback callback за локални GitHub App приложения; това е най-малката стабилна промяна без rewrite на OAuth логиката.
- **Последица:** `start-smoke.ps1` не стартира тунел и не пренаписва `.env`; GitHub App callback-ът се задава еднократно, wildcard matching се изключва. Отдалечен достъп изисква отделен стабилен HTTPS tunnel/proxy, а не Quick Tunnel. Портът `8000` става част от фиксирания callback договор.

### 2026-11-16 - Диагностика и стабилизиране на Preview (нестабилни/празни резултати)
- **Контекст:** Наблюдава се нестабилно поведение: понякога \Preview complete\ с 0/0/0/0 (list връща празен набор) и понякога 34 репота с масови временни \check failed\ (unknown, запазени броячи), вероятно зависимо от активния акаунт/токен и достъпа/отговора на GitHub за \/user/repos\ и per-repo compare заявките.
- **Решение (предложение, без незабавна промяна на Sync/compare/merge):** (1) да се потвърди чрез Network отговорът на \POST /api/sync\ \mode:"list"\ (\ccount/status/total/results\) и на per-repo заявките при частични провали; (2) да се добави минимална read-only диагностика в list отговора (брой owned репа, fork-ове, с валиден parent/upstream) без изтичане на тайни; (3) при масови временни грешки (напр. 429/502) да се въведат ограничен retry/backoff и/или по-нисък preview concurrency и неутрален/предупредителен тон, когато preview е завършил само с временни провали и запазени статуси; (4) да се провери стабилността на активния акаунт/сесия и GitHub App installation/repo grants.
- **Причина:** да се локализира дали проблемът е в изброяването/достъпа/контекста или във временни API грешки, без да се маскира със UI и без риск за данни.
- **Последици/ограничения:** не променя Sync/Compare/Merge алгоритъма и безопасните проверки; не изисква реален Sync, промени в GitHub настройки/репозитория, изтриване на история/credentials или commit/push. За визуално потвърждение на вече направените UI фиксове е нужен рестарт/презареждане на smoke.

### 2026-11-17 - Четири fork-only counters в Dashboard
- **Решение:** Dashboard показва TOTAL FORKS, UP TO DATE, TO BE SYNCED и UNSYNCABLE само за репозитории със съществуващо GitHub поле `fork: true`; AHEAD-only остава явно видима подкатегория в UNSYNCABLE. List режимът на `/api/sync` включва полето `fork`; другите режими не променят формата на отговора си.
- **Причина:** Потребителят уточни, че 36-те реда в list отговора включват 34 fork-а и 2 оригинални репозитория, които не трябва да се броят; броенето трябва да ползва вече наличните GitHub данни без нова discovery логика.
- **Последица:** Променени са само API сериализацията за list режима и frontend представянето/броенето/filter-ите; discovery, fork класификацията, synchronization логиката, OAuth и auth остават непокътнати. Synced/синхронизируемите репозитории са дефинирани само за fork-ове; diverged и AHEAD-only остават извън автоматична синхронизация.

### 2026-11-18 - Release hardening defaults за web/auth
- **Решение:** `COOKIE_SECURE` по подразбиране е `auto` (scheme-based поведение за loopback), с изрични `true`/`false`; state-changing `/api/*` заявките проверяват Origin/Referer само когато е изпратен такъв header; frontend URL-ите са origin-relative; Broker redact-ва `code`/`state` в access логовете и почиства изтекли транзакции на всеки 60s.
- **Причина:** Публичното exposure изисква по-строги cookie/CSRF/log defaults, но локалният loopback single-user сценарий трябва да продължи да работи без HTTPS и без допълнителна конфигурация.
- **Последица:** Клиенти без Origin/Referer (CLI, TestClient) не се блокират; крос-сайт POST с Origin към друг host се връща 403. Cookie Secure при HTTPS proxy изисква `COOKIE_SECURE=true` или коректно `X-Forwarded-Proto`; HSTS и CSP се добавят само като headers, без промяна на OAuth/sync логиката.

### 2026-11-18 - MIT-only лиценз, Python 3.11 минимум и премахване на PAT fallback инструкциите
- **Решение:** Проектът се разпространява само под стандартния MIT License; минималната поддържана версия е Python 3.11 поради `httpx2==2.16.0`; README вече не обещава форма за ръчен PAT на welcome страницата; CI и локалната environment проверка проверяват версията на Python и трите JS файла.
- **Причина:** Изискваше се правна и техническа консистентност за публичен release без платени функции, без unsupported ownership claims и без подвеждаща second authentication mechanism.
- **Последица:** `LICENSE`, `COPYRIGHT.md` и README са синхронизирани; Python 3.10 не е поддържан; API Bearer поддръжката остава само за програмни клиенти, но не е описана като браузърен fallback. OAuth, sync логиката и GitHub настройките не са променяни.

### 2026-11-18 - PR към architectquant без изчистване на repo
- **Решение:** Не се изчиства `architectquant/DREAMEROL-SYNC` до 2–3 файла преди PR. Запазва се пълният проект, а единственият конфликт в `README.md` се решава чрез merge commit, като се запазва текущата версия на README.
- **Причина:** По-малкият base би намалил само броя на потенциалните конфликти, но би въвел нов голям destructive diff и риск от изтриване на нужни файлове. След локално установен единичен конфликт изчистването не дава допълнителна полза.
- **Последица:** PR #1 остава с пълния проект; `architectquant/main` не се променя извън стандартния merge на PR. Изчистване би се правило само на отделен клон с backup и изрично посочени файлове.

### 2026-11-21 - Batch read-only проверка в Dashboard вместо 35 отделни заявки
- **Контекст:** При валидна сесия на `architectquant` автоматичният check завърши `35/35 complete ... 35 unverified` и броячите останаха `35/0/0/0`, докато read-only `/api/debug/compare-forks` за 4 репозитория върна `VERIFIED_FRESH` (3 up-to-date, 1 behind). `DASHBOARD/app.js:682-686` изпраща по един `POST /api/sync` на fork; `api/routes.py:372` за всяка заявка вика отново `get_forks()`, т.е. 71 GitHub GET базово (до 1296 при липсващи parent метаданни).
- **Решение:** Одобрена е frontend-only промяна: `runBackgroundChecks()` да изпраща всички forks в един `POST /api/sync {dry_run:true, repositories:[...]}` (или 4 парчета по 10, ако се запази междинен прогрес). Backend вече приема списък и прави `get_forks()` веднъж. Не се променят `api/routes.py`, Sync/Compare/Merge, OAuth, counters или история.
- **Причина:** Намалява GitHub заявките от 71 на 36 (worst 1296 на 71) и премахва повторната discovery като най-вероятна причина за масови 403/rate limit; това е най-малката промяна без риск за защитените компоненти.
- **Последица:** При един batch липсва прогресивно обновяване по репо — статусът и броячите се обновяват след целия отговор. Алтернативата с 4×10 запазва частичен прогрес с 39 GET базово.
- **Статус:** Одобрено от потребителя на 2026-11-21 02:50; **не е изпълнено**. Насрочено за 2026-11-22 с read-only потвърждение на съобщението за грешка, регресионен тест, `node --check`, targeted и пълен pytest и браузърна проверка без реален Sync. SYNC не се прави без отделно одобрение; без commit/push.
