import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const formData = await req.formData();
  const text = formData.get("text") as string;

  // Contoh koneksi ke backend IndoBERT (FastAPI)
  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const result = await response.json();

  return NextResponse.json({
    result: result.label, // “Hoax” atau “Valid”
    confidence: result.confidence,
  });
}