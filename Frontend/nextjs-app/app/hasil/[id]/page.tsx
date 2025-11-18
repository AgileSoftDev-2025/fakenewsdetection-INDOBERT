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
  const analyzedAt = new Date(data.created_at || Date.now()).toLocaleString("id-ID", {
    dateStyle: 'long',
    timeStyle: 'short'
  });

  const banner = isValid
    ? {
        bg: "bg-green-100/70",
        iconStroke: "stroke-green-700",
        heading: "✅ Berita Valid",
        desc: "Berdasarkan analisis AI, berita ini kemungkinan besar valid dan dapat dipercaya.",
      }
    : {
        bg: "bg-red-100/70",
        iconStroke: "stroke-red-700",
        heading: "⚠️ Kemungkinan Hoax",
        desc: "Berdasarkan analisis AI, berita ini kemungkinan besar tidak akurat atau menyesatkan.",
      };

  return (
    <div className="container py-6">
      {/* Header Info */}
      <div className="mb-4 text-center">
        <p className="text-xs text-slate-500">Hasil Analisis Berita</p>
        <p className="text-sm text-slate-600">Dibagikan pada: {analyzedAt}</p>
      </div>

      {/* Banner Hasil */}
      <div className={`card p-12 ${banner.bg} flex flex-col items-center text-center mb-6`}>
        {isValid ? (
          <svg xmlns="http://www.w3.org/2000/svg" className={`h-20 w-20 ${banner.iconStroke}`} viewBox="0 0 24 24" fill="none" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M8 12l3 3 5-6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" className={`h-20 w-20 ${banner.iconStroke}`} viewBox="0 0 24 24" fill="none" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M9 9l6 6M15 9l-6 6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
        <h1 className="mt-4 text-2xl font-bold text-slate-900">{banner.heading}</h1>
        <p className="mt-2 max-w-2xl text-base text-slate-700">{banner.desc}</p>
      </div>

      {/* Detail Analisis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Info Detail */}
        <div className="card p-6">
          <div className="mb-4 flex items-center gap-3">
            <div className="text-3xl">📊</div>
            <div>
              <div className="text-base font-semibold text-slate-800">Detail Analisis</div>
              <div className="text-xs text-slate-500">Informasi hasil pengecekan</div>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="flex justify-between text-sm border-b border-slate-200 pb-2">
              <span className="text-slate-600">Status:</span>
              <span className={`font-semibold ${isValid ? 'text-green-700' : 'text-red-700'}`}>
                {isValid ? 'Valid' : 'Hoax'}
              </span>
            </div>
            
            <div className="flex justify-between text-sm border-b border-slate-200 pb-2">
              <span className="text-slate-600">Probabilitas Hoax:</span>
              <span className="font-semibold text-slate-800">
                {(data.prob_hoax * 100).toFixed(1)}%
              </span>
            </div>
            
            <div className="flex justify-between text-sm border-b border-slate-200 pb-2">
              <span className="text-slate-600">Model AI:</span>
              <span className="font-medium text-slate-800">{data.model_version || 'indobert-base'}</span>
            </div>
            
            <div className="flex justify-between text-sm">
              <span className="text-slate-600">Waktu Analisis:</span>
              <span className="font-medium text-slate-800">{analyzedAt}</span>
            </div>
          </div>
        </div>

        {/* Konten yang Dianalisis */}
        <div className="card p-6">
          <div className="mb-4 flex items-center gap-3">
            <div className="text-3xl">📝</div>
            <div>
              <div className="text-base font-semibold text-slate-800">Konten yang Dianalisis</div>
              <div className="text-xs text-slate-500">Teks yang diperiksa oleh AI</div>
            </div>
          </div>
          
          {data.title && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-slate-600 mb-1">Judul:</div>
              <div className="text-sm text-slate-800 font-medium">{data.title}</div>
            </div>
          )}
          
          <div>
            <div className="text-xs font-semibold text-slate-600 mb-1">Isi Berita:</div>
            <div className="text-sm text-slate-700 leading-relaxed max-h-40 overflow-y-auto p-3 bg-slate-50 rounded border border-slate-200">
              {data.text || data.extracted_text || 'Tidak ada teks yang tersedia'}
            </div>
          </div>
        </div>
      </div>

      {/* Rekomendasi Verifikasi */}
      <div className="card p-6 mb-6">
        <div className="mb-4 flex items-center gap-3">
          <div className="text-3xl">🔍</div>
          <div>
            <div className="text-base font-semibold text-slate-800">Verifikasi Lebih Lanjut</div>
            <div className="text-xs text-slate-500">Selalu cek dari berbagai sumber terpercaya</div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a 
            href="https://turnbackhoax.id" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-50 hover:bg-slate-100 rounded-lg border border-slate-200 transition-colors"
          >
            <span className="text-2xl">🛡️</span>
            <div>
              <div className="text-sm font-semibold text-slate-800">TurnBackHoax</div>
              <div className="text-xs text-slate-600">Cek fakta berita hoax</div>
            </div>
          </a>
          
          <a 
            href="https://cekfakta.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-50 hover:bg-slate-100 rounded-lg border border-slate-200 transition-colors"
          >
            <span className="text-2xl">✅</span>
            <div>
              <div className="text-sm font-semibold text-slate-800">CekFakta</div>
              <div className="text-xs text-slate-600">Verifikasi informasi</div>
            </div>
          </a>
          
          <a 
            href="https://www.liputan6.com/cek-fakta" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-50 hover:bg-slate-100 rounded-lg border border-slate-200 transition-colors"
          >
            <span className="text-2xl">📰</span>
            <div>
              <div className="text-sm font-semibold text-slate-800">Liputan6 Cek Fakta</div>
              <div className="text-xs text-slate-600">Media fact-checking</div>
            </div>
          </a>
          
          <a 
            href="https://www.kominfo.go.id/content/all/laporan_isu_hoaks" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-50 hover:bg-slate-100 rounded-lg border border-slate-200 transition-colors"
          >
            <span className="text-2xl">🏛️</span>
            <div>
              <div className="text-sm font-semibold text-slate-800">Kominfo</div>
              <div className="text-xs text-slate-600">Laporan hoaks resmi</div>
            </div>
          </a>
        </div>
      </div>

      {/* CTA */}
      <div className="card p-8 bg-gradient-to-r from-blue-50 to-indigo-50 text-center">
        <div className="text-4xl mb-3">🤖</div>
        <h3 className="text-lg font-bold text-slate-800 mb-2">Cek Berita Anda Sendiri</h3>
        <p className="text-sm text-slate-600 mb-5 max-w-md mx-auto">
          Gunakan teknologi AI untuk memverifikasi keaslian berita dan lindungi diri dari hoaks
        </p>
        <Link href="/" className="btn inline-block">
          🚀 Mulai Cek Berita Sekarang
        </Link>
      </div>

      {/* Footer Disclaimer */}
      <div className="mt-6 text-center text-xs text-slate-500 p-4 bg-slate-50 rounded-lg">
        <p>⚠️ Hasil analisis ini dibuat oleh AI dan bersifat prediktif.</p>
        <p className="mt-1">Selalu verifikasi informasi dari berbagai sumber terpercaya sebelum menyebarkan.</p>
      </div>
    </div>
  );
}