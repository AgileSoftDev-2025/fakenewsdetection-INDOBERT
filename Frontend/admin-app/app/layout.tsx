import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FakeNewsDetector Admin - Dashboard",
  description: "Panel Administrasi untuk mengelola sistem deteksi hoax",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
