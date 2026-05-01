# Google AI Studio `moy-projekt` Audit

Date: 2026-05-01
Source repo: `https://github.com/olyalyazinchenk-wq/moy-projekt`
Local clone: `external/google-ai-studio-moy-projekt`
Branch: `main`
Commit: `d7626b8 feat: Initialize AI Studio project structure`

## Короткий вывод (RU)

- Это **не** новый backend Telegram‑бота: проект представляет собой отдельный React/Vite UI‑макет (эксперт/админ панель + превью для клиента).
- Использовать как UX‑референс и бэклог для будущего рабочего места human review.
- **Не** переносить в продакшен медицинские формулировки/утверждения из мок‑данных: там есть небезопасные и чрезмерно уверенные фразы.

## Verdict

Google AI Studio did not create a replacement for the Telegram bot backend.

It created a separate React/Vite mockup for an expert/admin dashboard and client mobile-style preview.

Use it as:

- UI/UX reference;
- future admin panel prototype;
- source of ideas for human review workspace;
- source for the missing “пример результата” experience.

Do not use it as:

- medical logic;
- final client copy;
- backend;
- safe dossier generator;
- source of truth for supplements or diagnoses.

## What is inside

Stack:

- React 19
- Vite
- TypeScript
- Tailwind CSS 4
- lucide-react
- motion
- recharts
- `@google/genai` dependency present but not materially used in the visible UI

Core files:

- `src/App.tsx` - shell with tabs
- `src/components/Sidebar.tsx` - navigation
- `src/components/Overview.tsx` - statistics mock
- `src/components/CaseList.tsx` - queue of cases
- `src/components/ReviewWorkspace.tsx` - expert review workspace
- `src/components/ClientAppMock.tsx` - mobile-style client result preview
- `src/components/ClientsList.tsx` - client database mock
- `src/components/DossiersList.tsx` - archive mock
- `src/components/SettingsView.tsx` - settings mock
- `src/data.ts` - mock cases
- `src/types.ts` - case/profile/draft types

## Useful ideas to keep

### 1. Expert review workspace

Useful structure:

- left side: immutable client facts;
- right side: editable AI draft;
- visible safety flags;
- generation blocked when lab quality is bad;
- templates for requesting clearer lab files;
- explicit approve/send action.

This matches our rule:

`AI draft -> human review -> client delivery`.

### 2. Case queue

Useful for Olga/operator:

- filter by status;
- show pending review;
- show needs info/lab resubmission;
- show product tier;
- show client complaint summary.

This is useful after we move beyond pure Telegram admin messages.

### 3. Client result preview

This is directly relevant to the current product problem:

- user said the bot does not show “пример результата” properly;
- Google AI Studio produced a visual mobile-like result screen;
- we can turn the idea into a safe static demo page or image.

But the current copy is not safe enough and must be rewritten.

### 4. Russian UI skill

`AGENTS.md` contains a useful style rule:

- natural Russian;
- no mechanical English translations;
- caring error messages;
- no diagnosis/treatment;
- concise Mini App text.

This is compatible with our current product direction.

## Critical risks found

The mock data and client preview contain unsafe or overconfident medical-style language.

Examples of unsafe categories:

- “тканевый железодефицит” as a strong conclusion;
- “усталость надпочечников”;
- “клеточная гипоксия”;
- “детокс / очищение систем”;
- “вернут вашей системе естественный ритм”;
- supplement-style claims that sound like treatment;
- doctor request wording that sounds like the bot is directing therapy.

These should not be copied into production.

Safe replacement direction:

- “можно предположить дефицитные риски”;
- “нужно подтвердить по анализам и врачу”;
- “нутрицевтические ориентиры поддержки”;
- “что обсудить с врачом”;
- “что не начинать самостоятельно”.

## Product decision

Do not merge the Google AI Studio project into the current backend now.

Reason:

- our North Star says the next target is one safe paid client cycle;
- this React dashboard is useful, but not required to complete that cycle;
- integrating it now would create a new UI branch and slow the pilot.

What we should do now:

1. Extract one safe “пример результата” from the design idea.
2. Add it to our bot as a Telegram-friendly preview:
   - short text first;
   - optionally PDF/image/static HTML later;
   - no unsafe medical claims.
3. Keep the full dashboard as future backlog for after the first client cycle.

## Recommended immediate action

Fix the current issue:

`не показывает пример результата`

Implementation direction:

- keep the button `Посмотреть пример результата`;
- make it send a concrete safe demo result, not only a generic explanation;
- show the demo structure:
  1. короткие приоритеты;
  2. что видно по анкете;
  3. рабочие гипотезы;
  4. что уточнить анализами;
  5. план на 3 дня;
  6. план на 2 недели;
  7. вопросы к врачу;
  8. пример нутрицевтических ориентиров без лечения.

## Backlog decision

Future feature name:

`Expert Review Dashboard / WellnessPro`

Scope after pilot:

- real case queue from `WellnessBot/data/submissions`;
- review editor;
- lab-resubmission templates;
- approve/send flow;
- archive of dossiers;
- client support timeline.

Do not start until:

- at least one full safe paid client cycle is completed;
- preferably 3 pilot clients are completed;
- data storage/VPS decision is made.

## Repository handling

The external repo was cloned for inspection only.

Added `external/` to `.gitignore` so it is not accidentally committed into the main project.
