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
# ============================================================
# TRADUÇÃO DE RÓTULOS VISÍVEIS
# ============================================================

UI_PT_EN = {
    # Filtros e sidebar
    "Comunidade asiática": "Asian community",
    "País de destino": "Destination country",
    "Sentimento": "Sentiment",
    "Período": "Period",
    "Salvar seleção no histórico": "Save selection to history",
    "Configuração da análise": "Analysis settings",
    "Filtros principais": "Main filters",
    "Modo apresentação": "Presentation mode",
    "Modo de uso": "Usage mode",

    # Camada social
    "Camada colaborativa": "Collaborative layer",
    "Meu perfil": "My profile",
    "Comentários e feed": "Comments and feed",
    "Salvar e coleções": "Saved items and collections",
    "Framing e debates": "Framing and debates",
    "Mensagens": "Messages",
    "Círculos e relatórios": "Circles and reports",
    "Diário, notificações e ranking": "Diary, notifications and ranking",
    "Navegação social": "Social navigation",
    "Seção atual": "Current section",

    # Subtítulos reais das seções sociais
    "Comunidade e comentários da análise": "Community and comments on the analysis",
    "Salvar análises, notícias e coleções": "Save analyses, news and collections",
    "Framing colaborativo, debate e revisão humana da IA": "Collaborative framing, debate and human review of the AI",
    "Mensagens diretas": "Direct messages",
    "Research Circles e relatórios colaborativos": "Research Circles and collaborative reports",
    "Diário da diáspora, notificações e ranking": "Diaspora diary, notifications and ranking",
    "Salvar notícia da seleção": "Save article from selection",
    "Acesso": "Access",

    # Conta social
    "Conta social": "Social account",
    "Criar conta": "Create account",
    "Entrar": "Log in",
    "Sair": "Log out",
    "Email": "Email",
    "Senha": "Password",
    "Nome": "Name",
    "Nome completo": "Full name",
    "Nome de usuário": "Username",
    "Bio": "Bio",
    "Instituição": "Institution",
    "Interesses": "Interests",
    "Salvar perfil": "Save profile",
    "Editar perfil": "Edit profile",
    "Perfil salvo com sucesso.": "Profile saved successfully.",
    "Conta criada com sucesso.": "Account created successfully.",
    "Login realizado com sucesso.": "Logged in successfully.",
    "Você precisa estar logado para usar esta função.": "You need to be logged in to use this feature.",

    # Comentários / feed
    "Escreva um comentário": "Write a comment",
    "Publicar comentário": "Post comment",
    "Comentários": "Comments",
    "Feed da comunidade": "Community feed",
    "Comentário publicado.": "Comment posted.",
    "Nenhum comentário ainda.": "No comments yet.",

    # Salvar / coleções
    "Salvar análise atual": "Save current analysis",
    "Análises salvas": "Saved analyses",
    "Notícias salvas": "Saved news",
    "Criar coleção": "Create collection",
    "Minhas coleções": "My collections",
    "Nome da coleção": "Collection name",
    "Salvar notícia": "Save article",
    "Adicionar à coleção": "Add to collection",
    "Análise salva.": "Analysis saved.",
    "Notícia salva.": "Article saved.",

    # Framing / debates
    "Votar no framing": "Vote on framing",
    "Framing colaborativo": "Collaborative framing",
    "Criar debate": "Create debate",
    "Debates": "Debates",
    "Título do debate": "Debate title",
    "Descrição do debate": "Debate description",
    "Concordo": "Agree",
    "Discordo": "Disagree",
    "Depende": "It depends",
    "Enviar voto": "Submit vote",

    # Mensagens
    "Nova mensagem": "New message",
    "Enviar mensagem": "Send message",
    "Destinatário": "Recipient",
    "Mensagem": "Message",
    "Conversas": "Conversations",
    "Caixa de entrada": "Inbox",

    # Círculos / relatórios
    "Criar círculo": "Create circle",
    "Círculos de pesquisa": "Research circles",
    "Relatórios colaborativos": "Collaborative reports",
    "Criar relatório": "Create report",
    "Título do relatório": "Report title",
    "Conteúdo do relatório": "Report content",
    "Adicionar colaborador": "Add collaborator",

    # Diário / notificações / ranking
    "Diário da diáspora": "Diaspora diary",
    "Escrever reflexão": "Write reflection",
    "Publicar reflexão": "Post reflection",
    "Notificações": "Notifications",
    "Ranking de participação": "Participation ranking",
    "Comentários úteis": "Useful comments",

    # Notícias/cards
    "Data": "Date",
    "Fonte": "Source",
    "Tom": "Tone",
    "Enquadramento": "Frame",
    "Abrir notícia": "Open article",
    "Notícias de exemplo": "Example news",
    "Resultados mais relevantes": "Most relevant results",

    # Análise
    "Notícias filtradas": "Filtered news",
    "Tom médio": "Average tone",
    "Diversidade de fontes": "Source diversity",
    "Cartões de achados": "Finding cards",
    "Baixar dados da seleção em CSV": "Download selected data as CSV",
}


VALUE_PT_EN = {
    # Sentimentos
    "positivo": "positive",
    "negativo": "negative",
    "neutro": "neutral",
    "positive": "positive",
    "negative": "negative",
    "neutral": "neutral",

    # Enquadramentos
    "Trabalho e migração": "Labor and migration",
    "Racismo e discriminação": "Racism and discrimination",
    "Saúde e pandemia": "Health and pandemic",
    "Crime e segurança": "Crime and security",
    "Economia e negócios": "Economy and business",
    "Cultura e identidade": "Culture and identity",
    "Política internacional": "International politics",
    "Enquadramento geral": "General framing",
}


def ui(text):
    """
    Traduz textos fixos da interface quando o idioma selecionado é inglês.
    Mantém o texto original quando o idioma é português.
    """
    if get_lang() == "en":
        return UI_PT_EN.get(text, text)
    return text


def value_label(text):
    """
    Traduz valores visíveis, como sentimento e enquadramento.
    Não altera o valor interno usado no banco/filtros.
    """
    if get_lang() == "en":
        return VALUE_PT_EN.get(str(text), str(text))
    return str(text)

