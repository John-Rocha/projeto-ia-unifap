import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TutorIA — CC0121 Inteligência Artificial",
  description: "Tutor inteligente para a disciplina de IA da UNIFAP",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${geistSans.variable} ${geistMono.variable} h-full`}>
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 antialiased">
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto max-w-5xl px-4 py-3 flex items-center gap-3">
            <a href="/" className="flex items-center gap-2 font-semibold text-indigo-600 hover:text-indigo-700">
              <span className="text-xl">🤖</span>
              <span>TutorIA</span>
            </a>
            <span className="text-slate-300">|</span>
            <span className="text-sm text-slate-500">CC0121 — Inteligência Artificial</span>
            <div className="ml-auto flex gap-4 text-sm">
              <a href="/" className="text-slate-600 hover:text-indigo-600">Aulas</a>
              <a href="/chat" className="text-slate-600 hover:text-indigo-600">Chat</a>
            </div>
          </div>
        </header>
        <main className="flex-1">{children}</main>
        <footer className="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-400">
          TutorIA · UNIFAP · CC0121
        </footer>
      </body>
    </html>
  );
}
