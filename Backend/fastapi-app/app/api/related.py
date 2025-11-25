from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
import re

router = APIRouter()

# Batas maksimal teks yang dikirim ke LLM (biar nggak kepanjangan)
MAX_TEXT_FOR_LLM = 1000


class RelatedNewsItem(BaseModel):
    title: str
    url: str
    source: Optional[str] = None
    published_at: Optional[str] = None


def normalize_query(raw: str) -> str:
    """
    Bersihkan query supaya cocok dengan aturan GNews:
    - hilangkan tanda baca aneh
    - rapikan spasi
    - batasi jumlah kata (misal 7 kata pertama)
    """
    # Hapus semua karakter non huruf/angka/underscore/whitespace
    cleaned = re.sub(r"[^\w\s]", " ", raw, flags=re.UNICODE)
    # Rapikan spasi berlebih
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Batasi ke beberapa kata pertama biar fokus
    words = cleaned.split()
    cleaned = " ".join(words[:7])
    return cleaned


async def extract_keywords_with_llm(text: str) -> str:
    """
    Gunakan LLM (OpenAI) untuk mengekstrak kata kunci dari konten berita.
    - Kalau OPENAI_API_KEY tidak ada atau terjadi error → balikin string kosong,
      nanti caller akan fallback ke normalize_query(text).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Kalau tidak ada API key, langsung fallback
    if not api_key:
        return ""

    # Batasi teks supaya nggak terlalu panjang
    text = text.strip()
    if len(text) > MAX_TEXT_FOR_LLM:
        text = text[:MAX_TEXT_FOR_LLM]

    prompt = (
        "Ekstrak 3–7 kata kunci penting dari teks berita berikut, "
        "tulis dalam SATU baris, hanya kata-kata dipisah spasi, "
        "tanpa koma, tanpa teks tambahan.\n\n"
        f"{text}"
    )

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, headers=headers, json=payload)

        if resp.status_code != 200:
            print("LLM error:", resp.status_code, resp.text)
            return ""

        data = resp.json()
        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        print("LLM keywords:", content)
        return content

    except Exception as e:
        print("LLM exception:", e)
        return ""


@router.get("/related-news", response_model=List[RelatedNewsItem])
async def get_related_news(query: str, limit: int = 4):
    """
    Ambil berita terkait dari API berita eksternal.
    - query: KONTEN berita (judul + snippet / isi singkat)
    - limit: jumlah berita yang dikembalikan
    """
    raw_q = query.strip()
    if not raw_q:
        raise HTTPException(status_code=400, detail="query is required")

    # 1) Coba pakai LLM untuk ekstrak keyword dari konten
    keywords = await extract_keywords_with_llm(raw_q)

    if keywords:
        q = normalize_query(keywords)
    else:
        # Kalau LLM tidak tersedia / gagal, fallback ke konten asli
        q = normalize_query(raw_q)

    if not q:
        raise HTTPException(status_code=400, detail="query is empty after processing")

    # 2) Panggil GNews dengan query yang sudah dibersihkan
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="NEWS_API_KEY is not set in environment",
        )

    endpoint = os.getenv("NEWS_API_ENDPOINT", "https://gnews.io/api/v4/search")

    params = {
        "q": q,
        "lang": "id",       # bahasa Indonesia
        "max": limit,
        "token": api_key,
        "sortby": "relevance",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(endpoint, params=params)
    except httpx.RequestError as e:  # termasuk ConnectTimeout, dll
        print("GNews request error:", repr(e))
        # Jangan lempar error ke user, cukup tidak ada rekomendasi
        return []

    if resp.status_code != 200:
        # JANGAN lempar ke user, cukup log dan balikin list kosong
        print("GNews error:", resp.status_code, resp.text)
        return []  # tidak ada rekomendasi

    data = resp.json()
    articles = data.get("articles", [])

    results: List[RelatedNewsItem] = []
    for a in articles:
        url = a.get("url")
        if not url:
            continue

        results.append(
            RelatedNewsItem(
                title=a.get("title") or "Tanpa judul",
                url=url,
                source=(a.get("source") or {}).get("name"),
                published_at=a.get("publishedAt"),
            )
        )

    return results[:limit]
