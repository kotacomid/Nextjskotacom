import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Footer from "@/components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "WebJasa - Jasa Pembuatan Website Profesional",
  description: "Solusi terpercaya untuk kebutuhan website bisnis Anda. Kami menghadirkan website modern, responsif, dan berkualitas tinggi untuk mengembangkan bisnis Anda.",
  keywords: ["jasa website", "pembuatan website", "website bisnis", "web development", "website murah", "website profesional"],
  authors: [{ name: "WebJasa Team" }],
  openGraph: {
    title: "WebJasa - Jasa Pembuatan Website Profesional",
    description: "Solusi terpercaya untuk kebutuhan website bisnis Anda. Kami menghadirkan website modern, responsif, dan berkualitas tinggi.",
    url: "https://webjasa.com",
    siteName: "WebJasa",
    locale: "id_ID",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "WebJasa - Jasa Pembuatan Website Profesional",
    description: "Solusi terpercaya untuk kebutuhan website bisnis Anda. Kami menghadirkan website modern, responsif, dan berkualitas tinggi.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className={inter.className}>
        <Navigation />
        <main className="pt-16">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
