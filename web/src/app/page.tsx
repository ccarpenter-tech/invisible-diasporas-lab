"use client";

import { useEffect, useMemo, useState } from "react";
import { supabase } from "@/lib/supabase";

type Article = {
  community?: string;
  destination_country?: string;
  sentiment?: string;
  date?: string;
  source?: string;
  domain?: string;
  url?: string;
  tone?: number | string;
  text_proxy?: string;
  title?: string;
};

export default function Home() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  const [community, setCommunity] = useState("All");
  const [country, setCountry] = useState("All");
  const [sentiment, setSentiment] = useState("All");

  useEffect(() => {
    async function loadArticles() {
      setLoading(true);

      const { data, error } = await supabase
        .from("articles")
        .select("*")
        .limit(2000);

      if (error) {
        console.error(error);
        alert("Erro ao carregar dados do Supabase. Veja o Console.");
      } else {
        setArticles(data || []);
      }

      setLoading(false);
    }

    loadArticles();
  }, []);

  const communities = useMemo(() => {
    return ["All", ...Array.from(new Set(articles.map((a) => a.community).filter(Boolean)))];
  }, [articles]);

  const countries = useMemo(() => {
    return ["All", ...Array.from(new Set(articles.map((a) => a.destination_country).filter(Boolean)))];
  }, [articles]);

  const sentiments = useMemo(() => {
    return ["All", ...Array.from(new Set(articles.map((a) => a.sentiment).filter(Boolean)))];
  }, [articles]);

  const filtered = useMemo(() => {
    return articles.filter((article) => {
      const matchCommunity = community === "All" || article.community === community;
      const matchCountry = country === "All" || article.destination_country === country;
      const matchSentiment = sentiment === "All" || article.sentiment === sentiment;

      return matchCommunity && matchCountry && matchSentiment;
    });
  }, [articles, community, country, sentiment]);

  const avgTone = useMemo(() => {
    const tones = filtered
      .map((a) => Number(a.tone))
      .filter((n) => !Number.isNaN(n));

    if (tones.length === 0) return null;

    return tones.reduce((sum, value) => sum + value, 0) / tones.length;
  }, [filtered]);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-10 rounded-3xl border border-white/10 bg-white/5 p-8">
          <p className="mb-3 text-sm uppercase tracking-[0.3em] text-cyan-300">
            Invisible Diasporas Lab
          </p>

          <h1 className="mb-4 text-4xl font-bold md:text-6xl">
            A diáspora asiática sob o olhar da mídia global
          </h1>

          <p className="max-w-3xl text-slate-300">
            Explore como comunidades asiáticas aparecem, desaparecem ou são enquadradas
            pela cobertura jornalística internacional.
          </p>
        </div>

        <section className="mb-8 grid gap-4 md:grid-cols-3">
          <FilterSelect
            label="Comunidade"
            value={community}
            options={communities as string[]}
            onChange={setCommunity}
          />

          <FilterSelect
            label="País de destino"
            value={country}
            options={countries as string[]}
            onChange={setCountry}
          />

          <FilterSelect
            label="Sentimento"
            value={sentiment}
            options={sentiments as string[]}
            onChange={setSentiment}
          />
        </section>

        {loading ? (
          <p>Carregando dados...</p>
        ) : (
          <>
            <section className="mb-8 grid gap-4 md:grid-cols-3">
              <MetricCard label="Notícias encontradas" value={filtered.length.toString()} />
              <MetricCard
                label="Tom médio"
                value={avgTone === null ? "—" : avgTone.toFixed(2)}
              />
              <MetricCard
                label="Total no banco"
                value={articles.length.toString()}
              />
            </section>

            <section className="grid gap-4">
              {filtered.slice(0, 20).map((article, index) => (
                <article
                  key={index}
                  className="rounded-2xl border border-white/10 bg-white/5 p-5"
                >
                  <div className="mb-2 flex flex-wrap gap-2 text-xs text-slate-300">
                    <span>{article.community || "Comunidade não informada"}</span>
                    <span>•</span>
                    <span>{article.destination_country || "Destino não informado"}</span>
                    <span>•</span>
                    <span>{article.sentiment || "Sentimento não informado"}</span>
                  </div>

                  <h2 className="mb-2 text-xl font-semibold">
                    {article.title || article.text_proxy?.slice(0, 120) || "Notícia sem título"}
                  </h2>

                  <p className="mb-3 text-sm text-slate-300">
                    Fonte: {article.source || article.domain || "não informada"} · Data:{" "}
                    {article.date || "não informada"} · Tom: {String(article.tone ?? "—")}
                  </p>

                  {article.url && (
                    <a
                      href={article.url}
                      target="_blank"
                      className="text-cyan-300 underline"
                    >
                      Abrir notícia
                    </a>
                  )}
                </article>
              ))}
            </section>
          </>
        )}
      </section>
    </main>
  );
}

function FilterSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm text-slate-300">{label}</span>
      <select
        className="w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-white"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  );
}