"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

type RelatedNewsItem = {
  title: string;
  url: string;
  source?: string;
  published_at?: string;
};

function formatDate(input?: string) {
  try {
    const d = input ? new Date(input) : new Date();
    return d.toLocaleString();
  } catch {
    return new Date().toLocaleString();
  }
}

export default function HasilAnalisisPage() {
  const searchParams = useSearchParams();
  const [relatedNews, setRelatedNews] = useState<RelatedNewsItem[]>([]);
  const [sharing, setSharing] = useState(false);
  const [loadingPdf, setLoadingPdf] = useState(false);
  const [modelVersion, setModelVersion] = useState<string>('v1');

  const resultRaw = searchParams.get('result') || '';
  const isValid = ["valid", "true", "1"].includes(resultRaw.toLowerCase());

  const type = searchParams.get('type') || '';
  const filename = searchParams.get('filename') || '';
  const title = searchParams.get('title') || '';
  const snippet = searchParams.get('snippet') || '';
  const ts = searchParams.get('ts') || '';
  const analyzedAt = formatDate(ts);

  const contentLabel = type === "file" ? filename || "—" : title || "—";
  const typeLabel = type ? (type === "file" ? "File" : "Teks") : "—";

  // Fetch model version
  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/model/version`)
      .then(res => res.json())
      .then(data => setModelVersion(data.version))
      .catch(() => console.error('Failed to fetch model version'));
  }, []);

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
          confidence: isValid ? "95%" : "92%", // Tambahkan field confidence //Fetch Confidence
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

  const handleBagikan = async () => {
    setSharing(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      
      console.log('🔄 Sending data to:', `${apiUrl}/results`);
      
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
            model_version: modelVersion,
            extracted_text: null
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Backend error:', errorText);
        throw new Error(`Gagal menyimpan hasil (${response.status}): ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Backend response:', data);
      
      if (!data.id) {
        throw new Error("ID tidak ditemukan dalam response");
      }

      const baseUrl = typeof window !== 'undefined' 
        ? window.location.origin 
        : (process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000');
      
      const shareUrl = `${baseUrl}/hasil/${data.id}`;
      console.log('📤 Share URL:', shareUrl);

      if (navigator.share) {
        await navigator.share({
          title: banner.heading,
          text: `Hasil analisis berita: ${banner.heading}`,
          url: shareUrl
        });
      } else {
        await navigator.clipboard.writeText(shareUrl);
        alert(`Link tersalin: ${shareUrl}`);
      }
    } catch (error) {
      console.error("❌ Error saat membagikan:", error);
      alert(`❌ Gagal membuat link: ${error instanceof Error ? error.message : 'Unknown error'}\n\nCek console untuk detail.`);
    } finally {
      setSharing(false);
    }
  };

  return (
    <div className="container py-6">
      {/* Banner */}
      <div className={`card p-12 ${banner.bg} flex flex-col items-center text-center mb-6`}>
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
            <div className="text-slate-500">Model AI:</div>
            <div className="text-slate-800">
              <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs font-semibold">
                🧠 {modelVersion}
              </span>
            </div>
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
        <div className="text-sm font-semibold text-slate-700">
          Tindakan Selanjutnya
        </div>
        <div className="text-xs text-slate-500">
          Pilih apa yang ingin Anda lakukan dengan hasil ini
        </div>
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
            onClick={handleBagikan}
            disabled={sharing}
            className="btn-outline"
          >
            {sharing ? "Membuat Link..." : "Bagikan"}
          </button>

          <Link href="/" className="btn ml-auto">Cek Lagi</Link>
        </div>
      </div>
    </div>
  );
}

