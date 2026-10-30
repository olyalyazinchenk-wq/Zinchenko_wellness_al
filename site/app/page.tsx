const telegramBase = "https://t.me/zinchenko_wellness_ai_1_bot";

const services = [
  { tag: "Знакомство", name: "ОК-Старт", price: "0 ₽", lead: "Определить одну цель и перестать метаться между советами.", includes: "Короткий скрининг, исходная точка 0–10 и один безопасный первый шаг.", start: "site_start" },
  { tag: "Быстрый формат", name: "ОК-Экспресс", price: "990 ₽", lead: "Увидеть повторяющиеся привычки, которые реально можно изменить.", includes: "Три дня дневника, три главных паттерна и план на семь дней.", start: "site_express", featured: true },
  { tag: "Глубокий разбор", name: "ОК-Разбор", price: "5 900 ₽", lead: "Собрать питание, симптомы, режим и анализы в одну картину.", includes: "Профиль ситуации, приоритеты и персональная стратегия на 30 дней.", start: "site_review" },
  { tag: "Сопровождение", name: "ОК-Результат 8", price: "14 900 ₽", lead: "Не просто получить план, а внедрить его без перегруза.", includes: "Разбор и восемь недель адаптации с регулярной корректировкой.", start: "site_result8" },
];

const faqs = [
  ["Можно ли начать, если у меня нет анализов?", "Да. Первый шаг начинается с цели, симптомов, режима и дневника питания. Анализы нужны только тогда, когда они действительно меняют решение."],
  ["Как проходит разбор ХМС по Осипову?", "Вы отправляете бланк и контекст в Telegram. Данные проверяются, сопоставляются с референсами отчёта и рассматриваются вместе с жалобами, питанием, лекарствами и другими анализами. ХМС используется как дополнительный источник информации, а не как самостоятельный диагноз."],
  ["Бот сам выдаёт назначения?", "Нет. Полные персональные разборы, красные флаги и детали по добавкам проходят проверку Ольги. При недостатке данных система сначала задаёт уточняющие вопросы."],
  ["Это заменяет приём врача?", "Нет. НутриОК не ставит диагнозы, не назначает лечение и не меняет лекарства. При опасных или острых симптомах необходима очная медицинская помощь."],
];

function TelegramLink({ start, children, className = "button button-primary", label }: { start: string; children: React.ReactNode; className?: string; label?: string }) {
  return (
    <a className={className} href={telegramBase + "?start=" + start} target="_blank" rel="noopener noreferrer" aria-label={label}>
      <span>{children}</span><span className="button-arrow" aria-hidden="true">↗</span>
    </a>
  );
}

export default function Home() {
  const structuredData = {
    "@context": "https://schema.org",
    "@graph": [
      { "@type": "Person", "@id": "#olga", name: "Ольга", jobTitle: "Нутрициолог", knowsAbout: ["нутрициологическая навигация", "дневник питания", "пищеварение", "интерпретация лабораторных данных", "ХМС по Осипову"] },
      { "@type": "ProfessionalService", "@id": "#nutriok", name: "НутриОК", description: "Нутрициологическая навигация: питание, симптомы, образ жизни и анализы в одной понятной стратегии.", founder: { "@id": "#olga" }, areaServed: "RU", serviceType: "Нутрициологическая консультация онлайн", sameAs: [telegramBase], hasOfferCatalog: { "@type": "OfferCatalog", name: "Форматы работы НутриОК", itemListElement: services.map((service) => ({ "@type": "Offer", name: service.name, description: service.includes, priceCurrency: "RUB", price: service.price.replace(/\D/g, "") })) } }
    ]
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />
      <header className="site-header">
        <a className="brand" href="#top" aria-label="НутриОК, на главную"><span className="brand-mark">Н</span><span><strong>НутриОК</strong><small>by Olga</small></span></a>
        <nav className="desktop-nav" aria-label="Основная навигация"><a href="#approach">Подход</a><a href="#osipov">ХМС по Осипову</a><a href="#services">Услуги</a><a href="#faq">Вопросы</a></nav>
        <TelegramLink start="site_header" className="header-action" label="Перейти в Telegram">Telegram</TelegramLink>
      </header>

      <main id="top">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-shade" aria-hidden="true" />
          <div className="hero-content">
            <p className="kicker">Нутрициологическая навигация Ольги</p>
            <h1 id="hero-title">НутриОК</h1>
            <p className="hero-statement">Разбор, после которого <mark>понятно</mark>, что делать.</p>
            <p className="hero-copy">Соединяю питание, симптомы, образ жизни и анализы в одну ясную картину. Без универсальных диет и десяти банок «на всякий случай».</p>
            <div className="hero-actions"><TelegramLink start="site_hero">Начать в Telegram</TelegramLink><a className="button button-ghost" href="#services">Выбрать формат <span aria-hidden="true">↓</span></a></div>
            <p className="pilot-note">18+ · контролируемый пилот · персональные разборы проверяет Ольга</p>
          </div>
        </section>

        <div className="signal-strip" aria-label="Принципы НутриОК"><span>Факты вместо догадок</span><span>Одна цель за цикл</span><span>План, который можно выполнить</span></div>

        <section className="pain-section section-shell" aria-labelledby="pain-title">
          <div className="section-index">01 / Узнавание</div>
          <div className="pain-layout">
            <div><p className="kicker coral">Когда тело говорит громче планов</p><h2 id="pain-title">Вы не обязаны привыкать к постоянному дискомфорту.</h2></div>
            <div className="symptom-list"><p>Живот снова вздулся, хотя вы не ели ничего «такого».</p><p>После еды нет сил, а сладкого хочется прямо сейчас.</p><p>Стул нестабильный, кожа реагирует, сон не восстанавливает.</p><p>Анализов много, рекомендаций ещё больше, ясности нет.</p></div>
          </div>
          <div className="honesty-line">Эти признаки не доказывают «дисбаланс микробиома». Они помогают сформулировать вопрос, который стоит разобрать последовательно.</div>
        </section>

        <section className="approach-section" id="approach" aria-labelledby="approach-title"><div className="section-shell">
          <div className="section-index light">02 / Метод</div>
          <div className="section-heading-row"><h2 id="approach-title">Не лечим таблицу. Разбираем человека.</h2><p>Один показатель редко объясняет самочувствие. Поэтому в центре не бланк анализа, а ваш контекст и измеримая цель.</p></div>
          <ol className="process-grid">
            <li><span>01</span><h3>Собираем контекст</h3><p>Цель, симптомы, диагнозы, лекарства, сон, движение и то, как вы едите сейчас.</p></li>
            <li><span>02</span><h3>Отделяем факты</h3><p>Проверяем дневник и анализы. Гипотезы не выдаём за измеренный результат.</p></li>
            <li><span>03</span><h3>Выбираем приоритет</h3><p>Не двадцать изменений сразу, а последовательность действий и понятная метрика.</p></li>
            <li><span>04</span><h3>Сверяем результат</h3><p>Смотрим, что изменилось, что оказалось невыполнимым и где план нужно адаптировать.</p></li>
          </ol>
        </div></section>

        <section className="expert-section section-shell" aria-labelledby="expert-title">
          <div className="section-index">03 / Эксперт</div>
          <div className="expert-grid">
            <div className="expert-title-wrap"><p className="kicker blue">Ольга, нутрициолог</p><h2 id="expert-title">Сначала логика. Потом рекомендации.</h2></div>
            <div className="expert-copy"><p className="large-copy">Моя задача — не впечатлить сложными терминами, а превратить разрозненные данные в маршрут, который вы понимаете и можете пройти.</p>
              <div className="principles"><div><strong>01</strong><span>Не назначаю анализы «списком на всякий случай».</span></div><div><strong>02</strong><span>Не обещаю найти одну причину всех симптомов.</span></div><div><strong>03</strong><span>Показываю, где факт, где гипотеза, а где нужен врач.</span></div></div>
            </div>
          </div>
        </section>

        <section className="osipov-section" id="osipov" aria-labelledby="osipov-title"><div className="section-shell osipov-layout">
          <div><div className="section-index light">04 / Специализация</div><p className="kicker lime">ХМС по Осипову</p><h2 id="osipov-title">Бланк становится понятнее. Границы метода — тоже.</h2><p className="osipov-lead">Вы присылаете результат, а я разбираю показатели, отклонения и возможные связи в контексте вашего питания, симптомов, лекарств и других анализов.</p><TelegramLink start="site_osipov" className="button button-light">Отправить анализ</TelegramLink></div>
          <div className="osipov-facts">
            <article><span>Что вы получите</span><h3>Структурированный разбор</h3><p>Показатели, референсы бланка, отклонения, уровень уверенности и вопросы, которые требуют уточнения.</p></article>
            <article><span>Что важно понимать</span><h3>Не самостоятельный диагноз</h3><p>Метод рассматривается как дополнительный источник данных и не заменяет клиническую диагностику.</p></article>
            <article><span>Как сохраняется безопасность</span><h3>Проверка перед выдачей</h3><p>Персональный вывод не отправляется клиенту как медицинское назначение без человеческой проверки.</p></article>
          </div>
        </div></section>

        <section className="services-section section-shell" id="services" aria-labelledby="services-title">
          <div className="section-index">05 / Форматы</div>
          <div className="section-heading-row dark-text"><h2 id="services-title">Начните с нужной глубины.</h2><p>Не уверены, что выбрать? ОК-Старт поможет определить следующий формат без оплаты.</p></div>
          <div className="service-grid">{services.map((service) => (
            <article className={service.featured ? "service-card featured" : "service-card"} key={service.name}>
              <div className="service-topline"><span>{service.tag}</span>{service.featured && <b>Пилот</b>}</div><h3>{service.name}</h3><div className="service-price">{service.price}</div><p className="service-lead">{service.lead}</p><p className="service-includes">{service.includes}</p>
              <TelegramLink start={service.start} className={service.featured ? "button button-dark" : "button button-outline"} label={"Выбрать " + service.name + " в Telegram"}>Выбрать</TelegramLink>
            </article>
          ))}</div>
          <p className="services-note">ОК-Ритм — поддерживающий формат после основной программы, 1 990 ₽ в месяц. Оплата в пилоте подтверждается вручную; лабораторные исследования оплачиваются отдельно.</p>
        </section>

        <section className="faq-section" id="faq" aria-labelledby="faq-title"><div className="section-shell faq-layout">
          <div><div className="section-index">06 / Вопросы</div><h2 id="faq-title">До того, как вы напишете.</h2></div>
          <div className="faq-list">{faqs.map(([question, answer]) => <details key={question}><summary><span>{question}</span><span className="faq-icon" aria-hidden="true">+</span></summary><p>{answer}</p></details>)}</div>
        </div></section>

        <section className="final-section" aria-labelledby="final-title"><div className="final-orbit" aria-hidden="true">0→10</div><div className="section-shell final-content"><p className="kicker">Первый шаг занимает одно сообщение</p><h2 id="final-title">Начните не с анализа.<br />Начните с цели.</h2><TelegramLink start="site_final" className="button button-dark button-large">Написать в Telegram</TelegramLink></div></section>
      </main>

      <footer className="site-footer">
        <div className="footer-brand"><strong>НутриОК</strong><span>Нутрициологическая навигация Ольги</span></div>
        <p>Информация носит образовательный и нутрициологический характер, не заменяет консультацию врача, диагностику или лечение. При острых симптомах обратитесь за медицинской помощью.</p>
        <div className="footer-links"><a href={telegramBase + "?start=site_footer"} target="_blank" rel="noopener noreferrer">Telegram ↗</a><a href="#top">Наверх ↑</a></div>
        <small>© 2026 НутриОК</small>
      </footer>
    </>
  );
}