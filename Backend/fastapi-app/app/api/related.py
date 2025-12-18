from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
import re
from collections import Counter

router = APIRouter()

# Berapa banyak kata kunci yang dipakai ke GNews
MAX_KEYWORDS = 7

# Stopword sederhana (bisa kamu tambah sendiri kalau mau)
ID_STOPWORDS = {
    "yang", "dan", "atau", "pada", "dengan", "untuk", "dari", "dalam",
    "itu", "ini", "tersebut", "akan", "telah", "sudah", "juga", "agar",
    "para", "karena", "namun", "tapi", "seperti", "adalah", "bahwa",
    "oleh", "kami", "kita", "mereka", "anda", "dia", "ia", "saat",
    "ketika", "jika", "jadi", "ke", "di", "sebagai", "lebih", "kurang",
    "masih", "bisa", "tidak", "tanpa", "setelah", "sebelum", "baru",
    "lagi", "hanya", "saja",
}


class RelatedNewsItem(BaseModel):
    title: str
    url: str
    source: Optional[str] = None
    published_at: Optional[str] = None


def normalize_query(raw: str) -> str:
    """
    Bersihkan query agar tidak error di GNews:
    - hilangkan tanda baca aneh
    - rapikan spasi
    - batasi jumlah kata
    """
    # Hapus semua karakter non huruf/angka/underscore/whitespace
    cleaned = re.sub(r"[^\w\s]", " ", raw, flags=re.UNICODE)
    # Rapikan spasi berlebih
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Batasi ke beberapa kata pertama biar fokus
    words = cleaned.split()
    cleaned = " ".join(words[:MAX_KEYWORDS])
    return cleaned


def extract_keywords_offline(text: str, max_keywords: int = MAX_KEYWORDS) -> str:
    """
    Ekstrak kata kunci secara offline (tanpa LLM):
    - lower case
    - buang tanda baca
    - buang stopword
    - pakai kata yang agak panjang dan sering muncul
    """
    # Lowercase
    text = text.lower()

    # Buang karakter non huruf/angka/whitespace
    text = re.sub(r"[^0-9a-zA-Z\u00C0-\u024f\u1e00-\u1eff\s]", " ", text)

    # Tokenisasi kasar
    tokens = re.findall(r"\w+", text, flags=re.UNICODE)

    # Filter stopword & kata terlalu pendek
    filtered = [
        t for t in tokens
        if len(t) > 3 and t not in ID_STOPWORDS
    ]

    if not filtered:
        return ""

    # Hitung frekuensi
    freq = Counter(filtered)

    # Urutkan: paling sering dulu, kalau seri pilih yang lebih panjang
    sorted_words = sorted(
        freq.items(),
        key=lambda x: (-x[1], -len(x[0]))
    )

    top_words = [w for (w, _) in sorted_words[:max_keywords]]
    return " ".join(top_words)


@router.get("/related-news", response_model=List[RelatedNewsItem])
async def get_related_news(query: str, limit: int = 4):
    """
    Ambil berita terkait dari API berita eksternal.
    - query: KONTEN berita (judul + snippet / isi dokumen)
    - limit: jumlah berita yang dikembalikan
    """
    raw_q = query.strip()
    if not raw_q:
        raise HTTPException(status_code=400, detail="query is required")

    # 1) Ekstrak keyword secara offline
    keywords = extract_keywords_offline(raw_q)

    if keywords:
        q = normalize_query(keywords)
    else:
        # Kalau gagal (teks terlalu pendek dll) fallback ke konten asli
        q = normalize_query(raw_q)

    if not q:
        raise HTTPException(status_code=400, detail="query is empty after processing")

    # API key & endpoint disimpan di environment (.env)
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

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(endpoint, params=params)

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
