'use client'
import useSWR from 'swr'

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function HistoryPage() {
  const { data, error, isLoading, mutate } = useSWR(`${API}/feedback?limit=100`, fetcher)
  return (
    <div>
      <h2>History Feedback</h2>
      {isLoading && <div>Memuat...</div>}
      {error && <div style={{ color: 'red' }}>Gagal memuat</div>}
      {Array.isArray(data) && (
        <table border={1} cellPadding={6}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Prediksi</th>
              <th>p1</th>
              <th>User Label</th>
              <th>Agreement</th>
              <th>Model</th>
            </tr>
          </thead>
          <tbody>
            {data.map((r: any) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.prediction === 1 ? 'Hoaks' : 'Bukan'}</td>
                <td>{Number(r.prob_hoax).toFixed(3)}</td>
                <td>{r.user_label === null || r.user_label === undefined || r.user_label === '' ? '-' : r.user_label}</td>
                <td>{r.agreement}</td>
                <td>{r.model_version}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
