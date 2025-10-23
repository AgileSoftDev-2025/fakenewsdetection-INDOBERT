'use client'
import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

type Result = { prediction: number; prob_hoax: number; model_version: string }

export default function HomePage() {
  const router = useRouter()
  const [tab, setTab] = useState<'text' | 'file'>('text')
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState<string | null>(null)

  const canAnalyze = useMemo(() => {
    if (tab === 'text') return body.trim().length >= 10 || title.trim().length >= 10
    return !!file
  }, [tab, title, body, file])

  const onDrop = (files: FileList | null) => {
    if (!files || files.length === 0) return
    setFile(files[0])
  }

  const submitText = async () => {
    const resp = await fetch(`${API}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, body, log_feedback: true })
    })
    if (!resp.ok) throw new Error(await resp.text())
    return resp.json() as Promise<Result>
  }

  const onAnalyze = async () => {
    setError(null)
    setResult(null)
    setLoading(true)
    try {
      if (tab === 'text') {
        const data = await submitText()
        setResult(data)
        // Redirect ke halaman hasil-analisis sesuai desain baru
        const resultParam = data.prediction === 1 ? 'hoax' : 'valid'
        const ts = new Date().toISOString()
        const snippet = (title || body).slice(0, 140)
        const q = new URLSearchParams({
          result: resultParam,
          type: 'text',
          title: title || body.slice(0, 60),
          snippet,
          ts,
        }).toString()
        router.push(`/hasil-analisis?${q}`)
      } else {
        if (!file) throw new Error('Pilih file gambar terlebih dahulu')
        const form = new FormData()
        form.append('file', file)
        form.append('log_feedback', 'true')
        const resp = await fetch(`${API}/predict-file`, {
          method: 'POST',
          body: form,
        })
        if (!resp.ok) throw new Error(await resp.text())
        const data: Result & { extracted_text?: string } = await resp.json()
        setResult(data)
        const resultParam = data.prediction === 1 ? 'hoax' : 'valid'
        const ts = new Date().toISOString()
        const snippet = (data.extracted_text || '').slice(0, 140)
        const q = new URLSearchParams({
          result: resultParam,
          type: 'file',
          filename: file.name,
          snippet,
          ts,
        }).toString()
        router.push(`/hasil-analisis?${q}`)
      }
    } catch (e: any) {
      setError(e.message || 'Gagal menganalisis')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="text-center mb-10">
        <h2 className="text-2xl font-semibold mb-2">Selamat Datang!</h2>
        <p className="text-slate-600">Verifikasi kebenaran berita dengan mudah. Masukkan teks, link, atau upload dokumen untuk dianalisis.</p>
      </div>

      <section className="card p-6">
        <div className="mb-4">
          <div className="text-sm font-semibold">Cek Berita</div>
          <p className="text-xs text-slate-500">Pilih salah satu metode untuk memverifikasi berita</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 bg-slate-100 p-1 rounded-lg w-full max-w-md">
          <button className={`tab ${tab==='text'?'tab-active':''}`} onClick={() => setTab('text')}>Teks</button>
          <button className={`tab ${tab==='file'?'tab-active':''}`} onClick={() => setTab('file')}>File</button>
        </div>

        {/* Content */}
        <div className="mt-4">
          {tab === 'text' ? (
            <div className="grid gap-3">
              <input className="input" placeholder="Judul (opsional)" value={title} onChange={e => setTitle(e.target.value)} />
              <textarea className="textarea" placeholder="Paste atau ketik berita yang ingin Anda verifikasi di sini..." value={body} onChange={e => setBody(e.target.value)} />
              <div className="text-xs text-slate-500">Minimal 10 karakter. Semakin lengkap teks, semakin akurat hasil analisis.</div>
            </div>
          ) : (
            <div className="grid gap-4">
              <div className="dropzone" onDragOver={e => e.preventDefault()} onDrop={e => { e.preventDefault(); onDrop(e.dataTransfer.files) }}>
                <div className="text-4xl">⬆️</div>
                <div>Drag & Drop File atau klik untuk memilih</div>
                <label className="btn-outline cursor-pointer">
                  <input type="file" accept="image/png,image/jpeg" className="hidden" onChange={e => onDrop(e.target.files)} />
                  Pilih File
                </label>
              </div>
              <div className="text-xs text-slate-500">Format yang didukung: PNG, JPG, PDF (Maksimal 10MB)</div>
              {file && <div className="text-sm">Dipilih: <span className="font-medium">{file.name}</span></div>}
            </div>
          )}
        </div>

        {/* Notice */}
        <div className="notice mt-6 flex items-start gap-3">
          <div className="mt-0.5">⚠️</div>
          <div>
            <div className="font-medium text-sm">Penting untuk Diketahui</div>
            <p className="text-sm">Hasil analisis adalah bantuan teknologi. Selalu verifikasi dengan sumber terpercaya dan gunakan pertimbangan kritis Anda.</p>
          </div>
        </div>

        <div className="mt-6">
          <button className="btn w-full max-w-xl" disabled={!canAnalyze || loading} onClick={onAnalyze}>
            {loading ? 'Memproses...' : 'Analisis Berita'}
          </button>
        </div>

        {error && <div className="mt-4 text-red-600 text-sm">{error}</div>}
        {result && (
          <div className="mt-6 rounded-lg border border-slate-200 p-4">
            <div>Hasil: <b>{result.prediction === 1 ? 'Hoaks' : 'Bukan Hoaks'}</b></div>
            <div>Prob Hoaks: {result.prob_hoax.toFixed(4)}</div>
            <div>Model Version: {result.model_version}</div>
          </div>
        )}
      </section>
    </div>
  )
}
