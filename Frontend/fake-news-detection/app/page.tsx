"use client";
import React, { useState } from "react";
import NewsForm from "@/components/NewsForm";
import { AnalysisResult } from "@/types";

export default function HomePage() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(formData: FormData) {
    setLoading(true);
    const res = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
    });

    const data: AnalysisResult = await res.json();
    setResult(data);
    setLoading(false);
  }

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Fake News Detection v2.0
      </h1>
      <p className="text-gray-600 mb-8 text-center">
        Masukkan teks atau unggah dokumen berita untuk memeriksa kebenarannya.
      </p>

      <NewsForm onSubmit={handleSubmit} loading={loading} />

      {result && (
        <div className="mt-8 w-full max-w-lg p-6 bg-white rounded-2xl shadow">
          <h2 className="text-xl font-semibold mb-3">Hasil Analisis</h2>
          <p className="text-gray-700">
            <strong>Status:</strong>{" "}
            <span
              className={`font-semibold ${
                result.result === "Hoax" ? "text-red-600" : "text-green-600"
              }`}
            >
              {result.result}
            </span>
          </p>
          <p>
            <strong>Confidence Score:</strong>{" "}
            {Math.round(result.confidence * 100)}%
          </p>
        </div>
      )}
    </main>
  );
}