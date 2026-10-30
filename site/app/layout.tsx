import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("host") ?? "localhost:3000";
  const protocol = host.includes("localhost") ? "http" : "https";
  const base = new URL(protocol + "://" + host);

  return {
    metadataBase: base,
    title: "НутриОК — нутрициолог Ольга | Разбор питания и анализов",
    description: "Нутрициологическая навигация Ольги: питание, симптомы, дневник и анализы в одной понятной стратегии. Разбор ХМС по Осипову с объяснением границ метода.",
    applicationName: "НутриОК",
    authors: [{ name: "Ольга" }],
    keywords: ["нутрициолог онлайн", "разбор анализов нутрициологом", "ХМС по Осипову разбор", "микробиом питание", "дневник питания", "пищеварение нутрициолог"],
    alternates: { canonical: "/" },
    openGraph: {
      type: "website", locale: "ru_RU", url: "/", siteName: "НутриОК",
      title: "НутриОК — разбор, после которого понятно, что делать",
      description: "Питание, симптомы, образ жизни и анализы в одной ясной стратегии.",
      images: [{ url: "/og.png", width: 1200, height: 630, alt: "НутриОК — нутрициологическая навигация Ольги" }],
    },
    twitter: { card: "summary_large_image", title: "НутриОК — нутрициологическая навигация Ольги", description: "Разбор, после которого понятно, что делать.", images: ["/og.png"] },
    robots: { index: false, follow: false, googleBot: { index: false, follow: false } },
    icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
  };
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="ru"><body>{children}</body></html>;
}