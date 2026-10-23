import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VidyaVaani • Synapse Voice AI Tutor",
  description: "A high-fidelity multilingual voice tutor engineered for educational equity. Strict textbook RAG, real-time regional neural speech, and zero hallucinations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>
        <div className="synapse-orb-top" />
        <div className="synapse-bloom" />
        {children}
      </body>
    </html>
  );
}
