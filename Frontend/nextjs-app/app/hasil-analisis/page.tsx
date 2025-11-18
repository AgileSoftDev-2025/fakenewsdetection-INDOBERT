'use client';

import Link from "next/link";
import { useState } from "react";

export default function HasilAnalisisPage({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const [sharing, setSharing] = useState(false);
  const [shareSuccess, setShareSuccess] = useState(false);

  const resultRaw = String(searchParams.result ?? "").toLowerCase();
  const isValid = ["valid", "true", "1"].includes(resultRaw);

  const type = String(searchParams.type ?? "");
  const filename = String(searchParams.filename ?? "");
  const title = String(searchParams.title ?? "");
  const snippet = String(searchParams.snippet ?? "");
  const analyzedAt = new Date(searchParams.ts ? String(searchParams.ts) : Date.now()).toLocaleString("id-ID");

  const contentLabel = type === "file" ? filename || "—" : title || "—";
  const typeLabel = type ? (type === "file" ? "File" : "Teks") : "—";

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

  // Fungsi untuk membagikan hasil
  const handleBagikan = async () => {
    setSharing(true);
    setShareSuccess(false);
    
    try {
      // 1. Kirim data ke backend untuk disimpan
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/results`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: title || null,
          text: snippet || contentLabel,
          prediction: isValid ? 0 : 1,
          prob_hoax: isValid ? 0.05 : 0.95,
          model_version: "indobert-base",
          extracted_text: null
        })
      });

      if (!response.ok) {
        throw new Error("Gagal menyimpan hasil ke database");
      }

      // 2. Ambil ID dari response
      const data = await response.json();
      
      if (!data.id) {
        throw new Error("ID tidak ditemukan dalam response");
      }

      // 3. Buat URL publik
      const shareUrl = `${window.location.origin}/hasil/${data.id}`;

      // 4. Share atau copy link
      if (navigator.share) {
        // Jika browser support Web Share API (mobile)
        await navigator.share({
          title: banner.heading,
          text: `Hasil analisis berita: ${banner.heading}`,
          url: shareUrl
        });
        setShareSuccess(true);
      } else {
        // Fallback: copy ke clipboard
        await navigator.clipboard.writeText(shareUrl);
        alert(`✅ Link berhasil disalin!\n\nLink ini bisa dibagikan ke siapa saja:\n${shareUrl}`);
        setShareSuccess(true);
      }
      
    } catch (error) {
      console.error("Error saat membagikan:", error);
      alert("❌ Gagal membuat link. Silakan coba lagi.");
    } finally {
      setSharing(false);
    }
  };

  return (
    <div className="container py-6">
      {/* Banner */}
      <div className={`card p-12 ${banner.bg} flex flex-col items-center text-center mb-6`}>
        {isValid ? (
          <svg xmlns="http://www.w3.org/2000/svg" className={`h-16 w-16 ${banner.iconStroke}`} viewBox="0 0 24 24" fill="none" strokeWidth="1.5">
            <circle cx="12" cy="12" r="9" className={banner.iconStroke}></circle>
            <path d="M8 12l3 3 5-6" className={banner.iconStroke} strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" className={`h-16 w-16 ${banner.iconStroke}`} viewBox="0 0 24 24" fill="none" strokeWidth="1.5">
            <circle cx="12" cy="12" r="9" className={banner.iconStroke}></circle>
            <path d="M9 9l6 6M15 9l-6 6" className={banner.iconStroke} strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
        <h2 className="mt-4 text-xl font-semibold text-slate-900">{banner.heading}</h2>
        <p className="mt-2 max-w-2xl text-sm text-slate-700">{banner.desc}</p>
      </div>

      {/* Content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Detail Input */}
        <div className="card p-5">
          <div className="mb-2 flex items-center gap-2 text-slate-700">
            <span>⬆️</span>
            <div>
              <div className="text-sm font-semibold">Detail Input</div>
              <div className="text-xs text-slate-500">Analisis dilakukan pada dokumen yang diupload</div>
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
            <li><a className="hover:underline text-blue-600" href="https://turnbackhoax.id" target="_blank" rel="noopener">TurnBackHoax.id</a></li>
            <li><a className="hover:underline text-blue-600" href="https://cekfakta.com" target="_blank" rel="noopener">CekFakta.com</a></li>
            <li><a className="hover:underline text-blue-600" href="https://www.liputan6.com/cek-fakta" target="_blank" rel="noopener">Liputan6 Cek Fakta</a></li>
            <li><a className="hover:underline text-blue-600" href="https://www.kominfo.go.id" target="_blank" rel="noopener">Kominfo</a></li>
          </ul>
        </div>
      </div>

      {/* Tindakan Selanjutnya */}
      <div className="card p-5 mt-6">
        <div className="text-sm font-semibold text-slate-700">Tindakan Selanjutnya</div>
        <div className="text-xs text-slate-500">Pilih apa yang ingin Anda lakukan dengan hasil ini</div>
        
        {shareSuccess && (
          <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded text-sm text-green-800">
            ✅ Link berhasil dibuat! Anda bisa membagikannya ke siapa saja.
          </div>
        )}
        
        <div className="mt-4 flex flex-wrap gap-3 items-center">
          <button
            type="button"
            className="btn-outline"
            onClick={handleBagikan}
            disabled={sharing}
          >
            {sharing ? "Membuat Link..." : "🔗 Bagikan Hasil"}
          </button>

          <Link href="/" className="btn ml-auto">
            🔍 Cek Lagi
          </Link>
        </div>
      </div>
    </div>
  );
}

