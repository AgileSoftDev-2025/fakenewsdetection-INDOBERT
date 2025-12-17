'use client'
import { useEffect, useState } from 'react'
import useSWR from 'swr'

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
const fetcher = (url: string) => fetch(url).then(r => r.json())

interface RetrainProgress {
  is_running: boolean
  progress: number
  stage: string
  message: string
  started_at?: number
  estimated_completion?: number
  current_epoch: number
  total_epochs: number
  error?: string
}

export default function AdminPage() {
  const { data: ver } = useSWR(`${API}/model/version`, fetcher)
  const { data: progress, mutate } = useSWR<RetrainProgress>(
    `${API}/retrain/progress`,
    fetcher,
    { refreshInterval: 2000 } // Poll every 2 seconds
  )

  const [elapsedTime, setElapsedTime] = useState<string>('--:--:--')
  const [estimatedRemaining, setEstimatedRemaining] = useState<string>('--:--:--')

  useEffect(() => {
    if (!progress?.started_at) return

    const interval = setInterval(() => {
      const now = Date.now() / 1000
      const elapsed = progress.started_at ? now - progress.started_at : 0
      setElapsedTime(formatDuration(elapsed))

      if (progress.estimated_completion) {
        const remaining = Math.max(0, progress.estimated_completion - now)
        setEstimatedRemaining(formatDuration(remaining))
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [progress?.started_at, progress?.estimated_completion])

  const formatDuration = (seconds: number): string => {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = Math.floor(seconds % 60)
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  }

  const getStageColor = (stage: string): string => {
    switch (stage) {
      case 'idle': return 'bg-gray-500'
      case 'preparing': return 'bg-blue-500'
      case 'training': return 'bg-yellow-500'
      case 'evaluating': return 'bg-purple-500'
      case 'saving': return 'bg-indigo-500'
      case 'uploading': return 'bg-cyan-500'
      case 'completed': return 'bg-green-500'
      case 'failed': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getStageIcon = (stage: string): string => {
    switch (stage) {
      case 'idle': return '⏸️'
      case 'preparing': return '🔧'
      case 'training': return '🎓'
      case 'evaluating': return '📊'
      case 'saving': return '💾'
      case 'uploading': return '☁️'
      case 'completed': return '✅'
      case 'failed': return '❌'
      default: return '⏳'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>

        {/* Model Version Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Model Information</h2>
          <div className="flex items-center space-x-2">
            <span className="text-gray-600">Current Version:</span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full font-mono font-bold">
              {ver?.version || 'Loading...'}
            </span>
          </div>
        </div>

        {/* Retrain Progress Card */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 px-6 py-4">
            <h2 className="text-xl font-semibold text-white flex items-center">
              🤖 Auto-Retrain Status
            </h2>
          </div>

          <div className="p-6 space-y-4">
            {/* Status Badge */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className={`w-3 h-3 rounded-full ${progress?.is_running ? 'bg-green-500 animate-pulse' : 'bg-gray-300'}`}></span>
                <span className="text-lg font-medium">
                  {progress?.is_running ? 'Retrain Running' : 'Idle'}
                </span>
              </div>
              
              <div className="flex items-center space-x-2">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStageColor(progress?.stage || 'idle')} text-white`}>
                  {getStageIcon(progress?.stage || 'idle')} {progress?.stage?.toUpperCase() || 'IDLE'}
                </span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-gray-600">
                <span>Progress</span>
                <span className="font-mono font-bold">{progress?.progress || 0}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  className={`h-full transition-all duration-500 ${
                    progress?.error ? 'bg-red-500' : 'bg-gradient-to-r from-purple-500 to-blue-500'
                  }`}
                  style={{ width: `${progress?.progress || 0}%` }}
                >
                  <div className="h-full w-full bg-white/20 animate-pulse"></div>
                </div>
              </div>
            </div>

            {/* Current Message */}
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <div className="text-sm text-gray-600 mb-1">Current Activity:</div>
              <div className="text-gray-900 font-medium">
                {progress?.message || 'No retrain in progress'}
              </div>
            </div>

            {/* Epoch Progress */}
            {progress?.is_running && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Training Epoch:</span>
                <span className="font-mono font-bold">
                  {progress.current_epoch} / {progress.total_epochs}
                </span>
              </div>
            )}

            {/* Time Information */}
            {progress?.is_running && (
              <div className="grid grid-cols-2 gap-4 pt-2 border-t">
                <div>
                  <div className="text-sm text-gray-600">Time Elapsed</div>
                  <div className="text-lg font-mono font-bold text-blue-600">{elapsedTime}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Estimated Remaining</div>
                  <div className="text-lg font-mono font-bold text-purple-600">{estimatedRemaining}</div>
                </div>
              </div>
            )}

            {/* Error Display */}
            {progress?.error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-start space-x-2">
                  <span className="text-red-500 text-xl">⚠️</span>
                  <div>
                    <div className="text-sm font-medium text-red-800">Error Occurred:</div>
                    <div className="text-sm text-red-600 mt-1">{progress.error}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
