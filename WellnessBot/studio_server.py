from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aiohttp import web

BOT_DIR = Path(__file__).resolve().parent
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from config import load_settings  # noqa: E402
from html_pdf_engine import (  # noqa: E402
    build_nutriok_report_context,
    create_nutriok_pdf,
    render_nutriok_report_html,
)
from intake_schema import GOAL_DEFAULT_METRICS  # noqa: E402
from nutriok_product import PRIMARY_GOALS, get_product_offer, normalize_product_code  # noqa: E402
from nutriok_safety import evaluate_delivery_gate, find_red_flags  # noqa: E402
from review_gate import (  # noqa: E402
    compute_file_sha256,
    is_release_approved,
    record_review,
)
from storage import load_submission, save_submission  # noqa: E402


STUDIO_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>НутриОК Studio · Кабинет Ольги Ковалевой и Витрина Разборов</title>
    <style>
        :root {
            --paper: #f5f1e8;
            --bright: #fffdf7;
            --ink: #171912;
            --muted: #5c5f54;
            --green: #c7f04b;
            --green-soft: #eef9c8;
            --coral: #ff6b4a;
            --coral-soft: #fff0ec;
            --blue: #3154d8;
            --blue-soft: #eef2ff;
            --line: rgba(23, 25, 18, 0.16);
        }

        * { box-sizing: border-box; }
        body {
            margin: 0;
            background: var(--paper);
            color: var(--ink);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.45;
        }
        .serif { font-family: Georgia, "Times New Roman", serif; }

        /* Top Navigation */
        .topbar {
            position: sticky;
            top: 0;
            z-index: 50;
            background: var(--ink);
            color: var(--bright);
            padding: 14px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--ink);
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brand-circle {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: var(--green);
            color: var(--ink);
            display: grid;
            place-items: center;
            font-family: Georgia, serif;
            font-weight: 700;
            font-size: 18px;
        }
        .brand-title strong {
            display: block;
            font-size: 17px;
            letter-spacing: -0.01em;
        }
        .brand-title span {
            font-size: 11px;
            color: rgba(255,253,247,0.7);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .tabs {
            display: flex;
            gap: 8px;
        }
        .tab-btn {
            background: rgba(255,253,247,0.1);
            color: var(--bright);
            border: 1px solid rgba(255,253,247,0.28);
            padding: 9px 16px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .tab-btn:hover { background: rgba(255,253,247,0.2); }
        .tab-btn.active {
            background: var(--green);
            color: var(--ink);
            border-color: var(--green);
        }
        .tg-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--blue);
            color: var(--bright);
            text-decoration: none;
            font-size: 12.5px;
            font-weight: 700;
            padding: 9px 15px;
            border-radius: 999px;
        }

        /* Funnel Strip */
        .kpi-strip {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            padding: 18px 28px 6px;
            max-width: 1480px;
            margin: 0 auto;
        }
        .kpi-card {
            background: var(--bright);
            border: 1.5px solid var(--ink);
            border-radius: 10px;
            padding: 14px 16px;
            box-shadow: 3px 3px 0 var(--ink);
        }
        .kpi-card.highlight { background: var(--green-soft); }
        .kpi-card.alert { background: var(--coral-soft); }
        .kpi-label {
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
        }
        .kpi-val {
            font-family: Georgia, serif;
            font-size: 32px;
            line-height: 1.05;
            margin: 4px 0 2px;
        }
        .kpi-sub { font-size: 11.5px; color: var(--muted); }

        /* Main Layout */
        .workspace {
            max-width: 1480px;
            margin: 0 auto;
            padding: 14px 28px 40px;
        }
        .cabinet-grid {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 20px;
            align-items: start;
        }

        /* Case List Sidebar */
        .sidebar-box {
            background: var(--bright);
            border: 1.5px solid var(--ink);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 4px 4px 0 var(--ink);
        }
        .sidebar-header {
            padding: 14px 16px;
            background: var(--ink);
            color: var(--bright);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .filter-row {
            display: flex;
            gap: 6px;
            padding: 10px 12px;
            border-bottom: 1px solid var(--line);
            background: var(--paper);
            flex-wrap: wrap;
        }
        .filter-chip {
            border: 1px solid var(--ink);
            background: var(--bright);
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
        }
        .filter-chip.active {
            background: var(--ink);
            color: var(--green);
        }
        .case-list {
            max-height: 680px;
            overflow-y: auto;
        }
        .case-item {
            padding: 13px 16px;
            border-bottom: 1px solid var(--line);
            cursor: pointer;
            transition: background 0.12s ease;
        }
        .case-item:hover { background: #f9f6ed; }
        .case-item.active {
            background: var(--green-soft);
            border-left: 5px solid var(--ink);
        }
        .badge {
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid var(--ink);
            background: var(--bright);
        }
        .badge.approved { background: var(--green); color: var(--ink); }
        .badge.review { background: var(--blue); color: var(--bright); border-color: var(--blue); }
        .badge.danger { background: var(--coral); color: var(--bright); border-color: var(--coral); }

        /* Detail Panel */
        .detail-box {
            background: var(--bright);
            border: 1.5px solid var(--ink);
            border-radius: 12px;
            padding: 22px 26px;
            box-shadow: 5px 5px 0 var(--ink);
        }
        .detail-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
            padding-bottom: 16px;
            border-bottom: 1.5px solid var(--ink);
            margin-bottom: 18px;
        }
        .action-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 14px 16px;
            background: var(--paper);
            border: 1.5px solid var(--ink);
            border-radius: 10px;
            margin-bottom: 18px;
            align-items: center;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            border-radius: 8px;
            border: 1.5px solid var(--ink);
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            background: var(--bright);
            color: var(--ink);
            text-decoration: none;
            transition: transform 0.1s ease;
        }
        .btn:hover { transform: translateY(-1px); }
        .btn-approve { background: var(--green); box-shadow: 2px 2px 0 var(--ink); }
        .btn-blue { background: var(--blue); color: var(--bright); }
        .btn-coral { background: var(--coral); color: var(--bright); }

        .two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 18px;
        }
        .info-card {
            background: var(--paper);
            border: 1px solid var(--ink);
            border-radius: 10px;
            padding: 14px 16px;
        }
        .info-card h4 {
            margin: 0 0 8px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
        }
        .diary-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 18px;
        }
        .diary-card {
            background: var(--bright);
            border: 1px solid var(--ink);
            border-radius: 8px;
            padding: 12px 14px;
        }
        .preview-frame {
            width: 100%;
            height: 820px;
            border: 1.5px solid var(--ink);
            border-radius: 10px;
            background: #fff;
        }

        /* Simulator View */
        .sim-grid {
            display: grid;
            grid-template-columns: 460px 1fr;
            gap: 22px;
            align-items: start;
        }
        .form-group { margin-bottom: 14px; }
        .form-group label {
            display: block;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .input, .select, .textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1.5px solid var(--ink);
            border-radius: 8px;
            background: var(--bright);
            font-size: 13.5px;
            font-family: inherit;
        }
        .goal-pills {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        .goal-pill {
            padding: 10px 12px;
            border: 1.5px solid var(--ink);
            border-radius: 8px;
            background: var(--bright);
            cursor: pointer;
            font-weight: 700;
            font-size: 12.5px;
            text-align: left;
        }
        .goal-pill.active {
            background: var(--green);
            box-shadow: 2px 2px 0 var(--ink);
        }
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--ink);
            color: var(--green);
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 13.5px;
            box-shadow: 4px 4px 0 var(--green);
            display: none;
            z-index: 100;
        }
    </style>
</head>
<body>

    <header class="topbar">
        <div class="brand">
            <div class="brand-circle">ОК</div>
            <div class="brand-title">
                <strong>НутриОК by Olga Kovaleva</strong>
                <span>Кабинет Эксперта · Сборка PDF · Симулятор Клиента</span>
            </div>
        </div>
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('cabinet')" id="tab-cabinet">1. Кабинет Ольги и Очередь</button>
            <button class="tab-btn" onclick="switchTab('preview')" id="tab-preview">2. Журнальный PDF-Разбор (A4)</button>
            <button class="tab-btn" onclick="switchTab('simulator')" id="tab-simulator">3. Интерактивный Симулятор Клиента</button>
        </div>
        <a class="tg-pill" href="https://t.me/zinchenko_wellness_ai_1_bot" target="_blank">
            Открыть @zinchenko_wellness_ai_1_bot ↗
        </a>
    </header>

    <section class="kpi-strip" id="kpi-strip">
        <div class="kpi-card">
            <div class="kpi-label">Всего кейсов в базе</div>
            <div class="kpi-val" id="kpi-total">—</div>
            <div class="kpi-sub">Хранилище НутриОК</div>
        </div>
        <div class="kpi-card highlight">
            <div class="kpi-label">Ждут проверки Ольги</div>
            <div class="kpi-val" id="kpi-pending">—</div>
            <div class="kpi-sub">Очередь экспертного ревью</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Одобрено (SHA-256 Gate)</div>
            <div class="kpi-val" id="kpi-approved">—</div>
            <div class="kpi-sub">Подписаны к выдаче</div>
        </div>
        <div class="kpi-card alert">
            <div class="kpi-label">Красные флаги / Safety</div>
            <div class="kpi-val" id="kpi-safety">—</div>
            <div class="kpi-sub">Автодоставка заблокирована</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Воронка (Старт → Разбор)</div>
            <div class="kpi-val" id="kpi-funnel" style="font-size:20px;margin-top:10px;">—</div>
            <div class="kpi-sub">По тарифам НутриОК</div>
        </div>
    </section>

    <main class="workspace">
        <!-- TAB 1: OLGA CABINET -->
        <div id="view-cabinet" class="cabinet-grid">
            <aside class="sidebar-box">
                <div class="sidebar-header">
                    <strong>Очередь кейсов (по SLA)</strong>
                    <button class="btn" style="padding:5px 10px;font-size:11px;background:var(--green);" onclick="seedDemoCase()">+ Создать демо-кейс</button>
                </div>
                <div class="filter-row">
                    <button class="filter-chip active" onclick="setFilter('all', this)">Все</button>
                    <button class="filter-chip" onclick="setFilter('pending', this)">Ждут Ольгу</button>
                    <button class="filter-chip" onclick="setFilter('approved', this)">Одобрены</button>
                    <button class="filter-chip" onclick="setFilter('safety', this)">Safety / Флаги</button>
                </div>
                <div class="case-list" id="case-list"></div>
            </aside>

            <section class="detail-box" id="case-detail">
                <div style="padding: 40px; text-align: center; color: var(--muted);">
                    Загрузка карточки кейса...
                </div>
            </section>
        </div>

        <!-- TAB 2: FULL EDITORIAL PDF PREVIEW -->
        <div id="view-preview" style="display:none;">
            <div class="detail-box">
                <div class="detail-header">
                    <div>
                        <span class="badge approved">Журнальный стандарт E1 · Палитра НутриОК</span>
                        <h2 class="serif" style="margin:6px 0 0;font-size:28px;" id="preview-title">Предпросмотр Персонального Разбора НутриОК</h2>
                    </div>
                    <div style="display:flex;gap:10px;">
                        <button class="btn btn-approve" onclick="generatePdfForActive()">⚡ Сгенерировать и скачать настоящий A4 PDF</button>
                        <button class="btn" onclick="switchTab('cabinet')">← Вернуться в карточку кейса</button>
                    </div>
                </div>
                <iframe id="full-preview-iframe" class="preview-frame"></iframe>
            </div>
        </div>

        <!-- TAB 3: INTERACTIVE CLIENT SIMULATOR -->
        <div id="view-simulator" style="display:none;" class="sim-grid">
            <div class="detail-box">
                <span class="badge approved">Живой конструктор кейса</span>
                <h2 class="serif" style="margin:8px 0 6px;font-size:26px;">Пройти путь клиента за 15 секунд</h2>
                <p style="font-size:13px;color:var(--muted);margin-top:0;">
                    Выберите цель, сдвиньте ползунок «Точка А (0–10)», проверьте дневник или протестируйте реакцию на красный флаг — и сразу получите готовый журнальный разбор.
                </p>

                <div class="form-group">
                    <label>1. Имя клиента и Тариф</label>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                        <input class="input" id="sim-name" value="Анна Морозова (Демо)">
                        <select class="select" id="sim-product">
                            <option value="ok_review">ОК-Разбор — 4 900 ₽ (Ревью Ольги)</option>
                            <option value="ok_express">ОК-Экспресс — 1 500 ₽ (Быстрый)</option>
                            <option value="ok_result_8">ОК-Результат 8 недель — 14 900 ₽</option>
                            <option value="ok_start">ОК-Старт — Бесплатно</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label>2. Главная цель (1 из 5)</label>
                    <div class="goal-pills" id="sim-goals">
                        <button type="button" class="goal-pill active" data-goal="energy" onclick="selectSimGoal('energy', this)">⚡ Энергия</button>
                        <button type="button" class="goal-pill" data-goal="digestion" onclick="selectSimGoal('digestion', this)">🌿 Пищеварение и комфорт</button>
                        <button type="button" class="goal-pill" data-goal="weight_appetite" onclick="selectSimGoal('weight_appetite', this)">⚖️ Вес и аппетит</button>
                        <button type="button" class="goal-pill" data-goal="sleep_stress" onclick="selectSimGoal('sleep_stress', this)">🌙 Сон и стресс</button>
                        <button type="button" class="goal-pill" data-goal="skin_hair" onclick="selectSimGoal('skin_hair', this)">✨ Кожа и волосы</button>
                    </div>
                </div>

                <div class="form-group">
                    <label>3. Ваша Точка А (Baseline 0–10): <strong id="sim-score-val" style="font-size:16px;">4 / 10</strong></label>
                    <input type="range" min="0" max="10" value="4" id="sim-score" style="width:100%;accent-color:var(--ink);" oninput="document.getElementById('sim-score-val').innerText = this.value + ' / 10'">
                </div>

                <div class="form-group">
                    <label>4. Дневник питания за 3 дня (текст / расшифровка голоса)</label>
                    <textarea class="textarea" id="sim-diary-1" rows="2" style="margin-bottom:6px;">День 1: Утром только капучино на бегу, в обед паста и салат, вечером плотный ужин в 21:30 и шоколад.</textarea>
                    <textarea class="textarea" id="sim-diary-2" rows="2" style="margin-bottom:6px;">День 2 (Голос STT): Проснулась разбитой, позавтракала тостом с сыром, после обеда клонило в сон, выпила 3 чашки кофе и мало воды.</textarea>
                    <textarea class="textarea" id="sim-diary-3" rows="2">День 3: На завтрак омлет из 2 яиц (было легче!), днём суп и курица, вечером снова тянуло на сладкое.</textarea>
                </div>

                <div class="form-group">
                    <label>5. Симптомы / Лекарства (можно проверить Красный флаг B5)</label>
                    <input class="input" id="sim-symptoms" value="Усталость после 14:00, вздутие к вечеру, пью витамин D 2000 МЕ">
                    <div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap;">
                        <button type="button" class="filter-chip" onclick="document.getElementById('sim-symptoms').value='стул второй день чёрный и слабость'">Тест флага: «стул второй день чёрный»</button>
                        <button type="button" class="filter-chip" onclick="document.getElementById('sim-symptoms').value='не стараясь потеряла 6 кг за 3 недели'">Тест флага: «потеряла 6 кг за 3 недели»</button>
                        <button type="button" class="filter-chip" onclick="document.getElementById('sim-symptoms').value='сдала общий анализ крови, ем черный хлеб'">Тест нейтральной фразы (0 флагов)</button>
                    </div>
                </div>

                <button class="btn btn-approve" style="width:100%;justify-content:center;padding:13px;" onclick="runSimulation()">
                    ✨ Создать кейс, проверить Safety Gate и собрать Журнальный Разбор
                </button>
            </div>

            <div class="detail-box">
                <div id="sim-result-banner" style="margin-bottom:14px;"></div>
                <iframe id="sim-preview-iframe" class="preview-frame"></iframe>
            </div>
        </div>
    </main>

    <div class="toast" id="toast"></div>

    <script>
        let allCases = [];
        let activeCaseId = null;
        let currentFilter = 'all';
        let simGoal = 'energy';

        function showToast(msg) {
            const el = document.getElementById('toast');
            el.innerText = msg;
            el.style.display = 'block';
            setTimeout(() => { el.style.display = 'none'; }, 3500);
        }

        function switchTab(tab) {
            ['cabinet', 'preview', 'simulator'].forEach(t => {
                document.getElementById('view-' + t).style.display = (t === tab) ? (t === 'cabinet' ? 'grid' : (t === 'simulator' ? 'grid' : 'block')) : 'none';
                document.getElementById('tab-' + t).classList.toggle('active', t === tab);
            });
            if (tab === 'preview' && activeCaseId) {
                document.getElementById('full-preview-iframe').src = '/api/cases/' + encodeURIComponent(activeCaseId) + '/html?t=' + Date.now();
            }
            if (tab === 'simulator' && activeCaseId) {
                document.getElementById('sim-preview-iframe').src = '/api/cases/' + encodeURIComponent(activeCaseId) + '/html?t=' + Date.now();
            }
        }

        function setFilter(filter, btn) {
            currentFilter = filter;
            document.querySelectorAll('.filter-row .filter-chip').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderCaseList();
        }

        function selectSimGoal(goal, btn) {
            simGoal = goal;
            document.querySelectorAll('#sim-goals .goal-pill').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        async function loadDashboard() {
            const res = await fetch('/api/cases');
            const data = await res.json();
            allCases = data.cases || [];

            document.getElementById('kpi-total').innerText = data.stats.total;
            document.getElementById('kpi-pending').innerText = data.stats.pending_review;
            document.getElementById('kpi-approved').innerText = data.stats.approved;
            document.getElementById('kpi-safety').innerText = data.stats.safety_flagged;
            document.getElementById('kpi-funnel').innerText =
                `Старт: ${data.stats.funnel.ok_start} · Экспресс: ${data.stats.funnel.ok_express} · Разбор: ${data.stats.funnel.ok_review}`;

            renderCaseList();
            if (!activeCaseId && allCases.length > 0) {
                selectCase(allCases[0].submission_id);
            } else if (activeCaseId) {
                selectCase(activeCaseId);
            }
        }

        function renderCaseList() {
            const listEl = document.getElementById('case-list');
            const filtered = allCases.filter(c => {
                if (currentFilter === 'pending') return c.needs_review && !c.is_approved;
                if (currentFilter === 'approved') return c.is_approved;
                if (currentFilter === 'safety') return (c.red_flags && c.red_flags.length > 0) || c.intake_status === 'awaiting_safety_review';
                return true;
            });

            if (filtered.length === 0) {
                listEl.innerHTML = `<div style="padding:24px;text-align:center;color:var(--muted);font-size:13px;">В этой категории пока нет кейсов. Нажмите «+ Создать демо-кейс».</div>`;
                return;
            }

            listEl.innerHTML = filtered.map(c => {
                const isAct = c.submission_id === activeCaseId ? 'active' : '';
                let badgeHtml = `<span class="badge review">${c.intake_status_ru}</span>`;
                if (c.is_approved) badgeHtml = `<span class="badge approved">✓ Одобрен (SHA-256)</span>`;
                else if (c.red_flags && c.red_flags.length > 0) badgeHtml = `<span class="badge danger">🚨 Красный флаг</span>`;

                return `
                    <div class="case-item ${isAct}" onclick="selectCase('${c.submission_id}')">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                            <strong style="font-size:14px;">${c.client_name}</strong>
                            ${badgeHtml}
                        </div>
                        <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">
                            ${c.product_title} · Цель: <strong>${c.goal_label}</strong> · Точка А: <strong>${c.baseline_score}/10</strong>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--muted);">
                            <span>ID: ${c.submission_id}</span>
                            <span>SLA: ${c.age_label}</span>
                        </div>
                    </div>
                `;
            }).join('');
        }

        async function selectCase(submissionId) {
            activeCaseId = submissionId;
            renderCaseList();
            const res = await fetch('/api/cases/' + encodeURIComponent(submissionId));
            const c = await res.json();

            const diaryHtml = (c.diary_days || []).map((d, i) => `
                <div class="diary-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <strong style="font-size:12.5px;">${d.day_label || ('День ' + (i+1))}</strong>
                        <span class="badge">${d.source || 'текст'}</span>
                    </div>
                    <div style="font-size:12px;color:var(--ink);">${d.meals_text || d.voice_transcript || 'Запись рациона'}</div>
                </div>
            `).join('') || `<div style="grid-column:1/-1;font-size:12.5px;color:var(--muted);">Дневник за 3 дня ещё не заполнен (или тариф ОК-Старт).</div>`;

            const reviewsHtml = (c.review_records || []).map(r => `
                <div style="padding:8px 10px;background:var(--bright);border:1px solid var(--line);border-radius:6px;margin-bottom:6px;font-size:12px;">
                    <strong>${r.decision === 'approved' ? '✅ Одобрено' : (r.decision === 'changes_requested' ? '✏️ Запрошены правки' : '🛑 Отклонено')}</strong>
                    · ${r.reviewer_name} · ${r.decided_at}
                    ${r.artifact_sha256 ? `<div style="font-family:monospace;font-size:10.5px;color:var(--blue);">SHA-256: ${r.artifact_sha256}</div>` : ''}
                    ${r.notes ? `<div style="margin-top:4px;color:var(--muted);">Комментарий: ${r.notes}</div>` : ''}
                </div>
            `).join('') || `<div style="font-size:12px;color:var(--muted);">Записей ревью пока нет — ожидает решения Ольги.</div>`;

            const detailEl = document.getElementById('case-detail');
            detailEl.innerHTML = `
                <div class="detail-header">
                    <div>
                        <div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;">
                            <span class="badge">${c.product_title}</span>
                            <span class="badge ${c.is_approved ? 'approved' : (c.red_flags.length ? 'danger' : 'review')}">
                                ${c.is_approved ? '✓ Выпуск разрешён (Release Approved)' : '🔒 Выпуск заблокирован до ревью Ольги'}
                            </span>
                            <span style="font-size:12px;color:var(--muted);">ID: <code>${c.submission_id}</code></span>
                        </div>
                        <h2 class="serif" style="margin:0;font-size:28px;">${c.client_name} · Цель: «${c.goal_label}»</h2>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:11px;text-transform:uppercase;color:var(--muted);font-weight:700;">Точка А (Baseline)</div>
                        <div class="serif" style="font-size:32px;line-height:1;">${c.baseline_score} / 10</div>
                    </div>
                </div>

                <div class="action-bar">
                    <button class="btn btn-approve" onclick="reviewCase('${c.submission_id}', 'approved')">✅ Одобрить и подписать SHA-256</button>
                    <button class="btn" onclick="promptChanges('${c.submission_id}')">✏️ Нужны правки (комментарий)</button>
                    <button class="btn btn-coral" onclick="reviewCase('${c.submission_id}', 'rejected')">🛑 Отклонить</button>
                    <button class="btn btn-blue" onclick="generatePdfForCase('${c.submission_id}')">📄 Собрать и скачать A4 PDF</button>
                    <button class="btn" onclick="switchTab('preview')">👁 Открыть на весь экран</button>
                </div>

                <div class="two-col">
                    <div class="info-card">
                        <h4>Метрика цели и Симптомы</h4>
                        <div style="font-size:13px;margin-bottom:6px;"><strong>Метрика:</strong> ${c.goal_metric}</div>
                        <div style="font-size:12.5px;color:var(--muted);"><strong>Контекст / жалобы:</strong> ${c.symptoms || 'Не указаны'}</div>
                        <div style="font-size:12.5px;color:var(--muted);margin-top:4px;"><strong>Лекарства / БАД:</strong> ${c.medications || 'Нет'}</div>
                    </div>
                    <div class="info-card">
                        <h4>Статус Safety Gate и Журнал Ревью Ольги</h4>
                        <div style="font-size:12.5px;margin-bottom:8px;">
                            <strong>Красные флаги (B5):</strong> ${c.red_flags.length ? `<span style="color:var(--coral);font-weight:700;">${c.red_flags.join(', ')}</span>` : '<span style="color:#2b6cb0;">Не обнаружены (0)</span>'}
                        </div>
                        ${reviewsHtml}
                    </div>
                </div>

                <div style="margin-bottom:16px;">
                    <h4 style="margin:0 0 8px;font-size:11.5px;text-transform:uppercase;letter-spacing:0.08em;color:var(--muted);">Дневник питания за 3 дня</h4>
                    <div class="diary-grid">${diaryHtml}</div>
                </div>

                <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <h4 style="margin:0;font-size:11.5px;text-transform:uppercase;letter-spacing:0.08em;color:var(--muted);">Живой предпросмотр журнального отчёта НутриОК (E1)</h4>
                        <a class="btn" style="padding:5px 12px;font-size:11.5px;" href="/api/cases/${encodeURIComponent(c.submission_id)}/pdf" target="_blank">📥 Скачать PDF файл</a>
                    </div>
                    <iframe class="preview-frame" src="/api/cases/${encodeURIComponent(c.submission_id)}/html?t=${Date.now()}"></iframe>
                </div>
            `;
        }

        async function reviewCase(submissionId, decision, notes = '') {
            const res = await fetch('/api/cases/' + encodeURIComponent(submissionId) + '/review', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ decision, notes })
            });
            const data = await res.json();
            if (data.ok) {
                showToast(data.message);
                await loadDashboard();
                await selectCase(submissionId);
            } else {
                showToast('Ошибка: ' + (data.error || 'не удалось сохранить ревью'));
            }
        }

        function promptChanges(submissionId) {
            const note = prompt('Введите комментарий для доработки черновика:', 'Уточнить питьевой режим и убрать упоминание железа до сдачи ферритина');
            if (note !== null) {
                reviewCase(submissionId, 'changes_requested', note);
            }
        }

        async function generatePdfForCase(submissionId) {
            showToast('Генерируем журнальный A4 PDF через Playwright...');
            window.open('/api/cases/' + encodeURIComponent(submissionId) + '/pdf?download=1', '_blank');
            setTimeout(() => loadDashboard(), 1500);
        }

        function generatePdfForActive() {
            if (activeCaseId) generatePdfForCase(activeCaseId);
        }

        async function seedDemoCase() {
            const res = await fetch('/api/simulate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    client_name: 'Екатерина Волкова (Пилот НутриОК)',
                    product_code: 'ok_review',
                    primary_goal: 'energy',
                    baseline_score: 4,
                    symptoms: 'Спад энергии после 14:00, тяга к сладкому вечером, кофе натощак',
                    medications: 'Магний цитрат 400 мг, витамин D 2000 МЕ',
                    diary_days: [
                        'День 1: Утром большой латте на голодный желудок, в 13:30 паста с курицей, вечером бутерброды и чай с конфетами.',
                        'День 2 (Голос STT): Завтрак пропустила, днём салат Цезарь и суп, к 16:00 сильная сонливость, поужинала в 21:40.',
                        'День 3: На завтрак 2 яйца и тост с авокадо, в обед гречка с индейкой, вечером творог с ягодами.'
                    ]
                })
            });
            const data = await res.json();
            if (data.submission_id) {
                activeCaseId = data.submission_id;
                showToast('Демо-кейс создан и открыт!');
                await loadDashboard();
            }
        }

        async function runSimulation() {
            const payload = {
                client_name: document.getElementById('sim-name').value,
                product_code: document.getElementById('sim-product').value,
                primary_goal: simGoal,
                baseline_score: parseInt(document.getElementById('sim-score').value, 10),
                symptoms: document.getElementById('sim-symptoms').value,
                medications: 'Витамин D 2000 МЕ',
                diary_days: [
                    document.getElementById('sim-diary-1').value,
                    document.getElementById('sim-diary-2').value,
                    document.getElementById('sim-diary-3').value,
                ]
            };
            const res = await fetch('/api/simulate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            activeCaseId = data.submission_id;
            const banner = document.getElementById('sim-result-banner');
            if (data.red_flags && data.red_flags.length > 0) {
                banner.innerHTML = `
                    <div style="background:var(--coral-soft);border:1.5px solid var(--coral);padding:12px 16px;border-radius:8px;">
                        <strong style="color:var(--coral);">🚨 Сработал Safety Gate (B5): обнаружены красные флаги [${data.red_flags.join(', ')}]</strong>
                        <div style="font-size:12.5px;margin-top:4px;">Автоматическая выдача заблокирована. Клиенту отправлена рекомендация обратиться к врачу, кейс передан на контроль.</div>
                    </div>
                `;
            } else {
                banner.innerHTML = `
                    <div style="background:var(--green-soft);border:1.5px solid var(--ink);padding:12px 16px;border-radius:8px;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong>✅ Кейс <code>${data.submission_id}</code> создан! Статус гейта: ${data.gate_status}</strong>
                            <div style="font-size:12px;color:var(--muted);">Журнальный разбор сформирован ниже и добавлен в очередь Ольги.</div>
                        </div>
                        <button class="btn btn-approve" onclick="switchTab('cabinet')">Открыть в кабинете Ольги →</button>
                    </div>
                `;
            }
            document.getElementById('sim-preview-iframe').src = '/api/cases/' + encodeURIComponent(data.submission_id) + '/html?t=' + Date.now();
            await loadDashboard();
            showToast('Симуляция выполнена!');
        }

        loadDashboard();
    </script>
</body>
</html>
"""


def _format_age(created_at: str | None) -> str:
    if not created_at:
        return "сегодня"
    try:
        dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        hours = max(0, int((now - dt).total_seconds() // 3600))
        if hours < 1:
            return "< 1 ч"
        if hours < 24:
            return f"{hours} ч"
        return f"{hours // 24} дн."
    except Exception:
        return "недавно"


STATUS_LABELS_RU = {
    "awaiting_expert_review": "Ждёт ревью Ольги",
    "awaiting_human_review": "Ждёт ревью Ольги",
    "awaiting_safety_review": "Safety-проверка",
    "awaiting_supplement_protocol_review": "Ревью БАД Ольгой",
    "draft_requires_edits": "Нужны правки",
    "rejected_by_admin": "Отклонён",
    "delivered_to_client": "Доставлен клиенту",
    "manual_payment_pending": "Ожидает оплаты",
}


def _summarize_submission(sub: dict[str, Any]) -> dict[str, Any]:
    intake = sub.get("intake") if isinstance(sub.get("intake"), dict) else {}
    profile = sub.get("profile") if isinstance(sub.get("profile"), dict) else {}
    medical = sub.get("medical_context") if isinstance(sub.get("medical_context"), dict) else {}

    product_code = normalize_product_code(
        sub.get("product_code")
        or intake.get("product_code")
        or sub.get("offer")
        or sub.get("tier")
        or "ok_review"
    )
    offer = get_product_offer(product_code)
    goal_key = str(
        intake.get("primary_goal")
        or sub.get("primary_goal")
        or "energy"
    )
    goal_label = PRIMARY_GOALS.get(goal_key, "Энергия и ресурс")
    baseline_raw = intake.get("baseline_score", sub.get("baseline_score", 4))
    try:
        baseline_score = int(baseline_raw)
    except (TypeError, ValueError):
        baseline_score = 4

    diary_days = intake.get("diary") or sub.get("nutrition_diary") or []
    symptoms = str(medical.get("symptoms") or sub.get("symptoms") or "")
    medications = str(intake.get("medications") or sub.get("medications") or "")
    red_flags = find_red_flags({"symptoms": symptoms, "medications": medications, "intake": intake})
    approved = is_release_approved(sub)
    intake_status = str(sub.get("intake_status") or "awaiting_expert_review")

    return {
        "submission_id": str(sub.get("submission_id") or ""),
        "client_name": str(
            profile.get("full_name")
            or profile.get("telegram_full_name")
            or "Клиент НутриОК"
        ),
        "product_code": product_code,
        "product_title": offer.name,
        "goal_key": goal_key,
        "goal_label": goal_label,
        "baseline_score": baseline_score,
        "goal_metric": str(
            intake.get("goal_metric")
            or sub.get("goal_metric")
            or GOAL_DEFAULT_METRICS.get(goal_key, "Шкала 0–10 в конце недели")
        ),
        "symptoms": symptoms,
        "medications": medications,
        "diary_days": diary_days if isinstance(diary_days, list) else [],
        "red_flags": red_flags,
        "is_approved": approved,
        "needs_review": intake_status in {
            "awaiting_expert_review",
            "awaiting_human_review",
            "awaiting_safety_review",
            "awaiting_supplement_protocol_review",
            "draft_requires_edits",
        },
        "intake_status": intake_status,
        "intake_status_ru": STATUS_LABELS_RU.get(intake_status, intake_status),
        "created_at": str(sub.get("created_at") or ""),
        "age_label": _format_age(sub.get("created_at")),
        "review_records": sub.get("review_records") or [],
    }


def create_studio_app() -> web.Application:
    settings = load_settings()
    settings.submissions_dir.mkdir(parents=True, exist_ok=True)
    settings.drafts_dir.mkdir(parents=True, exist_ok=True)

    async def handle_index(request: web.Request) -> web.Response:
        return web.Response(text=STUDIO_HTML, content_type="text/html")

    async def handle_list_cases(request: web.Request) -> web.Response:
        files = sorted(
            settings.submissions_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        cases: list[dict[str, Any]] = []
        funnel = {"ok_start": 0, "ok_express": 0, "ok_review": 0, "ok_result_8": 0}
        pending_count = 0
        approved_count = 0
        safety_count = 0

        for path in files[:40]:
            sub = load_submission(settings.submissions_dir, path.stem)
            if not isinstance(sub, dict):
                continue
            item = _summarize_submission(sub)
            cases.append(item)
            pcode = item["product_code"]
            if pcode in funnel:
                funnel[pcode] += 1
            if item["is_approved"]:
                approved_count += 1
            if item["needs_review"] and not item["is_approved"]:
                pending_count += 1
            if item["red_flags"] or item["intake_status"] == "awaiting_safety_review":
                safety_count += 1

        return web.json_response(
            {
                "cases": cases,
                "stats": {
                    "total": len(cases),
                    "pending_review": pending_count,
                    "approved": approved_count,
                    "safety_flagged": safety_count,
                    "funnel": funnel,
                },
            }
        )

    async def handle_get_case(request: web.Request) -> web.Response:
        submission_id = request.match_info["submission_id"]
        sub = load_submission(settings.submissions_dir, submission_id)
        if not sub:
            raise web.HTTPNotFound(text="Case not found")
        return web.json_response(_summarize_submission(sub))

    async def handle_case_html(request: web.Request) -> web.Response:
        submission_id = request.match_info["submission_id"]
        sub = load_submission(settings.submissions_dir, submission_id)
        if not sub:
            raise web.HTTPNotFound(text="Case not found")
        html = render_nutriok_report_html({}, submission=sub)
        return web.Response(text=html, content_type="text/html")

    async def handle_case_pdf(request: web.Request) -> web.Response:
        submission_id = request.match_info["submission_id"]
        sub = load_submission(settings.submissions_dir, submission_id)
        if not sub:
            raise web.HTTPNotFound(text="Case not found")

        pdf_path = settings.drafts_dir / f"NutriOK_{submission_id}.pdf"
        await asyncio.to_thread(create_nutriok_pdf, {}, str(pdf_path), sub)
        sub["pdf_path"] = str(pdf_path)
        save_submission(settings.submissions_dir, submission_id, sub)

        headers = {}
        if request.query.get("download") == "1":
            headers["Content-Disposition"] = f'attachment; filename="NutriOK_{submission_id}.pdf"'
        return web.FileResponse(path=pdf_path, headers=headers)

    async def handle_review_case(request: web.Request) -> web.Response:
        submission_id = request.match_info["submission_id"]
        sub = load_submission(settings.submissions_dir, submission_id)
        if not sub:
            return web.json_response({"ok": False, "error": "Кейс не найден"}, status=404)

        body = await request.json()
        decision = str(body.get("decision") or "approved")
        notes = str(body.get("notes") or "")

        pdf_path_raw = str(sub.get("pdf_path") or "").strip()
        pdf_path = Path(pdf_path_raw) if pdf_path_raw else (settings.drafts_dir / f"NutriOK_{submission_id}.pdf")
        if decision == "approved" and not pdf_path.exists():
            await asyncio.to_thread(create_nutriok_pdf, {}, str(pdf_path), sub)
            sub["pdf_path"] = str(pdf_path)

        admin_id = int((settings.admin_chat_ids or (481955956,))[0])
        rec = record_review(
            sub,
            reviewer_id=admin_id,
            reviewer_name="Ольга Ковалева",
            decision=decision,  # type: ignore[arg-type]
            artifact_path=pdf_path,
            notes=notes,
            admin_ids={admin_id},
        )
        if decision == "approved":
            sub["intake_status"] = "delivered_to_client"
            # Re-render PDF with Olga's verification stamp embedded and update SHA-256
            await asyncio.to_thread(create_nutriok_pdf, {}, str(pdf_path), sub)
            new_sha = compute_file_sha256(pdf_path)
            sub["review_records"][-1]["artifact_sha256"] = new_sha
            sub["approved_artifact_sha256"] = new_sha
        elif decision == "changes_requested":
            sub["intake_status"] = "draft_requires_edits"
        elif decision == "rejected":
            sub["intake_status"] = "rejected_by_admin"

        save_submission(settings.submissions_dir, submission_id, sub)
        return web.json_response(
            {
                "ok": True,
                "message": f"Решение «{decision}» сохранено и подписано (SHA-256: {sub.get('approved_artifact_sha256', rec.artifact_sha256)[:12]}…)",
            }
        )

    async def handle_simulate(request: web.Request) -> web.Response:
        body = await request.json()
        now_dt = datetime.now(timezone.utc)
        submission_id = f"{now_dt.strftime('%Y%m%dT%H%M%SZ')}_studio"
        product_code = normalize_product_code(body.get("product_code") or "ok_review")
        goal_key = str(body.get("primary_goal") or "energy")
        baseline_score = int(body.get("baseline_score") or 4)
        symptoms = str(body.get("symptoms") or "")
        medications = str(body.get("medications") or "")
        raw_days = body.get("diary_days") or []

        diary_days = []
        for idx, text in enumerate(raw_days[:3], start=1):
            source = "voice" if "голос" in str(text).lower() or "stt" in str(text).lower() else "text"
            diary_days.append(
                {
                    "day_label": f"День {idx}",
                    "meals_text": str(text),
                    "water_coffee_text": "",
                    "voice_transcript": str(text) if source == "voice" else "",
                    "photo_file_ids": [],
                    "source": source,
                }
            )

        goal_metric = GOAL_DEFAULT_METRICS.get(goal_key, "Оценка состояния 0–10 в конце недели")
        sub: dict[str, Any] = {
            "submission_id": submission_id,
            "created_at": now_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "offer": product_code,
            "product_code": product_code,
            "primary_goal": goal_key,
            "baseline_score": baseline_score,
            "goal_metric": goal_metric,
            "symptoms": symptoms,
            "medications": medications,
            "nutrition_diary": diary_days,
            "profile": {
                "telegram_user_id": int((settings.admin_chat_ids or (481955956,))[0]),
                "full_name": str(body.get("client_name") or "Демо-клиент НутриОК"),
            },
            "medical_context": {
                "symptoms": symptoms,
                "goal": PRIMARY_GOALS.get(goal_key, goal_key),
                "red_flags": "нет",
            },
            "intake": {
                "schema_version": 1,
                "product_code": product_code,
                "primary_goal": goal_key,
                "baseline_score": baseline_score,
                "goal_metric": goal_metric,
                "diary": diary_days,
                "medications": medications,
                "allergies": "нет",
                "pd_consent_at": now_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "age_confirmed_18": True,
            },
        }

        decision = evaluate_delivery_gate(
            product_code,
            "Наблюдение по дневному рациону и персональный план питания на 7 дней.",
            sub,
        )
        sub["delivery_gate"] = decision.as_dict()
        sub["auto_delivery_decision"] = decision.as_dict()
        sub["intake_status"] = decision.status

        pdf_path = settings.drafts_dir / f"NutriOK_{submission_id}.pdf"
        sub["pdf_path"] = str(pdf_path)
        save_submission(settings.submissions_dir, submission_id, sub)

        return web.json_response(
            {
                "ok": True,
                "submission_id": submission_id,
                "gate_status": decision.status,
                "red_flags": find_red_flags(sub),
            }
        )

    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/cases", handle_list_cases)
    app.router.add_get("/api/cases/{submission_id}", handle_get_case)
    app.router.add_get("/api/cases/{submission_id}/html", handle_case_html)
    app.router.add_get("/api/cases/{submission_id}/pdf", handle_case_pdf)
    app.router.add_post("/api/cases/{submission_id}/review", handle_review_case)
    app.router.add_post("/api/simulate", handle_simulate)
    return app


if __name__ == "__main__":
    port = int(os.environ.get("NUTRIOK_STUDIO_PORT", "8090"))
    print(f"Starting NutriOK Olga Studio on http://127.0.0.1:{port}")
    web.run_app(create_studio_app(), host="127.0.0.1", port=port)
