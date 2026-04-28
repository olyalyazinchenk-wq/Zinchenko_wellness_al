# Lab Order Links Through HelloDoc

Date: 2026-04-21
Owner: Olga / Wellness Bot
Purpose: define the approved route for clients who need to order labs before or after nutrition-navigation intake.

## Approved Links

Primary link:

- `https://hellodoc.app/s/27u6a/`

Backup link:

- `https://hellodoc.app/s/gdgjq/`

## How The Bot Should Phrase It

The bot may write:

```text
Если анализы уже есть — пришлите их сюда, в этот чат: PDF, фото бланка или ключевые показатели текстом.

Если анализов пока нет — это нормально. Можно сначала пройти анкету, а анализы сдать позже.
Для сдачи можно выбрать Helix или Invitro через HelloDoc по ссылке Ольги:
https://hellodoc.app/s/27u6a/

Если первая ссылка не откроется, используйте резервную:
https://hellodoc.app/s/gdgjq/

Когда результаты будут готовы, просто вернитесь в этот чат и отправьте их сюда.
```

## Tone Rule

This should sound like a practical route, not pressure.

Do not write:

- "обязательно сдайте только здесь",
- "без этого мы не сможем работать",
- "срочно оплатите анализы".

Correct positioning:

- analysis ordering is a convenience path,
- the client can start without labs,
- if the client already has labs, they should send them into the current Telegram chat,
- if the client has no labs, HelloDoc is the practical ordering route,
- unclear photos should be resent in better quality,
- confirmed results are interpreted through nutritiological references.
