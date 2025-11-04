import React from 'react'
import './globals.css'
export const metadata = {
  title: 'FakeNews Detection',
  description: 'Deteksi hoaks dengan IndoBERT'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body>
        <div className="container py-6">
          <div className="card px-6 py-4 mb-8 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="h-10 w-10 rounded-full bg-slate-900 text-white grid place-items-center">FN</div>
              <div>
                <div className="font-semibold">FakeNewsDetector</div>
                <div className="text-xs text-slate-500">Dashboard Pengguna</div>
              </div>
              <span className="badge">v1.0</span>
            </div>
            <nav className="flex items-center gap-4 text-sm">
              <a href="/" className="hover:underline">Home</a>
              <a href="/history" className="hover:underline">History</a>
              <a href="/admin" className="hover:underline">Admin</a>
              <button className="btn-outline">Keluar</button>
            </nav>
          </div>

          {children}
        </div>
      </body>
    </html>
  );
}
