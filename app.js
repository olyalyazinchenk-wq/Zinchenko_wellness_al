const productConfig = {
    telegramHandle: "zinchenko_wellness_ai_1_bot",
};

function syncTelegramLinks() {
    const url = `https://t.me/${productConfig.telegramHandle}`;
    document.querySelectorAll(".js-telegram-link").forEach((link) => {
        link.setAttribute("href", url);
    });
}

function wireCtaModal() {
    const modal = document.getElementById("ctaModal");
    const openButtons = document.querySelectorAll(".js-cta-open-modal");
    const closeButton = document.getElementById("closeModalButton");

    if (!modal) return;

    const openModal = () => {
        modal.classList.add("is-active");
        document.body.style.overflow = "hidden"; // Prevent scrolling when modal is open
    };

    const closeModal = () => {
        modal.classList.remove("is-active");
        document.body.style.overflow = ""; // Restore scrolling
    };

    openButtons.forEach((btn) => {
        btn.addEventListener("click", openModal);
    });

    if (closeButton) {
        closeButton.addEventListener("click", closeModal);
    }

    // Close on click outside the card
    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Close on Escape key press
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && modal.classList.contains("is-active")) {
            closeModal();
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
                    link.style.color = active ? "var(--accent)" : "var(--muted)";
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
    wireCtaModal();
    markActiveNav();
});
