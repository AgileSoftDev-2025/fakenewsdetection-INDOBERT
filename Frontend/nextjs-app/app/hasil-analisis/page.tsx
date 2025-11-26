"use client";
import Link from "next/link";
import { useState } from "react"; // Tambahkan useState

// ... (Helper formatDate tetap sama) ...
'use client'
import Link from "next/link";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

type RelatedNewsItem = {
  title: string;
  url: string;
  source?: string;
  published_at?: string;
};

// Hasil Analisis Page
// Cara pakai:
//   /hasil-analisis?result=valid&type=file&filename=NamaFile.pdf&ts=2025-09-09T19:43:49
//   /hasil-analisis?result=hoax&type=text&title=Judul%20Berita
// result: "valid" | "true" | "1" | "hoax" | "false" | "0"
// type:   "file" | "text" (opsional, hanya untuk detail tampilan)
// filename/title: info ringkas konten (opsional)
// ts: ISO datetime string (opsional), default now

function formatDate(input?: string) {
  try {
    const d = input ? new Date(input) : new Date();
    return d.toLocaleString();
  } catch {
    return new Date().toLocaleString();
  }
}

export default function HasilAnalisisPage({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  // --- STATE TAMBAHAN ---
  const [loadingPdf, setLoadingPdf] = useState(false);
export default function HasilAnalisisPage() {
  const searchParams = useSearchParams();
  const [relatedNews, setRelatedNews] = useState<RelatedNewsItem[]>([]);
  const [sharing, setSharing] = useState(false);
  // ---------------------

  const resultRaw = String(searchParams.result ?? "").toLowerCase();
  const isValid = ["valid", "true", "1"].includes(resultRaw);
  
  // Detail input
  const type = String(searchParams.type ?? "");
  const filename = String(searchParams.filename ?? "");
  const title = String(searchParams.title ?? "");
  const snippet = String(searchParams.snippet ?? "");
  const analyzedAt = formatDate(String(searchParams.ts ?? ""));
  const resultRaw = searchParams.get('result') || '';
  const isValid = ["valid", "true", "1"].includes(resultRaw.toLowerCase());
  const isHoax = ["hoax", "false", "0"].includes(resultRaw.toLowerCase());

  const type = searchParams.get('type') || '';
  const filename = searchParams.get('filename') || '';
  const title = searchParams.get('title') || '';
  const snippet = searchParams.get('snippet') || '';
  const ts = searchParams.get('ts') || '';
  const analyzedAt = formatDate(ts);

  const contentLabel = type === "file" ? filename || "—" : title || "—";
  const typeLabel = type ? (type === "file" ? "File" : "Teks") : "—";

  const handleDownloadPdf = async () => {
    setLoadingPdf(true);
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      
      const response = await fetch(`${baseUrl}/generate-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: title || "Tanpa Judul",
          content: snippet || contentLabel,
          prediction: isValid ? "VALID (Fakta)" : "HOAX (Palsu)",
          date: analyzedAt
        }),
      });

      if (!response.ok) throw new Error("Gagal generate PDF");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Laporan-Analisis-${Date.now()}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error) {
      console.error(error);
      alert("Gagal mengunduh PDF. Pastikan backend berjalan.");
    } finally {
      setLoadingPdf(false);
    }
  };
  // Fetch related news on component mount
  useEffect(() => {
    const searchQuery = `${title} ${snippet}`.trim();
    if (!searchQuery) return;

    async function fetchRelatedNews() {
      try {
        const params = new URLSearchParams({
          query: searchQuery,
          limit: "4",
        });

        const baseUrl =
          process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

        const resp = await fetch(
          `${baseUrl}/related-news?${params.toString()}`,
          { cache: "no-store" }
        );

        if (resp.ok) {
          const data = await resp.json();
          setRelatedNews(data);
        } else {
          console.error("Gagal fetch related-news:", await resp.text());
        }
      } catch (err) {
        console.error("Gagal mengambil related news:", err);
      }
    }

    fetchRelatedNews();
  }, [title, snippet]);

  const banner = isValid
    ? {
        bg: "bg-green-100/70",
        iconStroke: "stroke-green-700",
        heading: "Berita Valid",
        desc: "Berdasarkan analisis, berita ini kemungkinan besar valid dan dapat dipercaya.",
      }
    : {
        bg: "bg-red-100/70",
        iconStroke: "stroke-red-700",
        heading: "Kemungkinan Hoax",
        desc: "Berdasarkan analisis, berita ini kemungkinan besar tidak akurat atau menyesatkan.",
      };

  const handleBagikan = async () => {
    setSharing(true);
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/results`, {
      // Ambil API URL dari env variable
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      
      console.log('🔄 Sending data to:', `${apiUrl}/results`);
      
      // Kirim data ke backend untuk disimpan
      const response = await fetch(`${apiUrl}/results`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            title: title || null,
            text: snippet || contentLabel,
            prediction: isValid ? 0 : 1,
            prob_hoax: isValid ? 0.05 : 0.95,
            model_version: "indobert-base",
            extracted_text: null
        })
      });
      if (!res.ok) throw new Error("Gagal save result");
      const data = await res.json();
      // Gunakan ID dari backend untuk membuat link share
      const shareUrl = `${window.location.origin}/hasil/${data.id}`;
      
      if (navigator.share) {
        await navigator.share({ title: "Hasil Analisis", text: "Cek berita ini!", url: shareUrl });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Backend error:', errorText);
        throw new Error(`Gagal menyimpan hasil (${response.status}): ${errorText}`);
      }

      // Ambil ID dari response
      const data = await response.json();
      console.log('✅ Backend response:', data);
      
      if (!data.id) {
        throw new Error("ID tidak ditemukan dalam response");
      }

      // Generate share URL (dinamis berdasarkan environment)
      const baseUrl = typeof window !== 'undefined' 
        ? window.location.origin 
        : (process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000');
      
      const shareUrl = `${baseUrl}/hasil/${data.id}`;
      console.log('📤 Share URL:', shareUrl);

      // Share atau copy link
      if (navigator.share) {
        await navigator.share({
          title: banner.heading,
          text: `Hasil analisis berita: ${banner.heading}`,
          url: shareUrl
        });
        setShareSuccess(true);
      } else {
        await navigator.clipboard.writeText(shareUrl);
        alert(`Link tersalin: ${shareUrl}`);
      }
    } catch (e) {
      console.error(e);
      alert("Gagal membagikan hasil.");
      
    } catch (error) {
      console.error("❌ Error saat membagikan:", error);
      alert(`❌ Gagal membuat link: ${error instanceof Error ? error.message : 'Unknown error'}\n\nCek console untuk detail.`);
    } finally {
      setSharing(false);
    }
  };


  const banner = isValid
    ? {
        bg: "bg-green-100/70",
        iconStroke: "stroke-green-700",
        heading: "Berita Valid",
        desc: "Berdasarkan analisis, berita ini kemungkinan besar valid dan dapat dipercaya.",
      }
    : {
        bg: "bg-red-100/70",
        iconStroke: "stroke-red-700",
        heading: "Kemungkinan Hoax",
        desc: "Berdasarkan analisis, berita ini kemungkinan besar tidak akurat atau menyesatkan.",
      };

  return (
    <div className="container py-6">
      {/* Banner */}
      <div className={`card p-12 ${banner.bg} flex flex-col items-center text-center mb-6`}>
         {/* ... Icon Logic ... */}
         {isValid ? (
          <svg xmlns="http://www.w3.org/2000/svg" className={`h-16 w-16 ${banner.iconStroke}`} viewBox="0 0 24 24" fill="none" strokeWidth="1.5">
        {/* Icon */}
        {isValid ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className={`h-16 w-16 ${banner.iconStroke}`}
            viewBox="0 0 24 24"
            fill="none"
            strokeWidth="1.5"
          >
            <circle cx="12" cy="12" r="9" className={banner.iconStroke}></circle>
            <path
              d="M8 12l3 3 5-6"
              className={banner.iconStroke}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className={`h-16 w-16 ${banner.iconStroke}`}
            viewBox="0 0 24 24"
            fill="none"
            strokeWidth="1.5"
          >
            <circle cx="12" cy="12" r="9" className={banner.iconStroke}></circle>
            <path
              d="M9 9l6 6M15 9l-6 6"
              className={banner.iconStroke}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        )}
        <h2 className="mt-4 text-xl font-semibold text-slate-900">
          {banner.heading}
        </h2>
        <p className="mt-2 max-w-2xl text-sm text-slate-700">
          {banner.desc}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Detail Input */}
        <div className="card p-5">
           <div className="mb-2 flex items-center gap-2 text-slate-700">
            <span>⬆️</span>
            <div>
              <div className="text-sm font-semibold">Detail Input</div>
              <div className="text-xs text-slate-500">
                Analisis dilakukan pada dokumen yang diupload
              </div>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-y-3 text-sm">
            <div className="text-slate-500">Tipe Input:</div>
            <div className="text-slate-800">{typeLabel}</div>
            <div className="text-slate-500">Waktu Analisis:</div>
            <div className="text-slate-800">{analyzedAt}</div>
            <div className="text-slate-500">Konten:</div>
            <div className="text-slate-800 truncate">{contentLabel}</div>
            {snippet && (
              <>
                <div className="text-slate-500">Cuplikan:</div>
                <div className="text-slate-800">{snippet}</div>
              </>
            )}
          </div>
        </div>

        {/* Rekomendasi */}
        <div className="card p-5">
           <div className="mb-2 text-sm font-semibold text-slate-700">Rekomendasi</div>
          <div className="text-xs text-slate-500 mb-3">Beberapa referensi dari berita asli yang serupa</div>
          <ul className="list-disc list-inside text-sm text-slate-800 space-y-1">
            <li><a className="hover:underline" href="#">Berita 1 Link</a></li>
            <li><a className="hover:underline" href="#">Berita 2 Link</a></li>
            <li><a className="hover:underline" href="#">Berita 3 Link</a></li>
            <li><a className="hover:underline" href="#">Berita 4 Link</a></li>
          <div className="mb-2 text-sm font-semibold text-slate-700">
            Rekomendasi
          </div>
          <div className="text-xs text-slate-500 mb-3">
            Beberapa referensi dari berita asli yang serupa
          </div>
          <ul className="list-disc list-inside text-sm text-slate-800 space-y-1">
            {(!relatedNews || relatedNews.length === 0) && (
              <li className="text-xs text-slate-500">
                Belum ada rekomendasi berita. Coba cek manual di Google atau
                situs cek fakta.
              </li>
            )}

            {relatedNews.map((item) => (
              <li key={item.url}>
                <a
                  className="hover:underline"
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  {item.title}
                </a>
                {item.source && (
                  <span className="text-xs text-slate-500 ml-1">
                    ({item.source})
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Tindakan Selanjutnya */}
      <div className="card p-5 mt-6">
        <div className="text-sm font-semibold text-slate-700">Tindakan Selanjutnya</div>
        <div className="text-xs text-slate-500">Pilih apa yang ingin Anda lakukan dengan hasil ini</div>
        <div className="mt-4 flex flex-wrap gap-3 items-center">
          
          <button 
            type="button" 
            onClick={handleDownloadPdf} 
            disabled={loadingPdf}
            className="btn-outline flex items-center gap-2"
          >
            {loadingPdf ? "Menyiapkan..." : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
                Simpan PDF
              </>
            )}
          </button>

          <button 
            type="button" 
        <div className="text-sm font-semibold text-slate-700">
          Tindakan Selanjutnya
        </div>
        <div className="text-xs text-slate-500">
          Pilih apa yang ingin Anda lakukan dengan hasil ini
        </div>
        <div className="mt-4 flex flex-wrap gap-3 items-center">
          <button type="button" className="btn-outline">Simpan</button>

          <button 
            type="button" 
            className="btn-outline"
            onClick={handleBagikan}
            disabled={sharing}
            className="btn-outline"
          >
            {sharing ? "..." : "Bagikan"}
            {sharing ? "Membuat Link..." : "Bagikan"}
          </button>

          <Link href="/" className="btn ml-auto">Cek Lagi</Link>
        </div>
      </div>
    </div>
  );
}
}
