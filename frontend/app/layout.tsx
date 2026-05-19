import type { Metadata } from "next";
import { IBM_Plex_Mono, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { ToastProvider } from "@/components/toast-provider";

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
});

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Product Launch Intelligence",
  description: "AI-powered product launch intelligence platform with real-time agent streaming.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${spaceGrotesk.variable} ${ibmPlexMono.variable} h-full dark`}>
      <body className="min-h-full flex flex-col antialiased">
        {children}
        <ToastProvider />
      </body>
    </html>
  );
}
