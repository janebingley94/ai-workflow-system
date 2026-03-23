import "./globals.css";
import type { ReactNode } from "react";
import { Space_Grotesk, IBM_Plex_Mono } from "next/font/google";

const space = Space_Grotesk({ subsets: ["latin"], variable: "--font-sans" });
const mono = IBM_Plex_Mono({ subsets: ["latin"], weight: ["400", "600"], variable: "--font-mono" });

export const metadata = {
  title: "AI Workflow System",
  description: "Drag-and-drop AI workflow system",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${space.variable} ${mono.variable}`}>
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <div className="pointer-events-none fixed inset-0 overflow-hidden">
          <div className="absolute -left-32 top-20 h-72 w-72 rounded-full bg-emerald-400/20 blur-[120px]" />
          <div className="absolute right-0 top-0 h-80 w-80 rounded-full bg-sky-500/20 blur-[140px]" />
          <div className="absolute bottom-0 left-1/3 h-80 w-80 rounded-full bg-rose-500/20 blur-[140px]" />
        </div>
        <div className="relative mx-auto min-h-screen max-w-6xl px-6 py-12">
          {children}
        </div>
      </body>
    </html>
  );
}
