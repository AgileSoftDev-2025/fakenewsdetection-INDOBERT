import Link from "next/link";

export default async function HasilPublikPage({
  params,
}: {
  params: { id: string };
}) {
  // Fetch data dari backend
  let data;
  let error = false;

  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/results/${params.id}`,
      { 
        cache: 'no-store',
        headers: {
          'Content-Type': 'application/json',
        }
      }
    );
    
    if (!response.ok) {
      throw new Error('Data tidak ditemukan');
    }
    
    data = await response.json();
  } catch (err) {
    console.error('Error fetching result:', err);
    error = true;
  }

  // Jika error, tampilkan halaman error
  if (error || !data) {
    return (
      <div className="container py-6 min-h-screen flex items-center justify-center">
        <div className="card p-12 bg-red-100/70 text-center max-w-lg">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-xl font-semibold text-slate-900 mb-2">
            Hasil Tidak Ditemukan
          </h2>
          <p className="text-sm text-slate-700 mb-6">
            Link yang Anda akses tidak valid atau sudah kedaluwarsa.
          </p>
          <Link href="/" className="btn">
            Kembali ke Beranda
          </Link>
        </div>
      </div>
    );
  }

  // Parse data dari backend
  const isValid = data.prediction === 0;
  const analyzedAt = new Date(data.created_at || Date.now()).toLocaleString();

  // Mapping data dari backend ke format yang dipakai di UI
  const type = ""; // Gak ada info type dari backend
  const filename = "";
  const title = data.title || "";
  const snippet = data.text || data.extracted_text || "";
  const contentLabel = title || snippet || "—";
  const typeLabel = "—";

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
      {/* Banner - SAMA PERSIS */}
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

      {/* Content grid - SAMA PERSIS */}
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

      {/* Tindakan Selanjutnya - SAMA PERSIS (tanpa tombol Simpan & Bagikan) */}
      <div className="card p-5 mt-6">
        <div className="text-sm font-semibold text-slate-700">Tindakan Selanjutnya</div>
        
        <div className="mt-4 flex flex-wrap gap-3 items-center">
          <Link href="/" className="btn ml-auto">Cek Berita Baru</Link>
        </div>
      </div>
    </div>
  );
}
