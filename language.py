"""
Camada de internacionalização (i18n) do Invisible Diasporas Lab.

Uso:
    from language import t, language_selector

    language_selector()          # mostra o seletor de idioma (PT / EN)
    st.title(t("hero_title"))    # devolve o texto no idioma atual

O idioma escolhido fica em st.session_state["lang"] (padrão: "pt").
"""

import streamlit as st

# ============================================================
# IDIOMAS DISPONÍVEIS
# ============================================================

LANGUAGES = {
    "pt": "Português",
    "en": "English",
}

DEFAULT_LANG = "pt"


# ============================================================
# DICIONÁRIO DE TRADUÇÕES
# ============================================================

TRANSLATIONS = {
    # ---------- IDIOMA QUE A IA DEVE USAR ----------
    "ai_language": {
        "pt": "Português",
        "en": "English",
    },

    # ---------- HERO / TOPO ----------
    "page_badge": {
        "pt": "Invisible Diasporas Lab · Media Visibility Intelligence",
        "en": "Invisible Diasporas Lab · Media Visibility Intelligence",
    },
    "hero_title": {
        "pt": "🌏 Monitor de Mídia da Diáspora Asiática",
        "en": "🌏 Asian Diaspora Media Monitor",
    },
    "hero_text": {
        "pt": "Um observatório interativo para analisar como a mídia global cobre as "
              "comunidades da diáspora asiática: tom, enquadramento, visibilidade e silêncio.",
        "en": "An interactive observatory to analyze how global media covers Asian diaspora "
              "communities: tone, framing, visibility and silence.",
    },
    "how_to_use_title": {
        "pt": "Como usar",
        "en": "How to use",
    },
    "how_to_use_text": {
        "pt": "Escolha uma comunidade, um país de destino e um sentimento na barra lateral. "
              "Depois explore as abas para ver perfil, mapa, risco, tempo, fontes e comparações.",
        "en": "Pick a community, a destination country and a sentiment in the sidebar. "
              "Then explore the tabs to see profile, map, risk, time, sources and comparisons.",
    },

    # ---------- SIDEBAR ----------
    "sidebar_config": {
        "pt": "Configuração da análise",
        "en": "Analysis settings",
    },
    "presentation_mode": {
        "pt": "Modo apresentação",
        "en": "Presentation mode",
    },
    "usage_mode": {
        "pt": "Modo de uso",
        "en": "Usage mode",
    },
    "full_exploration": {
        "pt": "Exploração completa",
        "en": "Full exploration",
    },
    "classroom": {
        "pt": "Sala de aula",
        "en": "Classroom",
    },
    "researcher": {
        "pt": "Pesquisador",
        "en": "Researcher",
    },
    "executive_briefing": {
        "pt": "Briefing executivo",
        "en": "Executive briefing",
    },
    "main_filters": {
        "pt": "Filtros principais",
        "en": "Main filters",
    },
    "community_filter": {
        "pt": "Comunidade asiática",
        "en": "Asian community",
    },
    "country_filter": {
        "pt": "País de destino",
        "en": "Destination country",
    },
    "sentiment_filter": {
        "pt": "Sentimento",
        "en": "Sentiment",
    },
    "period_filter": {
        "pt": "Período",
        "en": "Period",
    },

    # ---------- ABAS ----------
    "tab_profile": {
        "pt": "Perfil 360",
        "en": "360 Profile",
    },
    "tab_map": {
        "pt": "Mapa crítico",
        "en": "Critical map",
    },
    "tab_radar": {
        "pt": "Radar e risco",
        "en": "Radar & risk",
    },
    "tab_time": {
        "pt": "Tempo e silêncio",
        "en": "Time & silence",
    },
    "tab_sources": {
        "pt": "Fontes e baseline",
        "en": "Sources & baseline",
    },
    "tab_explorer": {
        "pt": "Explorador",
        "en": "Explorer",
    },
    "tab_comparisons": {
        "pt": "Comparações",
        "en": "Comparisons",
    },
    "tab_reports": {
        "pt": "Relatórios",
        "en": "Reports",
    },
    "tab_about": {
        "pt": "Sala, glossário e sobre",
        "en": "Classroom, glossary & about",
    },

    # ---------- PERFIL 360 ----------
    "profile_title": {
        "pt": "Perfil 360 da seleção",
        "en": "360 profile of the selection",
    },
    "news_count": {
        "pt": "Notícias filtradas",
        "en": "Filtered news",
    },
    "avg_tone": {
        "pt": "Tom médio",
        "en": "Average tone",
    },
    "dominant_frame": {
        "pt": "Enquadramento",
        "en": "Framing",
    },
    "source_diversity": {
        "pt": "Diversidade de fontes",
        "en": "Source diversity",
    },
    "tone_help": {
        "pt": "valores abaixo de 0 indicam cobertura mais negativa; valores próximos de 0 "
              "indicam tom neutro; valores acima de 0 indicam cobertura mais positiva.",
        "en": "values below 0 indicate more negative coverage; values near 0 indicate a neutral "
              "tone; values above 0 indicate more positive coverage.",
    },
    "findings_cards": {
        "pt": "Cartões de achados",
        "en": "Findings cards",
    },
    "example_news": {
        "pt": "Notícias de exemplo",
        "en": "Sample news",
    },
    "download_csv": {
        "pt": "Baixar dados da seleção em CSV",
        "en": "Download selection data as CSV",
    },

    # ---------- EXPLORADOR SEMÂNTICO ----------
    "semantic_explorer": {
        "pt": "Explorador semântico e recomendações",
        "en": "Semantic explorer and recommendations",
    },
    "suggested_questions": {
        "pt": "Perguntas sugeridas",
        "en": "Suggested questions",
    },
    "search_input": {
        "pt": "Digite uma busca",
        "en": "Type a search",
    },
    "search_placeholder": {
        "pt": "Ex.: trabalhadores filipinos no Golfo",
        "en": "E.g.: Filipino workers in the Gulf",
    },
    "results_number": {
        "pt": "Número de resultados",
        "en": "Number of results",
    },
    "relevant_results": {
        "pt": "Resultados mais relevantes",
        "en": "Most relevant results",
    },

    # ---------- CAMADA SOCIAL (social_layer.py) ----------
    "profile_menu": {
        "pt": "👤 Meu perfil",
        "en": "👤 My profile",
    },
    "social_navigation": {
        "pt": "Navegação social",
        "en": "Social navigation",
    },
    "social_profile": {
        "pt": "Meu perfil",
        "en": "My profile",
    },
    "social_comments": {
        "pt": "Comentários e feed",
        "en": "Comments and feed",
    },
    "social_save": {
        "pt": "Salvar e coleções",
        "en": "Save and collections",
    },
    "social_framing": {
        "pt": "Framing e debates",
        "en": "Framing and debates",
    },
    "social_messages": {
        "pt": "Mensagens",
        "en": "Messages",
    },
    "social_circles": {
        "pt": "Círculos e relatórios",
        "en": "Circles and reports",
    },
    "social_diary": {
        "pt": "Diário, notificações e ranking",
        "en": "Diary, notifications and ranking",
    },
    "current_section": {
        "pt": "Seção atual",
        "en": "Current section",
    },
}


# ============================================================
# FUNÇÕES PÚBLICAS
# ============================================================

def get_lang() -> str:
    """Devolve o código do idioma atual ('pt' ou 'en')."""
    return st.session_state.get("lang", DEFAULT_LANG)


def t(key: str) -> str:
    """
    Traduz uma chave para o idioma atual.

    Se a chave não existir, devolve a própria chave (facilita achar o que falta).
    Se faltar a tradução no idioma atual, cai no português.
    """
    lang = get_lang()
    entry = TRANSLATIONS.get(key)

    if entry is None:
        return key

    return entry.get(lang, entry.get(DEFAULT_LANG, key))


def language_selector() -> str:
    """
    Mostra um seletor de idioma e guarda a escolha em st.session_state['lang'].

    Deve ser chamado uma vez no topo do app. Devolve o idioma escolhido.
    """
    if "lang" not in st.session_state:
        st.session_state["lang"] = DEFAULT_LANG

    codes = list(LANGUAGES.keys())
    current_index = codes.index(st.session_state["lang"])

    choice = st.selectbox(
        "🌐",
        options=codes,
        index=current_index,
        format_func=lambda code: LANGUAGES.get(code, code),
        label_visibility="collapsed",
        key="lang_selectbox",
    )

    st.session_state["lang"] = choice
    return choice
