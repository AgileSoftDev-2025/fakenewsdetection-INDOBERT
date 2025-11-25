'use client'
import useSWR from 'swr'

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function AdminPage() {
  const { data: ver } = useSWR(`${API}/model/version`, fetcher)

  return (
    <div>
      <h2>Admin</h2>
      <div>Model Version: <b>{ver?.version || '-'}</b></div>
      <p>Endpoint retrain belum diaktifkan di tahap ini.</p>
    </div>
  )
}
