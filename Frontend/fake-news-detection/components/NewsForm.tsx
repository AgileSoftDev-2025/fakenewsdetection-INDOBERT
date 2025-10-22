"use client";
import React, { useState, FormEvent } from "react";
import { NewsFormProps } from "@/types";

const NewsForm: React.FC<NewsFormProps> = ({ onSubmit, loading }) => {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    if (file) formData.append("file", file);
    if (text) formData.append("text", text);
    onSubmit(formData);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white shadow-md rounded-2xl p-6 w-full max-w-lg"
    >
      <textarea
        placeholder="Salin dan tempel berita di sini..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full h-40 border border-gray-300 rounded-xl p-3 mb-4"
      ></textarea>

      <div className="flex items-center justify-between mb-4">
        <input
          type="file"
          accept=".txt,.pdf,.doc,.docx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white font-semibold py-3 rounded-xl hover:bg-blue-700 transition"
      >
        {loading ? "Menganalisis..." : "Analisis Berita"}
      </button>
    </form>
  );
};

export default NewsForm;