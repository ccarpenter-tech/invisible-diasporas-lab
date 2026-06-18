
import os
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from language import t, ui, value_label, language_selector

# ============================================================
# APP MERGEADO
# Base: app.py anexado + funcionalidades avançadas do texto colado.
# ============================================================

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Invisible Diasporas Lab",
    page_icon="🌏",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "diaspora_asian_media.sqlite"
EMB_PATH = DATA_DIR / "article_embeddings.npy"


# ============================================================
# CSS / VISUAL DE PRODUTO
# ============================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f2eb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1320px;
    }

    h1, h2, h3 {
        color: #25211d;
        letter-spacing: -0.02em;
    }

    .hero {
        background: linear-gradient(135deg, #211c19 0%, #5e4637 55%, #b7835a 100%);
        padding: 2.2rem 2rem;
        border-radius: 26px;
        color: white;
        margin-bottom: 1.4rem;
        box-shadow: 0 14px 35px rgba(0,0,0,0.14);
    }

    .hero h1 {
        color: white;
        font-size: 2.45rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #f7efe5;
        font-size: 1.05rem;
        max-width: 960px;
    }

    .product-tag {
        display: inline-block;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.24);
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.85rem;
        margin-bottom: 0.7rem;
    }

    .method-box {
        background: #fffaf3;
        border-left: 5px solid #b7835a;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #342c26;
    }

    .soft-box {
        background: white;
        border: 1px solid #eee3d8;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    }

    .finding-card {
        background: white;
        border: 1px solid #eee3d8;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    }

    .news-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        border: 1px solid #eee3d8;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }

    .risk-critical {
        background: #4b1f1f;
        color: white;
        padding: 0.9rem 1.1rem;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .risk-high {
        background: #9a4d2f;
        color: white;
        padding: 0.9rem 1.1rem;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .risk-medium {
        background: #d9a441;
        color: #2b2118;
        padding: 0.9rem 1.1rem;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .risk-low {
        background: #dfe9da;
        color: #24351f;
        padding: 0.9rem 1.1rem;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .small-caption {
        color: #6b6259;
        font-size: 0.9rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        flex-wrap: wrap;
    }

    .stTabs [data-baseweb="tab"] {
        background: #fffaf3;
        border-radius: 999px;
        padding: 0.45rem 1rem;
        border: 1px solid #eadccf;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SELETOR DE IDIOMA
# ============================================================

lang_left, lang_right = st.columns([5, 1])

with lang_right:
    language_selector()

# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data
def load_tables():
    conn = sqlite3.connect(DB_PATH)

    articles = pd.read_sql("SELECT * FROM articles", conn)
    migration_destination = pd.read_sql("SELECT * FROM migration_destination", conn)
    migration_origin = pd.read_sql("SELECT * FROM migration_origin", conn)

    conn.close()

    articles["date"] = pd.to_datetime(articles["date"], errors="coerce")
    articles["tone"] = pd.to_numeric(articles["tone"], errors="coerce")
    articles["year"] = pd.to_numeric(articles["year"], errors="coerce")

    return articles, migration_destination, migration_origin


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


@st.cache_data
def load_embeddings():
    return np.load(EMB_PATH).astype("float32")


articles, migration_destination, migration_origin = load_tables()


# ============================================================
# FUNÇÕES GERAIS
# ============================================================

def get_secret_value(name, default=None):
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)



def summarize_with_claude(rows, selected_community, selected_country):
    api_key = get_secret_value("ANTHROPIC_API_KEY")
    model_name = get_secret_value("ANTHROPIC_MODEL", "claude-haiku-4-5")

    if not api_key:
        return "Resumo por IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit."

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        context = "\n\n".join(
            [
                f"Comunidade: {r['community']}\n"
                f"Destino: {r['destination_country']}\n"
                f"Data: {r['date']}\n"
                f"Fonte: {r['source']}\n"
                f"Sentimento: {r['sentiment']}\n"
                f"Tom: {r['tone']}\n"
                f"URL: {r['url']}"
                for _, r in rows.head(10).iterrows()
            ]
        )

        language_name = t("ai_language")

        prompt = f"""
Você é uma analista de comunicação social.

Responda no seguinte idioma: {language_name}.

Analise a cobertura midiática sobre a comunidade {selected_community} em {selected_country}.
Explique:
- o tom geral da cobertura;
- os possíveis enquadramentos;
- sinais de visibilidade ou invisibilidade midiática;
- uma interpretação crítica final.

Não invente dados. Use apenas o contexto.

Notícias:
{context}
"""

        message = client.messages.create(
            model=model_name,
            max_tokens=450,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    except Exception as e:
        return f"Não foi possível gerar o resumo por IA. Erro: {e}"


def classify_frame(text):
    text = str(text).lower()

    frames = {
        "Trabalho e migração": [
            "worker", "labor", "labour", "employment", "domestic worker",
            "trabalhador", "trabalho", "emprego", "migrante", "migrant"
        ],
        "Racismo e discriminação": [
            "racism", "racist", "discrimination", "hate crime",
            "racismo", "discriminação", "xenophobia", "xenofobia"
        ],
        "Saúde e pandemia": [
            "covid", "pandemic", "virus", "health",
            "pandemia", "saúde", "coronavirus", "coronavírus"
        ],
        "Crime e segurança": [
            "crime", "criminal", "police", "security", "violence",
            "crime", "polícia", "segurança", "violência"
        ],
        "Economia e negócios": [
            "business", "trade", "economy", "investment", "market",
            "negócios", "economia", "comércio", "investimento", "mercado"
        ],
        "Cultura e identidade": [
            "culture", "identity", "festival", "heritage", "community",
            "cultura", "identidade", "festival", "comunidade", "herança"
        ],
        "Política internacional": [
            "diplomacy", "foreign policy", "government", "election",
            "política", "governo", "diplomacia", "eleição"
        ]
    }

    scores = {}
    for frame, keywords in frames.items():
        scores[frame] = sum(1 for kw in keywords if kw in text)

    best_frame = max(scores, key=scores.get)

    if scores[best_frame] == 0:
        return "Enquadramento geral"

    return best_frame


def add_frames(df):
    df = df.copy()
    if "frame" not in df.columns:
        df["frame"] = df["text_proxy"].fillna("").apply(classify_frame)
    return df


def build_pair_invisibility(filtered_all, migration_destination, migration_origin):
    coverage_pair = (
        filtered_all
        .groupby(["destination_country", "iso3", "community"])
        .size()
        .reset_index(name="coverage_count")
    )

    base_pairs = (
        migration_destination[["destination_country", "iso3"]]
        .assign(_key=1)
        .merge(migration_origin[["community"]].assign(_key=1), on="_key")
        .drop(columns="_key")
    )

    pair_inv = base_pairs.merge(
        coverage_pair,
        on=["destination_country", "iso3", "community"],
        how="left"
    )

    pair_inv["coverage_count"] = pair_inv["coverage_count"].fillna(0)

    pair_inv = pair_inv.merge(
        migration_destination[
            [
                "destination_country",
                "iso3",
                "destination_migrant_stock_2020",
                "migrant_share_population_2020"
            ]
        ],
        on=["destination_country", "iso3"],
        how="left"
    )

    pair_inv = pair_inv.merge(
        migration_origin[
            [
                "community",
                "origin_global_migrant_stock_2020"
            ]
        ],
        on="community",
        how="left"
    )

    pair_inv["demographic_proxy"] = np.sqrt(
        pair_inv["destination_migrant_stock_2020"] *
        pair_inv["origin_global_migrant_stock_2020"]
    )

    pair_inv["coverage_per_100k_proxy"] = (
        pair_inv["coverage_count"] /
        pair_inv["demographic_proxy"] *
        100000
    )

    pair_inv["invisibility_index_proxy"] = (
        np.log1p(pair_inv["demographic_proxy"]) /
        (np.log1p(pair_inv["coverage_count"]) + 1)
    )

    return pair_inv.sort_values("invisibility_index_proxy", ascending=False)


def build_country_invisibility(filtered_all, migration_destination):
    coverage_country = (
        filtered_all
        .groupby(["destination_country", "iso3"])
        .size()
        .reset_index(name="coverage_count")
    )

    country_inv = migration_destination.merge(
        coverage_country,
        on=["destination_country", "iso3"],
        how="left"
    )

    country_inv["coverage_count"] = country_inv["coverage_count"].fillna(0)

    country_inv["coverage_per_100k_destination_migrants"] = (
        country_inv["coverage_count"] /
        country_inv["destination_migrant_stock_2020"] *
        100000
    )

    country_inv["invisibility_index_country"] = (
        np.log1p(country_inv["destination_migrant_stock_2020"]) /
        (np.log1p(country_inv["coverage_count"]) + 1)
    )

    return country_inv.sort_values("invisibility_index_country", ascending=False)


def risk_label(value, all_values):
    q50 = all_values.quantile(0.50)
    q75 = all_values.quantile(0.75)
    q90 = all_values.quantile(0.90)

    if value >= q90:
        return "Invisibilidade crítica", "risk-critical"
    elif value >= q75:
        return "Alta invisibilidade", "risk-high"
    elif value >= q50:
        return "Invisibilidade moderada", "risk-medium"
    else:
        return "Baixa invisibilidade", "risk-low"


def tone_explanation(avg_tone):
    if pd.isna(avg_tone):
        return "Não há tom médio disponível para esta seleção."
    if avg_tone <= -2:
        return "A cobertura apresenta tom médio negativo."
    elif avg_tone >= 2:
        return "A cobertura apresenta tom médio positivo."
    else:
        return "A cobertura apresenta tom médio próximo de neutro."


def source_diversity_index(df):
    if df.empty or df["domain"].dropna().nunique() <= 1:
        return 0.0

    counts = df["domain"].fillna("Fonte desconhecida").value_counts()
    probabilities = counts / counts.sum()
    shannon = -(probabilities * np.log(probabilities)).sum()
    max_shannon = np.log(len(counts))

    if max_shannon == 0:
        return 0.0

    return float(shannon / max_shannon)


def detect_silence_periods(df):
    if df.empty:
        return pd.DataFrame(columns=["period_start", "period_end", "silent_months"])

    monthly = (
        df
        .groupby(pd.Grouper(key="date", freq="ME"))
        .size()
        .reset_index(name="count")
    )

    if monthly.empty:
        return pd.DataFrame(columns=["period_start", "period_end", "silent_months"])

    full_range = pd.date_range(
        start=monthly["date"].min(),
        end=monthly["date"].max(),
        freq="ME"
    )

    full = pd.DataFrame({"date": full_range})
    full = full.merge(monthly, on="date", how="left")
    full["count"] = full["count"].fillna(0)
    full["silent"] = full["count"] == 0

    periods = []
    start = None

    for _, row in full.iterrows():
        if row["silent"] and start is None:
            start = row["date"]
        elif not row["silent"] and start is not None:
            end = previous_date
            months = len(pd.date_range(start=start, end=end, freq="ME"))
            periods.append(
                {
                    "period_start": start.date(),
                    "period_end": end.date(),
                    "silent_months": months
                }
            )
            start = None
        previous_date = row["date"]

    if start is not None:
        end = full["date"].iloc[-1]
        months = len(pd.date_range(start=start, end=end, freq="ME"))
        periods.append(
            {
                "period_start": start.date(),
                "period_end": end.date(),
                "silent_months": months
            }
        )

    return pd.DataFrame(periods).sort_values("silent_months", ascending=False) if periods else pd.DataFrame(columns=["period_start", "period_end", "silent_months"])


def pandemic_phase(year):
    if year <= 2019:
        return "Pré-pandemia"
    elif year in [2020, 2021]:
        return "Pandemia"
    else:
        return "Pós-pandemia"


def narrative_risk_score(filtered, pair_row, global_pair_inv):
    if filtered.empty or pair_row is None:
        return 0, "Risco não calculável"

    invisibility_percentile = (
        (global_pair_inv["invisibility_index_proxy"] <= pair_row["invisibility_index_proxy"]).mean()
    )

    avg_tone = filtered["tone"].mean()
    tone_risk = 0
    if avg_tone <= -2:
        tone_risk = 1
    elif avg_tone < 0:
        tone_risk = 0.5

    sensitive_frames = ["Crime e segurança", "Racismo e discriminação", "Saúde e pandemia"]
    frame_risk = filtered["frame"].isin(sensitive_frames).mean()

    diversity = source_diversity_index(filtered)
    low_diversity_risk = 1 - diversity

    score = (
        invisibility_percentile * 40 +
        tone_risk * 25 +
        frame_risk * 20 +
        low_diversity_risk * 15
    )

    if score >= 75:
        label = "Risco narrativo crítico"
    elif score >= 55:
        label = "Risco narrativo alto"
    elif score >= 35:
        label = "Risco narrativo moderado"
    else:
        label = "Risco narrativo baixo"

    return round(score, 1), label


def normalize_metric(value, min_value, max_value):
    if pd.isna(value) or max_value == min_value:
        return 0.0
    return float((value - min_value) / (max_value - min_value))


def radar_metrics(filtered, pair_row, pair_inv_global):
    total_news = len(filtered)
    avg_tone = filtered["tone"].mean() if total_news else 0
    diversity = source_diversity_index(filtered)
    frame_diversity = filtered["frame"].nunique() / max(1, articles["frame"].nunique())

    max_news = max(1, articles.groupby(["community", "destination_country"]).size().max())

    coverage_score = min(total_news / max_news, 1)
    tone_score = normalize_metric(avg_tone, -5, 5)
    invisibility_score = 0

    if pair_row is not None:
        invisibility_score = normalize_metric(
            pair_row["invisibility_index_proxy"],
            pair_inv_global["invisibility_index_proxy"].min(),
            pair_inv_global["invisibility_index_proxy"].max()
        )

    temporal_presence = filtered["date"].dt.to_period("M").nunique() / max(
        1,
        articles["date"].dt.to_period("M").nunique()
    )

    return pd.DataFrame(
        {
            "dimensão": [
                "Volume",
                "Tom positivo",
                "Invisibilidade",
                "Diversidade de fontes",
                "Diversidade de enquadramentos",
                "Presença temporal"
            ],
            "valor": [
                coverage_score,
                tone_score,
                invisibility_score,
                diversity,
                frame_diversity,
                temporal_presence
            ]
        }
    )


def generate_insights(filtered, pair_row, selected_community, selected_country, pair_inv_global):
    insights = []

    if filtered.empty:
        return ["Não há notícias disponíveis para gerar insights com os filtros atuais."]

    avg_tone = filtered["tone"].mean()
    total_news = len(filtered)
    top_frame = filtered["frame"].value_counts().idxmax() if not filtered.empty else "não identificado"
    diversity = source_diversity_index(filtered)

    insights.append(
        f"A seleção contém {total_news} notícias sobre {selected_community} em {selected_country}."
    )

    insights.append(tone_explanation(avg_tone))

    if top_frame:
        insights.append(f"O enquadramento predominante identificado é: {top_frame}.")

    if pair_row is not None:
        label, _ = risk_label(pair_row["invisibility_index_proxy"], pair_inv_global["invisibility_index_proxy"])
        insights.append(f"O diagnóstico de invisibilidade é: {label}.")

    if diversity < 0.35:
        insights.append("A diversidade de fontes é baixa: poucas fontes concentram a cobertura.")
    elif diversity > 0.70:
        insights.append("A cobertura apresenta alta diversidade de fontes jornalísticas.")

    years = sorted(filtered["year"].dropna().unique().tolist())
    if len(years) > 1:
        insights.append(f"A cobertura aparece distribuída entre {int(min(years))} e {int(max(years))}.")

    return insights


def story_mode_text(selected_community, selected_country, filtered, pair_row, risk_text):
    if filtered.empty:
        return f"Não há cobertura suficiente para construir uma narrativa sobre {selected_community} em {selected_country}."

    avg_tone = filtered["tone"].mean()
    dominant_frame = filtered["frame"].value_counts().idxmax()
    total_news = len(filtered)

    if pair_row is not None:
        invisibility = pair_row["invisibility_index_proxy"]
    else:
        invisibility = None

    story = (
        f"A comunidade {selected_community} em {selected_country} aparece no corpus por meio de "
        f"{total_news} notícias filtradas. O enquadramento predominante é '{dominant_frame}', "
        f"o que sugere que a cobertura tende a organizar essa comunidade principalmente a partir desse tema. "
        f"O tom médio da cobertura é {avg_tone:.2f}, portanto {tone_explanation(avg_tone).lower()} "
    )

    if invisibility is not None:
        story += (
            f"O índice proxy de invisibilidade é {invisibility:.2f}, classificado como {risk_text.lower()}. "
            f"Isso indica que a visibilidade midiática deve ser interpretada em relação ao peso demográfico "
            f"e não apenas ao número absoluto de notícias. "
        )

    story += (
        "Em termos comunicacionais, o resultado ajuda a observar se a mídia trata a diáspora como sujeito social complexo "
        "ou se ela aparece apenas em contextos específicos, como trabalho, crise, segurança, economia ou cultura."
    )

    return story


def build_report(selected_community, selected_country, selected_sentiment, filtered, pair_row, insights, narrative_score, narrative_label, story):
    total_news = len(filtered)
    avg_tone = filtered["tone"].mean() if total_news else np.nan
    dominant_frame = filtered["frame"].value_counts().idxmax() if total_news and "frame" in filtered.columns else "não identificado"
    diversity = source_diversity_index(filtered)

    if pair_row is not None:
        invisibility = f"{pair_row['invisibility_index_proxy']:.2f}"
        coverage = int(pair_row["coverage_count"])
        demographic_proxy = f"{pair_row['demographic_proxy']:,.0f}".replace(",", ".")
    else:
        invisibility = "não disponível"
        coverage = total_news
        demographic_proxy = "não disponível"

    avg_tone_text = f"{avg_tone:.2f}" if not pd.isna(avg_tone) else "não disponível"

    report = f"""
# Executive Briefing — Invisible Diasporas Lab

## Seleção
Comunidade: {selected_community}
País de destino: {selected_country}
Sentimento filtrado: {selected_sentiment}

## Principais métricas
Notícias encontradas: {total_news}
Cobertura usada no índice: {coverage}
Tom médio: {avg_tone_text}
Enquadramento predominante: {dominant_frame}
Diversidade de fontes: {diversity:.2f}
Proxy demográfico: {demographic_proxy}
Índice de invisibilidade: {invisibility}
Narrative Risk Score: {narrative_score}/100
Classificação do risco narrativo: {narrative_label}

## 3 principais achados
""" + "\n".join([f"- {i}" for i in insights[:3]]) + f"""

## Story Mode
{story}

## Recomendação de pesquisa
Investigar qualitativamente as notícias mais relevantes para entender se a comunidade é representada como sujeito social,
como força de trabalho, como problema público, como ator econômico ou como presença cultural.

## Observação metodológica
O índice comunidade × destino é um proxy comparativo.
Ele combina o tamanho global da diáspora de origem com o peso migratório do país de destino.
Ele não representa uma contagem bilateral exata de migrantes por origem e destino.
"""

    return report


def render_news_cards(df, max_items=6):
    examples = df.sort_values("date", ascending=False).head(max_items)

    for _, row in examples.iterrows():
        st.markdown(
            f"""
            <div class="news-card">
            <b>{row['community']} · {row['destination_country']} · {value_label(row['sentiment'])}</b><br>
            {ui("Data")}: {row['date'].date()} · {ui("Fonte")}: {row['source']} · {ui("Tom")}: {row['tone']}<br>
            {ui("Enquadramento")}: {value_label(row.get('frame', 'não identificado'))}<br>
            <a href="{row['url']}" target="_blank">{ui("Abrir notícia")}</a>
            </div>
            """,
            unsafe_allow_html=True
        )


def recommend_readings(filtered, all_articles, selected_community, selected_country):
    recommendations = {}

    if filtered.empty:
        return recommendations

    avg_tone = filtered["tone"].mean()

    if avg_tone < 0:
        opposite = all_articles[
            (all_articles["community"] == selected_community) &
            (all_articles["tone"] > 0)
        ].head(5)
        recommendations["Leia também: notícias com tom mais positivo"] = opposite
    else:
        opposite = all_articles[
            (all_articles["community"] == selected_community) &
            (all_articles["tone"] < 0)
        ].head(5)
        recommendations["Leia também: notícias com tom mais negativo"] = opposite

    same_community_other_country = all_articles[
        (all_articles["community"] == selected_community) &
        (all_articles["destination_country"] != selected_country)
    ].head(5)

    recommendations["Mesma comunidade em outros países"] = same_community_other_country

    same_country_other_community = all_articles[
        (all_articles["community"] != selected_community) &
        (all_articles["destination_country"] == selected_country)
    ].head(5)

    recommendations["Outras comunidades no mesmo país"] = same_country_other_community

    return recommendations


def claude_story(rows, selected_community, selected_country, story):
    api_key = get_secret_value("ANTHROPIC_API_KEY")
    model_name = get_secret_value("ANTHROPIC_MODEL", "claude-haiku-4-5")

    if not api_key:
        return "Story Mode com IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit."

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        context = "\n\n".join(
            [
                f"Data: {r['date']}\nFonte: {r['source']}\nSentimento: {r['sentiment']}\nTom: {r['tone']}\nURL: {r['url']}"
                for _, r in rows.head(10).iterrows()
            ]
        )

        language_name = t("ai_language")

        prompt = f"""
Transforme a análise abaixo em uma narrativa crítica curta, com tom acadêmico acessível.

Responda no seguinte idioma: {language_name}.

Análise inicial:
{story}

Notícias:
{context}
"""

        message = client.messages.create(
            model=model_name,
            max_tokens=450,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    except Exception as e:
        return f"Não foi possível gerar a narrativa por IA. Erro: {e}"


# ============================================================
# DADOS PRONTOS
# ============================================================

articles = add_frames(articles)
pair_inv_global = build_pair_invisibility(articles, migration_destination, migration_origin)
country_inv_global = build_country_invisibility(articles, migration_destination)


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="product-tag">{t("page_badge")}</div>
        <h1>{t("hero_title")}</h1>
        <p>{t("hero_text")}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="method-box">
    <b>{t("how_to_use_title")}:</b> {t("how_to_use_text")}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(t("sidebar_config"))

presentation_mode = st.sidebar.toggle(t("presentation_mode"), value=False)

analysis_mode = st.sidebar.radio(
    t("usage_mode"),
    [
        t("full_exploration"),
        t("classroom"),
        t("researcher"),
        t("executive_briefing")
    ],
    index=0
)

st.sidebar.header(t("main_filters"))

communities = sorted(articles["community"].dropna().unique().tolist())
countries = sorted(articles["destination_country"].dropna().unique().tolist())
sentiments = sorted(articles["sentiment"].dropna().unique().tolist())

selected_community = st.sidebar.selectbox(ui("Comunidade asiática"), communities)
selected_country = st.sidebar.selectbox(ui("País de destino"), countries)

sentiment_display = [value_label(s) for s in sentiments]
selected_sentiment_display = st.sidebar.selectbox(ui("Sentimento"), sentiment_display)
selected_sentiment = sentiments[sentiment_display.index(selected_sentiment_display)]

min_date = articles["date"].min().date()
max_date = articles["date"].max().date()

date_range = st.sidebar.date_input(
    t("period_filter"),
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date

)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date


filtered = articles.copy()

filtered = filtered[
    (filtered["date"].dt.date >= start_date) &
    (filtered["date"].dt.date <= end_date)
]

filtered = filtered[filtered["community"] == selected_community]
filtered = filtered[filtered["destination_country"] == selected_country]
filtered = filtered[filtered["sentiment"] == selected_sentiment]

pair_selected = pair_inv_global[
    (pair_inv_global["community"] == selected_community) &
    (pair_inv_global["destination_country"] == selected_country)
]

pair_row = pair_selected.iloc[0] if not pair_selected.empty else None

risk_text = "Risco não disponível"
risk_css = "risk-low"

if pair_row is not None:
    risk_text, risk_css = risk_label(
        pair_row["invisibility_index_proxy"],
        pair_inv_global["invisibility_index_proxy"]
    )

narrative_score, narrative_label = narrative_risk_score(
    filtered,
    pair_row,
    pair_inv_global
)

insights = generate_insights(
    filtered,
    pair_row,
    selected_community,
    selected_country,
    pair_inv_global
)

story = story_mode_text(
    selected_community,
    selected_country,
    filtered,
    pair_row,
    risk_text
)

# ============================================================
# CAMADA SOCIAL COLABORATIVA — SUPABASE

if "history" not in st.session_state:
    st.session_state["history"] = []

if st.sidebar.button(ui("Salvar seleção no histórico")):
    st.session_state["history"].append(
        {
            "community": selected_community,
            "country": selected_country,
            "sentiment": selected_sentiment,
            "start": str(start_date),
            "end": str(end_date)
        }
    )


# ============================================================
# MODO APRESENTAÇÃO
# ============================================================

if presentation_mode:
    st.subheader("🎤 Modo apresentação")

    col1, col2, col3, col4 = st.columns(4)

    total_news = len(filtered)
    avg_tone = filtered["tone"].mean() if total_news else np.nan

    col1.metric("Notícias", f"{total_news:,}".replace(",", "."))
    col2.metric("Tom médio", f"{avg_tone:.2f}" if total_news else "—")
    col3.metric("Invisibilidade", risk_text)
    col4.metric("Narrative Risk", f"{narrative_score}/100")

    st.markdown(
        f"""
        <div class="{risk_css}">
        Diagnóstico: {risk_text} · {narrative_label}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Principais achados")
    for insight in insights[:4]:
        st.write("• " + insight)

    st.markdown("### Story Mode")
    st.write(story)

    st.markdown(f"### {ui('Notícias de exemplo')}")
    render_news_cards(filtered, max_items=3)

    st.stop()


# ============================================================
# ABAS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    [
        t("tab_profile"),
        t("tab_map"),
        t("tab_radar"),
        t("tab_time"),
        t("tab_sources"),
        t("tab_explorer"),
        t("tab_comparisons"),
        t("tab_reports"),
        t("tab_about"),
    ]
)


# ============================================================
# TAB 1 — PERFIL 360
# ============================================================

with tab1:
    st.subheader(t("profile_title"))

    total_news = len(filtered)
    avg_tone = filtered["tone"].mean() if total_news else np.nan
    dominant_frame = filtered["frame"].value_counts().idxmax() if total_news else "—"
    diversity = source_diversity_index(filtered)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(t("news_count"), f"{total_news:,}".replace(",", "."))
    col2.metric(t("avg_tone"), f"{avg_tone:.2f}" if total_news else "—")
    col3.metric(t("dominant_frame"), dominant_frame)
    col4.metric(t("source_diversity"), f"{diversity:.2f}")

    st.markdown(
        f"""
        <div class="method-box">
        <b>{t("avg_tone")}:</b> {t("tone_help")}
        </div>
        """,
        unsafe_allow_html=True
    )

    if not filtered.empty:
        c1, c2 = st.columns([1, 1])

        with c1:
            sentiment_count = (
                filtered
                .groupby("sentiment")
                .size()
                .reset_index(name="count")
            )

            fig_sentiment = px.pie(
                sentiment_count,
                names="sentiment",
                values="count",
                title="Distribuição do sentimento",
                hole=0.45
            )

            st.plotly_chart(fig_sentiment, use_container_width=True)

        with c2:
            frame_count = (
                filtered
                .groupby("frame")
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=False)
            )

            fig_frame = px.bar(
                frame_count,
                x="count",
                y="frame",
                orientation="h",
                title="Enquadramentos predominantes"
            )

            st.plotly_chart(fig_frame, use_container_width=True)

        st.markdown(f"### {t('findings_cards')}")

        finding_1 = f"A cobertura filtrada reúne {total_news} notícias sobre {selected_community} em {selected_country}."
        finding_2 = f"O enquadramento predominante é '{dominant_frame}'."
        finding_3 = tone_explanation(avg_tone)

        f1, f2, f3 = st.columns(3)

        with f1:
            st.markdown(f"<div class='finding-card'><b>Achado 1</b><br>{finding_1}</div>", unsafe_allow_html=True)

        with f2:
            st.markdown(f"<div class='finding-card'><b>Achado 2</b><br>{finding_2}</div>", unsafe_allow_html=True)

        with f3:
            st.markdown(f"<div class='finding-card'><b>Achado 3</b><br>{finding_3}</div>", unsafe_allow_html=True)

        st.markdown(f"### {t('example_news')}")
        render_news_cards(filtered, max_items=5)

        csv = filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
            t("download_csv"),
            data=csv,
            file_name="selecao_diaspora.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhuma notícia encontrada com esses filtros.")


# ============================================================
# TAB 2 — MAPA CRÍTICO
# ============================================================

with tab2:
    st.subheader("Mapa crítico de invisibilidade")

    st.markdown(
        """
        <div class="method-box">
        O mapa mostra hotspots de invisibilidade por país de destino.
        Países mais escuros indicam maior invisibilidade relativa.
        </div>
        """,
        unsafe_allow_html=True
    )

    community_articles = articles[articles["community"] == selected_community]

    country_inv_for_map = build_country_invisibility(
        community_articles,
        migration_destination
    )

    if not country_inv_for_map.empty:
        fig_map = px.choropleth(
            country_inv_for_map,
            locations="iso3",
            color="invisibility_index_country",
            hover_name="destination_country",
            hover_data={
                "coverage_count": True,
                "destination_migrant_stock_2020": ":,.0f",
                "coverage_per_100k_destination_migrants": ":.2f",
                "iso3": False
            },
            color_continuous_scale="OrRd",
            title=f"Hotspots de invisibilidade — {selected_community}"
        )

        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("### Top 5 hotspots críticos")

        top_hotspots = country_inv_for_map.head(5)[
            [
                "destination_country",
                "coverage_count",
                "destination_migrant_stock_2020",
                "coverage_per_100k_destination_migrants",
                "invisibility_index_country"
            ]
        ]

        st.dataframe(top_hotspots, use_container_width=True, hide_index=True)
    else:
        st.info("Não há dados suficientes para o mapa crítico.")


# ============================================================
# TAB 3 — RADAR E NARRATIVE RISK
# ============================================================

with tab3:
    st.subheader("Radar da cobertura e Narrative Risk Score")

    if pair_row is not None:
        label, css_class = risk_label(
            pair_row["invisibility_index_proxy"],
            pair_inv_global["invisibility_index_proxy"]
        )

        st.markdown(
            f"""
            <div class="{css_class}">
            Status de invisibilidade: {label}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="{risk_css}">
        Narrative Risk Score: {narrative_score}/100 · {narrative_label}
        </div>
        """,
        unsafe_allow_html=True
    )

    radar_df = radar_metrics(filtered, pair_row, pair_inv_global)

    fig_radar = px.line_polar(
        radar_df,
        r="valor",
        theta="dimensão",
        line_close=True,
        range_r=[0, 1],
        title="Radar da cobertura"
    )

    fig_radar.update_traces(fill="toself")

    st.plotly_chart(fig_radar, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    if pair_row is not None:
        col1.metric("Cobertura encontrada", int(pair_row["coverage_count"]))
        col2.metric("Índice de invisibilidade", f"{pair_row['invisibility_index_proxy']:.2f}")
        col3.metric("Proxy demográfico", f"{pair_row['demographic_proxy']:,.0f}".replace(",", "."))

    st.markdown("### Explique este resultado")

    with st.expander("Por que o índice pode ser alto?"):
        st.write(
            "O índice aumenta quando há uma combinação de presença demográfica relevante e pouca cobertura midiática encontrada no corpus."
        )

    with st.expander("Por que o risco narrativo pode ser alto?"):
        st.write(
            "O Narrative Risk Score combina invisibilidade, tom negativo, enquadramentos sensíveis e baixa diversidade de fontes."
        )

    with st.expander("Esse número é uma verdade absoluta?"):
        st.write(
            "Não. Ele é um indicador comparativo. Serve para orientar análise crítica, não para substituir leitura qualitativa das notícias."
        )


# ============================================================
# TAB 4 — TEMPO, PANDEMIA E SILÊNCIO
# ============================================================

with tab4:
    st.subheader("Linha do tempo, pandemia e silêncio midiático")

    if not filtered.empty:
        monthly = (
            filtered
            .groupby(pd.Grouper(key="date", freq="ME"))
            .size()
            .reset_index(name="news_count")
        )

        fig_volume = px.line(
            monthly,
            x="date",
            y="news_count",
            markers=True,
            title=f"Volume mensal — {selected_community} em {selected_country}"
        )

        st.plotly_chart(fig_volume, use_container_width=True)

        timeline_events = pd.DataFrame(
            {
                "ano": [2019, 2020, 2021, 2022, 2023],
                "evento": [
                    "Pré-pandemia",
                    "Pandemia de Covid-19",
                    "Debates sobre racismo anti-asiático",
                    "Reabertura e reorganização migratória",
                    "Normalização pós-pandemia"
                ]
            }
        )

        st.markdown("### Eventos-chave para leitura da cobertura")
        st.dataframe(timeline_events, use_container_width=True, hide_index=True)

        phase_df = filtered.copy()
        phase_df["fase"] = phase_df["year"].apply(lambda x: pandemic_phase(int(x)))

        phase_summary = (
            phase_df
            .groupby("fase")
            .agg(
                noticias=("url", "count"),
                tom_medio=("tone", "mean"),
                enquadramentos=("frame", "nunique")
            )
            .reset_index()
        )

        st.markdown("### Antes, durante e depois da pandemia")
        st.dataframe(phase_summary, use_container_width=True, hide_index=True)

        fig_phase = px.bar(
            phase_summary,
            x="fase",
            y="noticias",
            title="Cobertura por fase histórica",
            text_auto=True
        )

        st.plotly_chart(fig_phase, use_container_width=True)

        st.markdown("### Silence Detector")

        silence_df = detect_silence_periods(filtered)

        if silence_df.empty:
            st.success("Não foram detectados longos períodos de silêncio dentro do intervalo filtrado.")
        else:
            st.warning("Foram encontrados períodos sem cobertura no intervalo analisado.")
            st.dataframe(silence_df.head(10), use_container_width=True, hide_index=True)

    else:
        st.info("Nenhum dado disponível para a seleção.")


# ============================================================
# TAB 5 — FONTES, DIVERSIDADE E BASELINE
# ============================================================

with tab5:
    st.subheader("Fontes jornalísticas, diversidade e baseline")

    if not filtered.empty:
        source_df = (
            filtered
            .groupby(["source", "domain"])
            .agg(
                noticias=("url", "count"),
                tom_medio=("tone", "mean")
            )
            .reset_index()
            .sort_values("noticias", ascending=False)
        )

        st.markdown("### Top fontes jornalísticas")
        st.dataframe(source_df.head(10), use_container_width=True, hide_index=True)

        fig_sources = px.bar(
            source_df.head(10),
            x="noticias",
            y="source",
            orientation="h",
            title="Fontes que mais aparecem na seleção"
        )

        st.plotly_chart(fig_sources, use_container_width=True)

        diversity = source_diversity_index(filtered)

        st.metric("Media Diversity Index", f"{diversity:.2f}")

        if diversity < 0.35:
            st.warning("A cobertura é concentrada em poucas fontes.")
        elif diversity < 0.70:
            st.info("A cobertura tem diversidade intermediária de fontes.")
        else:
            st.success("A cobertura apresenta alta diversidade de fontes.")

        st.markdown("### Comparação com baseline geral")

        baseline_tone = articles["tone"].mean()
        selection_tone = filtered["tone"].mean()

        baseline_news = (
            articles
            .groupby(["community", "destination_country"])
            .size()
            .mean()
        )

        baseline_inv = pair_inv_global["invisibility_index_proxy"].mean()

        selection_inv = pair_row["invisibility_index_proxy"] if pair_row is not None else np.nan

        baseline_df = pd.DataFrame(
            {
                "Indicador": [
                    "Tom médio da seleção",
                    "Tom médio geral",
                    "Notícias da seleção",
                    "Média de notícias por combinação",
                    "Invisibilidade da seleção",
                    "Invisibilidade média geral"
                ],
                "Valor": [
                    f"{selection_tone:.2f}",
                    f"{baseline_tone:.2f}",
                    len(filtered),
                    f"{baseline_news:.2f}",
                    f"{selection_inv:.2f}" if not pd.isna(selection_inv) else "n/d",
                    f"{baseline_inv:.2f}"
                ]
            }
        )

        st.dataframe(baseline_df, use_container_width=True, hide_index=True)

    else:
        st.info("Nenhum dado disponível para fontes e baseline.")


# ============================================================
# TAB 6 — EXPLORADOR E RECOMENDAÇÕES
# ============================================================

with tab6:
    st.subheader(t("semantic_explorer"))

    suggested_questions = {
        "Trabalho migrante": "trabalhadores migrantes condições de trabalho",
        "Discriminação": "racismo discriminação xenofobia contra comunidade asiática",
        "Cultura": "cultura identidade comunidade festival tradição",
        "Pandemia": "pandemia covid saúde comunidade asiática",
        "Economia": "negócios comércio investimento economia diáspora asiática",
        "Violência": "violência crime segurança ataques contra asiáticos"
    }

    st.markdown(f"### {t('suggested_questions')}")

    bcols = st.columns(3)

    for idx, (label_btn, query_text) in enumerate(suggested_questions.items()):
        with bcols[idx % 3]:
            if st.button(label_btn):
                st.session_state["semantic_query"] = query_text

    query = st.text_input(
        t("search_input"),
        value=st.session_state.get("semantic_query", ""),
        placeholder=t("search_placeholder")
    )

    top_n = st.slider(t("results_number"), 3, 15, 5)

    if query:
        try:
            model = load_embedding_model()
            embeddings = load_embeddings()

            query_emb = model.encode(
                [query],
                normalize_embeddings=True
            )

            subset = filtered.copy()

            if subset.empty:
                st.warning("Nenhuma notícia disponível com os filtros atuais.")
            else:
                valid_ids = subset["article_id"].astype(int).values
                subset_embeddings = embeddings[valid_ids]

                scores = cosine_similarity(query_emb, subset_embeddings)[0]
                subset["similarity"] = scores

                results = subset.sort_values("similarity", ascending=False).head(top_n)

                st.markdown(f"### {t('relevant_results')}")

                render_news_cards(results, max_items=top_n)

                if st.button("Gerar Story Mode com IA"):
                    with st.spinner("Gerando narrativa..."):
                        ai_story = claude_story(results, selected_community, selected_country, story)

                    st.markdown("### Narrativa por IA")
                    st.write(ai_story)

        except Exception as e:
            st.error(f"Erro na busca semântica: {e}")
    else:
        st.info("Digite uma consulta ou escolha uma pergunta sugerida.")

    st.markdown("### Recomendações de leitura")

    recs = recommend_readings(filtered, articles, selected_community, selected_country)

    if recs:
        for title, rec_df in recs.items():
            with st.expander(title):
                if rec_df.empty:
                    st.write("Nenhuma recomendação disponível.")
                else:
                    render_news_cards(rec_df, max_items=5)
    else:
        st.info("Não há recomendações disponíveis para esta seleção.")


# ============================================================
# TAB 7 — COMPARAÇÕES E RANKINGS
# ============================================================

with tab7:
    st.subheader("Comparações e rankings")

    st.markdown("### Comparar duas comunidades no mesmo país")

    c1, c2, c3 = st.columns(3)

    with c1:
        comp_country = st.selectbox("País para comparação", countries, index=countries.index(selected_country))

    with c2:
        comp_comm_a = st.selectbox("Comunidade A", communities, index=communities.index(selected_community))

    with c3:
        default_b = 1 if len(communities) > 1 else 0
        comp_comm_b = st.selectbox("Comunidade B", communities, index=default_b)

    comp_df = pair_inv_global[
        (pair_inv_global["destination_country"] == comp_country) &
        (pair_inv_global["community"].isin([comp_comm_a, comp_comm_b]))
    ][
        [
            "community",
            "destination_country",
            "coverage_count",
            "coverage_per_100k_proxy",
            "invisibility_index_proxy"
        ]
    ]

    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    if not comp_df.empty:
        fig_comp = px.bar(
            comp_df,
            x="community",
            y="invisibility_index_proxy",
            title=f"Invisibilidade comparada em {comp_country}",
            text_auto=".2f"
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("### Comparar uma comunidade em dois países")

    p1, p2, p3 = st.columns(3)

    with p1:
        country_comm = st.selectbox("Comunidade para comparação entre países", communities, index=communities.index(selected_community))

    with p2:
        country_a = st.selectbox("País A", countries, index=countries.index(selected_country))

    with p3:
        default_country_b = 1 if len(countries) > 1 else 0
        country_b = st.selectbox("País B", countries, index=default_country_b)

    comp_country_df = pair_inv_global[
        (pair_inv_global["community"] == country_comm) &
        (pair_inv_global["destination_country"].isin([country_a, country_b]))
    ][
        [
            "community",
            "destination_country",
            "coverage_count",
            "coverage_per_100k_proxy",
            "invisibility_index_proxy"
        ]
    ]

    st.dataframe(comp_country_df, use_container_width=True, hide_index=True)

    if not comp_country_df.empty:
        fig_country = px.bar(
            comp_country_df,
            x="destination_country",
            y="invisibility_index_proxy",
            title=f"Invisibilidade de {country_comm} por país",
            text_auto=".2f"
        )
        st.plotly_chart(fig_country, use_container_width=True)

    st.markdown("### Visibilidade × tom")

    scatter_df = (
        articles
        .groupby(["community", "destination_country"])
        .agg(
            coverage_count=("url", "count"),
            avg_tone=("tone", "mean")
        )
        .reset_index()
        .merge(
            pair_inv_global[["community", "destination_country", "demographic_proxy", "invisibility_index_proxy"]],
            on=["community", "destination_country"],
            how="left"
        )
    )

    fig_scatter = px.scatter(
        scatter_df,
        x="coverage_count",
        y="avg_tone",
        size="demographic_proxy",
        color="community",
        hover_name="destination_country",
        title="Visibilidade × tom médio",
        labels={
            "coverage_count": "Volume de cobertura",
            "avg_tone": "Tom médio"
        }
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### Ranking crítico")

    rank_option = st.radio(
        "Ranking",
        [
            "Top 5 maior invisibilidade",
            "Top 5 maior cobertura",
            "Top 5 menor invisibilidade"
        ],
        horizontal=True
    )

    if rank_option == "Top 5 maior invisibilidade":
        rank_df = pair_inv_global.sort_values("invisibility_index_proxy", ascending=False).head(5)
    elif rank_option == "Top 5 maior cobertura":
        rank_df = pair_inv_global.sort_values("coverage_count", ascending=False).head(5)
    else:
        rank_df = pair_inv_global.sort_values("invisibility_index_proxy", ascending=True).head(5)

    st.dataframe(
        rank_df[
            [
                "destination_country",
                "community",
                "coverage_count",
                "coverage_per_100k_proxy",
                "invisibility_index_proxy"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 8 — RELATÓRIOS E STORY MODE
# ============================================================

with tab8:
    st.subheader("Story Mode e relatórios")

    st.markdown("### Story Mode")

    st.markdown(
        f"""
        <div class="soft-box">
        {story}
        </div>
        """,
        unsafe_allow_html=True
    )

    report = build_report(
        selected_community,
        selected_country,
        selected_sentiment,
        filtered,
        pair_row,
        insights,
        narrative_score,
        narrative_label,
        story
    )

    st.markdown("### Executive Briefing")

    st.text_area(
        "Relatório gerado automaticamente",
        value=ui(report),
        height=460
    )

    st.download_button(
        "Baixar briefing em Markdown",
        data=report.encode("utf-8"),
        file_name="executive_briefing_diaspora.md",
        mime="text/markdown"
    )

    st.markdown("### Histórico de consultas nesta sessão")

    if st.session_state["history"]:
        st.dataframe(pd.DataFrame(st.session_state["history"]), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma seleção foi salva no histórico ainda. Use o botão na barra lateral.")


# ============================================================
# TAB 9 — SALA DE AULA, PESQUISADOR, GLOSSÁRIO E SOBRE
# ============================================================

with tab9:
    st.subheader("Sala de aula, modo pesquisador, glossário e sobre")

    if analysis_mode == "Sala de aula":
        st.markdown("### Perguntas para discussão em sala")

        classroom_questions = [
            "O que significa uma comunidade ser numerosa, mas pouco coberta pela mídia?",
            "A cobertura negativa ainda pode ser considerada uma forma de visibilidade?",
            "Em quais contextos a mídia tende a tornar uma diáspora visível?",
            "Quais temas aparecem mais: cultura, trabalho, crise, crime, economia ou política?",
            "O silêncio midiático também é uma forma de representação?",
            "Que limitações existem ao transformar cobertura jornalística em números?"
        ]

        for q in classroom_questions:
            st.write("• " + q)

    elif analysis_mode == "Pesquisador":
        st.markdown("### Modo pesquisador")

        researcher_df = pd.DataFrame(
            {
                "Elemento": [
                    "Unidade de análise",
                    "Fonte jornalística",
                    "Fonte demográfica",
                    "Variável de tom",
                    "Variável de invisibilidade",
                    "Classificação de framing",
                    "Limitação principal"
                ],
                "Descrição": [
                    "Notícias/metadados jornalísticos relacionados a comunidades asiáticas",
                    "BigQuery/GDELT",
                    "UN DESA International Migrant Stock 2020",
                    "Média do tom emocional das notícias",
                    "Proxy entre cobertura midiática e peso demográfico",
                    "Classificação por palavras-chave em categorias temáticas",
                    "As tabelas UN DESA usadas não são matriz bilateral origem × destino"
                ]
            }
        )

        st.dataframe(researcher_df, use_container_width=True, hide_index=True)

    else:
        st.markdown("### Glossário interativo")

    with st.expander("Diáspora"):
        st.write("Comunidade que vive fora de seu território de origem, mantendo vínculos culturais, históricos, familiares ou simbólicos com esse lugar.")

    with st.expander("Invisibilidade midiática"):
        st.write("Distância entre a presença social/demográfica de um grupo e a atenção que ele recebe na cobertura jornalística.")

    with st.expander("Framing / enquadramento"):
        st.write("Forma como a mídia organiza narrativamente um tema, destacando certos aspectos e apagando outros.")

    with st.expander("Tom médio"):
        st.write("Indicador que resume a tonalidade emocional das notícias. Valores negativos sugerem cobertura mais negativa; valores positivos sugerem cobertura mais positiva.")

    with st.expander("Proxy demográfico"):
        st.write("Indicador aproximado usado quando não há dado bilateral exato. Neste app, combina o tamanho global da diáspora de origem com o peso migratório do país de destino.")

    with st.expander("Busca semântica"):
        st.write("Busca por significado, não apenas por palavra-chave. Ela usa embeddings multilíngues para encontrar notícias conceitualmente próximas da consulta.")

    st.markdown("### Sobre o projeto")

    st.markdown(
        """
        <div class="soft-box">
        <b>Projeto Final A2 — Programação / Comunicação Digital — FGV</b><br><br>
        Desenvolvido por Carolina Carpenter, Matheus Constantin e Gabriel Sampaio.<br><br>
        O objetivo é analisar a diáspora asiática sob o olhar da mídia global,
        investigando cobertura, tom, enquadramento e invisibilidade midiática.
        A versão final funciona como um observatório interativo de análise de mídia.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
try:
    from social_layer import render_social_layer

    render_social_layer(
        selected_community=selected_community,
        selected_country=selected_country,
        selected_sentiment=selected_sentiment,
        start_date=start_date,
        end_date=end_date,
        filtered=filtered,
        articles=articles,
        story=story if "story" in globals() else "",
    )
except ModuleNotFoundError:
    st.info("Camada social não instalada: adicione social_layer.py ao projeto.")
except Exception as e:
    st.warning(f"Camada social temporariamente indisponível: {e}")
