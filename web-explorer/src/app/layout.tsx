import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "quantum·circuits — MIPT in random Clifford circuits",
  description:
    "Interactive research explorer for the measurement-induced phase transition in hybrid random Clifford circuits: live Gottesman–Knill simulator, the deposited purification dataset, finite-size scaling explorer, exact free-fermion results, and bit-exact reproducibility.",
  keywords: [
    "quantum circuits",
    "measurement-induced phase transition",
    "MIPT",
    "Clifford circuits",
    "stabilizer formalism",
    "Gottesman-Knill",
    "purification",
    "entanglement transition",
    "finite-size scaling",
  ],
  icons: {
    icon: "https://z-cdn.chatglm.cn/z-ai/static/logo.svg",
  },
  openGraph: {
    title: "quantum·circuits — MIPT in random Clifford circuits",
    description:
      "p_c = 0.1597(8), ν = 1.24(7). Run the stabilizer simulator in your browser and explore the deposited data.",
    siteName: "quantum-circuits explorer",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-950 text-zinc-100`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
