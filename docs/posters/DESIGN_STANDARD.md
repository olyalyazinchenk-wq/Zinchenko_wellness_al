# Дизайн-стандарт постеров Ольги Зинченко v2

> Источники: nexu-io/open-design (craft-правила) + styles.refero.design (реальные токены топ-брендов)

## 🎨 Палитры (на выбор)

### Основная — тёмная премиум
```
--bg:         #0f0f0f    (фон)
--surface:    #161616    (карточки/модули)
--fg:         #f0f0f0    (основной текст)
--muted:      rgba(255,255,255,0.50)
--border:     rgba(255,255,255,0.06)
--accent:     #c0847a    (тёплый rose — сигнатура Ольги)
```

### Альтернатива 1 — Anthropic-style (тёплая светлая)
```
--bg:         #faf9f5
--surface:    #f0eee6
--fg:         #141413
--muted:      #70706d
--border:     #e3dacc
--accent:     #c0847a
```

### Альтернатива 2 — Stripe-style (строгая)
```
--bg:         #f8fafd
--surface:    #ffffff
--fg:         #0d1738
--muted:      #64748d
--border:     #e5edf5
--accent:     #8087ff
--accent-alt: #ffbb00
```

## 🔤 Типографика (жёстко)

| Роль | Размер | leading | tracking |
|------|--------|---------|----------|
| Display | 48–72px | 1.0–1.2 | **-0.02em – -0.03em** |
| H1 | 32–48px | 1.0–1.2 | **-0.01em – -0.02em** |
| H2 | 24–32px | 1.2–1.3 | -0.01em |
| Body | 15–18px | 1.5–1.6 | **0** (default) |
| Small/Caption | 11–14px | 1.5 | **+0.01em – +0.02em** |
| **ALL CAPS** | любой | — | **+0.06em обязательно** |

- Шрифт: `Inter` (display+body) или `Inter` + `Georgia` (serif для цитат)
- Макс 2 начертания. System-fallback: `-apple-system, BlinkMacSystemFont, system-ui, sans-serif`
- Body: `max-width: 65ch`. **Никакого `text-align: justify` никогда**

## 🚫 Анти-AI-шлак (P0 — блок)

```
ЗАПРЕЩЕНО HEX: #6366f1 #4f46e5 #4338ca #3730a3 #8b5cf6 #7c3aed #a855f7
               (все индиго/пурпурные Tailwind)

ЗАПРЕЩЕНО:
- Градиент purple→blue/cyan/pink на герое
- ✨🚀🎯⚡🔥💡 как иконки
- lorem ipsum / «placeholder text»
- Карточка border-radius + цветной border-left одновременно
- Выдуманные метрики
- >2 использований --accent на экран
```

## 📐 Структура постера

```
1. Badge-лейбл (12px, ALL CAPS, letter-spacing: 0.08em)
2. H1 заголовок (48px, tracking: -0.02em)
3. Подзаголовок (16px, muted, max-width: 65ch)
4. Bento-grid из модулей (2 колонки для десктопа)
5. Акцентный блок (одно смелое высказывание)
6. Футер: имя, промокод, ссылка
```

## 🏷 Брендинг Ольги

Всегда в футере:
```
Ольга Зинченко, нутрициолог
Промокод Витамакс: 844131
СЗ ref: https://ru.siberianhealth.com/ru/shop/catalog/product/500659/?referral=2663395625
```

## ✓ Pre-flight проверка (перед отправкой)

1. `grep "#6366f1\|#4f46e5\|#4338ca\|#3730a3\|#8b5cf6\|#7c3aed\|#a855f7"` → 0 совпадений
2. Кол-во `var(--accent)` или `#c0847a` → ≤ 2–3 на весь постер
3. ALL CAPS → `letter-spacing ≥ 0.06em`
4. Display-текст → отрицательный tracking
5. Body → `max-width: 65ch`, не justify
6. Нет lorem ipsum, ✨🚀🎯⚡🔥💡, unsplash.com
7. Каждый `<section>` → `data-od-id`
8. Футер содержит сигнатуру Ольги

## 📊 Что дали ресурсы

### styles.refero.design
- **20 премиум брендов** с извлечёнными цветами (Stripe, Anthropic, Cursor, Superhuman, ElevenLabs, Linear, Raycast, Apple…)
- Реальные HEX-значения из продакшен-сайтов → строим не на вкус, а на данных
- Подтверждение: все топ-бренды используют **1 акцент**, нейтральную базу, и 4px базовый spacing

### open-design (nexu-io)
- Исчерпывающие craft-правила по цвету, типографике, анимации
- Anti-AI-slop: 7 кардинальных грехов, которые выдают AI-дизайн
- Чек-лист из 10 пунктов pre-flight
