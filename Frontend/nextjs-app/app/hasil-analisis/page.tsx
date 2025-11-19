import Link from "next/link";

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
  const resultRaw = String(searchParams.result ?? "").toLowerCase();
  const isValid = ["valid", "true", "1"].includes(resultRaw);
  const isHoax = ["hoax", "false", "0"].includes(resultRaw);

  // Detail input (opsional)
  const type = String(searchParams.type ?? "");
  const filename = String(searchParams.filename ?? "");
  const title = String(searchParams.title ?? "");
  const snippet = String(searchParams.snippet ?? "");
  const analyzedAt = formatDate(String(searchParams.ts ?? ""));

  const contentLabel = type === "file" ? filename || "—" : title || "—";
  const typeLabel = type ? (type === "file" ? "File" : "Teks") : "—";

  const banner = isValid
    ? {
        // Hijau muda dengan sedikit transparansi
        bg: "bg-green-100/70",
        iconStroke: "stroke-green-700",
        heading: "Berita Valid",
        desc: "Berdasarkan analisis, berita ini kemungkinan besar valid dan dapat dipercaya.",
      }
    : {
        // Merah muda dengan sedikit transparansi
        bg: "bg-red-100/70",
        iconStroke: "stroke-red-700",
        heading: "Kemungkinan Hoax",
        desc: "Berdasarkan analisis, berita ini kemungkinan besar tidak akurat atau menyesatkan.",
      };

  return (
    <div className="container py-6">
      {/* Top bar dihilangkan sesuai permintaan (hanya gunakan tombol "Cek Lagi" di bawah) */}

      {/* Banner */}
      <div className={`card p-12 ${banner.bg} flex flex-col items-center text-center mb-6`}>
        {/* Icon */}
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
            <li><a className="hover:underline" href="#">Berita 1 Link</a></li>
            <li><a className="hover:underline" href="#">Berita 2 Link</a></li>
            <li><a className="hover:underline" href="#">Berita 3 Link</a></li>
            <li><a className="hover:underline" href="#">Berita 4 Link</a></li>
          </ul>
        </div>
      </div>

      {/* Tindakan Selanjutnya */}
      <div className="card p-5 mt-6">
        <div className="text-sm font-semibold text-slate-700">Tindakan Selanjutnya</div>
        <div className="text-xs text-slate-500">Pilih apa yang ingin Anda lakukan dengan hasil ini</div>
        <div className="mt-4 flex flex-wrap gap-3 items-center">
          {/* TODO: Tambahkan handler Simpan di sini. Misal: onClick={() => handleSimpan(data)} */}
          <button type="button" className="btn-outline">Simpan</button>

          {/* TODO: Tambahkan handler Bagikan di sini. Misal: onClick={() => handleBagikan(url)} */}
          <button type="button" className="btn-outline">Bagikan</button>

          <Link href="/" className="btn ml-auto">Cek Lagi</Link>
        </div>
      </div>
    </div>
  );
}
