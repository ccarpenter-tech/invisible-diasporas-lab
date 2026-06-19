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
    "não identificado": "not identified",
    "n/d": "n/a",
}



# ============================================================
# TRADUÇÕES ADICIONAIS (cobertura completa da interface)
# ============================================================

UI_PT_EN.update({
    '### Antes, durante e depois da pandemia': '### Before, during and after the pandemic',
    '### Collab Report': '### Collab Report',
    '### Comparar duas comunidades no mesmo país': '### Compare two communities in the same country',
    '### Comparar uma comunidade em dois países': '### Compare one community in two countries',
    '### Comparação com baseline geral': '### Comparison with the overall baseline',
    '### Criar círculo de pesquisa': '### Create research circle',
    '### Debate Mode': '### Debate Mode',
    '### Diário da diáspora': '### Diaspora diary',
    '### Encontrar pesquisadores': '### Find researchers',
    '### Eventos-chave para leitura da cobertura': '### Key events for reading the coverage',
    '### Executive Briefing': '### Executive Briefing',
    '### Explique este resultado': '### Explain this result',
    '### Feed geral da comunidade': '### General community feed',
    '### Framing Battle: algoritmo × humanos': '### Framing Battle: algorithm × humans',
    '### Glossário interativo': '### Interactive glossary',
    '### Histórico de consultas nesta sessão': '### Query history in this session',
    '### Invisible Case of the Week': '### Invisible Case of the Week',
    '### Mapa de vozes': '### Map of voices',
    '### Minhas análises e notícias salvas': '### My saved analyses and news',
    '### Minhas estatísticas': '### My statistics',
    '### Modo pesquisador': '### Researcher mode',
    '### Narrativa por IA': '### AI narrative',
    '### Notificações': '### Notifications',
    '### Nova conversa': '### New conversation',
    '### Perguntas para discussão em sala': '### Questions for classroom discussion',
    '### Principais achados': '### Main findings',
    '### Ranking crítico': '### Critical ranking',
    '### Ranking de comentários úteis': '### Ranking of useful comments',
    '### Recomendações de leitura': '### Reading recommendations',
    '### Revisão humana de IA / Story Mode': '### Human review of AI / Story Mode',
    '### Silence Detector': '### Silence Detector',
    '### Sobre o projeto': '### About the project',
    '### Story Mode': '### Story Mode',
    '### Top 5 hotspots críticos': '### Top 5 critical hotspots',
    '### Top fontes jornalísticas': '### Top journalistic sources',
    '### Visibilidade × tom': '### Visibility × tone',
    '### 🌐 Camada colaborativa': '### 🌐 Collaborative layer',
    '**Análises salvas**': '**Saved analyses**',
    '**Notícias salvas**': '**Saved news**',
    'A IA interpretou bem?': 'Did the AI interpret it well?',
    'A camada social ainda não está configurada. Adicione SUPABASE_URL e SUPABASE_ANON_KEY nos Secrets do Streamlit.': 'The social layer is not configured yet. Add SUPABASE_URL and SUPABASE_ANON_KEY in the Streamlit Secrets.',
    'A cobertura apresenta alta diversidade de fontes jornalísticas.': 'The coverage shows high diversity of journalistic sources.',
    'A cobertura apresenta alta diversidade de fontes.': 'The coverage shows high source diversity.',
    'A cobertura apresenta tom médio negativo.': 'The coverage has a negative average tone.',
    'A cobertura apresenta tom médio positivo.': 'The coverage has a positive average tone.',
    'A cobertura apresenta tom médio próximo de neutro.': 'The coverage has an average tone close to neutral.',
    'A cobertura tem diversidade intermediária de fontes.': 'The coverage has intermediate source diversity.',
    'A cobertura é concentrada em poucas fontes.': 'The coverage is concentrated in a few sources.',
    'A diversidade de fontes é baixa: poucas fontes concentram a cobertura.': 'Source diversity is low: a few sources concentrate the coverage.',
    'Achado': 'Finding',
    'Adicionar colaborador por username': 'Add collaborator by username',
    'Afirmação para debate': 'Statement for debate',
    'Ainda não há comentários nesta análise.': 'There are no comments on this analysis yet.',
    'Ainda não há reações suficientes para ranking.': 'There are not enough reactions for a ranking yet.',
    'Alta invisibilidade': 'High invisibility',
    'Avaliação salva.': 'Review saved.',
    'Baixa invisibilidade': 'Low invisibility',
    'Baixar briefing em Markdown': 'Download briefing as Markdown',
    'Busca por significado, não apenas por palavra-chave. Ela usa embeddings multilíngues para encontrar notícias conceitualmente próximas da consulta.': 'Search by meaning, not just by keyword. It uses multilingual embeddings to find news conceptually close to the query.',
    'Busca semântica': 'Semantic search',
    'Buscar por username, nome ou instituição': 'Search by username, name or institution',
    'Camada social não instalada: adicione social_layer.py ao projeto.': 'Social layer not installed: add social_layer.py to the project.',
    'Camada social temporariamente indisponível': 'Social layer temporarily unavailable',
    'Caso da semana indisponível.': 'Case of the week unavailable.',
    'Cobertura encontrada': 'Coverage found',
    'Cobertura por fase histórica': 'Coverage by historical phase',
    'Colaborador adicionado.': 'Collaborator added.',
    'Coleção criada.': 'Collection created.',
    'Coleção pública': 'Public collection',
    'Comentário sobre a interpretação da IA': "Comment on the AI's interpretation",
    'Comentários por país de destino': 'Comments by destination country',
    'Comparações e rankings': 'Comparisons and rankings',
    'Comunidade A': 'Community A',
    'Comunidade B': 'Community B',
    'Comunidade para comparação entre países': 'Community for cross-country comparison',
    'Comunidade que vive fora de seu território de origem, mantendo vínculos culturais, históricos, familiares ou simbólicos com esse lugar.': 'A community living outside its territory of origin, keeping cultural, historical, family or symbolic ties to that place.',
    'Conta criada. Confirme seu email e depois faça login.': 'Account created. Confirm your email and then log in.',
    'Contas, perfis, comentários, mensagens, coleções, debates e análise humana colaborativa.': 'Accounts, profiles, comments, messages, collections, debates and collaborative human analysis.',
    'Conversa criada.': 'Conversation created.',
    'Criar conversa': 'Create conversation',
    'Criar debate desta análise': 'Create debate from this analysis',
    'Crie um projeto no Supabase, rode o SQL das tabelas sociais e adicione as chaves no Streamlit Secrets.': 'Create a Supabase project, run the SQL for the social tables and add the keys in the Streamlit Secrets.',
    'Círculo criado.': 'Circle created.',
    'Círculos disponíveis': 'Available circles',
    'Debate criado.': 'Debate created.',
    'Descrição': 'Description',
    'Diagnóstico': 'Diagnosis',
    'Digite uma consulta ou escolha uma pergunta sugerida.': 'Type a query or choose a suggested question.',
    'Discussão atual': 'Current discussion',
    'Distribuição do sentimento': 'Sentiment distribution',
    'Distância entre a presença social/demográfica de um grupo e a atenção que ele recebe na cobertura jornalística.': 'Distance between the social/demographic presence of a group and the attention it receives in news coverage.',
    'Diáspora': 'Diaspora',
    'Enquadramentos': 'Framings',
    'Enquadramentos predominantes': 'Predominant framings',
    'Entrar neste círculo': 'Join this circle',
    'Entre ou crie uma conta para usar a camada colaborativa.': 'Log in or create an account to use the collaborative layer.',
    'Enviar': 'Send',
    'Erro': 'Error',
    'Erro ao comentar': 'Error while commenting',
    'Erro ao criar conta': 'Error while creating account',
    'Erro ao entrar': 'Error while logging in',
    'Erro ao enviar': 'Error while sending',
    'Erro ao salvar perfil': 'Error while saving profile',
    'Erro na busca semântica': 'Error in the semantic search',
    'Escolha uma conversa': 'Choose a conversation',
    'Escolha uma notícia': 'Choose a news item',
    'Escrever comentário público': 'Write a public comment',
    'Esse número é uma verdade absoluta?': 'Is this number an absolute truth?',
    'Estatísticas indisponíveis agora.': 'Statistics unavailable right now.',
    'Fase': 'Phase',
    'Fontes jornalísticas, diversidade e baseline': 'Journalistic sources, diversity and baseline',
    'Fontes que mais aparecem na seleção': 'Sources that appear most in the selection',
    'Foram encontrados períodos sem cobertura no intervalo analisado.': 'Periods without coverage were found in the analyzed range.',
    'Forma como a mídia organiza narrativamente um tema, destacando certos aspectos e apagando outros.': 'How the media narratively organizes a topic, highlighting certain aspects and erasing others.',
    'Framing / enquadramento': 'Framing',
    'Gerar Story Mode com IA': 'Generate Story Mode with AI',
    'Hotspots de invisibilidade': 'Invisibility hotspots',
    'Indicador aproximado usado quando não há dado bilateral exato. Neste app, combina o tamanho global da diáspora de origem com o peso migratório do país de destino.': 'Approximate indicator used when there is no exact bilateral data. In this app, it combines the global size of the origin diaspora with the migratory weight of the destination country.',
    'Indicador que resume a tonalidade emocional das notícias. Valores negativos sugerem cobertura mais negativa; valores positivos sugerem cobertura mais positiva.': 'Indicator summarizing the emotional tone of the news. Negative values suggest more negative coverage; positive values suggest more positive coverage.',
    'Invisibilidade': 'Invisibility',
    'Invisibilidade comparada em': 'Invisibility compared in',
    'Invisibilidade crítica': 'Critical invisibility',
    'Invisibilidade de': 'Invisibility of',
    'Invisibilidade midiática': 'Media invisibility',
    'Invisibilidade moderada': 'Moderate invisibility',
    'Justificativa': 'Justification',
    'Justificativa opcional': 'Optional justification',
    'Leia também: notícias com tom mais negativo': 'Read also: news with a more negative tone',
    'Leia também: notícias com tom mais positivo': 'Read also: news with a more positive tone',
    'Linha do tempo, pandemia e silêncio midiático': 'Timeline, pandemic and media silence',
    'Logado como': 'Logged in as',
    'Mapa crítico de invisibilidade': 'Critical invisibility map',
    'Marcar todas como lidas': 'Mark all as read',
    'Media Diversity Index': 'Media Diversity Index',
    'Mesma comunidade em outros países': 'Same community in other countries',
    'Narrative Risk': 'Narrative Risk',
    'Nenhum dado disponível para a seleção.': 'No data available for the selection.',
    'Nenhum dado disponível para fontes e baseline.': 'No data available for sources and baseline.',
    'Nenhuma notícia disponível com os filtros atuais.': 'No news available with the current filters.',
    'Nenhuma notícia encontrada com esses filtros.': 'No news found with these filters.',
    'Nenhuma notícia filtrada para salvar.': 'No filtered news to save.',
    'Nenhuma notícia filtrada para votar framing.': 'No filtered news to vote on framing.',
    'Nenhuma recomendação disponível.': 'No recommendation available.',
    'Nenhuma seleção foi salva no histórico ainda. Use o botão na barra lateral.': 'No selection has been saved to history yet. Use the button in the sidebar.',
    'Nota para salvar esta análise': 'Note to save this analysis',
    'Nota privada sobre a notícia': 'Private note about the news item',
    'Notícia para classificar': 'News item to classify',
    'Notícias': 'News',
    'Não foi possível criar a conta.': 'Could not create the account.',
    'Não foram detectados longos períodos de silêncio dentro do intervalo filtrado.': 'No long periods of silence were detected within the filtered range.',
    'Não há dados suficientes para o mapa crítico.': 'There is not enough data for the critical map.',
    'Não há notícias disponíveis para gerar insights com os filtros atuais.': 'There are no news available to generate insights with the current filters.',
    'Não há recomendações disponíveis para esta seleção.': 'There are no recommendations available for this selection.',
    'Não há tom médio disponível para esta seleção.': 'There is no average tone available for this selection.',
    'Não. Ele é um indicador comparativo. Serve para orientar análise crítica, não para substituir leitura qualitativa das notícias.': 'No. It is a comparative indicator. It serves to guide critical analysis, not to replace qualitative reading of the news.',
    'O Narrative Risk Score combina invisibilidade, tom negativo, enquadramentos sensíveis e baixa diversidade de fontes.': 'The Narrative Risk Score combines invisibility, negative tone, sensitive framings and low source diversity.',
    'O que falta configurar?': 'What is missing to configure?',
    'O índice aumenta quando há uma combinação de presença demográfica relevante e pouca cobertura midiática encontrada no corpus.': 'The index increases when there is a combination of relevant demographic presence and little media coverage found in the corpus.',
    'Outras comunidades no mesmo país': 'Other communities in the same country',
    'Pandemia': 'Pandemic',
    'País A': 'Country A',
    'País B': 'Country B',
    'País para comparação': 'Country for comparison',
    'Perfil atualizado.': 'Profile updated.',
    'Por que o risco narrativo pode ser alto?': 'Why can the narrative risk be high?',
    'Por que o índice pode ser alto?': 'Why can the index be high?',
    'Post publicado.': 'Post published.',
    'Postar no círculo': 'Post to the circle',
    'Proxy demográfico': 'Demographic proxy',
    'Pré-pandemia': 'Pre-pandemic',
    'Publicar no círculo': 'Publish to the circle',
    'Pós-pandemia': 'Post-pandemic',
    'Qual é o framing dominante?': 'What is the dominant framing?',
    'Radar da cobertura': 'Coverage radar',
    'Radar da cobertura e Narrative Risk Score': 'Coverage radar and Narrative Risk Score',
    'Ranking': 'Ranking',
    'Reflexão qualitativa': 'Qualitative reflection',
    'Reflexão salva.': 'Reflection saved.',
    'Relatório criado.': 'Report created.',
    'Relatório gerado automaticamente': 'Automatically generated report',
    'Risco narrativo alto': 'High narrative risk',
    'Risco narrativo baixo': 'Low narrative risk',
    'Risco narrativo crítico': 'Critical narrative risk',
    'Risco narrativo moderado': 'Moderate narrative risk',
    'Risco não calculável': 'Risk not computable',
    'Sair da conta': 'Log out',
    'Sala de aula, modo pesquisador, glossário e sobre': 'Classroom, researcher mode, glossary and about',
    'Salvar avaliação da IA': 'Save AI review',
    'Salvar reflexão': 'Save reflection',
    'Seguidores': 'Followers',
    'Seguindo.': 'Following.',
    'Seguir': 'Follow',
    'Sem dados para caso da semana.': 'No data for the case of the week.',
    'Sem notificações.': 'No notifications.',
    'Status de invisibilidade': 'Invisibility status',
    'Story Mode e relatórios': 'Story Mode and reports',
    'Sua posição': 'Your position',
    'Tema': 'Theme',
    'Texto inicial': 'Initial text',
    'Tornar reflexão pública': 'Make reflection public',
    'Título da reflexão': 'Reflection title',
    'Título do círculo': 'Circle title',
    'Título do relatório colaborativo': 'Collaborative report title',
    'URL do avatar/foto': 'Avatar/photo URL',
    'Username': 'Username',
    'Username da pessoa': "Person's username",
    'Usuário': 'User',
    'Usuário não encontrado.': 'User not found.',
    'Visibilidade × tom médio': 'Visibility × average tone',
    'Você ainda não tem conversas.': "You don't have any conversations yet.",
    'Você entrou no círculo.': 'You joined the circle.',
    'Volume mensal': 'Monthly volume',
    'Votar framing': 'Vote on framing',
    'Votar no debate': 'Vote in the debate',
    'Voto registrado.': 'Vote recorded.',
    'Voto salvo.': 'Vote saved.',
    'Votos humanos de framing': 'Human framing votes',
    'em': 'in',
    'por país': 'by country',
    'Índice de invisibilidade': 'Invisibility index',
    '🌐 Camada colaborativa': '🌐 Collaborative layer',
    '🎤 Modo apresentação': '🎤 Presentation mode',
    'O que significa uma comunidade ser numerosa, mas pouco coberta pela mídia?': 'What does it mean for a community to be numerous but rarely covered by the media?',
    'A cobertura negativa ainda pode ser considerada uma forma de visibilidade?': 'Can negative coverage still be considered a form of visibility?',
    'Em quais contextos a mídia tende a tornar uma diáspora visível?': 'In which contexts does the media tend to make a diaspora visible?',
    'Quais temas aparecem mais: cultura, trabalho, crise, crime, economia ou política?': 'Which topics appear most: culture, labor, crisis, crime, economy or politics?',
    'O silêncio midiático também é uma forma de representação?': 'Is media silence also a form of representation?',
    'Que limitações existem ao transformar cobertura jornalística em números?': 'What limitations exist when turning news coverage into numbers?',
    'Top 5 maior invisibilidade': 'Top 5 highest invisibility',
    'Top 5 maior cobertura': 'Top 5 highest coverage',
    'Top 5 menor invisibilidade': 'Top 5 lowest invisibility',
    'Sim': 'Yes',
    'Parcialmente': 'Partially',
    'Não': 'No',
})


# ------------------------------------------------------------
# Cobertura completa de rótulos visíveis (PT -> EN)
# ------------------------------------------------------------
UI_PT_EN.update({
    '### Antes, durante e depois da pandemia': '### Before, during and after the pandemic',
    '### Collab Report': '### Collab Report',
    '### Comparar duas comunidades no mesmo país': '### Compare two communities in the same country',
    '### Comparar uma comunidade em dois países': '### Compare one community in two countries',
    '### Comparação com baseline geral': '### Comparison with the overall baseline',
    '### Criar círculo de pesquisa': '### Create research circle',
    '### Debate Mode': '### Debate Mode',
    '### Diário da diáspora': '### Diaspora diary',
    '### Encontrar pesquisadores': '### Find researchers',
    '### Eventos-chave para leitura da cobertura': '### Key events for reading the coverage',
    '### Executive Briefing': '### Executive Briefing',
    '### Explique este resultado': '### Explain this result',
    '### Feed geral da comunidade': '### Community general feed',
    '### Framing Battle: algoritmo × humanos': '### Framing Battle: algorithm × humans',
    '### Glossário interativo': '### Interactive glossary',
    '### Histórico de consultas nesta sessão': '### Query history in this session',
    '### Invisible Case of the Week': '### Invisible Case of the Week',
    '### Mapa de vozes': '### Map of voices',
    '### Minhas análises e notícias salvas': '### My saved analyses and news',
    '### Minhas estatísticas': '### My statistics',
    '### Modo pesquisador': '### Researcher mode',
    '### Narrativa por IA': '### AI narrative',
    '### Notificações': '### Notifications',
    '### Nova conversa': '### New conversation',
    '### Perguntas para discussão em sala': '### Questions for classroom discussion',
    '### Principais achados': '### Key findings',
    '### Ranking crítico': '### Critical ranking',
    '### Ranking de comentários úteis': '### Ranking of useful comments',
    '### Recomendações de leitura': '### Reading recommendations',
    '### Revisão humana de IA / Story Mode': '### Human review of AI / Story Mode',
    '### Silence Detector': '### Silence Detector',
    '### Sobre o projeto': '### About the project',
    '### Story Mode': '### Story Mode',
    '### Top 5 hotspots críticos': '### Top 5 critical hotspots',
    '### Top fontes jornalísticas': '### Top journalistic sources',
    '### Visibilidade × tom': '### Visibility × tone',
    '### 🌐 Camada colaborativa': '### 🌐 Collaborative layer',
    '**Análises salvas**': '**Saved analyses**',
    '**Notícias salvas**': '**Saved news**',
    'A IA interpretou bem?': 'Did the AI interpret it well?',
    'A camada social ainda não está configurada. Adicione SUPABASE_URL e SUPABASE_ANON_KEY nos Secrets do Streamlit.': 'The social layer is not configured yet. Add SUPABASE_URL and SUPABASE_ANON_KEY to the Streamlit Secrets.',
    'A cobertura apresenta alta diversidade de fontes jornalísticas.': 'The coverage shows high diversity of journalistic sources.',
    'A cobertura apresenta alta diversidade de fontes.': 'The coverage shows high source diversity.',
    'A cobertura apresenta tom médio negativo.': 'The coverage shows a negative average tone.',
    'A cobertura apresenta tom médio positivo.': 'The coverage shows a positive average tone.',
    'A cobertura apresenta tom médio próximo de neutro.': 'The coverage shows an average tone close to neutral.',
    'A cobertura tem diversidade intermediária de fontes.': 'The coverage has intermediate source diversity.',
    'A cobertura é concentrada em poucas fontes.': 'The coverage is concentrated in a few sources.',
    'A diversidade de fontes é baixa: poucas fontes concentram a cobertura.': 'Source diversity is low: a few sources concentrate the coverage.',
    'Achado': 'Finding',
    'Adicionar colaborador por username': 'Add collaborator by username',
    'Afirmação para debate': 'Statement for debate',
    'Ainda não há comentários nesta análise.': 'There are no comments on this analysis yet.',
    'Ainda não há reações suficientes para ranking.': 'There are not enough reactions for a ranking yet.',
    'Alta invisibilidade': 'High invisibility',
    'Avaliação salva.': 'Evaluation saved.',
    'Baixa invisibilidade': 'Low invisibility',
    'Baixar briefing em Markdown': 'Download briefing as Markdown',
    'Busca por significado, não apenas por palavra-chave. Ela usa embeddings multilíngues para encontrar notícias conceitualmente próximas da consulta.': 'Search by meaning, not just by keyword. It uses multilingual embeddings to find news conceptually close to the query.',
    'Busca semântica': 'Semantic search',
    'Buscar por username, nome ou instituição': 'Search by username, name or institution',
    'Camada social não instalada: adicione social_layer.py ao projeto.': 'Social layer not installed: add social_layer.py to the project.',
    'Camada social temporariamente indisponível': 'Social layer temporarily unavailable',
    'Caso da semana indisponível.': 'Case of the week unavailable.',
    'Cobertura encontrada': 'Coverage found',
    'Cobertura por fase histórica': 'Coverage by historical phase',
    'Colaborador adicionado.': 'Collaborator added.',
    'Coleção criada.': 'Collection created.',
    'Coleção pública': 'Public collection',
    'Comentário sobre a interpretação da IA': 'Comment on the AI interpretation',
    'Comentários por país de destino': 'Comments by destination country',
    'Comparações e rankings': 'Comparisons and rankings',
    'Comunidade A': 'Community A',
    'Comunidade B': 'Community B',
    'Comunidade para comparação entre países': 'Community for cross-country comparison',
    'Comunidade que vive fora de seu território de origem, mantendo vínculos culturais, históricos, familiares ou simbólicos com esse lugar.': 'A community that lives outside its territory of origin, keeping cultural, historical, family or symbolic ties to that place.',
    'Conta criada. Confirme seu email e depois faça login.': 'Account created. Confirm your email and then log in.',
    'Contas, perfis, comentários, mensagens, coleções, debates e análise humana colaborativa.': 'Accounts, profiles, comments, messages, collections, debates and collaborative human analysis.',
    'Conversa criada.': 'Conversation created.',
    'Criar conversa': 'Create conversation',
    'Criar debate desta análise': 'Create a debate from this analysis',
    'Crie um projeto no Supabase, rode o SQL das tabelas sociais e adicione as chaves no Streamlit Secrets.': 'Create a project on Supabase, run the SQL for the social tables and add the keys to the Streamlit Secrets.',
    'Círculo criado.': 'Circle created.',
    'Círculos disponíveis': 'Available circles',
    'Debate criado.': 'Debate created.',
    'Descrição': 'Description',
    'Diagnóstico': 'Diagnosis',
    'Digite uma consulta ou escolha uma pergunta sugerida.': 'Type a query or pick a suggested question.',
    'Discussão atual': 'Current discussion',
    'Distribuição do sentimento': 'Sentiment distribution',
    'Distância entre a presença social/demográfica de um grupo e a atenção que ele recebe na cobertura jornalística.': "The gap between a group's social/demographic presence and the attention it receives in news coverage.",
    'Diáspora': 'Diaspora',
    'Enquadramentos': 'Frames',
    'Enquadramentos predominantes': 'Predominant frames',
    'Entrar neste círculo': 'Join this circle',
    'Entre ou crie uma conta para usar a camada colaborativa.': 'Log in or create an account to use the collaborative layer.',
    'Enviar': 'Send',
    'Erro': 'Error',
    'Erro ao comentar': 'Error while commenting',
    'Erro ao criar conta': 'Error while creating account',
    'Erro ao entrar': 'Error while logging in',
    'Erro ao enviar': 'Error while sending',
    'Erro ao salvar perfil': 'Error while saving profile',
    'Erro na busca semântica': 'Error in semantic search',
    'Escolha uma conversa': 'Choose a conversation',
    'Escolha uma notícia': 'Choose a news item',
    'Escrever comentário público': 'Write a public comment',
    'Esse número é uma verdade absoluta?': 'Is this number an absolute truth?',
    'Estatísticas indisponíveis agora.': 'Statistics unavailable right now.',
    'Fase': 'Phase',
    'Fontes jornalísticas, diversidade e baseline': 'Journalistic sources, diversity and baseline',
    'Fontes que mais aparecem na seleção': 'Sources that appear most in the selection',
    'Foram encontrados períodos sem cobertura no intervalo analisado.': 'Periods with no coverage were found within the analyzed range.',
    'Forma como a mídia organiza narrativamente um tema, destacando certos aspectos e apagando outros.': 'The way the media narratively organizes a topic, highlighting certain aspects and erasing others.',
    'Framing / enquadramento': 'Framing',
    'Gerar Story Mode com IA': 'Generate Story Mode with AI',
    'Hotspots de invisibilidade': 'Invisibility hotspots',
    'Indicador aproximado usado quando não há dado bilateral exato. Neste app, combina o tamanho global da diáspora de origem com o peso migratório do país de destino.': 'An approximate indicator used when there is no exact bilateral data. In this app, it combines the global size of the origin diaspora with the migratory weight of the destination country.',
    'Indicador que resume a tonalidade emocional das notícias. Valores negativos sugerem cobertura mais negativa; valores positivos sugerem cobertura mais positiva.': 'An indicator that summarizes the emotional tone of the news. Negative values suggest more negative coverage; positive values suggest more positive coverage.',
    'Invisibilidade': 'Invisibility',
    'Invisibilidade comparada em': 'Invisibility compared in',
    'Invisibilidade crítica': 'Critical invisibility',
    'Invisibilidade de': 'Invisibility of',
    'Invisibilidade midiática': 'Media invisibility',
    'Invisibilidade moderada': 'Moderate invisibility',
    'Justificativa': 'Justification',
    'Justificativa opcional': 'Optional justification',
    'Leia também: notícias com tom mais negativo': 'Read also: news with a more negative tone',
    'Leia também: notícias com tom mais positivo': 'Read also: news with a more positive tone',
    'Linha do tempo, pandemia e silêncio midiático': 'Timeline, pandemic and media silence',
    'Logado como': 'Logged in as',
    'Mapa crítico de invisibilidade': 'Critical map of invisibility',
    'Marcar todas como lidas': 'Mark all as read',
    'Media Diversity Index': 'Media Diversity Index',
    'Mesma comunidade em outros países': 'Same community in other countries',
    'Narrative Risk': 'Narrative Risk',
    'Nenhum dado disponível para a seleção.': 'No data available for the selection.',
    'Nenhum dado disponível para fontes e baseline.': 'No data available for sources and baseline.',
    'Nenhuma notícia disponível com os filtros atuais.': 'No news available with the current filters.',
    'Nenhuma notícia encontrada com esses filtros.': 'No news found with these filters.',
    'Nenhuma notícia filtrada para salvar.': 'No filtered news to save.',
    'Nenhuma notícia filtrada para votar framing.': 'No filtered news to vote on framing.',
    'Nenhuma recomendação disponível.': 'No recommendations available.',
    'Nenhuma seleção foi salva no histórico ainda. Use o botão na barra lateral.': 'No selection has been saved to the history yet. Use the button in the sidebar.',
    'Nota para salvar esta análise': 'Note to save this analysis',
    'Nota privada sobre a notícia': 'Private note about the news item',
    'Notícia para classificar': 'News item to classify',
    'Notícias': 'News',
    'Não foi possível criar a conta.': 'The account could not be created.',
    'Não foram detectados longos períodos de silêncio dentro do intervalo filtrado.': 'No long periods of silence were detected within the filtered range.',
    'Não há dados suficientes para o mapa crítico.': 'There is not enough data for the critical map.',
    'Não há notícias disponíveis para gerar insights com os filtros atuais.': 'There is no news available to generate insights with the current filters.',
    'Não há recomendações disponíveis para esta seleção.': 'There are no recommendations available for this selection.',
    'Não há tom médio disponível para esta seleção.': 'There is no average tone available for this selection.',
    'Não. Ele é um indicador comparativo. Serve para orientar análise crítica, não para substituir leitura qualitativa das notícias.': 'No. It is a comparative indicator. It is meant to guide critical analysis, not to replace qualitative reading of the news.',
    'O Narrative Risk Score combina invisibilidade, tom negativo, enquadramentos sensíveis e baixa diversidade de fontes.': 'The Narrative Risk Score combines invisibility, negative tone, sensitive frames and low source diversity.',
    'O que falta configurar?': 'What still needs to be configured?',
    'O índice aumenta quando há uma combinação de presença demográfica relevante e pouca cobertura midiática encontrada no corpus.': 'The index increases when there is a combination of relevant demographic presence and little media coverage found in the corpus.',
    'Outras comunidades no mesmo país': 'Other communities in the same country',
    'Pandemia': 'Pandemic',
    'País A': 'Country A',
    'País B': 'Country B',
    'País para comparação': 'Country for comparison',
    'Perfil atualizado.': 'Profile updated.',
    'Por que o risco narrativo pode ser alto?': 'Why can the narrative risk be high?',
    'Por que o índice pode ser alto?': 'Why can the index be high?',
    'Post publicado.': 'Post published.',
    'Postar no círculo': 'Post in the circle',
    'Proxy demográfico': 'Demographic proxy',
    'Pré-pandemia': 'Pre-pandemic',
    'Publicar no círculo': 'Publish in the circle',
    'Pós-pandemia': 'Post-pandemic',
    'Qual é o framing dominante?': 'What is the dominant framing?',
    'Radar da cobertura': 'Coverage radar',
    'Radar da cobertura e Narrative Risk Score': 'Coverage radar and Narrative Risk Score',
    'Ranking': 'Ranking',
    'Reflexão qualitativa': 'Qualitative reflection',
    'Reflexão salva.': 'Reflection saved.',
    'Relatório criado.': 'Report created.',
    'Relatório gerado automaticamente': 'Automatically generated report',
    'Risco narrativo alto': 'High narrative risk',
    'Risco narrativo baixo': 'Low narrative risk',
    'Risco narrativo crítico': 'Critical narrative risk',
    'Risco narrativo moderado': 'Moderate narrative risk',
    'Risco não calculável': 'Risk not computable',
    'Sair da conta': 'Log out',
    'Sala de aula, modo pesquisador, glossário e sobre': 'Classroom, researcher mode, glossary and about',
    'Salvar avaliação da IA': 'Save AI evaluation',
    'Salvar reflexão': 'Save reflection',
    'Seguidores': 'Followers',
    'Seguindo.': 'Now following.',
    'Seguir': 'Follow',
    'Sem dados para caso da semana.': 'No data for the case of the week.',
    'Sem notificações.': 'No notifications.',
    'Status de invisibilidade': 'Invisibility status',
    'Story Mode e relatórios': 'Story Mode and reports',
    'Sua posição': 'Your position',
    'Tema': 'Theme',
    'Texto inicial': 'Initial text',
    'Tornar reflexão pública': 'Make reflection public',
    'Título da reflexão': 'Reflection title',
    'Título do círculo': 'Circle title',
    'Título do relatório colaborativo': 'Collaborative report title',
    'URL do avatar/foto': 'Avatar/photo URL',
    'Username': 'Username',
    'Username da pessoa': "Person's username",
    'Usuário': 'User',
    'Usuário não encontrado.': 'User not found.',
    'Visibilidade × tom médio': 'Visibility × average tone',
    'Você ainda não tem conversas.': 'You have no conversations yet.',
    'Você entrou no círculo.': 'You joined the circle.',
    'Volume mensal': 'Monthly volume',
    'Votar framing': 'Vote on framing',
    'Votar no debate': 'Vote on the debate',
    'Voto registrado.': 'Vote recorded.',
    'Voto salvo.': 'Vote saved.',
    'Votos humanos de framing': 'Human framing votes',
    'em': 'in',
    'por país': 'by country',
    'Índice de invisibilidade': 'Invisibility index',
    '🌐 Camada colaborativa': '🌐 Collaborative layer',
    '🎤 Modo apresentação': '🎤 Presentation mode',
})


# Rótulos adicionais (radar, timeline, mensagens de IA)
UI_PT_EN.update({
    'Risco não disponível': 'Risk not available',
    'Volume': 'Volume',
    'Tom positivo': 'Positive tone',
    'Diversidade de enquadramentos': 'Frame diversity',
    'Presença temporal': 'Temporal presence',
    'Pandemia de Covid-19': 'Covid-19 pandemic',
    'Debates sobre racismo anti-asiático': 'Debates on anti-Asian racism',
    'Reabertura e reorganização migratória': 'Reopening and migratory reorganization',
    'Normalização pós-pandemia': 'Post-pandemic normalization',
    'Volume de cobertura': 'Coverage volume',
    'Não foi possível gerar o resumo por IA': 'The AI summary could not be generated',
    'Não foi possível gerar a narrativa por IA': 'The AI narrative could not be generated',
    'Resumo por IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit.': 'AI summary unavailable: add ANTHROPIC_API_KEY to the Streamlit Secrets.',
    'Story Mode com IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit.': 'AI Story Mode unavailable: add ANTHROPIC_API_KEY to the Streamlit Secrets.',
})


# Rótulos adicionais da camada social
UI_PT_EN.update({
    'automático': 'automatic',
    'Sem texto ainda.': 'No text yet.',
    'Reflexão': 'Reflection',
    'Você recebeu uma nova conversa.': 'You received a new conversation.',
    'Nova mensagem direta recebida.': 'New direct message received.',
    'começou a seguir você.': 'started following you.',
    'Seu comentário recebeu reação': 'Your comment received the reaction',
    'Você foi adicionado ao relatório': 'You were added to the report',
    'comentário': 'comment',
    'autor': 'author',
    'contexto': 'context',
    'reações': 'reactions',
    'comentários': 'comments',
})

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

