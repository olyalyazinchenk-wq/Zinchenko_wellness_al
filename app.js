const productConfig = {
    telegramHandle: "zinchenko_wellness_ai_1_bot",
};

function syncTelegramLinks() {
    const url = `https://t.me/${productConfig.telegramHandle}`;
    document.querySelectorAll(".js-telegram-link").forEach((link) => {
        link.setAttribute("href", url);
    });
}

function wireChecklistCopy() {
    const button = document.getElementById("copyChecklistButton");
    const checklist = document.getElementById("launchChecklist");

    if (!button || !checklist) {
        return;
    }

    button.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(checklist.textContent.trim());
            button.textContent = "Чек-лист скопирован";
        } catch (error) {
            button.textContent = "Скопируйте вручную ниже";
            console.error(error);
        }
    });
}

function markActiveNav() {
    const links = document.querySelectorAll(".nav-links a");
    const sections = [...links]
        .map((link) => document.querySelector(link.getAttribute("href")))
        .filter(Boolean);

    if (!links.length || !sections.length) {
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                links.forEach((link) => {
                    const active = link.getAttribute("href") === `#${entry.target.id}`;
                    link.style.color = active ? "var(--accent-deep)" : "var(--muted)";
                });
            });
        },
        {
            rootMargin: "-35% 0px -50% 0px",
            threshold: 0,
        }
    );

    sections.forEach((section) => observer.observe(section));
}

document.addEventListener("DOMContentLoaded", () => {
    syncTelegramLinks();
    wireChecklistCopy();
    markActiveNav();
});
