# WORKLOG

## 2026-11-22 19:14 - PR #2 създаден и подготвен за merge
- **Date/time:** 2026-11-22 19:14 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/repository-refresh-20261122` @ `eb2f457`, синхронизиран с `origin`.
- **Last completed:** Push към `GabrielRules` и създаване на PR #2 `Complete Repository Refresh — DREAMEROL-SYNC` → `architectquant:main`. Добавен е `docs/DREAMEROL_SYNC_TECHNICAL_DOC.md` по изрично одобрение. Конфликтът след преместване на базата на `df05316` е решен с `git merge -s ours`; локалното дърво е непроменено.
- **State:** PR `open`, `mergeable:true`, `mergeable_state:clean`. Diff: 3 commit-а, 44 файла, `+14353/-414`, `0` изтрити файла. Няма изтрити файлове спрямо базата; `.env`, `.venv`, логове, кешове и secrets не са в PR-а. MERGE НЕ е извършван.
- **Tests:** Локално `compileall`, 3× `node --check`, PowerShell parse, `pip check` → OK; pytest `506 passed in 8.11s`. GitHub Actions: 0 check runs / `status:pending` за PR #2.
- **Known issues/blockers:** Няма write достъп до `architectquant` с наличните credential-и (`GabrielRules` токен: push=false; `.env` токенът е за `Dreamerol`). Merge трябва да се направи от страницата на PR #2 от потребител с права.
- **Next exact step:** Изчакване на потвърждение от потребителя за MERGE; след това проверка на endpoint-а и fetch на `architectquant/main`. БЕЗ автоматичен merge.

## 2026-11-22 19:00 - Подготовка на PR за пълно обновяване на architectquant repository
- **Date/time:** 2026-11-22 19:00 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch:** `feature/repository-refresh-20261122`, създаден от актуалния `architectquant/main` (`3c93bb0`).
- **Last completed:** Локалното съдържание от `9102af4` е приложено върху клона; 43 файла са индексирани. Трите локално изтрити screenshots остават извън PR. Няма изтрити файлове спрямо `architectquant/main`.
- **State:** Изключени са `.env`, `.venv`, `__pycache__`, `.pytest_cache`, `node_modules`, логове, временни файлове, `data/sync_history.json` и локални credentials. Сканирането за secrets не откри реални стойности. Push и PR предстоят; MERGE не е извършван.
- **Tests:** `compileall`, `node --check` (3 файла), PowerShell parse и `pip check` → без грешки; `506 passed in 8.11s`.
- **Known issues/blockers:** Няма write достъп до `architectquant/DREAMEROL-SYNC`; ще се пусне клонът от `GabrielRules/DREAMEROL-SYNC` и ще се създаде PR към `architectquant:main`.
- **Next exact step:** Push на клона, създаване на PR, проверка на CI и изчакване на потвърждение от потребителя за MERGE.

## 2026-11-22 18:14 - Край на сесията: пълен запис
- **Date/time:** 2026-11-22 18:14 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch:** `feature/github-app-auth`.
- **Last completed:** Край на работната сесия. Проверени са `git status`, 7 променени и 6 untracked файла (общо 13), пълнотата на двата WORKLOG файла и `.env` (игнориран, не е в commit). Създава се локален commit `chore: save work session 2026-11-22`.
- **State:** Всички днешни промени и нови файлове са записани на диска и включени в commit. Няма push, merge или реален Sync.
- **Tests:** Пълен pytest → `506 passed in 7.67s`.
- **Known issues/blockers:** Няма.
- **Next exact step:** Край на сесията. Без допълнителни промени без изрично одобрение.

## 2026-11-22 18:08 - Стабилизиране на dashboard бутоните при скрол
- **Date/time:** 2026-11-22 18:08 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch:** `feature/github-app-auth`; локалният commit `cfbb3dd` остава, след това има нови неcommitted промени.
- **Last completed:** CDP проверка в чист профил доказа, че стиловете на dashboard бутоните не се променят при скрол. Вдигнат е само cache-bust на `dashboard.css` → `20261122s`, за да се зареди пресен CSS в основния Chrome.
- **State:** Променени са `DASHBOARD/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла. CSS стойности, auth и логика не са пипани.
- **Tests:** `dashboard.css?v=20261122s` → `200`; targeted `1 passed`, full `506 passed`.
- **Known issues/blockers:** Ако сивите бутони се появят отново, вероятен източник е разширение/външен dark-mode стил в основния Chrome профил, не приложението.
- **Next exact step:** Потребителят да потвърди в отворения Chrome. Без commit/push без изрично одобрение.

## 2026-11-22 18:01 - Един ред на бутона и стартиран Broker
- **Date/time:** 2026-11-22 18:01 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch:** `feature/github-app-auth`; локалният commit `cfbb3dd` остава, след това има нови неcommitted промени.
- **Last completed:** Добавен е `white-space: nowrap` за `.button-label`, за да не се превива `Sign in with GitHub`. Стартиран е локалният Auth Broker на порт 8000 със съществуващия `.env`.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122r`. Auth логиката, OAuth и backend кодът не са променяни.
- **Tests:** `POST /auth/start` → `422` (alive), `POST /api/auth/start` → `200`; targeted `1 passed`, full `506 passed`. CDP при 1440x900, 375x812 и 1024x768: `labelLines=1`, `labelWhiteSpace=nowrap`, бутон `400x92`.
- **Known issues/blockers:** Broker-ът е само локално стартиран.process; ако се рестартира машината/сървърът, трябва да се стартира отново.
- **Next exact step:** Потребителят да потвърди в Chrome. Без commit/push без изрично одобрение.

## 2026-11-22 17:55 - Обновен dashboard banner
- **Date/time:** 2026-11-22 17:55 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch:** `feature/github-app-auth`; локалният commit от 17:41 (`cfbb3dd`) остава, след това има нови неcommitted промени.
- **Last completed:** Потребителят замени `DASHBOARD/dreamerol-sync-hero.png` с по-високо качество със същото име. Добавен е cache-bust `?v=20261122q` в `DASHBOARD/index.html` и dashboardът е отворен в Chrome.
- **State:** Променени са `DASHBOARD/index.html` и двата worklog файла; самият PNG не е редактиран от модела. `assets/dreamerol-sync-hero.png` остава непокътнат.
- **Tests:** `GET /dashboard/static/dreamerol-sync-hero.png?v=20261122q` → `200 image/png`; SHA256 на обслужения отговор съвпада с файла в `DASHBOARD/`.
- **Known issues/blockers:** Няма.
- **Next exact step:** Потребителят да потвърди визуално в отворения Chrome. Без commit/push без изрично одобрение.

## 2026-11-22 17:41 - Одобреният изглед е запазен локално
- **Date/time:** 2026-11-22 17:41 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch:** `feature/github-app-auth`.
- **Last completed:** Потребителят потвърди настоящия Welcome изглед като финален и поиска само запазване без промени. Създава се локален commit с вече одобрените `web/style.css`, `web/index.html`, `web/assets/hero-welcome.jpg`, `tests/test_dashboard_workflow.py` и двата worklog файла.
- **State:** Без визуални промени. Изображението, auth потокът, OAuth, API и backend логиката не са пипани.
- **Tests:** Последни реални проверки от 17:39: целеви тест `1 passed`, пълен pytest `506 passed`, CDP `subtitleHeadingCenterMatch=true`, бутон `400x92`, банер `880x586`, `POST /api/auth/start` запазен.
- **Known issues/blockers:** Няма.
- **Next exact step:** Без по-нататъшни промени без изрично одобрение. Няма push, merge или реален Sync.

## 2026-11-22 17:39 - Tagline без крайна точка
- **Date/time:** 2026-11-22 17:39 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Tagline-ът е `Click. Any fork. Always up-to-date` без последна точка. Центриран е по една ос със заглавието (`headingCenterX=712`, `subtitleCenterX=712` desktop; `188`/`188` mobile).
- **State:** Променени са `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла. Размер, тежест, цвят, вертикална позиция и останалият дизайн не са пипани; cache-bust остава `20261122p`.
- **Tests:** Целевият Welcome тест → `1 passed in 0.34s`; пълен pytest → `506 passed in 7.81s`. CDP: `subtitleHeadingCenterMatch=true`, `fontWeight=600`, `fontSize=27.5px`/`24px`, бутон `400x92`, без horizontal scroll, `POST /api/auth/start` запазен.
- **Known issues/blockers:** Няма.
- **Next exact step:** Потребителят да потвърди след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:24 - Tagline semibold
- **Date/time:** 2026-11-22 17:24 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Добавен е `font-weight: 600` само към tagline-а `Click. Any fork. Always up-to-date.`. Всичко останало е непроменено.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122p`.
- **Tests:** Целевият Welcome тест → `1 passed in 0.32s`; пълен pytest → `506 passed in 7.72s`. CDP: `subtitleFontWeight=600`, размер/цвят/позиция същите, бутон `400x92`, банер `880x586`, без horizontal scroll, `POST /api/auth/start` запазен.
- **Known issues/blockers:** Няма.
- **Next exact step:** Потребителят да потвърди след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:21 - Финален субтилен UI polish
- **Date/time:** 2026-11-22 17:21 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Пет минимални корекции: по-мека/по-широка radial mask за безшевено сливане на banner фона, tagline `27.5px` desktop, `Not signed in.` `21px`/`#d0dcf2` и по-голям долен padding на картата (`56px`/`44px`). Лого, размери на банер/карта/бутон, останали цветове и подравняване са непроменени.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122o`. Auth логиката и изображението не са пипани.
- **Tests:** Целевият Welcome тест → `1 passed in 0.34s`; пълен pytest → `506 passed in 7.70s`. CDP: subtitle `27.5px`, status `21px`/`rgb(208,220,242)`, padding-bottom `56px`, hero `880x586`, карта `880x438`, бутон `400x92`, ширините съвпадат, `POST /api/auth/start` запазен, без horizontal scroll.
- **Known issues/blockers:** Няма.
- **Next exact step:** Потребителят да потвърди финалния polish след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:16 - Потвърден 880px горен банер
- **Date/time:** 2026-11-22 17:16 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Банерът беше временно разширен до цяла ширина (1361px), но по оплакване на потребителя е върнат `max-width: 880px` на `.welcome-shell`. Картата остава `width: 100%; max-width: none`, за да е с еднаква ширина с банера. Потребителят потвърди изгледа (`Stana`).
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122n`. Текстовете, бутонът `400x92`, иконката `34x34`, цветовете и auth логиката са непроменени.
- **Tests:** Целевият Welcome тест → `1 passed in 0.32s`; пълен pytest → `506 passed in 5.92s`. CDP desktop: hero `880x586`, карта `880x425`, ширините съвпадат, бутон `400x92`, без horizontal scroll, `POST /api/auth/start` запазен.
- **Known issues/blockers:** Няма.
- **Next exact step:** Няма активна задача. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:10 - GitHub иконка и текст 34px
- **Date/time:** 2026-11-22 17:10 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** GitHub иконката и текстът на бутона са изравнени на 34px — максималният размер, който се побира в 400px бутон. Бутонът е `400x92`; на мобилен двата елемента са 22px, за да няма превиване. Auth логиката не е пипана.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122l`.
- **Tests:** Целевият Welcome тест → `1 passed in 0.33s`; пълен pytest → `506 passed in 6.05s`. CDP desktop: иконка `34x34`, шрифт `34px`, бутон `400x92`, етикет `313px` без превиване; mobile: `22px`/`279x72`. `POST /api/auth/start` запазен.
- **Known issues/blockers:** Няма нови. Вертикалният скрол на PC остава от предходното 1.5x мащабиране.
- **Next exact step:** Потребителят да потвърди размера след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:08 - Долен Welcome блок 1.5x
- **Date/time:** 2026-11-22 17:08 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Целият долен блок е мащабиран 1.5x — карта `501x405`, заглавие `60px`, подзаглавие `25.5px`, бутон `400x72` с шрифт `22.5px` и иконка `30x30`, gap преди бутона `45px`. На mobile бутонът е намален само за тесен екран, за да не се превива текстът. Banner изображението и auth логиката остават непроменени.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122j`.
- **Tests:** Целевият Welcome тест → `1 passed in 0.35s`; пълен pytest → `506 passed in 5.94s`. CDP desktop: карта `501x405`, бутон `400x72`, hero `880x586`, без horizontal scroll, `POST /api/auth/start` запазен. CDP mobile: бутон `279x72` без превиване.
- **Known issues/blockers:** При 1440x900 по-високият блок вече скролва вертикално; хоризонтален скрол няма. Това е очаквано след 1.5x мащабиране.
- **Next exact step:** Потребителят да потвърди новия мащаб след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:02 - Разстояние преди Sign in with GitHub
- **Date/time:** 2026-11-22 17:02 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Добавено е 30px разстояние между подзаглавието и green бутона (`margin: 10px 0 30px`). Всичко останало — banner, карта, typography, auth — е непроменено.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122h`.
- **Tests:** Целевият Welcome тест → `1 passed in 0.32s`; пълен pytest → `506 passed in 5.86s`. CDP: `subtitleButtonGap=30` desktop/mobile, PC центриране запазено, `POST /api/auth/start` непроменен, без horizontal scroll.
- **Known issues/blockers:** Няма.
- **Next exact step:** Потребителят да потвърди разстоянието след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 17:00 - Висококачествен HERO-WELLCOME asset
- **Date/time:** 2026-11-22 17:00 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Използва се новият файл, който потребителят качи в `DASHBOARD/HERO-WELLCOME.jpg` — копиран е върху `web/assets/hero-welcome.jpg`. Нов natural размер `1321x880`; HTML intrinsic атрибутите и cache-bust са обновени на `20261122g`. Вертикалният padding е намален леко, за да остане центрирането точно при по-високия banner. Картата, текстовете, бутонът и auth логиката не са пипани.
- **State:** Променени са `web/assets/hero-welcome.jpg`, `web/index.html`, `web/style.css`, `tests/test_dashboard_workflow.py` и двата worklog файла. Референцията `DASHBOARD/WELLCOME-PROMQNA.jpg` остава неизползвана.
- **Tests:** Целевият Welcome тест → `1 passed in 0.26s`; пълен pytest → `506 passed in 7.78s`. CDP desktop 1440x900: hero `880x586`, карта `334x262`, `shellTopGap=22`, `shellBottomGap=22`, без horizontal scroll, `POST /api/auth/start` запазен. CDP mobile 375x812: hero `347x231`, карта `334x227`, без horizontal scroll.
- **Known issues/blockers:** Няма. Изображението е заменено само със предоставената от потребителя версия със същото име.
- **Next exact step:** Потребителят да потвърди новото изображение след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:56 - Голям центриран Welcome banner
- **Date/time:** 2026-11-22 16:56 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Banner изображението вече е `width: 100%`, `max-width: none`, `height: auto`, `object-fit: contain` и заема цялата налична ширина (880px при 1440px екран), без да е смалявано от старата 334px променлива. Картата си остава 334px чрез нов `--welcome-card-width`; намалени са празнините около banner, а на PC съдържанието е центрирано и вертикално (`shellTopGap=99`, `shellBottomGap=99`). Мобилен остава подравнен отгоре.
- **State:** Променени са `web/style.css`, `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла; cache-bust `20261122f`. Изображението, текстовете, typography-то, бутонът, theme guard и auth логиката не са пипани.
- **Tests:** `node --check web\app.js` → OK; целевият Welcome тест → `1 passed in 0.31s`; пълен pytest → `506 passed in 7.61s`. CDP desktop 1440x900: hero `880x432`, карта `334x262`, бутон `268x48`, `align-items=center`, без horizontal scroll, `POST /api/auth/start` запазен. CDP mobile 375x812: hero `347x170`, карта `334x227`, без horizontal scroll.
- **Known issues/blockers:** Няма нови блокери. Изображението е оригиналното 334x164 и се упълнява от CSS, както изрично поиска потребителят (не е сменяно с друго).
- **Next exact step:** Потребителят да потвърди крайния изглед след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:49 - Подзаглавие без "One"
- **Date/time:** 2026-11-22 16:49 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Подзаглавието на Welcome е `Click. Any fork. Always up-to-date.` вместо `One click. Any fork. Always up-to-date.`.
- **State:** Променени са `web/index.html`, `tests/test_dashboard_workflow.py` и двата worklog файла. Portrait подредбата, HERO-WELLCOME, theme guard и auth потокът остават непроменени.
- **Tests:** Целевият Welcome тест → `1 passed in 0.32s`; пълен pytest → `506 passed in 7.68s`.
- **Known issues/blockers:** Няма.
- **Next exact step:** Потребителят да потвърди текста след Ctrl+F5. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:48 - Portrait Welcome с оригиналния HERO-WELLCOME
- **Date/time:** 2026-11-22 16:48 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Потребителят уточни, че `DASHBOARD/WELLCOME-PROMQNA.jpg` е само референция за външен вид, не asset, и че цялото трябва да е PORTRAIT. Върнат е оригиналният `HERO-WELLCOME` (`web/assets/hero-welcome.jpg`, 334x164); HD файлът е изтрит. `--welcome-hero-width` и `.sync-panel` са по 334px, бутонът e 270px, за да не прелива. Текстовете, цветовете, theme guard и auth остават както са.
- **State:** Променени са `web/index.html`, `web/style.css`, `tests/test_dashboard_workflow.py` и двата worklog файла; изтрит е `web/assets/hero-welcome-hd.jpg`. Cache-bust `20261122e`. Референцията `DASHBOARD/WELLCOME-PROMQNA.jpg` остава непокътната и не се използва.
- **Tests:** `node --check web\app.js` → OK; целевият Welcome тест → `1 passed in 0.32s`; пълен pytest → `506 passed in 6.03s`. CDP: hero/panel `334x164`/`334x283` desktop и `334x164`/`334x227` mobile, бутон `270x48`, `overallPortrait=true`, asset `hero-welcome.jpg?v=20261122e`, `brandMarkCount=0`, `footerCount=0`, blend/mask активни, `POST /api/auth/start` запазен, без horizontal scroll.
- **Known issues/blockers:** Няма нови блокери. Точната визуална прилика с референцията зависи от потребителя, защото моделът не чете изображения.
- **Next exact step:** Потребителят да направи Ctrl+F5 в отворения Chrome и да потвърди portrait изгледа. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:36 - Професионално изчистване на Welcome
- **Date/time:** 2026-11-22 16:36 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** Визуално refinement без смяна на концепцията: логото е с HD asset, `mix-blend-mode: screen` и radial mask, за да се слее с тъмния фон и да няма правоъгълен фон; картата е с по-фина рамка, по-малък padding и по-малко празно място; `WELCOME TO` е 20px с по-малък letter-spacing, вторият ред остава 30px; бутонът е 300x48 със субтилен green glow; премахнати са зеленото `D` и долният текст, който потребителят видя.
- **State:** Променени са `web/index.html`, `web/style.css`, `tests/test_dashboard_workflow.py` и двата worklog файла; добавен е `web/assets/hero-welcome-hd.jpg`. Cache-bust `20261122d`. Auth потокът, `/api/auth/start`, API, GitHub App, OAuth и Dashboard не са пипани.
- **Tests:** `node --check web\app.js` → OK; целевият Welcome тест → `1 passed in 0.31s`; пълен pytest → `506 passed in 7.70s`. CDP: `brandMarkCount=0`, `footerCount=0`, `heroMixBlendMode=screen`, radial mask активен, HD asset `1336x656` зареден, desktop hero `640x314`/панел `640x255`/бутон `300x48`, mobile `347x170`/`347x292`/`300x48`, редове `20/30px` и `14/21px`, `POST /api/auth/start` запазен, без horizontal scroll.
- **Known issues/blockers:** Няма нови блокери. Визуалното съответствие с референтния JPG зависи от потребителя, защото моделът не чете изображения.
- **Next exact step:** Потребителят да направи Refresh в отворения Chrome и да потвърди крайния изглед. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:22 - Hero без банер, 2x по-голям и по-малък втори ред
- **Date/time:** 2026-11-22 16:22 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** По нова корекция от потребителя е премахнат фонът/рамката/сенката на `.hero-banner` (вече няма „шапка“ около изображението), а самият HERO е уголемен от 320px на 640px desktop и е изравнен по ширина с долната `.sync-panel`. Вторият ред `DREAMEROL SYNC` е намален до `0.75em`.
- **State:** Променени са `web/index.html`, `web/style.css`, `tests/test_dashboard_workflow.py` и двата worklog файла. Cache-bust `20261122c`; бутонът остава 320px, но вече не се изисква еднаква ширина с hero-то. Auth потокът, API и Dashboard не са пипани.
- **Tests:** `node --check web\app.js` → OK; целевият Welcome тест → `1 passed in 0.31s`; пълен pytest → `506 passed in 7.29s`. CDP: `heroBackground=none`, `heroBorderWidth=0px`, `heroBoxShadow=none`; desktop hero `640x314` и панел `640x330`; mobile hero/панел `347x170`/`347x292`; втори ред `30px` desktop и `21px` mobile (точно 0.75 от 40/28); `POST /api/auth/start` запазен; без horizontal scroll.
- **Known issues/blockers:** Няма нови блокери. Визуалното съответствие с JPG зависи от потребителя, защото моделът не чете изображения.
- **Next exact step:** Потребителят да направи Refresh в отворения Chrome и да каже дали сега изглежда правилно. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:18 - Заглавие на два реда и еднаква ширина hero/бутон
- **Date/time:** 2026-11-22 16:18 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон.
- **Last completed:** По искане на потребителя заглавието е разделено на `WELCOME TO` и `DREAMEROL SYNC` в два отделни реда. Ширината на `HERO-WELLCOME` и на бутона `Sign in with GitHub` вече се задава от една CSS променлива `--welcome-action-width` (320px desktop, компенсирана за mobile padding).
- **State:** Променени са `web/index.html`, `web/style.css`, `tests/test_dashboard_workflow.py` и двата worklog файла. Cache-bust е `20261122b` за `style.css` и hero asset-а; `app.js` и auth потокът остават непроменени.
- **Tests:** `node --check web\app.js` → OK; целевият Welcome тест → `1 passed in 0.33s`; пълен pytest → `506 passed in 7.35s`. CDP: desktop hero `320x157` = бутон `320x52`; mobile hero `309x152` = бутон `309x52`; два реда с `display: block`; `POST /api/auth/start` запазен; без horizontal scroll.
- **Known issues/blockers:** Няма нови блокери. Визуалното съответствие с JPG пак зависи от потребителя, защото моделът не чете изображения.
- **Next exact step:** Потребителят да направи Refresh в вече отворения Chrome и да потвърди двата реда и еднаквата ширина. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 16:03 - Welcome redesign с hero банер
- **Date/time:** 2026-11-22 16:03 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `bbee575`, `ahead 2`; без commit, push, merge или смяна на клон след локалния запис от 15:43.
- **Last completed:** Преработен е само Welcome frontend: нов hero банер със статичен asset, заглавие `Welcome to DREAMEROL SYNC`, подзаглавие `One click. Any fork. Always up-to-date.`, зелен GitHub бутон с иконка и disable/loading състояние. Auth потокът, `/api/auth/start`, API, GitHub App, OAuth и Dashboard не са променяни.
- **State:** Променени са `web/index.html`, `web/style.css`, `tests/test_dashboard_workflow.py`; добавен е `web/assets/hero-welcome.jpg` (копие от `DASHBOARD/HERO-WELLCOME.jpg`). Съществуващите 7 untracked изображения са непокътнати. Моделът не може визуално да чете JPG, затова дизайнът следва текстовото описание на потребителя и готовия hero файл.
- **Tests:** `node --check web\app.js` → OK; целевият `test_welcome_uses_theme_guard_with_github_green_signin` → `1 passed`; пълен pytest → `506 passed in 6.85s`. Жива CDP проверка -> банерът се зарежда (`334x164`, desktop `520x255`, mobile `321x158`), `themeGuard=on`, бутон `rgb(35,134,54)`, desktop `scrollWidth=799/innerWidth=814`, mobile `scrollWidth=375/innerWidth=375`, кликът вика `POST /api/auth/start`.
- **Known issues/blockers:** Няма нови блокери. Визуалното съответствие с референтния JPG не е потвърдено от модела, защото липсва image input; проверено е чрез DOM/computed styles.
- **Next exact step:** Потребителят да направи Refresh и визуално да потвърди Hero секцията, цветовете и мобилния изглед. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 15:43 - Локален Git commit със запазени Dashboard промени
- **Date/time:** 2026-11-22 15:43 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth`; локален commit `Save Dashboard updates` е създаден в тази стъпка, без push, merge или смяна на клон.
- **Last completed:** По изрично одобрение са прегледани `git status`, `git diff`, `git ls-files --others --exclude-standard` и `git log --oneline -10`; включени са 20 променени tracked файла, `docs/WORKLOG/LOG_20-11-26.md`, `docs/WORKLOG/LOG_22-11-26.md` и `tests/conftest.py`.
- **State:** Изключени са 6 локални изображения (`DASHBOARD/WELLCOME.jpg`, `assets/DREAMEROL-SYNC-Mihaela Koseva.jpg`, `assets/LOGO-DREAMEROL-SYNC.jpg`, `assets/SCREENSHOT1.png`, `assets/SCREENSHOT2.png`, `assets/SCREENSHOT3.png`), защото не са tracked и README сочи към фиксирани raw URL-и от по-стари commit-и. Няма push към GitHub.
- **Tests:** Преди записа: `506 passed in 6.16s`; `git diff --check` показва само trailing whitespace в README/docs, не е failing проверка.
- **Known issues/blockers:** Няма нови блокери. Симулацията остава отворена; тя не доказва реално GitHub състояние.
- **Next exact step:** Потребителят да потвърди локалния commit; при поискване изображенията могат да се добавят с отделен commit. Без push без изрично одобрение.

## 2026-11-22 15:34 - Пълен pytest: 506 passed
- **Date/time:** 2026-11-22 15:34 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88`, `ahead 1`; без commit, push, merge или смяна на клон.
- **Last completed:** Пускат са всички тестове след документните промени и симулациите; няма промяна в проектния код.
- **State:** Симулираният профил `simulated-account-b` остава отворен на CDP `9556`, сървърът на `8001` е активен. Worklog файловете са обновени; uncommitted промените и untracked файловете са непокътнати.
- **Tests:** `& 'C:\AI-Projects\DREAMEROL-SYNC\.venv\Scripts\python.exe' -m pytest -q -p no:cacheprovider` → `506 passed in 6.16s`, без предупреждения.
- **Known issues/blockers:** Няма нови блокери. Симулацията не изпълнява реални GitHub write и не доказва реално състояние на репозитории.
- **Next exact step:** По желание на потребителя да се затворят CDP табът и локалният сървър или да се пусне SYNC върху част от 85-те READY fork-а. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 15:30 - Нов симулиран профил с 15 UNSYNCABLE и 5 проверъчни грешки
- **Date/time:** 2026-11-22 15:30 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88`, `ahead 1`; без commit, push, merge или смяна на клон.
- **Last completed:** Отворен е нов изкуствен акаунт `simulated-account-b`: 100 fork + 10 original; 85 READY TO SYNC, 10 divergent и 5 `ahead` с failed check. Точните несинхронизируеми имена са извлечени от DOM: divergent `fork-009, 018, 031, 034, 051, 056, 064, 084, 093, 099`; unverified-ahead `fork-005, 011, 096, 097, 100` (префикс `simulated-account-b/`). Броячите са `100/0/85/15`, 10-те original не се броят.
- **State:** Контролираният Chrome/CDP таб остава отворен на `http://127.0.0.1:8001/dashboard` (порт `9556`); локалният Dashboard сървър слуша на `8001` (PID `20180`). Старият таб/сървър от предходния тест са спрени. Променени са само worklog файловете; проектният код, `.env`, broker, OAuth, GitHub App и `data/sync_history.json` не са пипани.
- **Tests:** Няма pytest — няма промяна в проектния код. Жива CDP проверка: 100 реда, 85 чекбокса, 10 реда `UNSYNCABLE`, 5 реда `UNVERIFIED!!!` с `(1 ahead, 0 behind)`, `summary-attention = 5 check(s) unverified`, `originalsInDom=0`, `checkCalls=10`, `listCalls=1`, `liveCalls=0`, `realFetchCalls=0`. Report: `%TEMP%\opencode\sim-profile-unsyncable-report.json`.
- **Known issues/blockers:** Няма нови блокери. Симулацията валидира UI класификацията и броячите, не реално GitHub състояние. Потвържденията за Welcome/Dashboard refresh от 21.11 остават неизвършени.
- **Next exact step:** Потребителят да потвърди визуално профила и при желание да пусне SYNC на част от 85-те READY или да поиска затваряне на таба/сървъра. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 15:20 - Ръчен SYNC тест завършен успешно
- **Date/time:** 2026-11-22 15:20 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88`, `ahead 1`; без commit, push, merge или смяна на клон.
- **Last completed:** Потребителят сам натиска бутоните в контролирания CDP таб със симулирания акаунт `simulated-account` (100 репо: 10 original, 90 fork = 10 UNSYNCABLE + 80 READY). Извършени са SYNC CHOSEN на 10 (`90/10/70/10`), втори SYNC CHOSEN на 10 (`90/20/60/10`) и SYNC ALL на останалите 60 → `SYNC ALL: 60 synchronized, 0 skipped, 0 failed`, крайни броячи `90/80/0/10`. 10-те original никога не влизат в UI/броячите.
- **State:** Контролираният Chrome/CDP таб остава отворен на `http://127.0.0.1:8001/dashboard` (порт `9555`, PID `5116`); локалният Dashboard сървър е рестартиран отделно и слуша на `8001` (PID `7360`). Наблюдателният Node процес е спрян, за да не затвори таба при timeout. Променени са само worklog файловете; проектният код, `.env`, broker, OAuth, GitHub App и `data/sync_history.json` не са пипани. Съществуващите uncommitted промени и untracked файлове са непокътнати.
- **Tests:** Няма pytest — няма промяна в проектния код. Жива CDP проверка на крайното състояние: `stat` и `summary` = `90/80/0/10`, 90 реда, 80 `UP TO DATE`, 10 `UNSYNCABLE`, 0 `READY`, 0 `UNVERIFIED`, `originalsInDom=0`, 60 реда в `Sync history`, `liveRequests=["live:60"]`, `confirms=1`, `realFetchCalls=0`. Първият ръчен етап е записан в `%TEMP%\opencode\sim-profile-100-manual-report.json`.
- **Known issues/blockers:** След втория SYNC CHOSEN страницата е била презаредена, при което браузърният stub се рестартира и наблюдателят изгуби брояча `liveCalls`; затова последната проверка е направена директно през CDP, не през report-а. Потвържденията за Welcome/Dashboard refresh от 21.11 остават неизвършени от потребителя. Важно: `up-to-date` след SYNC идва от браузърния stub (60 `dry_run` проверки преди `live:60`, но без follow-up проверка след него); симулацията не доказва реално GitHub състояние и не изпълнява сървърните safety checks.
- **Next exact step:** Потребителят да потвърди визуално крайното състояние `90/80/0/10` и при желание да се затворят локалният сървър и контролираният Chrome. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-22 15:07 - Симулиран профил със 100 репозитория: SYNC 10 + SYNC ALL 70
- **Date/time:** 2026-11-22 15:07 (see `docs/WORKLOG/LOG_22-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88`, `ahead 1`; без commit, push, merge или смяна на клон.
- **Last completed:** В отделен контролиран Chrome/CDP таб е отворен изкуствен акаунт `simulated-account` със 100 репозитория (90 fork: 80 READY + 10 UNSYNCABLE; 10 original с `fork:false`). API отговорите са прихванати само в браузъра; SYNC CHOSEN на 10 даде `90/10/70/10`, последващият SYNC ALL на 70 даде `90/80/0/10`. 10-те original не се броят (`originalsInDom=0`) и няма реални GitHub write (`realFetchCalls=0`, `live:10` и `live:70` са само в stub-а).
- **State:** Локалният Dashboard сървър на `8001` е стартиран за теста и след това спрян; контролираният Chrome е затворен. Променени са само двата worklog файла; проектният код, `.env`, broker, OAuth, GitHub App и `data/sync_history.json` не са пипани. Съществуващите uncommitted промени и untracked screenshot/asset файлове са непокътнати.
- **Tests:** Няма pytest — няма промяна в проектния код. Жива CDP проверка: initial `90/0/80/10`, 90 реда, 80 чекбокса; след SYNC CHOSEN `10 synchronized` и `90/10/70/10`; след SYNC ALL `70 synchronized` и `90/80/0/10`; 2 записа в stub `/api/history`, 2 потвърждения, `listCalls=1`, `checkCalls=89`, `realFetchCalls=0`. Report: `%TEMP%\opencode\sim-profile-100-report.json`; снимка: `%TEMP%\opencode\sim-profile-100-final.png` (моделът не може да я визуално прочете).
- **Known issues/blockers:** Първият опит изчака грешно съобщение (`Check complete...`) след Sync и прекъсна; скриптът е коригиран и повторният пълен тест мина. Потвържденията за Welcome и Dashboard refresh от 21.11 остават неизвършени от потребителя.
- **Next exact step:** Ако потребителят иска, да се пусне същият симулиран профил в режим без автоматични кликове, за да натисне сам SYNC CHOSEN/SYNC ALL; иначе да се потвърдят старите refresh промени. Без commit, push, merge или реален Sync без изрично одобрение.

## 2026-11-21 22:51 - Welcome без съобщение за смяна на профил
- **Date/time:** 2026-11-21 22:51 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88`, `ahead 1`; без push, merge или checkout.
- **Last completed:** Премахнати са текстът `Sign in with GitHub to choose a different account.` и `switchIntent` логиката в `web/app.js`; Welcome вече има един поток за вход. `web/app.js?v=20261121k`. Backup: `%TEMP%\opencode\welcome-remove-switch-text-backup-20261121-225001`.
- **State:** Live статичният файл през `8001` не съдържа стария текст и `switchIntent`. Няма реален Sync, GitHub write, push, merge или commit от агента.
- **Tests:** `node --check web\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `506 passed, 1 warning in 6.15s`.
- **Known issues/blockers:** Няма нови блокери.
- **Next exact step:** Потребителят да направи Refresh на Welcome и да потвърди, че долният текст е изчезнал; утре остава и потвърждението за Dashboard Refresh от записа 22:47.

## 2026-11-21 22:47 - Край на сесията (състояние за утре)
- **Date/time:** 2026-11-21 22:47 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88`, local branch `ahead 1` спрямо `origin/feature/github-app-auth`; без push, merge или checkout.
- **Last completed:** Потребителят потвърди, че Refresh работи правилно: възстановява списъка и броячите при `READY TO SYNC`, `ALL` и `UNSYNCABLE`, включително при страница, получена с репозитории от падащото меню. След потвърждението са обновени само `docs/WORKLOG/LOG_21-11-26.md` и този `WORKLOG.md`; нов код не е писан.
- **State:** `git status --short --branch` показва смесени uncommitted кодови/тестови промени и untracked screenshot/asset файлове; те са умишлено оставени непокътнати. Няма активни pytest/node/Sync операции; работят само очакваните локални сървъри: Auth Broker на `8000` (PID `7596`) и Dashboard на `8001` (PID `24704`). Няма commit, push, merge или GitHub write.
- **Tests:** Последно реално изпълнение: `node --check DASHBOARD\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `506 passed, 1 warning in 8.03s`. След това не са пускани нови тестове.
- **Known issues/blockers:** Няма блокери. Uncommitted промените са очакваното текущо състояние и не са за commit без изрично одобрение.
- **Next exact step (утре):** Потребителят да направи Refresh в Dashboard и да потвърди, че списъкът и броячите се възстановяват правилно. След това да се реши дали да се прави commit само с изрично одобрение.

## 2026-11-21 22:45 - Refresh пази филтъра и търсенето
- **Date/time:** 2026-11-21 22:45 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (без push, merge или checkout).
- **Last completed:** Snapshot-ът вече съдържа `statusFilter` и `searchText`; оживяват преди рендиране на списъка, но не пускат проверки. `app.js?v=20261121l`. Backup: `%TEMP%\opencode\dashboard-filter-refresh-backup-20261121-224355`.
- **State:** Жива проверка: преди/след refresh `filter=to-be-synced`, `rows=1`, `snapshotFilter=to-be-synced`, `reloadSyncRequests=0`. Няма реален Sync, GitHub write, push, merge или commit от агента.
- **Tests:** `node --check DASHBOARD\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `506 passed, 1 warning in 8.03s`. Разширен е `test_reload_restores_saved_dashboard_without_rechecking_repositories`.
- **Known issues/blockers:** Няма нови блокери. Първото зареждане след ъпдейт може да използва стар кеширан `app.js`; новият `?v=...l` го заобикаля.
- **Next exact step:** Потребителят да направи refresh с избран филтър и да потвърди, че остава същият изглед. Без нов commit, push, merge или Sync без одобрение.

## 2026-11-21 22:40 - Refresh не рестартира проверките
- **Date/time:** 2026-11-21 22:40 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (без push, merge или checkout).
- **Last completed:** Добавен е `dreamerol.dashboardSnapshot.<account>` snapshot в `sessionStorage`; записва се завършено състояние, избор, статус, броячи, история и последна операция, включително принудително на `pagehide`. `initDashboard()` възстановява snapshot-а преди `preview()`, само несъвместим/липсващ snapshot пуска нови авто проверки. `app.js?v=20261121k`. Backup: `%TEMP%\opencode\dashboard-snapshot-pagehide-backup-20261121-223724`.
- **State:** Жива CDP проверка преди/след refresh: `stats=[40,35,3,2]` и в двата случая, същият статус, `snapshotKeys=[dreamerol.dashboardSnapshot.gabrielrules]`, `reloadSyncRequests=0`. Няма реален Sync, GitHub write, push, merge или commit от агента.
- **Tests:** `node --check DASHBOARD\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `506 passed, 1 warning in 7.80s`. Добавен е `test_reload_restores_saved_dashboard_without_rechecking_repositories`.
- **Known issues/blockers:** Няма нови блокери. Важи само за същата сесия/account в същия таб; смяна на профил изчиства snapshot-а.
- **Next exact step:** Потребителят да направи refresh в своя Dashboard таб и да потвърди, че списъкът и броячите остават непроменени без нови проверки. Без нов commit, push, merge или Sync без одобрение.

## 2026-11-21 22:29 - Welcome в палитрата на Dashboard banner
- **Date/time:** 2026-11-21 22:29 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (без push, merge или checkout).
- **Last completed:** Welcome guard използва colors от `DASHBOARD/dashboard.css`: `#060913`, виолетово/сини радиални градиенти, панел `#0e1422 → #080d1b`, border `rgba(99,102,241,.36)`, текст `#eef3ff`/`#9aa9c4`, brand mark `#3BEE7E → #079447`. Sign in бутонът остана зелен `#238636`/`#2ea043`. Backup: `%TEMP%\opencode\welcome-dashboard-banner-colors-backup-20261121-222740`.
- **State:** Live CDP потвърди `guard=on`, `cleaned=24`, body gradient и brand mark в новите цветове. Сървърът на порт 8001 не е рестартиран; стилът е само статичен CSS под съществуващото `?v=20261121j` и `no-store`. Няма реален Sync, GitHub write, push, merge или commit от агента.
- **Tests:** `python -m pytest -q -p no:cacheprovider` → `505 passed, 1 warning in 6.22s`. Обновен е `test_welcome_uses_theme_guard_with_github_green_signin`.
- **Known issues/blockers:** Няма нови блокери. Потвърждението за refresh snapshot от авторизирания Dashboard таб все още зависи от потребителя.
- **Next exact step:** Потребителят да направи refresh на Welcome и да каже дали цветовете допадат. Без нов commit, push, merge или Sync без одобрение.

## 2026-11-21 22:22 - Welcome текстове са изчистени
- **Date/time:** 2026-11-21 22:22 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (без push, merge или checkout).
- **Last completed:** В `web/index.html` подзаглавието под Welcome е сменено на `Sign in with GitHub to synchronize your forks securely.` и е премахнат повтореният `<footer>DREAMEROL SYNC</footer>`. Backup: `%TEMP%\opencode\welcome-text-backup-20261121-222142`.
- **State:** Live HTML през рестартирания сървър (PID `24704`) съдържа новия текст, не съдържа стария `preview and` и няма `<footer>`. Заглавието `DREAMEROL SYNC` и brand mark остават. Няма реален Sync, GitHub write, push, merge или commit от агента.
- **Tests:** `python -m pytest -q -p no:cacheprovider` → `505 passed, 1 warning in 7.91s`. Разширен е `test_welcome_uses_theme_guard_with_github_green_signin`.
- **Known issues/blockers:** Няма нови блокери. Потвърждението за refresh snapshot от авторизирания Dashboard таб зависи от потвърждението на потребителя.
- **Next exact step:** Потребителят да направи refresh и да потвърди броячите и изчистения Welcome текст. Без нов commit, push, merge или Sync без одобрение.

## 2026-11-21 22:12 - Refresh пази последните Sync броячи
- **Date/time:** 2026-11-21 22:12 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (проверено преди тази промяна; без push, merge или checkout).
- **Last completed:** След успешния Sync на 3 репо (потвърден от потребителя) `applyOperation()` вече запазва `operationCounts` и при restored операция, а `updateStats()` използва този snapshot докато текат проверките; при завършване `finalizePreviewUi()` го изчиства и остават live броячите. Cache-bust `v=20261121j` за Dashboard/Welcome. Backup: `%TEMP%\opencode\refresh-counter-snapshot-backup-20261121-220814`.
- **State:** Локалният Dashboard сървър е рестартиран с одобрение: PID `5684` → `24704`. `/dashboard` връща `200`, `Cache-Control: no-store`, `Pragma: no-cache`, `app.js?v=20261121j`. Welcome е живо проверен със зелен button `rgb(35,134,54)` и тъмен GitHub фон `rgb(13,17,23)`. Няма реален Sync, GitHub write, push, merge или commit от агента.
- **Tests:** `node --check DASHBOARD\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `505 passed, 1 warning in 7.91s`. Добавен е `test_refresh_keeps_last_sync_counters_until_fresh_checks_finish`; обновен е по-стар assert за `const counts = ...`.
- **Known issues/blockers:** Жива проверка на Dashboard snapshot не е възможна в контролирания CDP профил, защото сесията липсва и `/dashboard` пренасочва към Welcome. Нужно е потребителят да направи refresh в своя авторизиран таб и да потвърди, че броячите не падат до нула.
- **Next exact step:** Потребителят да направи refresh и да потвърди задържаните броячи и зелените/сини цветове. Ако broker все още връща оранжево, да се използва новият Sign in линк `/?switch=1&v=20261121j`. Без нов commit, push, merge или Sync без одобрение.

## 2026-11-21 22:04 - Welcome: GitHub зелени цветове и защита от кеш
- **Date/time:** 2026-11-21 22:04 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (проверено; без push, merge или checkout).
- **Last completed:** Welcome (`/?switch=1`) зарежда `theme_guard.js` и има scoped `@layer dreamerol-guard` в `web/style.css`: green GitHub button `#238636`/hover `#2ea043`, brand mark green gradient, dark GitHub body `#0d1117`, text `#f0f6fc`./cache-bust: `style.css?v=20261121i`, `app.js?v=20261121i`, Sign in линк `/?switch=1&v=20261121i`. Backup: `%TEMP%\opencode\welcome-github-green-backup-20261121-220116` и `%TEMP%\opencode\welcome-nocache-backup-20261121-220349`.
- **State:** Жив CDP тест с активно разширение: `guard=on`, `cleaned=25`, `button rgb(35,134,54)`, `h1 rgb(240,246,252)`, `body rgb(13,17,23)`. Добавени са `Cache-Control: no-store` и `Pragma: no-cache` за `/` и `/dashboard` в `api/app.py`; live сървърът не е рестартиран, затова тези headers ще влязат в сила при следващ рестарт. Няма реален Sync, GitHub write, push или merge от агента.
- **Tests:** `node --check DASHBOARD\theme_guard.js` и `web\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `504 passed, 1 warning in 8.21s`. Добавени са `test_welcome_uses_theme_guard_with_github_green_signin` и `test_html_pages_are_not_cached`.
- **Known issues/blockers:** Ако потребителят все още вижда оранжево в вече отворен Welcome таб, причината е кеширана стара страница; трябва еднократно Ctrl+F5 или да се влезе чрез новия `Sign in` линк от Dashboard. Сървърният `no-store` header изисква рестарт на process 5684, който не е извършен.
- **Next exact step:** Потребителят да направи hard refresh/нов Sign in линк и да потвърди зелените цветове. При поискване — рестарт на локалния Dashboard сървър за `no-store`; без нов commit, push, merge или Sync от агента.

## 2026-11-21 21:58 - Sync history в UI само с последната операция
- **Date/time:** 2026-11-21 21:58 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `3658a88` (проверено; без push, merge или checkout).
- **Last completed:** `renderedHistoryEntries()` в `DASHBOARD/app.js` вече чете само `authoritativeOperations.slice(0, 1)`; секцията `Sync history and last result` показва последната Sync операция с всички per-repo редове, вместо 2–3 операции. Backup: `%TEMP%\opencode\history-latest-only-backup-20261121-215749`.
- **State:** Пълната история остава непроменена в `data/sync_history.json` и `/api/history` (до 20 операции, `api/sync_history.py:15`). Локалният commit `3658a88 Stabilize dashboard checks and theme guard` от предходната стъпка е запазен; след него са uncommitted само `DASHBOARD/app.js`, `tests/test_dashboard_workflow.py` и двата worklog файла от тази промяна, плюс по-старите несвързани файлове (`README.md`, `api/`, `fork_sync/`, `DECISIONS.md`, screenshots, `tests/conftest.py`). Няма реален Sync, GitHub write, push или merge.
- **Tests:** `node --check DASHBOARD\app.js` → OK; `python -m pytest -q -p no:cacheprovider` → `502 passed, 1 warning in 7.92s`. Добавен е `test_history_section_shows_only_latest_authoritative_operation` и проверка, че `_MAX_OPERATIONS = 20` остава непроменено.
- **Known issues/blockers:** Welcome на `127.0.0.1` остава извън обхвата на `theme_guard.js`; потребителят избра да спре със съществуващия commit `3658a88` без нов commit за тази малка UI промяна.
- **Next exact step:** Потребителят да потвърди визуално в Dashboard, че `Sync history and last result` показва само последната дата/операция. Без нов commit, push, merge или Sync без отделно одобрение.

## 2026-11-21 21:38 - Подредба по състояние и refreshFollow-up след Sync
- **Date/time:** 2026-11-21 21:38 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** По изрично одобрение е добавена постоянна подредба в Dashboard: `READY TO SYNC` → `UP TO DATE` → `UNSYNCABLE/непроверени`, с запазване на реда вътре в групата (`sortReposForDisplay()` в `utils.js`, използвана от `filteredRepos()`). Cache-bust: `app.js?v=20261121h`, `utils.js?v=20261121d`; backup `%TEMP%\opencode\repo-order-backup-20261121-2132`. След едно одобрено презареждане: 3 READY, 34 UP TO DATE, 2 UNSYNCABLE, без write заявки и без JS грешки.
- **State:** Предишният реален Sync от 21:29 остава успешен и записан (`99d31057…`, `success:1`, 2 комита за `GabrielRules/TEST2`). След refresh обаче пресен `dry_run` показва `TEST2` отново `behind_by:1`, затова е обратно в READY групата; причината не е доказана. Не е правен втори Sync. Не са пипани `.env`, broker, OAuth, GitHub App, core sync алгоритми, hosts или Chrome настройки. Няма commit или push.
- **Tests:** `node --check DASHBOARD\app.js` и `node --check DASHBOARD\utils.js` → OK; `python -m pytest -q -p no:cacheprovider` → `501 passed, 1 warning in 6.05s`. Жива проверка: URL `/dashboard`, `scripts` с `app.js?v=20261121h`, ред `READY → UP TO DATE → UNSYNCABLE`, `writes=[]`, `errors=[]`; `/api/sync dry_run` за `TEST2` HTTP `200`, `behind_by:1`, `last_successful_sync 2026-11-21T19:29:36Z`.
- **Known issues/blockers:** При нормален refresh броячите винаги започват от `0/0/0/0`, докато текат проверките, и се попълват накрая — `preview()` нулира `checkedCount` и стартира нова проверка. Ако се иска запазване на последните показатели още при зареждане, това е отделна промяна. Welcome на `127.0.0.1` остава извън обхвата на theme guard.
- **Next exact step:** Да се изясни дали `behind_by:1` след успешния Sync е нов upstream commit или несинхронизирано състояние в GitHub — само read-only проверка или сравняване на commits, без втори Sync без одобрение. По желание отделно да се добави показване на последните известни броячи при refresh. Без commit/push.

## 2026-11-21 19:04 - dreamerol.local: цветовете са коректни, Dark Mode остава за другите сайтове
- **Date/time:** 2026-11-21 19:04 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** След ръчно влизане от потребителя сесията е валидна; `dreamerol_session` е дублирана in-memory от `domain=127.0.0.1` към `domain=dreamerol.local` със същите `path=/`, `httpOnly=true`, `secure=false`, `sameSite=Lax`, `expires`; стойността не е показвана, логвана или записвана. Проверени са нови табове `http://dreamerol.local:8001/dashboard` и `http://dreamerol.local:8001/?switch=1`: няма инжектиран `dark_1.css`, възстановени са проектните цветове, Dashboard е авторизиран и показва `39/34/3/2` и в двете групи броячи.
- **State:** Контролен таб `http://127.0.0.1:8000/healthz` все още получава `dark_1.css` и сив `body rgb(183,183,183)`, значи Dark Mode работи за не-изключени адреси. Extension storage е само `{state:"dark", whitePagesList:["dreamerol.local"]}`. hosts, DNS, Chrome/cookie и backup са както в 18:58; проектни файлове, `.env`, broker, OAuth и GitHub App не са пипани.
- **Tests:** Няма pytest. Живи проверки: `/api/auth/status` `200 AUTHENTICATED` (`GabrielRules`); batch `/api/sync` = 1 list + 4 batch, всички HTTP `200`; JS грешки `[]`; Dreamerol Dashboard `Check complete: 39 forks checked...`, `stats=39/34/3/2`, `summary=39/34/3/2`. Welcome: `body rgb(245,247,251)` / `background rgb(16,20,29)`. Dashboard: `body rgb(238,243,255)` / `background rgb(6,9,19)`, `rgb(74,222,128)`, `rgb(251,191,36)`, `rgb(248,113,113)`.
- **Known issues/blockers:** Broker все още пренасочва към `http://127.0.0.1:8001/dashboard` при нов логин, затова винаги трябва да се отваря `dreamerol.local` адресът; промяна на `.env`/broker изисква отделно одобрение. Cookie-то за `dreamerol.local` е копие и ще изтече заедно с оригиналното — тогава е нужен нов login и ново копиране.
- **Next exact step:** Потребителят да ползва само `http://dreamerol.local:8001/dashboard` и `http://dreamerol.local:8001/?switch=1`. При изтичане на сесията: нов логин с одобрение, после повторно in-memory копиране на cookie. Без Sync, commit или push.

## 2026-11-21 18:58 - dreamerol.local: частично изпълнено, сесията липсва
- **Date/time:** 2026-11-21 18:58 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** С UAC е добавен само `127.0.0.1 dreamerol.local` в hosts (`25 → 26` реда, старите записи непокътнати); `ipconfig /flushdns` → `Successfully flushed the DNS Resolver Cache.`; в Chrome профила `cdp-profile-auth` е зададено `whitePagesList: ["dreamerol.local"]` само през `chrome.storage.local.set`, без други extension настройки.
- **State:** Backup: `%TEMP%\opencode\dreamerol-local-execute-20261121-185233`. Не е правено копиране на cookie, нови табове, Dashboard/batch проверка, `.env`, broker, OAuth, GitHub App, CSS или проектни файлове. Стойността на `dreamerol_session` не е показвана, логвана или записвана.
- **Tests:** Няма pytest. Check: hosts SHA преди промяна съвпадаше с backup; `/api/auth/status` в контролирания профил върна `401 {"detail":"Sign in through the Auth Broker first."}`; `Network.getCookies` за `http://127.0.0.1:8001` върна `0` cookie-та с име `dreamerol_session`. Спрях според условието за сесиен проблем.
- **Known issues/blockers:** Сесията в контролирания CDP профил е изчезнала (вероятно session/short-lived cookie след затварянето на браузъра). Без нея не може да се запази авторизиран Dashboard чрез in-memory duplication, а нов OAuth login е забранен без отделно одобрение.
- **Next exact step:** Да се поиска отделно одобрение за нов OAuth login в контролирания профил или потребителят да влезе ръчно; след това да се повтори проверката на cookie attributes, in-memory duplication за `dreamerol.local` и отваряне на `http://dreamerol.local:8001/?switch=1` и `/dashboard`. Без Sync, commit или push.

## 2026-11-21 18:53 - dreamerol.local: блокиран от липса на admin права
- **Date/time:** 2026-11-21 18:53 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** Създаден е нов backup `%TEMP%\opencode\dreamerol-local-execute-20261121-185233` (hosts, Preferences, Secure Preferences, extension storage). Опит за append на `127.0.0.1 dreamerol.local` в `C:\Windows\System32\drivers\etc\hosts` не успя: `FileSystem.writeFile` грешка, текущият потребител не е Administrator.
- **State:** Няма промяна в hosts, Chrome, extension storage, cookie, `.env`, broker, OAuth, GitHub App, CSS или Git history. Не са правени `ipconfig /flushdns`, Page exclusion и cookie duplication. Предходните uncommitted промени и новите `DASHBOARD/SCREENSHOT-NOW*.png` са запазени.
- **Tests:** Няма тестове в тази стъпка. Извършени са само backup и read-only проверка на правата; протоколът е в дневния лог.
- **Known issues/blockers:** С текущите права hosts файлът не може да се редактира от агента. Нужно е или потребителят да добави реда ръчно в elevated editor, или изрично одобрение за UAC/elevated PowerShell. При проблем със сесията спирам и докладвам; нов OAuth login не се прави.
- **Next exact step:** Потребителят да одобри elevated изпълнение или сам да добави `127.0.0.1 dreamerol.local` към hosts. След това: `ipconfig /flushdns`, Page exclusion `dreamerol.local`, in-memory duplicate на `dreamerol_session`, проверка на `http://dreamerol.local:8001/?switch=1` и `/dashboard`, проверка че Dark Mode остава активен за не-изключен hostname.

## 2026-11-21 18:43 - Диагноза на цветовете и FINAL CHECK SUMMARY
- **Date/time:** 2026-11-21 18:43 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** Read-only диагноза по четирите въпроса. В CDP табовете (`?switch=1`, Welcome) разширението `pjbgfifennfhnbkhoidkdchbflppjncb` все още инжектира `dark_1.css` с `disabled:false`; computed `body` е `rgb(183,183,183)` върху `rgb(15,15,15)`. Временното изключване на link/sheet в текущия таб върна `body rgb(245,247,251)`, `background rgb(16,20,29)`, `h1 rgb(245,247,251)`; след повторно включване сивите стойности се върнаха. Няма CSS или Chrome настройки промени.
- **State:** Снимките `DASHBOARD/SCREENSHOT-NOW.png` и `DASHBOARD/SCREENSHOT-NOW2.png` са добавени от потребителя (untracked); Windows OCR разчита Welcome/`Sign in with GitHub` и `SYNC CHOSEN SYNC ALL`, но не и `FINAL CHECK SUMMARY`. Моделът не може директно да чете PNG. Контролираният CDP Chrome се затвори при опит за навигация към `/dashboard`, затова жив Dashboard DOM не е уловен в тази стъпка. Кодът не е променян; HEAD и предходните uncommitted промени са запазени.
- **Tests:** Няма нови pytest проверки — задачата е само диагностична. Служебните HTTP/CDP/OCR проверки са read-only; `/api/auth/status` в CDP профила върна `200 AUTHENTICATED` за `GabrielRules` преди затварянето на браузъра. Няма реален Sync или GitHub write.
- **Known issues/blockers:** `updateStats()` (`DASHBOARD/app.js:415-448`) попълва едновременно `stat-*` и `summary-*` от един и същи `counts`; `renderFinalSummary()` е на `app.js:200-205`. Четири нули в `FINAL CHECK SUMMARY` при ненулеви основни броячи не са възможни от текущия зареден JS — нужни са или пълен Dashboard screenshot/DOM, или проверка за кеширана/друга версия. Ако `repositories` е празен, и двете групи са `0`; при `listError` и двете са `—`. `FINAL CHECK SUMMARY` дублира основните четири брояча; уникални са статусът, `summary-attention` и `ahead-note`.
- **Next exact step:** Да се получи пълен screenshot/дом text от реалния Dashboard (с `#summary-total` и `#stat-total`), за да се потвърди дали нулите са в двете групи; отделно одобрение остава нужно за hosts/Chrome Page exclusion (`dreamerol.local`) срещу Extension.inject-а. Без CSS промени, реален Sync, commit или push.

## 2026-11-21 18:27 - BFCache рестарт на batch проверката е отстранен
- **Date/time:** 2026-11-21 18:27 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено преди и след промените; без commit, push, merge или checkout).
- **Last completed:** След backup (`%TEMP%\opencode\dreamerol-bfcache-backup-20261121-182227`) `pageshow` handlerът в `DASHBOARD/app.js` е заменен с `handlePageShowRestore()`. При `event.persisted` вече не се викат винаги `invalidatePendingOperations()` + `initDashboard({force:true})`: не-persisted събитие и активен Sync връщат рано; завършената проверка само прерисува прогрес/броячи/редове; активната batch проверка само обновява същия UI без нов `preview()`/`/api/sync`. Първоначалното зареждане (`initDashboard()`) и нормалният refresh остават непокътнати.
- **State:** Променени са `DASHBOARD/app.js`, `tests/test_dashboard_workflow.py`, `docs/WORKLOG/LOG_21-11-26.md`, `docs/WORKLOG/WORKLOG.md` и `docs/development/CHANGELOG_AI.md`. Не са пипани CSS, OAuth/auth broker, GitHub App, core sync алгоритми, `.env`, hosts или Chrome настройки. Запазени са README редакцията на потребителя и всички предходни uncommitted промени. Няма реален Sync или GitHub write.
- **Tests:** `node --check DASHBOARD\app.js` → OK. Targeted `python -m pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `69 passed, 1 warning in 2.37s`. Пълен `python -m pytest -q -p no:cacheprovider` → `492 passed, 1 warning in 6.17s`. Добавени са `page_show_source()`, `test_bfcache_completed_batch_does_not_restart_or_reset_counters` и `test_bfcache_active_batch_does_not_start_parallel_check`; обновен е съществуващият `pageshow` assert.
- **Browser verification:** Жива CDP проверка с един dashboard tab (`GabrielRules`, 39 fork-а): след restore със завършена проверка имаше 1 list + 4 batch заявки преди и след Back/Forward, статус `Check complete: 39 forks checked...` и броячи `39/34/3/2` без промяна. След restore по средата на batch има 1 list + 1 batch преди и след връщането, броячите остават `39/0/0/0`, а текущата проверка завършва с общо 1 list + 4 batch и същите `39/34/3/2`. Няма нови `/api/sync` заявки при BFCache restore.
- **Known issues/blockers:** Постоянното решение за сивия UI от външното Chrome разширение `pjbgfifennfhnbkhoidkdchbflppjncb` остава на пауза: направени са само backup (`dreamerol-local-backup-20261121-182150`) и точен план за `dreamerol.local` + Page exclusion, но hosts/Chrome промени изискват отделно одобрение. `.env`/`BROKER_DASHBOARD_URL` не може да се смени на `dreamerol.local` без промяна във валидацията на `auth_broker/config.py`. Моделът не може визуално да чете PNG файлове.
- **Uncommitted changes:** `DASHBOARD/app.js`, `DASHBOARD/dashboard.css`, `DASHBOARD/index.html`, `DASHBOARD/utils.js`, `DECISIONS.md`, `README.md`, `api/routes.py`, `api/sync_history.py`, `docs/WORKLOG/LOG_19-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`, `fork_sync/github.py`, `fork_sync/synchronizer.py`, `tests/test_dashboard_progress.py`, `tests/test_dashboard_strict_counts.py`, `tests/test_sync_history.py`; untracked: `assets/DREAMEROL-SYNC-Mihaela Koseva.jpg`, `assets/SCREENSHOT1.png`, `assets/SCREENSHOT2.png`, `assets/SCREENSHOT3.png`, `docs/WORKLOG/LOG_20-11-26.md`, `docs/WORKLOG/LOG_21-11-26.md`, `tests/conftest.py`, `tests/test_dashboard_workflow.py`.
- **Next exact step:** Няма незавършена стъпка по BFCache задачата. При поискване: (1) отделно одобрение и изпълнение на `dreamerol.local` плана с вече направен backup; (2) визуална проверка от потребителя, че цветовете на Welcome и Dashboard не са сиви; (3) без commit, push, merge, реален Sync или GitHub write.

## 2026-11-21 17:22 - Анализ на сивия UI и клик върху брояч (без кодови промени)
- **Date/time:** 2026-11-21 17:22 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** Анализ на двата проблема. `git diff -- DASHBOARD/dashboard.css` показва само 2 добавени `.check-retry` правила спрямо HEAD; backup `dreamerol-original-before-transfer` е същият CSS. CDP установи, че сивият вид идва от инжектиран външен stylesheet `chrome-extension://pjbgfifennfhnbkhoidkdchbflppjncb/scripts/content/theme_general/dark_1.css`, който презаписва цветовете на `rgb(183,183,183)`. При временно изключване на този stylesheet в страницата се връщат проектните цветове: `#e0e7ff` TOTAL, `rgb(74,222,128)` UP TO DATE, `rgb(251,191,36)` READY TO SYNC, `rgb(248,113,113)` UNSYNCABLE, статусни badge-и и button borders. Stylesheet-ът е върнат в първоначално състояние. Не е променян CSS в хранилището.
- **State:** Проблем 2 не е възпроизведен. `index.html` има `<article class="stat..."><strong id="stat-*">` без click handlers; `app.js` няма listener за броячите, нито `refreshDashboard()`. Жив CDP тест с `#stat-to-be-synced.click()` по време на проверка: филтърът остана `all`, броячите останаха `39/0/0/0`, нямаше `/api/sync` или нови заявки. Същото е потвърдено в backup app.js и commit `7fb24b7`. Поради изискването да не се прави предпоставителна промяна при неустановена причина, кодът не е пипан.
- **Known issues/blockers:** Нужно е уточнение кой точно елемент е кликнат (горен `.stat`, долен `.summary-grid`, или друг) и в коя браузърна сесия/профил, за да се възпроизведе рестартът. За сивия UI решението е в браузъра: да се изключи разширението със stylesheet `pjbgfifennfhnbkhoidkdchbflppjncb` или да се ползва профил без него; не бива да се добавя CSS override срещу разширението. Моделът не може визуално да чете PNG attach-ментите, затова сравнението е по Git diff/backup/computed styles.
- **Next exact step:** Да се потвърди от потребителя как да се процедира: изключване на браузърното разширение и/или предоставяне на повече детайли за клика върху брояч. Без промяна в кода докато причината за рестарта не е потвърдена.

## 2026-11-21 17:13 - `UNSYNCABLE` без `(AHEAD-ONLY)` и потвърден UI
- **Date/time:** 2026-11-21 17:13 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** След backup (`%TEMP%\opencode\dreamerol-ahead-label-backup-20261121-170807`) UI статусът за `ahead` е само `UNSYNCABLE`; премахнат е tooltip-ът с `AHEAD-ONLY`. Вътрешната класификация, `is-ahead`, behind/ahead числата, API отговорите и sync проверките са непроменени. Cache-bust: `app.js?v=20261121d`.
- **State:** След одобрение е направен само OAuth sign-in през UI; активен акаунт `architectquant`, `GitHub Connected`. Дублираните табове от OAuth потока са затворени; остана един `/dashboard`. Няма реален Sync или GitHub write. README.md и всички предходни uncommitted промени са запазени.
- **Tests:** `node --check DASHBOARD\app.js` и `node --check DASHBOARD\utils.js` → OK. Targeted `67 passed, 1 warning in 2.37s`; пълен `490 passed, 1 warning in 7.95s`. Добавен `test_ahead_only_status_renders_as_plain_unsyncable`.
- **Browser verification:** Реален DOM потвърден: `35 / 31 / 3 / 1`, статус `35 forks checked; no GitHub repositories were modified.`, `architectquant/DREAMEROL-SYNC` → `UNSYNCABLE` без `AHEAD-ONLY` и без title, няма `(CHECKED)`, няма `SYNC RESULTS`, `Sync history and last result` и `#sync-history` са налични. `200` за `/api/auth/status`, `/api/history`, `/api/sync`; без JS exceptions, console errors, failed requests или HTTP `>=400`. History записът е локален check summary и завършва на `(Time unavailable)`, защото architectquant няма backend operation записи; форматирането от backend `created_at` е покрито с тестове.
- **Next exact step:** Няма незавършена стъпка по тази задача; при поискване може да се направи нова read-only проверка или да се спре smoke стекът.

## 2026-11-21 17:00 - Реални timestampи в Sync history
- **Date/time:** 2026-11-21 17:00 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; без commit, push, merge или checkout).
- **Last completed:** След backup (`%TEMP%\opencode\dreamerol-history-time-backup-20261121-165735`) добавен `formatHistoryTimestamp()` в `DASHBOARD/utils.js` за локално време `DD.MM.YYYY, HH:mm` и `Time unavailable`. `DASHBOARD/app.js` вече чете `created_at` от backend операциите в `/api/history` и го показва в `(...)` след всеки history ред; fallbackките без реален запис показват `Time unavailable`. След жив Sync се извиква повторно `/api/history`, за да не се използва клиентският `new Date()` timestamp в history визуализацията. Cache-bust: `app.js?v=20261121c`, `utils.js?v=20261121c`.
- **State:** Backend sync history, API endpoints, Sync/Compare/Merge алгоритми, batch проверки, броячи, OAuth/GitHub App и README.md редакцията са непроменени. Няма реален Sync, GitHub write, commit/push/merge.
- **Tests:** `node --check DASHBOARD\app.js` и `node --check DASHBOARD\utils.js` → OK. Targeted `66 passed, 1 warning in 2.38s`; пълен `489 passed, 1 warning in 7.84s`. Нови тестове: локален формат от ISO, липсващ/невалиден timestamp, използване на `operation.created_at`; обновен е source-assert в `test_one_success_and_one_failure_keep_per_repository_results`.
- **Known issues/blockers:** Реалната браузърна проверка на `(timestamp)` и предходните UI промени остава блокирана: `/api/auth/status` връща `401`, табовете са `/dashboard` и `/?switch=1`. Не е докосван OAuth. Потребителят не е отговорил на въпроса за повторно влизане и вместо това даде тази задача.
- **Next exact step:** След валидна OAuth сесия да се презареди `/dashboard` и да се потвърди: history редовете завършват на `(DD.MM.YYYY, HH:mm)` от backend `created_at`, липсващите показват `(Time unavailable)`, `(CHECKED)` и `SYNC RESULTS` ги няма, `Sync history and last result` е наличен.

## 2026-11-21 16:50 - UI премахване на `(CHECKED)` и `SYNC RESULTS`
- **Date/time:** 2026-11-21 16:50 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено; същите uncommitted промени, без commit, push, merge или checkout).
- **Last completed:** След одобрение и backup (`%TEMP%\opencode\dreamerol-ui-backup-20261121-164701`) премахнато е `(CHECKED)` от `.repo-status` в `DASHBOARD/app.js`; статусните текстове са запазени. Премахната е цялата `<section id="sync-summary">` от `DASHBOARD/index.html` заедно с полетата `SUCCESSFULLY SYNCHRONIZED`, `SKIPPED`, `FAILED`, `MANUAL ATTENTION`, както и DOM референциите и `renderSyncSummary()` в `app.js`. Cache-bust на app.js е `v=20261121b`.
- **State:** `Sync history and last result`, `#sync-history`, `renderHistory()` и `/api/history` са изрично запазени; backend sync history, API endpoints и данни не са пипани. Batch проверките, броячите, Sync/Compare/Merge, OAuth/GitHub App и README.md редакцията са непроменени. Няма реален Sync или GitHub write.
- **Tests:** `node --check DASHBOARD\app.js` и `node --check DASHBOARD\utils.js` → OK. Targeted `python -m pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `63 passed, 1 warning in 2.24s`. Пълен `python -m pytest -q -p no:cacheprovider` → `486 passed, 1 warning in 7.66s`. Добавени са `test_repo_status_does_not_display_checked_marker` и `test_sync_results_section_removed_but_history_preserved`; `test_refresh_restores_operation_without_returning_to_zero_counters` е обновен след премахването на `renderSyncSummary()`.
- **Known issues/blockers:** Реална браузърна проверка на DOM не е завършена: CDP табовете са `/dashboard` и `/?switch=1`; `/api/auth/status` връща `401` и Dashboard пренасочва към Welcome. Задължително одобрение от потребителя преди повторно влизане през GitHub UI — не е извършено. При презареждане няма JS exceptions, но трябва да се отбележи, че очакваните `401 /api/auth/status` и `404 /favicon.ico` идват от Welcome таба.
- **Next exact step:** Да се поиска одобрение за повторно влизане през съществуващия GitHub account (или потребителят да влезе ръчно), след което да се презареди `/dashboard` и да се потвърди: без `(CHECKED)`, без `SYNC RESULTS`, налични `Sync history and last result` и `#sync-history`, без JS/API грешки.

## 2026-11-21 16:30 - Smoke проверка на batch проверката
- **Date/time:** 2026-11-21 16:30 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено след проверката; същите uncommitted промени, без commit, push, merge или смяна на клон).
- **Last completed:** Стартиран локалният smoke стек с `./scripts/start-smoke.ps1 -Watchdog` — Broker 8000/`healthz 200`, Dashboard 8001/`dashboard 200`, watchdog активен. Отворен Dashboard в контролиран Chrome (CDP 9224), потвърдена валидна OAuth сесия `AUTHENTICATED` за `GabrielRules`. След автоматични read-only проверки броячите са `39 TOTAL / 34 UP TO DATE / 3 READY TO SYNC / 2 UNSYNCABLE`, статус `Check complete: 39 forks checked`.
- **State:** Код не е променян в тази стъпка — само двата worklog файла. Smoke процесите остават стартирани (Broker PID 7596, Dashboard PID 5684, watchdog PID 21552); контролираният Chrome е PID 24616. `README.md` редакцията на потребителя и всички предходни uncommitted промени са запазени. Няма реален Sync, GitHub write, промяна в OAuth/GitHub App, `.env`, credentials или `data/sync_history.json`.
- **Tests:** Няма ново пускане на pytest. Извършени са само read-only HTTP/CDP проверки: `/healthz` `200`, `/` `200`, `/dashboard` `200`, `/api/auth/status` от браузърната сесия `200 AUTHENTICATED`, `/api/sync` `200`, 39 `.repo-row` в DOM, `readyState=complete`, без JS exceptions, console errors, failed requests или HTTP `>=400`. Снимка: `%TEMP%\opencode\dashboard-20261121-1620.png`; агентът не може да я визуално инспектира, затова заключението е по DOM.
- **Known issues/blockers:** Долната секция `SYNC RESULTS` показва стария запис от 19.11 (`2 SKIPPED / 0 FAILED / 0 MANUAL ATTENTION`), който не е CURRENT counter snapshot; първоначалните `0/0/0/0` бяха междинни преди приключване на проверката. Сесията е за `GabrielRules`, не за `architectquant`; за проверка на 35-те architectquant fork-а е нужен преход към този акаунт с изрично одобрение.
- **Next exact step:** Потребителят визуално потвърди `39 / 34 / 3 / 2` като коректни — batch проверката е потвърдена в реален Dashboard. Ако се изисква architectquant, да се направи read-only проверка след смяна на акаунта; без реален Sync, commit или push.

## 2026-11-21 16:07 - Batch проверка на background fork заявките
- **Date/time:** 2026-11-21 16:07 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (git статус проверен преди и след промените; съществуващите uncommitted промени са запазени, без commit, push, merge или смяна на клон).
- **Last completed:** След изрично одобрение днес frontend-only промяна в `runBackgroundChecks()`: 35-те fork-а се проверяват с 4 `POST /api/sync {dry_run:true, repositories:[...]}` по 10 вместо 35 отделни заявки. Резултатите се мапват по `repository` и се прилагат към пълния дедупликиран масив; грешка/timeout/липсващ резултат маркира само съответните редове. `api/routes.py`, Sync/Compare/Merge, OAuth, counters и история не са променяни. Backup: `%TEMP%\opencode\dreamerol-batch-backup-*`.
- **State:** Променени са `DASHBOARD/app.js`, `tests/test_dashboard_workflow.py` и документацията. Запазени са README редакцията на потребителя и всички предходни uncommitted промени. Няма реален Sync, GitHub write, промяна в `.env`/credentials/`data/sync_history.json` или Git история.
- **Tests:** `node --check DASHBOARD\app.js` и `node --check DASHBOARD\utils.js` → OK; targeted `pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `61 passed, 1 warning`; пълен `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1` → `484 passed, 1 warning in 8.07s`. `git diff --check` показва само предишни CRLF/whitespace предупреждения в `README.md`, `docs/WORKLOG/WORKLOG.md` и `tests/test_sync_history.py`, не от тези кодови промени.
- **Known issues/blockers:** Все още няма браузърна проверка с валидна OAuth сесия след batch промяната; очаква се потребителят да потвърди, че `35/0/0/0 + 35 unverified` е заменено от реални `up-to-date`/`READY TO SYNC` числа. Старият работещ вариант не може да бъде възстановен като код — съществува само в документацията от 17.11; поради това counters не са пипани в тази стъпка.
- **Next exact step:** Потребителят да направи read-only проверка в `http://127.0.0.1:8001/dashboard` с валидна сесия и да сподели финалния статус/броячите; при нужда да се потвърди конкретната грешка от единичен `dry_run`. Без реален Sync, commit или push.

## 2026-11-21 02:27 - Потвърдена Fresh проверка от реалния Dashboard
- **Date/time:** 2026-11-21 02:27 (see `docs/WORKLOG/LOG_21-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (git статус проверен в началото на сесията; съществуващите uncommitted промени са запазени, без commit, push, merge или смяна на клон).
- **Last completed:** С валидна OAuth сесия на `architectquant` в локалния Dashboard потребителят изпълни два пъти read-only `POST /api/debug/compare-forks` (00:20:05Z и 00:23:01Z) и сподели JSON отговорите. И двата са HTTP `200` и напълно съвпадащи по съдържание: `discovery_diagnostics` = 39 owned / 35 fork candidates / 35 valid / 0 unavailable; `total: 4`; 3 репозитория са `VERIFIED_FRESH` + `up-to-date` (`ahead_by=0`, `behind_by=0`) и `architectquant/RUMMIKUB-CONSOLE-GAME` е `VERIFIED_FRESH` + `behind` (`behind_by=1`, `ahead_by=0`, `raw_status=behind`). Няма `UNVERIFIED`, `fresh_api_error`, 404 или масови check failures.
- **State:** Код не е променян в тази стъпка — само `docs/WORKLOG/LOG_21-11-26.md` и този WORKLOG. `README.md` има промени, направени от потребителя днес (184 insertions / 88 deletions спрямо HEAD); агентът не ги е пипал и те трябва да се запазят. Няма реален Sync, GitHub write, промяна в `.env`/credentials, Git история или нови тестове.
- **Tests:** Няма ново пускане на pytest; последните реални резултати остават от 2026-11-20 00:27 (targeted `58 passed`, пълен `481 passed, 1 warning`, `node --check` OK). Настоящата проверка е read-only live API през вече авторизирана браузърна сесия.
- **Known issues/blockers:** `total_commits: 0` при `behind_by: 1` за RUMMIKUB е сурово поле от GitHub Compare API; класификацията ползва само `ahead_by`/`behind_by` (`fork_sync/synchronizer.py:201-230`). `total: 4` е броят на заявените за проверка репозитория, не на всички 35 валидни fork-а. Потвърден симптом (01:48:56): `Check incomplete: 35/35 complete ... 35 unverified` → броячи `35/0/0/0`; debug endpoint-ът (02:20) е read-only и не обновява Dashboard. Проблемът е в автоматичния `/api/sync` check път, не в `computeDashboardCounts()`. Статично потвърдено (02:40), че `api/routes.py:372` вика `get_forks()` за всяка от 35-те заявки (`app.js:682-686`): базово 71 GitHub GET (1 list + 35 discovery + 35 compare), до 1296 при липсващи parent метаданни, ×3 опита при 429/5xx/timeout. Историята пази само summary; реалните per-repo съобщения са само в живия DOM (няма CDP достъп).
- **Next exact step (одобрено 02:50, насрочено за 2026-11-22, днес НЕ е изпълнено):** frontend-only batch проверка — `runBackgroundChecks()` в `DASHBOARD/app.js:663-764` да изпраща всички fork-ове с един `POST /api/sync {dry_run:true, repositories:[...]}` (алтернатива 4×10 по 10, ако се пази прогрес), без промяна в `api/routes.py`, Sync/Compare/Merge, OAuth, counters или история. Предварително read-only потвърждение на съобщението за грешка чрез DOM dump + един суров `dry_run` за RUMMIKUB (`app.js:512` крие backend `message`). След промяната: регресионен тест за 35 fork-а, `node --check`, targeted + пълен pytest, браузърна проверка без реален Sync. Евентуален SYNC само за `architectquant/RUMMIKUB-CONSOLE-GAME` и само с изрично одобрение; без commit/push. Решението е в `DECISIONS.md` под 2026-11-21.

## 2026-11-20 00:27 - Instant readiness в Dashboard след одобрен smoke test
- **Date/time:** 2026-11-20 00:27 (see `docs/WORKLOG/LOG_20-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено преди и след прехвърлянето); няма commit, push, merge или смяна на клон.
- **Last completed:** След изолиран CDP smoke test с mocks (9/9 PASS) и изрично одобрение са прехвърлени файл по файл `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `tests/test_dashboard_workflow.py`; `DASHBOARD/index.html` е само с bump на version query на `20261120a`. Запазени са съществуващите локални промени и counter snapshot логиката от 23:24.
- **State:** Backup `C:\Users\PC-Admin\AppData\Local\Temp\opencode\dreamerol-original-before-instant-20261120-002624` съдържа засегнатите файлове, HEAD/Git status и SHA256 манифест. `README.md`, auth/OAuth, GitHub App, core sync алгоритъмът, `.env`, credentials и `data/sync_history.json` не са пипани. Локалният smoke стек остава активен и обслужва новия код.
- **Tests:** Изолиран mock smoke: 9/9 проверки PASS (`liveCalls=0`); `node --check` за `app.js`/`utils.js` → OK; targeted `pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `58 passed, 1 warning`; пълен `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1` → `481 passed, 1 warning in 7.85s`. HTTP: broker `/healthz` `200 {"status":"ok"}`, `/dashboard` `200`, `/dashboard/static/app.js?v=20261120a` `200` съдържа `runBackgroundChecks`, `backgroundScanActive`, `listErrorMessage`, `isSelectableCandidate`; CSS `200`; `/api/auth/status` без сесия `401` (очаквано).
- **Known issues/blockers:** Няма активни блокери. Няма browser E2E тест в оригиналния проект; frontend поведението е доказано с изолиран headless Chrome CDP smoke с mocks. Screenshot-ите са в `%TEMP%\opencode\dashboard-smoke-success.png` и `%TEMP%\opencode\dashboard-smoke-403.png`.
- **Next exact step:** Потребителят да направи визуална проверка в `http://127.0.0.1:8001/dashboard` с валидна сесия; без commit, push, merge, реален Sync или GitHub write операции.

## 2026-11-19 23:24 - Fix: Sync counters и reload snapshot
- **Date/time:** 2026-11-19 23:24 (see `docs/WORKLOG/LOG_19-11-26.md`)
- **Branch/HEAD:** `feature/github-app-auth` @ `6bde761` (проверено преди промените); няма commit, push, merge или смяна на клон.
- **Last completed:** Поправен е пропускът, установен при визуална проверка: `2 synchronized` в SYNC RESULTS не обновяваше горните четири брояча, а след reload те падаха на `0/0/0/0`. Резултатите вече се обединяват с редовете, успешните целеви репозитория преминават от READY TO SYNC в UP TO DATE, а snapshot от `counts_before` се пази в записа на операцията и се връща от localStorage/`/api/history`. Добавен е version query към JS/CSS, за да не се зарежда стар cache.
- **State:** Променени са `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `DASHBOARD/index.html` и `tests/test_dashboard_workflow.py` (+ документация). `README.md`, `.env`, auth/OAuth, GitHub App и core sync алгоритъмът не са променяни. `data/sync_history.json` съдържа реалната Sync операция на потребителя от визуалната проверка (`GabrielRules/TEST2`, `GabrielRules/TEST3`, `2 synchronized`, `21:10:58Z`) и не е връщан към backup. Агентът не е правил реален Sync или GitHub write операция; локалният стек е рестартиран и обслужва новите файлове.
- **Tests:** `node --check DASHBOARD\app.js` + `node --check DASHBOARD\utils.js` → OK; target `pytest -q -p no:cacheprovider tests/test_dashboard_workflow.py tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `53 passed`; финален `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1` → `476 passed in 7.50s`. HTTP проверки: broker `/healthz` `200 {"status":"ok"}`, `/dashboard` `200`, `/dashboard/static/app.js?v=20261119c` съдържа `operationCountsAfter` и `counts_before`.
- **Known issues/blockers:** Очаква се още една визуална проверка от потребителя: след нов Sync горните числа да се обновят веднага, а след reload да не се връщат на `0/0/0/0`. Няма browser E2E автоматизация. Старите записи в localStorage без `counts_before` не показват snapshot, докато не завърши нова проверка.
- **Next exact step:** Потребителят да направи нов Sync от `http://127.0.0.1:8001/dashboard` и reload; при нужда да се провери Network/Console. Без commit, push, merge или GitHub операции.

## 2026-11-19 22:45 - Dashboard MVP и финална проверка
- **Date/time:** 2026-11-19 22:45 (see `docs/WORKLOG/LOG_19-11-26.md`)
- **Branch/HEAD:** оригиналният проект е `feature/github-app-auth` @ `6bde761` (проверено чрез `git status` / `git rev-parse --short HEAD`); активната работа беше в `%TEMP%\opencode\dreamerol-dashboard-fix`, копие без `.git`.
- **Last completed:** Финална проверка на деветте сценария: operationId lifecycle, рестарт на `sync_history`, двойно стартиране, независими repo-та, timeout/грешка, background polling без презапис, refresh restore, бърз READY и финална safety проверка с потвърждение. Добавени са целеви тестове и autouse изолация на `sync_history`.
- **State:** Проверени чрез SHA-256 файлове: `api/routes.py`, `api/sync_history.py`, `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `DASHBOARD/dashboard.css`, `tests/conftest.py`, `tests/test_sync_history.py`, `tests/test_dashboard_workflow.py`. Документите са обединени върху оригиналната основа без презапис на съществуващи записи. Няма промяна в `.env`, credentials, Git конфигурацията или историята.
- **Tests:** `node --check DASHBOARD\app.js` + `node --check DASHBOARD\utils.js` → `JS_SYNTAX_OK`; целеви `pytest -q tests/test_sync_history.py tests/test_dashboard_workflow.py` → `16 passed, 1 warning`; финален `pytest -q -p no:cacheprovider` с `PYTHONDONTWRITEBYTECODE=1` → `473 passed, 1 warning` (Starlette/httpx deprecation). Тестовете са с mocks/fakes и autouse guard срещу реални GitHub write заявки; `data/sync_history.json` остава идентичен с backup-а.
- **Known issues/blockers:** Няма активни блокери. Няма browser E2E тест; frontend контролът е покрит чрез чисти JS helper тестове и source-level assertions, не чрез реален браузър. Точното JSON тяло от стария live `POST /api/sync` не може да се възстанови от Uvicorn логовете, но не е нужно за текущата поправка.
- **Next exact step:** Локална визуална проверка на новия Dashboard; без commit, push, merge или GitHub операции.

## Current checkpoint
- **Date/time:** 2026-11-18 19:10 (see `docs/WORKLOG/LOG_18-11-26.md`)
- **Branch/HEAD:** feature/github-app-auth @ 1639995 (проверено чрез `git status` / `git rev-parse --short HEAD`; commit `Document GitHub OAuth smoke test results` е направен, push няма; клонът е `ahead 17`)
- **Last completed:** Нов одобрен OAuth login през контролирания Chrome и read-only диагностика на `403` за тестовата двойка. `/api/auth/status` е `200 AUTHENTICATED` с `accountMatchesExpected: true`. GitHub App инсталацията за `GabrielRules` е `All repositories` + `Read and write access to code`. targeted `dry_run:true` за `GabrielRules/TEST` обаче връща HTTP `403` от `GET /user` преди compare; 90-секундно изчакване не промени резултата.
- **State:** Работното дърво е чисто преди тази документална промяна; HEAD `1639995`, ahead 17. Няма промени в source code, auth/OAuth, API, sync логика, `.env`, GitHub App permissions или credentials; няма натискан SYNC, реален Sync, push или извеждане на токени/secrets. Последните GitHub commit-и остават `0c82ac0` (original) и `42212b1` (fork).
- **Tests:** Няма ново пускане на pytest в тази стъпка. Изпълнени са само read-only CDP/HTTP проверки: `/api/auth/status` `200 AUTHENTICATED`, account match `true`, GitHub App installation `All repositories` + code read/write, targeted dry-run `403`, GitHub public rate limit `60 remaining`, repo commit-и непроменени. Последният пълен suite остава `457 passed` от предходната проверка.
- **Known issues/blockers:** fresh OAuth токенът минава логина и `_resolve_account`, но при `POST /api/sync` `GET /user` връща `403` (`api/routes.py:239-248`), затова dry-run не стига до `behind_by`/`ahead_by`. Owner-settings на GitHub App не са достъпни от текущия `GabrielRules` вход (`/settings/apps/dreamerol-sync` → 404), така че account-profile permission и token-expiration Opt-out остават непроверени. 403-ът не е доказан като rate limit след 90s изчакване и публичния IP rate limit е `60`. Натискането на SYNC от потребителя по-рано не промени репозиториите. README пази стария `WEBSITE` URL умишлено; `DREAMEROL FORK SYNC` е за отделна продуктова проверка.
- **Next exact step:** 1) От акаунта собственик на GitHub App да се проверят account/permissions и token expiration Opt-out, без промяна без одобрение. 2) При нужда да се изясни защо токенът губи достъп до `GET /user` веднага след успешен login. 3) НЕ се натиска SYNC, докато targeted dry-run не върне `200` с `behind_by: 3`, `ahead_by: 0`. 4) Push не се прави без изрично одобрение.


## 2026-11-16 07:20 - Fix: Preserve repository status on temporary Preview errors
- **Last completed:** Dashboard fix: temporary Preview/API failures no longer overwrite last known successful repo status or counters (stored as preview_error, shown as check-failed/last-known state); initial failures become unknown (not Diverged); successful Preview clears error and updates status normally. Progressive loading and account isolation preserved.
- **State:** Modified DASHBOARD/app.js, DASHBOARD/utils.js, 	ests/test_dashboard_progress.py, docs/WORKLOG/LOG_16-11-26.md, docs/WORKLOG/WORKLOG.md (plus prior uncommitted workspace changes preserved). No Sync/Compare/Merge algorithm changes, no real Sync, no commit/push.
- **Tests:** 
ode --check DASHBOARD/app.js DASHBOARD/utils.js web/app.js OK; python -m pytest tests/test_dashboard_progress.py -q → 14 passed; python -m pytest tests/test_sync_history.py tests/test_dashboard_progress.py tests/test_api.py tests/test_web_auth.py -q → 65 passed, 1 warning (env starlette/httpx deprecation). No real Sync executed.
- **Next exact step:** Restart smoke if needed and manually verify in browser that transient Preview errors preserve prior status/counters and clear on next successful Preview; do not run real Sync or commit/push.

## 2026-11-16 07:47 - Fix: Preview UX (spinner only) and preview state correctness
- **Last completed:** Removed Preview progress bar/thermometer completely (UI/CSS/logic), leaving only spinner + "Checking repositories…" shown immediately and always hidden on success/error/cancel/completion. Fixed stale/incorrect preview state (e.g. indicator stuck after complete, partial counts like 1/6, old preview mutating new state) via generation-guarded updates, AbortController/session isolation, and centralized finalize in finally/abort for current generation only.
- **State:** Modified DASHBOARD/index.html, DASHBOARD/app.js, DASHBOARD/utils.js, DASHBOARD/dashboard.css, 	ests/test_dashboard_progress.py, docs/WORKLOG/LOG_16-11-26.md, docs/WORKLOG/WORKLOG.md (plus prior uncommitted workspace changes preserved). No Sync/Compare/Merge algorithm changes, no real Sync, no GitHub/credential/history changes, no commit/push.
- **Tests:** 
ode --check DASHBOARD/app.js DASHBOARD/utils.js web/app.js OK; python -m pytest tests/test_dashboard_progress.py -q → 25 passed; python -m pytest tests/test_sync_history.py tests/test_dashboard_progress.py tests/test_api.py tests/test_web_auth.py -q → 76 passed, 1 warning (env starlette/httpx deprecation). No real Sync executed. (Visual behavior requires browser/smoke restart to confirm.)
- **Next exact step:** Restart smoke (scripts/stop-smoke.ps1 / scripts/start-smoke.ps1 -Watchdog) and manually verify in browser: spinner shows at Preview start and disappears on complete/error/cancel/account switch, no stuck "checking...", counters/list consistent and deduped; do not run real Sync or commit/push.

## 2026-11-16 08:14 - Диагностика: Preview връща 0 или масови временни грешки (предложение)
- **Last completed:** Диагностика без промени по код: \ /0/0/0\ се обяснява с успешен list (\mode:"list"\) и празен \get_forks\ за текущия auth/достъп контекст; случай \34/1/0/0 + 33 temporary check failure(s)\ с пер-repo грешки (unknown при липса на известен статус) без превръщане в Diverged. Записано предложение в \DECISIONS.md\.
- **State:** Променени само документация/логове: \docs/WORKLOG/LOG_16-11-26.md\, \docs/WORKLOG/WORKLOG.md\, \DECISIONS.md\ (предишни uncommitted кодови промени в работното дърво са запазени). Без промени в Sync/Compare/Merge, без реален Sync, без промени в GitHub/credentials/история, без commit/push.
- **Tests:** не са изпълнявани нови тестове в тази стъпка (само анализ/документация).
- **Next exact step:** Утре (1) да се потвърди в Network отговорът на \POST /api/sync\ (\mode:"list"\ и per-repo) и активният акаунт; (2) при нужда да се добави минимална read-only list диагностика и стабилизиране при масови временни грешки (retry/backoff/понижен concurrency, неутрален тон) с регресионни тестове, без промяна на Sync/Compare/Merge и без реален Sync.

## 2026-11-17 15:52 - BEHIND/AHEAD анализ (без кодови промени)
- **Last completed:** Анализ на текущия алгоритъм: behind/ahead идват от `ahead_by`/`behind_by` на официалния GitHub Compare API (`fork_sync/github.py:99-110`, `fork_sync/synchronizer.py:92-102`), без локална git/divergence калкулация. Потвърдено е, че се сравняват default branch на upstream (base) и fork (head), без разместване на посоките. Петте GabrielRules fork-а (AI-STUDIO, PORTFOLIO, CARDFOLIO, ALLSTATS, RESUME) са проверени срещу GitHub API: всички `identical`, `ahead_by=0`, `behind_by=0`, кодовият и каноничният URL дават еднакви стойности. Потребителят потвърди този обхват като целеви; кодовите промени са изрично отложени за отделно одобрение.
- **State:** Променени само `docs/WORKLOG/LOG_17-11-26.md` и `docs/WORKLOG/WORKLOG.md`. Предходните uncommitted кодови промени са запазени; няма промени в Sync/Compare/Merge, няма реален Sync, няма промени в GitHub/credentials/история, няма commit/push.
- **Tests:** Не са изпълнявани нови тестове в тази стъпка (само analysis и live GitHub API проверки чрез временни скриптове извън репото).
- **Next exact step:** Изчакване на изрично одобрение за минимална read-only диагностика и толерантност към изчезнали fork-ове (404) според `DECISIONS.md`; без промяна в Sync/Compare/Merge, без реален Sync, без commit/push.

## 2026-11-17 15:57 - Read-only диагностика и 404 толерантност
- **Last completed:** След изрично одобрение е добавена минимална read-only диагностика в `POST /api/sync` при `dry_run:true, mode:"list"` — ново поле `diagnostics` с `owned_repositories`, `fork_candidates`, `valid_forks`, `unavailable_forks` (в останалите режими е `null`). `ForkSynchronizer.get_forks()` вече пази тези броячи и пропуска fork, чието доизвличане на родител върне HTTP 404, вместо да прекъсва цялото изброяване с 502. `preview_fork` запазва 404 като `error` с ясен HTTP детайл; Compare/Merge алгоритъмът не е променен.
- **State:** Променени: `api/routes.py`, `fork_sync/synchronizer.py`, `tests/test_api.py`, `tests/test_synchronizer.py`, `tests/test_web_auth.py`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Предходните uncommitted кодови промени са запазени; няма реален Sync, няма промени в GitHub/credentials/история, няма commit/push.
- **Tests:** `python -m pytest tests/test_synchronizer.py tests/test_api.py -q` → **41 passed, 1 warning**; `python -m pytest -q --ignore=tests/test_dashboard_progress.py` → **387 passed, 1 warning** (starlette/httpx deprecation); `python -m compileall -q api/routes.py fork_sync/synchronizer.py tests/test_api.py tests/test_synchronizer.py tests/test_web_auth.py` → OK; `git diff --check` → само CRLF предупреждения. Пълният `python -m pytest -q` е блокиран от предходен `SyntaxError` в `tests/test_dashboard_progress.py:199` (walrus в `assert` без скоби), несвързан с тези промени.
- **Next exact step:** Проверка в браузър/Network на реалния list отговор с новите диагностични броячи; при желание отделно одобрение за поправка на предходния синтаксис на `tests/test_dashboard_progress.py:199`. Без реален Sync и без commit/push.

## 2026-11-17 16:06 - Проверка на diagnostics чрез Dashboard (спряно)
- **Last completed:** Локалният smoke стек е стартиран (Broker 8000, Dashboard 8001; `healthz` и двата OK) и Dashboard-ът е отворен в браузъра. Реалните четири diagnostics числа от `POST /api/sync` (`mode:"list"`) не са получени, защото няма достъп до браузърния Network панел и няма валидна сесия/PAT в това средище; публичният GitHub core rate limit е 9 оставащи заявки. Потребителят избра „Спираме тук“.
- **State:** Код не е променян след 15:57; само `docs/WORKLOG/LOG_17-11-26.md` и `docs/WORKLOG/WORKLOG.md`. Smoke процесите остават стартирани; Предходните uncommitted промени са запазени; без реален Sync и без commit/push.
- **Tests:** Не са изпълнявани нови тестове в тази стъпка.
- **Next exact step:** Когато потребителят реши: да се логне в отворения Dashboard, да направи `mode:"list"` заявка и да сподели `diagnostics` обекта (или да осигури авторизация за директно извикване). Без кодови промени без изрично одобрение.

## 2026-11-17 20:09 - Hero композиция и четири филтъра
- **Last completed:** Hero изображението вече е чист нормален поток в началото на картата, без HTML дублиране на DREAMEROL SYNC/подзаглавие върху него. Акаунтът е в отделен dark-glass ред под изображението, дясно подравнен; следва един purple-to-blue `SYNC` бутон, центриран в същата карта, и компактен статус. Статусните тонове са неутрален/зелен/жълт/червен според реалното съобщение; премахнат е червеният вид при нормална проверка с UNSYNCABLE/AHEAD.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `DASHBOARD/app.js`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Филтърът е само `ALL`, `UP TO DATE`, `TO BE SYNCED`, `UNSYNCABLE`; AHEAD-only остава видим като `AHEAD-ONLY` с tooltip в UNSYNCABLE. Без промяна в класификацията, counters, API, auth или sync логиката; без реален Sync, commit или push.
- **Tests:** `node --check DASHBOARD/app.js` и `node --check DASHBOARD/utils.js` → OK. Headless Chrome/CDP при 1440/1024/390 px → 1 SYNC бутон, 0 CHECK бутона, 4 опции, 4 карти, естествено изображение `1672x941`, `scrollWidth = innerWidth`, без припокриване и с центриран бутон. `python -m pytest -q tests/test_api.py tests/test_dashboard_strict_counts.py tests/test_web_auth.py` → `69 passed, 1 warning`.
- **Next exact step:** Ръчна проверка в браузър с валидна OAuth сесия; при нужда само фина настройка на визуални разстояния. Без реален Sync, Git cleanup, commit или push.

## 2026-11-17 20:17 - Фаза 1: точни PENDING/CHECKING състояния и зелен SYNC
- **Last completed:** Добавени са ясни състояния `PENDING`, `CHECKING`, `UP TO DATE`, `TO BE SYNCED` и UNSYNCABLE подкатегории `AHEAD-ONLY`, `DIVERGED`, `ERROR`. Чакащите проверки вече не се показват като ERROR; прогресът и статусът показват само завършени проверки и намаляващ pending брой; статистите показват `CHECKING` по време на проверка и реални числа след край. Непълна проверка се маркира като incomplete вместо завършена. Единственият SYNC бутон вече е green gradient със зелен glow, без промяна на hero, позиция, потвърждение или sync safety.
- **State:** Променени: `DASHBOARD/app.js`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма промени в backend, API, auth, OAuth, synchronization или съществуващи тестове; без реален Sync, commit или push.
- **Tests:** `node --check` за `app.js`/`utils.js` → OK; `python -m pytest -q tests/test_api.py tests/test_dashboard_strict_counts.py tests/test_web_auth.py` → `69 passed, 1 warning`. Headless Chrome с 36 mock записа: междинно `33 PENDING + 3 CHECKING`, `0 PENDING като ERROR`, `CHECKING` статистики; финално `0 PENDING/0 CHECKING`, `36 / 36`, `36 = 30 + 2 + 4`, реални ERROR и AHEAD-ONLY редове, един green SYNC бутон с white text.
- **Next exact step:** Фаза 2 — само read-only проверка на реална сесия/payload, броячи, автоматична проверка, липса на CHECK, hero/SYNC позиция и SyntaxError; без файлови промени и без реален Sync.

## 2026-11-17 20:30 - CHECK FAILED / UNVERIFIED вместо потвърдено UNSYNCABLE
- **Last completed:** Неуспешните или непотвърдени per-repo проверки вече се показват като `CHECK FAILED / UNVERIFIED`, не се влагат в `UNSYNCABLE` и спират финалното показване на четирите брояча. Успешните числови класификации остават непроменени, а последното известно състояние се показва като `(LAST KNOWN)` с изрично предупреждение, че числата са непълни.
- **State:** Променени: `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `DASHBOARD/dashboard.css`, `tests/test_dashboard_strict_counts.py`, `tests/test_dashboard_progress.py`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`, `docs/development/CHANGELOG_AI.md`. Запазени са всички предходни uncommitted промени; без промени в OAuth, API, discovery, Compare/Merge или Sync; без реален Sync, commit или push.
- **Tests:** `node --check` за `app.js`/`utils.js` → OK; `git diff --check` → OK; `python -m pytest -q` → `428 passed, 1 warning`. Inline helper проверката даде `36/34/0/2` при пълни данни и `36/0/0/2 + 34 check errors` при масови неуспешни проверки.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия и реални per-repo отговори; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 20:36 - Premium emerald 3D SYNC и центриран акаунт панел
- **Last completed:** SYNC бутонът вече е наситено green/emerald с 3D дълбочина: gradient `#39E879 → #16C75B → #079447`, долен ръб `#056B35`, горен highlight, фини layered сенки, subtle glow, white bold текст, hover lift `-2px` и pressed `+4px`. Акаунт панелът е преместен в собствен центриран ред под бутона и пред статуса.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Запазени са всички предишни uncommitted промени; hero изображението, JS поведението, OAuth, API и Sync логиката не са променяни; без реален Sync, commit или push.
- **Tests:** CDP проверки при 1440×1200 и 390×844 → ред `artwork → SYNC → account → status → stats`, центриране на бутон и акаунт, без припокриване/horizontal overflow, 1 SYNC бутон, 0 CHECK бутони, hero изображение заредено `1672×941`; проверка на button states → emerald gradient, 3D shadow, hover `-2px`, pressed `+4px` = `true`. `node --check` за `app.js`/`utils.js` → OK; `git diff --check -- DASHBOARD/index.html DASHBOARD/dashboard.css` → OK.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия за новия ред/стил и реални per-repo отговори; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 20:47 - Горна лента с акаунт и SYNC ALL под hero
- **Last completed:** Създадена е тънка dark-glass лента над hero с лява идентичност `DREAMEROL SYNC` и десен компактен GitHub акаунт панел. Акаунтът вече не е част от hero; единственият бутон е `SYNC ALL`, центриран директно под непромененото hero изображение. Съществуващият `#sync-button-label` остава в DOM като скрит, за да не се променя JS поведението.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Запазени са всички предишни uncommitted промени; няма промени в JS, counters, classification, OAuth, API, backend или Sync; без реален Sync, commit или push.
- **Tests:** CDP проверки при 1440×1200 и 390×844 → `oneSyncAllButton`, `noCheckButton`, `jsLabelPreserved`, `accountAboveHero`, `accountFieldsVisible`, `desktopAccountRight`, `mobileBrandAboveAccount`, `heroArtUnchanged`, `aspectRatioPreserved`, `heroFullWidth`, `noAccountOverlayOnHero`, `syncDirectlyBelowHero`, `syncCentered`, `statusAfterSync`, `statsAfterStatus`, `repoAfterStats`, `toolsInsideRepo`, `noOverlap`, `noOverflow`, `topStripSlim`, `darkGlassStrip` = `true`; desktop лента `62px`, mobile лента `120px`; 1 SYNC ALL бутон, 0 CHECK бутони. `node --check` за `app.js`/`utils.js` → OK; `git diff --check -- DASHBOARD/index.html DASHBOARD/dashboard.css` → OK.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия за реални `GabrielRules`/`GitHub Connected`, новия ред/стил и реални per-repo отговори; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 20:58 - Финална лента с акаунт и premium emerald 3D бутон
- **Last completed:** Горната лента е опростена: премахнати са `Active account`, `GitHub Connected` и Switch account. Останаха GitHub икона, потребителско име, green indicator само при `is-online` и един auth контрол — `Sign out` при успешна авторизация или `Sign in` към съществуващия welcome URL в останалите състояния. Бутонът `SYNC ALL` вече използва точната палитра `#39E879 / #16C75B / #079447 / #056B35`, 20px радиус, по-широко разстояние между буквите и изразени hover/pressed/disabled състояния.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Запазени са всички предишни uncommitted промени; няма промени в JS, counters, classification, OAuth, API, backend или Sync; без реален Sync, commit или push.
- **Tests:** CDP проверки при 1440×1200 и 390×844 → layout checks = `true`; симулирани auth състояния → authenticated: `GabrielRules` видимо, green indicator видим, `Sign out` видим, `Sign in` скрит, само един контрол; unauthenticated/error: само `Sign in`. Проверки на бутона → emerald gradient, white bold text, 3D lower edge/top highlight/glow, 20px radius, `2.16px` letter spacing, hover `-2px`, pressed `+4px`, smaller pressed shadow, disabled appearance = `true`. `node --check` за `app.js`/`utils.js` → OK; `git diff --check` → OK; `python -m pytest -q tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `35 passed`.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия за реалния authenticated вид и реални per-repo отговори; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 21:05 - Само SYNC ALL в бутона и разширяване
- **Last completed:** Премахнати са `#sync-button-label`, `#sync-button-count` (`Select TO BE SYNCED forks`) и CSS за вторичния текст. Бутонът съдържа само `SYNC ALL`, разширен е до `520×74` desktop / `328×68` mobile и остава центриран под hero с непроменена emerald 3D палитра. `Restoring session...` е преместен в status зоната след progress панелите; JS съобщенията не са променени.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Добавен е скрит `#user-avatar` за съществуващия JS reference. Няма промени в JS, counters, classification, OAuth, API, backend, synchronization scope/selection/confirmation или Sync; без реален Sync, commit или push.
- **Tests:** CDP `verify-final-button-cleanup.cjs` при 1440×1200 и 390×844 → всички проверки за текст, липса на вторичен текст, статус зона, ширина/височина, центриране, hero и emerald палитра = `true`. `verify-final-nav-button.cjs` и `verify-premium-button-states.cjs` → `true`; `node --check`, `git diff --check` → OK; `pytest` → `35 passed`.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия за реалния вид и реални per-repo отговори; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 21:11 - Disabled оптимизация и гравиран 3D текст
- **Last completed:** Disabled състоянието на `SYNC ALL` е направено по-ясно и по-малко бледо: `opacity:0.9`, `brightness(0.9) saturate(0.82)`, запазена emerald палитра и lower edge, намален glow, `cursor:not-allowed` и фин анимиран sheen като индикатор за незавършена проверка. При hover върху disabled бутона CSS показва tooltip с реалните условия: проверката на репозиториите да завърши и да има избран подходящ fork. `SYNC ALL` получи слоест text-shadow за фино гравиран ефект, без промяна в повдигнатия вид на самия бутон.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма промени в HTML, JS, counters, classification, OAuth, API, backend, synchronization scope/selection/confirmation или Sync; без реален Sync, commit или push.
- **Tests:** CDP при 1440×1200 и 390×844 → enabled checks `noTooltipWhenEnabled`, `noShimmerWhenEnabled`, `engravedLettering`, `wideButton`, `buttonCentered`, палитра/3D = `true`; disabled checks `disabledNotPale`, `greenPreserved`, `raisedWhenDisabled`, `reducedGlow`, `checkingSheen`, `tooltipVisible`, `engravedTextDisabled` = `true`. `verify-premium-button-states.cjs` и `verify-final-nav-button.cjs` → `true`; `node --check`, `git diff --check` → OK; `pytest` → `35 passed`.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия за tooltip/sheen, гравирания текст и реални per-repo отговори; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 21:22 - Поправка на размера на GitHub аватара
- **Last completed:** GitHub аватарът в горната лента вече е малък кръгъл профилен образ с фиксирани `40×40px` desktop / `36×36px` mobile размери. Добавени са `flex:0 0 auto`, `object-fit:cover`, `border-radius:50%`, `overflow:hidden` и защита от разтягане; при показан avatar GitHub иконата се крие, а при скрит avatar старата икона остава.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма промени в HTML, JS, avatar source, counters, OAuth, API, backend, synchronization scope/selection/confirmation или Sync; без реален Sync, commit или push.
- **Tests:** CDP `verify-avatar-size.cjs` при 1440×1200 и 390×844 → всички проверки за размери, кръгла форма, object-fit, подравняване, липса на припокриване/overflow и невлияние върху hero = `true`. `verify-final-nav-button.cjs` и `verify-final-button-cleanup.cjs` → `true`; `node --check`, `git diff --check` → OK; `pytest` → `35 passed`.
- **Next exact step:** Ръчна браузърна проверка с валидна OAuth сесия за реалния avatar URL и подравняването; без реален Sync, Git cleanup, commit или push.

## 2026-11-17 21:30 - Край на деня checkpoint
- **Last completed:** Обновени са `CURRENT_STATUS.md` и `NEXT_STEPS.md` с актуалното състояние; по-старите секции от 2026-11-15 са запазени като исторически. Прегледани са Git статусът, клон/HEAD и днешният worklog.
- **State:** Запазени са 27 променени tracked файла, 2 изтрити root лога (с копия в `docs/WORKLOG/`) и 24 untracked файла. Няма изчистване, restore, stash, reset, checkout, commit или push. Няма нови кодови или дизайн промени.
- **Tests:** Не са стартирани нови тестове в тази стъпка; записани са последните реални резултати от деня: `428 passed, 1 warning` (20:30), targeted `35 passed` (21:22), CDP проверки `true`, `node --check` и targeted `git diff --check` OK.
- **Next exact step:** Валидна OAuth браузърна проверка → GitHub App settings → реален smoke login/preview/sync/logout → пълни проверки преди одобрен commit/push.

## 2026-11-17 21:36 - Финална visual polish на SYNC ALL бутона
- **Last completed:** `DASHBOARD/dashboard.css` вече задава по-ярък наситен emerald gradient (`#3BEE7E → #16D46A → #079447`) с фина green glow, по-голям bold white текст (`22px` desktop / `20px` mobile), по-голям SYNC икон (`28px` / `24px`) и леко по-широк бутон (`560px` desktop). Запазени са premium 3D дълбочината, гравираният текст, центрирането и disabled tooltip/sheen.
- **State:** Променени: `DASHBOARD/dashboard.css`, `CURRENT_STATUS.md`, `NEXT_STEPS.md`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма HTML/JS/backend/OAuth/API/counter/selection/safety/sync промени; hero artwork и account navigation са непроменени; без commit или push.
- **Tests:** CDP `verify-final-button-cleanup.cjs` и `verify-premium-button-states.cjs` при 1440×1200 и 390×844 → всички checks `true`, включително четливост, по-голям текст/икон, brighter border, emerald gradient/glow и disabled състояние. `verify-final-nav-button.cjs` и `verify-avatar-size.cjs` → `true`; `node --check`, targeted `git diff --check` → OK; targeted `pytest` → `35 passed`.
- **Next exact step:** Валидна OAuth браузърна проверка на реалния вид и counters → GitHub App settings → реален smoke login/preview/sync/logout → пълни проверки преди одобрен commit/push.

## 2026-11-17 21:41 - Изчистване на етикета UNSYNCABLE (DIVERGED)
- **Last completed:** Етикетът в таблицата с репозитории за `diverged` е само `UNSYNCABLE`; премахнати са `(DIVERGED)` и скобите само в frontend presentation слоя.
- **State:** Променени: `DASHBOARD/app.js`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Запазени са вътрешната класификация, ahead/behind детекцията, tooltip, counters, филтриране, selection, safety и synchronization логиката. Другите етикети не са променяни; без commit или push.
- **Tests:** `node --check DASHBOARD/app.js`, `node --check DASHBOARD/utils.js`, targeted `git diff --check -- DASHBOARD/app.js` → OK; `python -m pytest -q tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `35 passed`.
- **Next exact step:** Валидна OAuth браузърна проверка на реалния етикет и counters → GitHub App settings → реален smoke login/preview/sync/logout → пълни проверки преди одобрен commit/push.

## 2026-11-17 21:49 - Увеличени SYNC икон и текст в бутона
- **Last completed:** `.button-icon` е `40px` desktop / `32px` mobile, а `.sync-title` (`SYNC ALL`) е `32px` desktop / `26px` mobile; бутонът е `600×86` desktop и остава центриран. Вкопаният ефект е засилен с допълнителни text-shadow и drop-shadow слоеве.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма HTML/JS/backend/OAuth/API/counter/selection/safety/sync промени; hero и account navigation са непроменени; без commit или push.
- **Tests:** CDP `verify-final-button-cleanup.cjs` и `verify-premium-button-states.cjs` при 1440×1200 и 390×844 → всички checks `true`, включително `largerLettering`, `largerIcon`, `engravedLettering`, `disabledNotPale` и `engravedTextDisabled`. `node --check`, targeted `git diff --check` → OK; targeted `pytest` → `35 passed`.
- **Next exact step:** Потвърди визуално с валидна OAuth сесия, че по-големите икон/текст са четливи в реален dashboard → GitHub App settings → smoke login/preview/sync/logout → пълни проверки преди одобрен commit/push.

## 2026-11-17 22:06 - Брандинг GITHUB SYNC CENTER — by DREAMEROL
- **Last completed:** `.brand` вече съдържа точно `GITHUB SYNC CENTER — by DREAMEROL` с отделни primary/secondary span-ове и emerald-green маркер/разделител. Primary е bold `13px` desktop / `11px` mobile, secondary е medium `11px` / `9px`.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_17-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Навигацията остава `74px` desktop / `93px` mobile; account панелът `255×56` / `340×54`, hero `1672×941`, sign-in URL и логиката са непроменени; без commit или push.
- **Tests:** CDP `verify-branding.cjs` при 1440×1200 и 390×844 → всички checks `true`. `node --check`, targeted `git diff --check` → OK; targeted `pytest` → `35 passed`.
- **Next exact step:** Потвърди визуално с валидна OAuth сесия → GitHub App settings → smoke login/preview/sync/logout → пълни проверки преди одобрен commit/push.

## 2026-11-18 01:35 - Само последен резултат в LAST SYNC RESULTS
- **Last completed:** В `Sync history and last results` вече има една секция с едно подзаглавие `LAST SYNC RESULTS` и един ред с последното събитие, форматирано като `време: резюме`. Премахнати са `HISTORY` и `#sync-results`, за да не се показват празен/дублиращ се списък.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/app.js`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Запазени са всички предишни uncommitted промени; без промени в auth, API, counters, sync логиката или Git история; без commit или push.
- **Tests:** `node --check` за `app.js`/`utils.js` и targeted `git diff --check` → OK; `python -m pytest -q tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `35 passed`; CDP `verify-last-result.cjs` при 1440×1200 и 390×844 → всички checks `true`.
- **Next exact step:** Потвърди с валидна OAuth сесия реалното време/резюме в отворения details панел; без реален Sync и без commit/push.

## 2026-11-18 01:43 - Резултатът в реда на менюто след тире
- **Last completed:** `#sync-history` е вътре в `<summary>` на `Sync history and last results`; тирето се добавя само чрез CSS `::before`, когато има запис. Премахнати са `<h3>LAST SYNC RESULTS</h3>` и всякаква видима bullet/списъчна форматировка; на desktop редът е един, на mobile се пренася естествено.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. JS, данни, timestamps, съобщения и functionality не са променяни; без commit или push.
- **Tests:** `python -m pytest -q tests/test_dashboard_strict_counts.py tests/test_dashboard_progress.py` → `35 passed`; CDP `verify-inline-result.cjs` при 1440×1200 и 390×844 → всички checks `true`.
- **Next exact step:** Проверка с валидна OAuth сесия, че реалният запис се появява в реда на менюто след тире; без реален Sync и без commit/push.

## 2026-11-18 01:51 - Стрелката на details реда е премахната
- **Last completed:** `summary` е `display: block` с `list-style: none`, празен `::marker` и скрит `::-webkit-details-marker`; визуалната стрелка пред `Sync history and last results` вече не се показва.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. HTML и JS не са променяни в тази стъпка; без commit или push.
- **Tests:** CDP `verify-inline-result.cjs` при 1440×1200 и 390×844 → всички checks `true`, включително `noDisclosureArrow`.
- **Next exact step:** Визуална проверка с валидна OAuth сесия; без реален Sync и без commit/push.

## 2026-11-18 01:59 - by DREAMEROL сочи към GitHub профила
- **Last completed:** Текстът `by DREAMEROL` в горния банер е обграден с `<a href="https://github.com/Dreamerol/" target="_blank" rel="noopener noreferrer">`. Добавени са `text-decoration: none` и под черта само при hover; останалите стилове са непроменени.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма JS, auth, API или sync промени; без commit или push.
- **Tests:** CDP `verify-brand-link.cjs` и `verify-branding.cjs` (1440×1200, 390×844) → всички checks `true`.
- **Next exact step:** Клик в браузър с валидна сесия да отвори профила; без реален Sync и без commit/push.

## 2026-11-18 02:03 - Hero изображението е линк към GitHub профила
- **Last completed:** `.hero-art` е обграден с `<a class="hero-art-link" href="https://github.com/Dreamerol/" target="_blank" rel="noopener noreferrer">`; добавен е `display:block; width:100%`, за да не се промени разположението. SYNC бутонът и `.hero-controls` не са в линка.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма JS, auth, API или sync промени; без commit или push.
- **Tests:** CDP `verify-brand-link.cjs` и `verify-branding.cjs` (1440×1200, 390×844) → всички checks `true`.
- **Next exact step:** Визуална проверка на клика в браузър с валидна сесия; без реален Sync и без commit/push.

## 2026-11-18 02:08 - Кредит в десния край на долния ред
- **Last completed:** Добавен е `.activity-credit` с текст `Made with ❤️ by Dreamerol · MIT Licensed`; `summary` е `display:flex` с `justify-content: space-between` и `flex-wrap: wrap`, за да е вдясно на desktop и да се пренася на mobile. Стрелката остава скрита, без заглавие и bullets.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма JS, auth, API или sync промени; без commit или push.
- **Tests:** CDP `verify-inline-result.cjs` при 1440×1200 и 390×844 → всички checks `true`.
- **Next exact step:** Потвърди визуално с валидна OAuth сесия; без реален Sync и без commit/push.

## 2026-11-18 02:13 - Падащо меню само с последния резултат
- **Last completed:** Върнати са нативната стрелка и етикетът `Sync history and last result`. `#sync-history` е извън `<summary>` и се показва само при отваряне; `renderHistory()` пак подава един запис чрез `history.slice(0, 1)`. Кредитът и линковете остават непроменени.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма JS, auth, API или sync промени; без commit или push.
- **Tests:** CDP `verify-dropdown-result.cjs` при 1440×1200 и 390×844 → всички checks `true`.
- **Next exact step:** Потвърди с валидна OAuth сесия реалното отваряне и записа; без реален Sync и без commit/push.

## 2026-11-18 02:19 - Стрелката подравнена с етикета на долния банер
- **Last completed:** `summary` използва CSS триъгълник (`::before`) вместо нативен маркер, за да не се изнася на отделен ред; `align-items:flex-start` + `margin-top:5px` го подравняват с първия текстови ред. При `details[open]` стрелката се завърта на 90°.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. HTML, JS, данни и functionality не са променяни; без commit или push.
- **Tests:** CDP `verify-dropdown-result.cjs` при 1440×1200 и 390×844 → всички checks `true`.
- **Next exact step:** Визуална проверка с валидна OAuth сесия; без реален Sync и без commit/push.

## 2026-11-18 02:22 - Кредитът е линк към портфолиото
- **Last completed:** `.activity-credit` е `<a href="https://dreamerol.github.io/MIHAELA-KOSEVA-AI/" target="_blank" rel="noopener noreferrer">`; добавени са `text-decoration:none` и под черта само при hover.
- **State:** Променени: `DASHBOARD/index.html`, `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма JS, auth, API или sync промени; без commit или push.
- **Tests:** CDP `verify-dropdown-result.cjs` при 1440×1200 и 390×844 → всички checks `true`, включително `creditLink`.
- **Next exact step:** Потвърди клика в браузър; без реален Sync и без commit/push.

## 2026-11-18 02:27 - Последният резултат е точно под етикета
- **Last completed:** `.activity-dropdown-result` няма ляв отстъп, тирето е на `li::before` (на един ред с данните), а отвореният `<summary>` има `padding-bottom:6px`. Текстът на резултата започва на същия x като етикета и на 6px под него на desktop.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. HTML, JS и данни не са променяни; без commit или push.
- **Tests:** CDP `verify-dropdown-result.cjs` при 1440×1200 и 390×844 → всички checks `true`, включително `resultUnderLabel` и `resultCloseToLabel`.
- **Next exact step:** Потвърди визуално с валидна OAuth сесия; без реален Sync и без commit/push.

## 2026-11-18 02:32 - Премахнато "0 unverified" от резюмето
- **Last completed:** В `renderHistory()` от шаблона на `summary` е изтрит `${unverified} unverified, `; примерният ред вече е `02:29:47: Automatic check: 36/36 complete, 36 forks, 34 up to date, 0 to be synced, 2 unsyncable`. Логиката за `needsAttention`, `checkingIncomplete` и съобщенията за проверки остава.
- **State:** Променени: `DASHBOARD/app.js`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Няма HTML/CSS, auth, API или sync промени; без commit или push.
- **Tests:** `node --check DASHBOARD/app.js` → OK; `python -m pytest -q` → `428 passed, 1 warning`; CDP `verify-dropdown-result.cjs` при 1440×1200 и 390×844 → всички checks `true`.
- **Next exact step:** Потвърди реалния запис с валидна OAuth сесия; без реален Sync и без commit/push.

## 2026-11-18 02:38 - Статусните етикети в списъка са центрирани
- **Last completed:** `.repo-status` в `DASHBOARD/dashboard.css:400` използва `justify-self: center`. Етикетите `UP TO DATE` и `TO BE SYNCED` в `#repo-list` вече имат общ хоризонтален център в своята колона.
- **State:** Променени: `DASHBOARD/dashboard.css`, `docs/WORKLOG/LOG_18-11-26.md`, `docs/WORKLOG/WORKLOG.md`. Само визуално подравняване; без HTML/JS/данни и без commit или push.
- **Tests:** CDP `measure-status-alignment.cjs` при 1440×1200 и 390×844 → център 510 / 200 за двата етикета, `noHorizontalOverflow: true`; `verify-dropdown-result.cjs`, `verify-brand-link.cjs`, `verify-branding.cjs` → всички checks `true`.
- **Next exact step:** Визуална проверка с реални форкове и валидна OAuth сесия; без реален Sync и без commit/push.

## 2026-11-18 03:11 - Security hardening преди публичен release
- **Last completed:** Приложен е одобреният minimal release-hardening пакет: `COOKIE_SECURE=auto` с възможност за `true`/`false`, Origin/Referer проверка за POST `/api/*`, redaction на callback `code`/`state` в access логовете, periodic cleanup на изтекли Broker транзакции, `openapi_url=None`, browser security headers и origin-relative frontend URL-и.
- **State:** HEAD `629afbb`, branch `feature/github-app-auth`, ahead 13. Променени: 27 tracked + docs, 2 изтрити root лога, 25 untracked файла (11 директории), 0 staged. Без commit, push, branch switching, реален Sync или промяна в GitHub настройките.
- **Tests:** `python -m pytest -q` → `434 passed, 1 warning`; `node --check web/app.js` и `node --check DASHBOARD/app.js` → OK; `git diff --check` → само LF→CRLF warnings; CDP `verify-dropdown-result.cjs`, `verify-brand-link.cjs`, `verify-branding.cjs`, `measure-status-alignment.cjs` → всички checks `true`.
- **Next exact step:** Phase 3 read-only synchronization safety review; потвърждение на реалните GitHub App permissions/callback/installation от GitHub UI; без реален Sync и без commit/push.

## 2026-11-18 03:19 - Phase 3 read-only synchronization safety review
- **Last completed:** Статичен одит на sync entry points, dry-run/confirmationcontract, единствената мутираща GitHub операция (`POST /merge-upstream`), fork/upstream валидация, error handling и test coverage. Няма промени в `fork_sync/`, `api/routes.py`, `main.py` или frontend логиката.
- **State:** HEAD `629afbb`, branch `feature/github-app-auth`, ahead 13. Без реален Sync, commit/push или GitHub промени. Констатациите са само докладвани; не е прилагана корекция по sync логиката.
- **Tests:** В Phase 3 не са пускани тестове (read-only static review); последният изпълнен suite остава `434 passed, 1 warning` от 03:11.
- **Next exact step:** Да се одобрят или отхвърлят предложените minimal sync-safety корекции; след това Phase 4 release/stability checks. Без реален Sync и без commit/push.

## 2026-11-18 03:32 - Минимални sync-safety корекции
- **Last completed:** Приложени са точки 2–5 от Phase 3 и тестовете от точка 7: `ambiguous` merge резултат без POST retry, GET-only bounded retry, strictly boolean `fork` при discovery, санитизиран HTTP статус в discovery грешките и regression покритие. Фиксираният confirmation token и останалата sync логика са непроменени.
- **State:** HEAD `629afbb`, branch `feature/github-app-auth`, ahead 13. Променени: `fork_sync/github.py`, `fork_sync/synchronizer.py`, `api/routes.py`, `DASHBOARD/utils.js`, 5 тестови файла и docs. Без commit, push, реален Sync или GitHub промени.
- **Tests:** `python -m pytest -q` → `453 passed, 1 warning` (StarletteDeprecationWarning); `python -m py_compile` и `node --check DASHBOARD/utils.js` → OK.
- **Next exact step:** Phase 4 release/stability checks; потвърждение на GitHub App настройки от GitHub UI; без реален Sync и без commit/push.

## 2026-11-18 04:02 - Phase 6 release readiness корекции
- **Last completed:** `LICENSE` заменен със стандартен MIT текст; премахнати са PolyForm references и неподкрепеното твърдение за собственост в `COPYRIGHT.md`; Python минимумът е 3.11 в README и `scripts/check.ps1`, а CI matrix-ът проверява 3.11 и 3.12; CI проверява `web/app.js`, `DASHBOARD/app.js` и `DASHBOARD/utils.js`; премахнати са подвеждащите PAT fallback инструкции за браузъра.
- **State:** HEAD `629afbb`, branch `feature/github-app-auth`, 30 modified, 2 deleted, 27 untracked, 0 staged. `.env` не е променян; локалният `.venv` е игнориран. Няма commit, push, reset, checkout, restore, stash, clean, реален Sync или GitHub промени.
- **Tests:** `.venv\Scripts\python.exe -m pip check` → `No broken requirements found`; `httpx2==2.16.0` импортиран успешно; `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` → `453 passed in 5.40s` без warnings; tokenize-aware compile 39 Python файла → OK; `node --check` за трите JS файла → OK; PowerShell parse → OK; `git diff --check` → само LF→CRLF warnings, без whitespace грешки.
- **Next exact step:** Потвърждение на GitHub App настройки и валидна OAuth сесия; ръчна ротация на `GITHUB_TOKEN` и `GITHUB_APP_CLIENT_SECRET`; commit/push само след изрично одобрение. Без реален Sync без одобрение.

## 2026-11-18 04:47 - End-of-Day лог и Broker restart проверки
- **Last completed:** Създаден е `docs/WORKLOG/END_OF_DAY_2026-11-18.md`. Auth Broker е рестартиран успешно само като процес: стар PID `22096` → нов PID `4200`; API PID `11000` и Dashboard не са рестартирани. Ключовете в `.env` са проверени само по наличие/клас, без стойности.
- **State:** HEAD `629afbb`, branch `feature/github-app-auth`, 30 modified, 2 deleted, 28 untracked (вкл. новия End-of-Day лог), 0 staged. Няма промени в source code, `.env`, GitHub App настройки или credentials по време на финалните проверки. Няма commit, push, реален Sync, нов OAuth login или прекъсване на активни сесии.
- **Tests:** Broker `/healthz` → 200 `ok`; API `/healthz` → 200; API `/` → 200; `/dashboard` → 200; `/api/auth/status` → 401 (очаквано без сесия). `broker.out.log`, `broker.err.log`, `dashboard.out.log`, `dashboard.err.log` — без грешни шаблони. broker start `04:35:06` e след `.env` last write `04:29:12`. По-рано днес: pytest `454 passed`, JS syntax checks OK, `git diff --check` OK.
- **Known issues/blockers:** Не е възможно съдържателно потвърждение дали е сменен само `GITHUB_APP_CLIENT_SECRET` и дали `GITHUB_TOKEN` е непроменен без забранено сравняване на secrets; класификацията `fine-grained PAT` не е доказателство за непромененост. OAuth Broker е готов според health/config, но не е тестван реален login. Чакащите OAuth транзакции от преди рестарта са изгубени.
- **Next exact step:** GitHub App UI проверки → валиден OAuth login и read-only preview само с разрешение → решение за сесии/CSRF/expiration → потвърждаване на credential промените от потребителя → commit/push само след одобрение. Без реален Sync без изрично одобрение.

## 2026-11-18 04:53 - SYNC вместо SYNC ALL и по-изразен текст в бутона
- **Last completed:** `DASHBOARD/index.html`: `aria-label` и видимият текст на основния бутон са `SYNC`. `DASHBOARD/dashboard.css`: 56px desktop / 46px mobile, `font-weight: 900`, `letter-spacing: 0.16em / 0.14em`, `-webkit-text-stroke: 1px` и 8-слоен текст-сянка. Добавен е regression тест за етикета и типографията.
- **State:** 30 modified, 2 deleted, 28 untracked, 0 staged. Променени са само трите UI/тест файла и docs. Няма промени в auth, API, sync логиката, `.env`, GitHub настройките или credentials; няма commit, push, реален Sync или нов OAuth login.
- **Tests:** targeted `21 passed`; `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` → `455 passed in 5.03s`; `node --check` за `DASHBOARD/app.js`, `DASHBOARD/utils.js`, `web/app.js` → OK; `git diff --check` → без грешки; стар етикет липсва в UI файловете. CDP при 1440×1200 и 390×844 → `labelIsSync`, `singleSyncSpan`, `noOldLabel`, `fontSize`, `heavyWeight`, `wideSpacing`, `stroke`, `layeredShadow`, `noOverflow`, `textFits` = `true` и за двата размера. Screenshot-ите са записани в temp, но моделът не може да ги визуално инспектира.
- **Next exact step:** Потребителят да потвърди визуално новия вид в отворения Dashboard; след това GitHub App UI проверки и read-only OAuth smoke само с разрешение. Без реален Sync и без commit/push без одобрение.

## 2026-11-18 04:56 - SYNC текстът е изравнен с иконата
- **Last completed:** `DASHBOARD/dashboard.css`: основният текст е 40px desktop / 32px mobile, равно на височината на `.button-icon`; `font-weight: 800`, `letter-spacing: 0.12em / 0.1em`, 1px контур и 6-слоен олекотен текст-сянка. `tests/test_dashboard_progress.py` проверява и размера на иконата.
- **State:** 30 modified, 2 deleted, 28 untracked, 0 staged. Няма промени в auth, API, sync логиката, `.env` или GitHub настройките; няма commit, push, реален Sync или нов OAuth login.
- **Tests:** targeted `21 passed`; пълен pytest `455 passed in 4.66s`; JS syntax и `git diff --check` OK. CDP при 1440×1200 и 390×844 → `labelIsSync`, `balancedWeight`, `sameHeightAsIcon`, `noOverflow`, `textFits` и останалите проверки = `true`; `titleHeight/iconHeight` = 40/40 desktop и 32/32 mobile. Screenshot-ите са записани в temp, но моделът не може да ги визуално инспектира.
- **Next exact step:** Потребителят да потвърди на око елегантния вид; след това GitHub App UI проверки и read-only OAuth smoke само с разрешение. Без реален Sync и без commit/push без одобрение.

## 2026-11-18 05:12 - Две sync действия: SYNC CHOSEN и SYNC ALL
- **Last completed:** `DASHBOARD/index.html`: добавени са `#sync-all-button` и `#sync-eligible-count`, а `#sync-button` е green `SYNC CHOSEN`. `DASHBOARD/dashboard.css`: червена палитра за `SYNC ALL`, възстановени са 32px/26px, `font-weight: 800`, `letter-spacing: 0.1em/0.08em` и 7-слоен текст-сянка без stroke; групата е с 12px gap на desktop и се подрежда на mobile. `DASHBOARD/app.js`: разделни handler-и, потвърждения, празни guard-и, eligible count и блокиране на двата бутона по време на preview/sync.
- **State:** 30 modified, 2 deleted, 28 untracked, 0 staged. Променени са само четирите UI/тест файла и docs. `dry_run:false`, `confirmation:"SYNC"`, payload форматът, server-side проверките и sync логиката са запазени; няма промени в auth, API, `.env`, GitHub настройки или credentials; няма commit, push, реален Sync или нов OAuth login.
- **Tests:** targeted `23 passed`; пълен pytest `457 passed, 1 warning in 5.71s`; `node --check DASHBOARD/app.js` и `node --check DASHBOARD/utils.js` OK; `scripts/check.ps1 -SkipTests` → `All checks passed`; `git diff --check` без whitespace грешки (само CRLF предупреждения). CDP `verify-sync-action-group.cjs` при 1440×1200 и 390×844 → `exactLabels`, `singleIds`, `countVisible`, `fontSize`, `fontWeight`, `sameHeight`, `titleMatchesIcon`, `noStroke`, `layeredShadow`, `greenPalette`, `redPalette`, `noOverflow`, `textFits`, `sideBySide/compactGap` (desktop) и `stacked` (mobile) = `true`.
- **Next exact step:** Потребителят да потвърди визуално двата бутона и брояча; след това GitHub App UI проверки и read-only OAuth smoke само с разрешение. Без реален Sync и без commit/push без одобрение.

## 2026-11-18 05:17 - Локален commit на днешните промени
- **Last completed:** След изрично одобрение е направен локален commit `7fb24b7 Finalize release readiness and dual sync actions` с 58 файла. Push не е правен.
- **State:** Работното дърво е чисто след комита. Този запис добавя само новия HEAD/състояние в WORKLOG и дневния лог. Няма промени в `.env`, GitHub настройките или credentials; няма реален Sync или нов OAuth login.
- **Tests:** След комита не са пускани нови тестове. Последните реални резултати остават targeted `23 passed`, pytest `457 passed, 1 warning`, JS syntax OK, `scripts/check.ps1 -SkipTests` OK и CDP проверки `true`.
- **Next exact step:** Край на сесията за днес. При следваща сесия: визуално потвърждение на двата бутона, GitHub App UI проверки и read-only OAuth smoke само с разрешение. Push и реален Sync — само с изрично одобрение.

## 2026-11-18 20:00 - Минимална поправка на сесията и 403 при `/api/sync`
- **Last completed:** `/api/sync` вече използва валидирания акаунт от сесията вместо допълнително `GET /user`; сесията и cookie се удължават при активност; GitHub 401 изчиства сесията/cookie и връща `REAUTH_REQUIRED` със структурирана грешка. Добавени са regression тестове за кеширан акаунт, sliding TTL, refresh на cookie и 401 почистване.
- **State:** HEAD `1639995`, branch `feature/github-app-auth`, ahead 17, без push. Променени: `api/auth.py`, `api/routes.py`, `tests/test_web_auth.py`, дневният лог и WORKLOG. Няма реален Sync, промяна в GitHub App настройките, `.env` или credentials.
- **Tests:** targeted `72 passed`; пълен pytest `461 passed in 4.62s`; `scripts/check.ps1` → `All checks passed` с `461 passed, 1 warning` (StarletteDeprecationWarning); `git diff --check` → само LF→CRLF предупреждения.
- **Next exact step:** Потребителят да одобри нов targeted `dry_run:true` през контролирания Chrome за `GabrielRules/TEST`; без реален Sync и без commit/push без изрично одобрение. Ако 403 остане, преминаваме към Installation Access Tokens с App private key.

## 2026-11-18 20:11 - Live dry-run потвърждава поправката
- **Last completed:** След рестарт на smoke стека и нов OAuth login targeted `dry_run:true` за `GabrielRules/TEST` върна HTTP `200` със `status: behind`, `message: 3 upstream commit(s) available.`, `behind_by: 3`, `ahead_by: 0`. Предишният 403 от `GET /user` не се повтори.
- **State:** HEAD `1639995`, branch `feature/github-app-auth`, ahead 17, без push. Променени остават 6-те файла от поправката и документацията. Контролиран Chrome на CDP порт `9224` е активен с валидна сесия; `/api/auth/status` е `200 AUTHENTICATED` и акаунтът съвпада с очаквания. Репозиториите са непроменени: `0c82ac0` (original), `42212b1` (fork). Няма реален Sync, commit/push или GitHub App промени.
- **Tests:** `verify-login.mjs` → `http 200`, `state AUTHENTICATED`, `accountMatchesExpected true`; `targeted-test-preview.mjs` → preview `http 200`, `behind_by 3`, `ahead_by 0`; `check-test-current-state.mjs` → SHAs непроменени. По-рано в сесията: targeted pytest `72 passed`, пълен pytest `461 passed`, `scripts/check.ps1` → `All checks passed`.
- **Next exact step:** Потребителят да реши дали да одобри реален `dry_run:false` Sync за `GabrielRules/TEST`; без commit/push и без промяна в GitHub App настройки без изрично одобрение.

## 2026-11-18 20:14 - Реален Sync за GabrielRules/TEST
- **Last completed:** След изрично одобрение е изпълнен `dry_run:false` Sync само за `GabrielRules/TEST`. API върна `200`, `status: synced`, `message: Synced 3 upstream commits.`, `behind_by: 3`, `ahead_by: 0` и `last_successful_sync: 2026-11-18T18:13:46Z`.
- **State:** HEAD `1639995`, branch `feature/github-app-auth`, ahead 17, без push. GitHub UI потвърди fork `GabrielRules/TEST:main` на `0c82ac0` и `This branch is up to date with architectquant/TEST:main.`; originalът остава `0c82ac0`. Локално остават същите 6 uncommitted файла; `.env`, GitHub App настройки и credentials не са променяни.
- **Tests:** `verify-login.mjs` → `AUTHENTICATED`; `live-sync-test.mjs` → `sync http 200`, `status synced`; `check-test-current-state.mjs` → и двата commit-а `0c82ac0`; `broker.err.log` и `dashboard.err.log` без грешки. По-рано: targeted pytest `72 passed`, пълен pytest `461 passed`, `scripts/check.ps1` → `All checks passed`.
- **Next exact step:** Край на текущата проверка. При нужда: одобрение за локален commit/push на 6-те променени файла; без допълнителен Sync, докато не има нов одобрен dry-run.

## 2026-11-18 20:16 - Локален commit на поправката
- **Last completed:** След изрично одобрение е направен локален commit `a927d6a Fix web auth session handling and sync 403` с 6 файла: поправката в `api/auth.py`/`api/routes.py`, regression тестовете и документацията за live dry-run и реалния Sync.
- **State:** HEAD `a927d6a`, branch `feature/github-app-auth`, ahead 18, без push. След docs-only записа за HEAD работното дърво трябва да е чисто. `.env`, GitHub App настройки и credentials не са променяни.
- **Tests:** След кодовия commit не са пускани нови тестове. Последните реални резултати остават targeted pytest `72 passed`, пълен pytest `461 passed`, `scripts/check.ps1` → `All checks passed` и live `dry_run:false` → `200 synced`.
- **Next exact step:** Push само с изрично одобрение. Нов Sync — само след нов одобрен `dry_run:true`.

## 2026-11-18 20:22 - Push към fork origin
- **Last completed:** `git push origin feature/github-app-auth` завърши успешно: `23a7e56..99428bd`. Пуснати са 19-те локални commit-а към `GabrielRules/DREAMEROL-SYNC`; Secret проверката на diff-а срещу origin показа само плейсхолдъри и тестови стойности, без `.env`.
- **State:** HEAD `99428bd`, branch `feature/github-app-auth`, синхронизиран с `origin/feature/github-app-auth` (ahead 0). `upstream`/`architectquant` не са пипани; PR не е създаван. Този запис ще бъде пуснат като docs-only commit.
- **Tests:** След push не са пускани нови тестове. Последните реални резултати остават targeted pytest `72 passed`, пълен pytest `461 passed`, `scripts/check.ps1` → `All checks passed`, live dry-run `200 behind_by:3 ahead_by:0` и live Sync `200 synced`.
- **Next exact step:** Край на сесията. Нов реален Sync — само след нов одобрен `dry_run:true`; PR или push към друг remote — само с изрично одобрение.

## 2026-11-18 20:29 - Финален read-only preview след Sync
- **Last completed:** Нов OAuth login (`AUTHENTICATED`, очакван акаунт) и пълен `dry_run:true` без `repositories`. Preview върна HTTP `200` с `37` репозитория: `35 UP TO DATE`, `0 TO BE SYNCED`, `2 UNSYNCABLE`. Двете UNSYNCABLE са `GabrielRules/DREAMEROL-SYNC` (`diverged`, `behind_by:3`, `ahead_by:21`) и `GabrielRules/OOP-PRINCIPLES-DESIGN` (`diverged`, `behind_by:2`, `ahead_by:4`).
- **State:** HEAD `5f682be`, branch `feature/github-app-auth`, синхронизиран с origin. Няма нов реален Sync, кодови промени, `.env`/credential промени или GitHub App настройки. `GabrielRules/TEST` вече е up to date.
- **Tests:** `verify-login.mjs` → `AUTHENTICATED` и очакван акаунт; `full-preview.mjs` → preview `http 200`, `total 37`, `35/0/2`, `complete true`, без parse грешка. По-рано: targeted pytest `72 passed`, пълен pytest `461 passed`, `scripts/check.ps1` → `All checks passed`, live Sync `200 synced`.
- **Next exact step:** Край на сесията. Ако се иска PR или Installation Access Tokens — само с изрично одобрение; нов Sync — само след нов одобрен dry-run.

## 2026-11-18 21:39 - PR към architectquant/DREAMEROL-SYNC
- **Last completed:** По изрично одобрение е създаден PR #1 `Fix web auth session handling and sync 403` от `GabrielRules:feature/github-app-auth` към `architectquant/DREAMEROL-SYNC:main` чрез GitHub API (поради липсващ `gh`). Token не е показан; използван е само съхраненият credential за `github.com`.
- **State:** HEAD `c092a7d`, branch `feature/github-app-auth`, синхронизиран с origin. Локалното дърво е чисто преди този docs-only запис. PR е `open`, `draft:false`, `head`/`base` са коректни. API.report: `45 commits`, `74 changed_files`, `+21306/-604`, `mergeable:null`, `mergeable_state:unknown` (GitHub все още изчислява). Няма push към `architectquant` извън PR; клонът остава в `GabrielRules`.
- **Tests:** Създаването на PR не променя код; тестовете от 20:29 остават валидни. Анонимна API проверка на PR #1 потвърди `state:open` и коректни `head`/`base`.
- **Next exact step:** Изчакай GitHub да изчисли `mergeable`, после провери PR #1 за конфликти/checks и докладвай. Merge — само след изрично одобрение. Нов реален Sync — само след нов одобрен dry-run.

## 2026-11-18 22:50 - Разрешен README конфликт в PR #1
- **Last completed:** След отваряне на PR-страницата GitHub върна `mergeable:false`, `mergeable_state:dirty`. `git merge-tree --write-tree --name-only architectquant/main HEAD` показа конфликт само в `README.md`. Направен е `git merge --no-commit --no-ff architectquant/main`, решен с `checkout --ours -- README.md` и е създаден merge commit `72f2a9f`, push-нат към origin.
- **State:** HEAD `72f2a9f` след merge commit, после `4403371` след docs commit; branch `feature/github-app-auth`, синхронизиран с origin. PR #1 остава `open`; head от API е `4403371`. След resolve `git merge-tree` върна само tree OID без конфликтни файлове. Отхвърлено е предложението за изчистване на `architectquant` до 2–3 файла, за да не се въвежда нов destructive diff.
- **Tests:** `git merge-tree` след merge commit: без конфликти. Повторна проверка на PR #1 след push (анонимно и с credential) върна `mergeable:null`, `mergeable_state:unknown`; `status_count:0`, `check_count:0`. Кодовите тестове не са пускани повторно, защото след 20:29 няма кодови промени — само README resolve.
- **Next exact step:** Merge в `architectquant/main` — само след изрично одобрение; ако GitHub продължи с `unknown`, провери PR страницата в браузъра. Изчистване на repo — само ако потребителят изрично посочи файловете и потвърди destructive промяна.

## 2026-11-18 22:52 - PR #1 остава отворен без локални конфликти
- **Last completed:** След push на `4403371` PR #1 е ре-проверен. `state:open`, `head:GabrielRules:feature/github-app-auth`, `base:main`, `commits:48`, `changed_files:74`. GitHub API не е изчислил `mergeable` и няма status/check runs.
- **State:** Локалното дърво е чисто на `4403371`; `git merge-tree architectquant/main HEAD` е без конфликти. Няма merge, няма нов реален Sync, няма промени в GitHub App настройките.
- **Tests:** `GET /pulls/1` анонимно и с credential → `mergeable:null`, `mergeable_state:unknown`; `GET /status` → `pending`, 0 statuses; `GET /check-runs` → 0 runs.
- **Next exact step:** Изчакай одобрение за merge или допълнителна проверка в браузъра. Без одобрение не се прави merge и не се изчиства repo.

## 2026-11-18 22:55 - Merge на PR #1 блокиран от липсващи write права
- **Last completed:** По одобрение е изпратен `PUT /repos/architectquant/DREAMEROL-SYNC/pulls/1/merge` с `merge_method:merge`. GitHub върна статус `404`; последваща проверка с credential-а показа `token_user:GabrielRules` и права върху `architectquant/DREAMEROL-SYNC`: `admin:false`, `maintain:false`, `push:false`, `triage:false`, `pull:true`.
- **State:** PR #1 остава `open`, `head:GabrielRules:feature/github-app-auth`, `base:main`. Merge не е извършван. Локалното `git merge-tree architectquant/main HEAD` е без конфликти. Не е правен push към `architectquant`.
- **Tests:** `PUT .../merge` → `404 Not Found`; `GET /repos/...` с credential → само `pull` права. Кодови тестове не са пускани, няма кодови промени след 20:29.
- **Next exact step:** Нужно е `architectquant` да направи merge от PR страницата, или да даде write/push достъп на `GabrielRules` към репозиторията. Без това не се повтаря merge опит. Нов реален Sync — само след нов одобрен dry-run.

## 2026-11-18 22:58 - PR #1 merge-нат чрез architectquant credential
- **Last completed:** По указание на потребителя е използван съхраненият credential за `architectquant` (`api_user:architectquant`, `admin:true`, `push:true`) и `PUT /repos/architectquant/DREAMEROL-SYNC/pulls/1/merge` върна `merged:true`, `merge_sha:b16c977776793c92bef7681c297e8e322974be9a`.
- **State:** PR #1 е `state:closed`, `merged:true`, `merged_at:2026-11-18T20:58:27Z`, `base:main`, `head:GabrielRules:feature/github-app-auth`. `git fetch architectquant main` потвърди, че `architectquant/main = b16c977`. Локалният branch `feature/github-app-auth` и `origin` остават на `44768e1`; token не е показан или записан.
- **Tests:** След merge GitHub API потвърди `merged:true`; локално `git merge-tree architectquant/main HEAD` преди merge беше без конфликти. Кодови тестове не са пускани повторно; последните реални резултати остават `72 passed`, `461 passed`, `scripts/check.ps1` → `All checks passed`, live Sync `200 synced`, preview `35/0/2`.
- **Next exact step:** Край на тази задача. Преглед на `architectquant/main` при нужда; нов реален Sync — само след нов одобрен dry-run; отделни подобрения (Installation Tokens, PR към Dreamerol) — само с изрично одобрение.

## 2026-11-18 23:27 - README с GitHub App линк
- **Last completed:** Добавен е кликаем badge и текстов линк към `https://github.com/apps/dreamerol-sync` в горната част на `README.md`, плюс `🤖 GITHUB APP` в навигационната таблица и `[📥 GitHub App]` в долните линкове. Заглавията и няколко секции са освежени с емоджита и цветен badge; техническото съдържание е непроменено.
- **State:** Променен е само `README.md` от приложението; локалната промяна предстои да бъде commit-ната и push-ната към `origin/feature/github-app-auth`. `architectquant/main` остава на `b16c977` от merge-а на PR #1; нова PR за README не е създавана.
- **Tests:** `git diff --check` без whitespace грешки (само CRLF предупреждение); `scripts/check.ps1` → `461 passed, 1 warning in 5.83s`, `All checks passed`. Линкът е проверен с 4 occurrence-а в README.
- **Next exact step:** Push към `origin`. Ако README-то трябва да стигне и до `architectquant/main`, да се създаде нов PR или да се pushне изрично с одобрение.

## 2026-11-18 23:47 - README с визуалната идентичност на Dreamerol
- **Last completed:** `README.md` е преписан с визуалната обвивка от по-стар README: два горни банера, навигационна таблица с бутони и визитка/контакт, долен банер, бутонна таблица, keywords и techstack лента. Съдържанието е актуалното от проекта — Python 3.11+, Auth Broker, saved accounts, Web Dashboard, fork-only counters, GitHub App изисквания, SYNC безопасност, статуси, структура и линк към публичната GitHub App страница.
- **State:** Промяната е commit-ната и push-ната към `origin` като `88b8c98`. `architectquant/main` след API обновяване е на `3675c09`; само `README.md` е променен там, без връщане на изтритите docs файлове.
- **Tests:** `scripts/check.ps1` → `461 passed, 1 warning in 5.46s`, `All checks passed`. Grep потвърди GitHub App линк, визитка, 5 долни бутона, techstack keywords, Web Dashboard, GitHub App installation requirements и Synchronization Results. `git rev-parse` потвърди еднакъв README blob `3f805c8` в локалния HEAD и в `architectquant/main`.
- **Next exact step:** Край на задачата. Без одобрение не се правят други push-ове, PR-ове или кодови промени.

## 2026-11-18 23:48 - README синхронизиран в двата remote-а
- **Last completed:** Локалният README е push-нат към `origin/feature/github-app-auth` (`88b8c98`) и обновен само като файл в `architectquant/main` (`3675c09`) чрез GitHub API с credential за `architectquant`.
- **State:** README blob `3f805c859118175114f7058c6264f5f7a008cc08` е еднакъв локално и в `architectquant/main`. Изтритите от `architectquant` `docs/`, `AGENTS.md`, `DECISIONS.md`, `CURRENT_STATUS.md` и `NEXT_STEPS.md` не са възстановявани.
- **Tests:** Няма нови кодови тестове след `scripts/check.ps1` от 23:47. Направена е self проверка на blob SHA.
- **Next exact step:** Край на сесията при липса на ново указание.

## 2026-11-19 00:01 - GitHub App badge центриран в README
- **Last completed:** `<p align="center">` около badge-а и текстовия линк е заменен с `<div align="center">`, за да се центрира надеждно в GitHub README.
- **State:** Промяната е commit-ната и push-ната към `origin/feature/github-app-auth` като `6bde761`. API обновяването на `README.md` в `architectquant/main` беше прекъснато от потребителя и **не е извършено**; там остава README blob `3f805c8`.
- **Tests:** `git diff --check` само с CRLF предупреждение; `scripts/check.ps1` → `461 passed, 1 warning in 4.66s`, `All checks passed`.
- **Next exact step:** След възобновяване — само ако потребителят изрично поиска — да се обнови README-то в `architectquant/main` чрез contents API. Не се правят нови push/merge без одобрение.

## 2026-11-19 00:15 - Край на сесията
- **Last completed:** Сесията е прекратена по искане на потребителя. Записани са крайното състояние и липсата на допълнителни push/merge операции след stop.
- **State:** HEAD `6bde761`, branch `feature/github-app-auth`, синхронизиран с `origin`. Работното дърво има само неcommit-нати промени в `docs/WORKLOG/LOG_19-11-26.md` и `docs/WORKLOG/WORKLOG.md` (записи за края на сесията). `architectquant/main` остава на `3675c09` със стар README blob `3f805c8`; центрираният badge е само в `GabrielRules`/локално (`c055335`).
- **Tests:** Последни реални проверки от 00:01: `git diff --check` без whitespace грешки (само CRLF предупреждение) и `scripts/check.ps1` → `461 passed, 1 warning`, `All checks passed`. След 00:01 няма нови тестове.
- **Next exact step:** При нова сесия — първо да се потвърди дали да се pushне само README-то в `architectquant/main`; лог промените да се commit-нат според одобрението. Без одобрение не се прави нищо допълнително.
