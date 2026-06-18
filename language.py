"""
Invisible Diasporas Lab — bilingual interface layer (Português / English).

This file keeps the app bilingual without requiring every UI string to be
manually rewritten. It provides:
- t(key): key-based translation
- ui(text): free-text Portuguese → English translation for visible labels/messages
- value_label(value): translated display labels for values while preserving internal data
- language_selector(): top-right language selector
- automatic Streamlit/Plotly patching so hardcoded visible strings also translate
"""

from __future__ import annotations

from functools import wraps
from typing import Any

import pandas as pd
import streamlit as st

LANGUAGES = {"pt": "Português", "en": "English"}
DEFAULT_LANG = "pt"
_PATCHED = False

TRANSLATIONS: dict[str, dict[str, str]] = {
    "ai_language": {"pt": "Português", "en": "English"},
    "page_badge": {"pt": "Invisible Diasporas Lab · Inteligência de visibilidade midiática", "en": "Invisible Diasporas Lab · Media visibility intelligence"},
    "hero_title": {"pt": "🌏 Monitor de Mídia da Diáspora Asiática", "en": "🌏 Asian Diaspora Media Monitor"},
    "hero_text": {
        "pt": "Um observatório interativo para analisar como a mídia global cobre as comunidades da diáspora asiática: tom, enquadramento, visibilidade e silêncio.",
        "en": "An interactive observatory to analyze how global media covers Asian diaspora communities: tone, framing, visibility and silence.",
    },
    "how_to_use_title": {"pt": "Como usar", "en": "How to use"},
    "how_to_use_text": {
        "pt": "Escolha uma comunidade, um país de destino, um sentimento e um período. Depois explore os painéis analíticos, a busca semântica, os relatórios e a camada colaborativa.",
        "en": "Choose a community, a destination country, a sentiment and a period. Then explore the analytical panels, semantic search, reports and collaborative layer.",
    },
    "sidebar_config": {"pt": "Configuração da análise", "en": "Analysis settings"},
    "presentation_mode": {"pt": "Modo apresentação", "en": "Presentation mode"},
    "usage_mode": {"pt": "Modo de uso", "en": "Usage mode"},
    "full_exploration": {"pt": "Exploração completa", "en": "Full exploration"},
    "classroom": {"pt": "Sala de aula", "en": "Classroom"},
    "researcher": {"pt": "Pesquisador", "en": "Researcher"},
    "executive_briefing": {"pt": "Briefing executivo", "en": "Executive briefing"},
    "main_filters": {"pt": "Filtros principais", "en": "Main filters"},
    "community_filter": {"pt": "Comunidade asiática", "en": "Asian community"},
    "country_filter": {"pt": "País de destino", "en": "Destination country"},
    "sentiment_filter": {"pt": "Sentimento", "en": "Sentiment"},
    "period_filter": {"pt": "Período", "en": "Period"},
    "tab_profile": {"pt": "Perfil 360", "en": "360 profile"},
    "tab_map": {"pt": "Mapa crítico", "en": "Critical map"},
    "tab_radar": {"pt": "Radar e risco", "en": "Radar & risk"},
    "tab_time": {"pt": "Tempo e silêncio", "en": "Time & silence"},
    "tab_sources": {"pt": "Fontes e baseline", "en": "Sources & baseline"},
    "tab_explorer": {"pt": "Explorador", "en": "Explorer"},
    "tab_comparisons": {"pt": "Comparações", "en": "Comparisons"},
    "tab_reports": {"pt": "Relatórios", "en": "Reports"},
    "tab_about": {"pt": "Sala, glossário e sobre", "en": "Classroom, glossary & about"},
    "profile_title": {"pt": "Perfil 360 da seleção", "en": "360 profile of the selection"},
    "news_count": {"pt": "Notícias filtradas", "en": "Filtered news"},
    "avg_tone": {"pt": "Tom médio", "en": "Average tone"},
    "dominant_frame": {"pt": "Enquadramento", "en": "Framing"},
    "source_diversity": {"pt": "Diversidade de fontes", "en": "Source diversity"},
    "tone_help": {"pt": "valores abaixo de 0 indicam cobertura mais negativa; valores próximos de 0 indicam tom neutro; valores acima de 0 indicam cobertura mais positiva.", "en": "values below 0 indicate more negative coverage; values near 0 indicate a neutral tone; values above 0 indicate more positive coverage."},
    "findings_cards": {"pt": "Cartões de achados", "en": "Finding cards"},
    "example_news": {"pt": "Notícias de exemplo", "en": "Example news"},
    "download_csv": {"pt": "Baixar dados da seleção em CSV", "en": "Download selected data as CSV"},
    "semantic_explorer": {"pt": "Explorador semântico e recomendações", "en": "Semantic explorer and recommendations"},
    "suggested_questions": {"pt": "Perguntas sugeridas", "en": "Suggested questions"},
    "search_input": {"pt": "Digite uma busca", "en": "Type a search query"},
    "search_placeholder": {"pt": "Ex.: trabalhadores filipinos no Golfo", "en": "Example: Filipino workers in the Gulf"},
    "results_number": {"pt": "Número de resultados", "en": "Number of results"},
    "relevant_results": {"pt": "Resultados mais relevantes", "en": "Most relevant results"},
    "profile_menu": {"pt": "👤 Meu perfil", "en": "👤 My profile"},
    "social_navigation": {"pt": "Navegação social", "en": "Social navigation"},
    "social_profile": {"pt": "Meu perfil", "en": "My profile"},
    "social_comments": {"pt": "Comentários e feed", "en": "Comments and feed"},
    "social_save": {"pt": "Salvar e coleções", "en": "Saved items and collections"},
    "social_framing": {"pt": "Framing e debates", "en": "Framing and debates"},
    "social_messages": {"pt": "Mensagens", "en": "Messages"},
    "social_circles": {"pt": "Círculos e relatórios", "en": "Circles and reports"},
    "social_diary": {"pt": "Diário, notificações e ranking", "en": "Diary, notifications and ranking"},
    "current_section": {"pt": "Seção atual", "en": "Current section"},
}

# Exact translations for UI strings, messages, chart titles and report sections.
UI_PT_EN: dict[str, str] = {
    # Sidebar / filters
    "Comunidade asiática": "Asian community",
    "País de destino": "Destination country",
    "Sentimento": "Sentiment",
    "Período": "Period",
    "Salvar seleção no histórico": "Save selection to history",
    "Configuração da análise": "Analysis settings",
    "Filtros principais": "Main filters",
    "Modo apresentação": "Presentation mode",
    "Modo de uso": "Usage mode",
    "Exploração completa": "Full exploration",
    "Sala de aula": "Classroom",
    "Pesquisador": "Researcher",
    "Briefing executivo": "Executive briefing",
    # Analysis headings
    "Perfil 360 da seleção": "360 profile of the selection",
    "Mapa crítico de invisibilidade": "Critical invisibility map",
    "Radar da cobertura e Narrative Risk Score": "Coverage radar and Narrative Risk Score",
    "Linha do tempo, pandemia e silêncio midiático": "Timeline, pandemic and media silence",
    "Fontes jornalísticas, diversidade e baseline": "News sources, diversity and baseline",
    "Explorador semântico e recomendações": "Semantic explorer and recommendations",
    "Comparações e rankings": "Comparisons and rankings",
    "Story Mode e relatórios": "Story Mode and reports",
    "Sala de aula, modo pesquisador, glossário e sobre": "Classroom, researcher mode, glossary and about",
    "Perfil 360": "360 profile",
    "Mapa crítico": "Critical map",
    "Radar e risco": "Radar & risk",
    "Tempo e silêncio": "Time & silence",
    "Fontes e baseline": "Sources & baseline",
    "Explorador": "Explorer",
    "Comparações": "Comparisons",
    "Relatórios": "Reports",
    "Sala, glossário e sobre": "Classroom, glossary & about",
    "Notícias filtradas": "Filtered news",
    "Tom médio": "Average tone",
    "Enquadramento": "Frame",
    "Diversidade de fontes": "Source diversity",
    "Distribuição do sentimento": "Sentiment distribution",
    "Enquadramentos predominantes": "Dominant frames",
    "Cartões de achados": "Finding cards",
    "Notícias de exemplo": "Example news",
    "Baixar dados da seleção em CSV": "Download selected data as CSV",
    "Resultados mais relevantes": "Most relevant results",
    "Perguntas sugeridas": "Suggested questions",
    "Digite uma busca": "Type a search query",
    "Ex.: trabalhadores filipinos no Golfo": "Example: Filipino workers in the Gulf",
    "Número de resultados": "Number of results",
    "Recomendações de leitura": "Reading recommendations",
    "Leia também: notícias com tom mais positivo": "Read also: news with a more positive tone",
    "Leia também: notícias com tom mais negativo": "Read also: news with a more negative tone",
    "Mesma comunidade em outros países": "Same community in other countries",
    "Outras comunidades no mesmo país": "Other communities in the same country",
    "Nenhuma recomendação disponível.": "No recommendation available.",
    "Não há recomendações disponíveis para esta seleção.": "No recommendations are available for this selection.",
    # Cards / chart labels
    "Data": "Date",
    "Fonte": "Source",
    "Tom": "Tone",
    "Abrir notícia": "Open article",
    "Notícias": "News",
    "Invisibilidade": "Invisibility",
    "Cobertura encontrada": "Coverage found",
    "Índice de invisibilidade": "Invisibility index",
    "Proxy demográfico": "Demographic proxy",
    "Top 5 hotspots críticos": "Top 5 critical hotspots",
    "Cobertura por fase histórica": "Coverage by historical phase",
    "Top fontes jornalísticas": "Top news sources",
    "Comparação com baseline geral": "Comparison with the general baseline",
    "Comparar duas comunidades no mesmo país": "Compare two communities in the same country",
    "Comparar uma comunidade em dois países": "Compare one community across two countries",
    "Ranking crítico": "Critical ranking",
    "Visibilidade × tom médio": "Visibility × average tone",
    "Relatório gerado automaticamente": "Automatically generated report",
    "Histórico de consultas nesta sessão": "Search history in this session",
    # Social layer / auth
    "Camada colaborativa": "Collaborative layer",
    "Conta social": "Social account",
    "Acesso": "Access",
    "Entrar": "Log in",
    "Criar conta": "Create account",
    "Sair": "Log out",
    "Sair da conta": "Log out",
    "Email": "Email",
    "Senha": "Password",
    "Nome": "Name",
    "Nome completo": "Full name",
    "Username": "Username",
    "Nome de usuário": "Username",
    "Bio": "Bio",
    "Instituição": "Institution",
    "Interesses": "Interests",
    "URL do avatar/foto": "Avatar/photo URL",
    "Salvar perfil": "Save profile",
    "Editar perfil": "Edit profile",
    "Meu perfil": "My profile",
    "Comentários e feed": "Comments and feed",
    "Salvar e coleções": "Saved items and collections",
    "Framing e debates": "Framing and debates",
    "Mensagens": "Messages",
    "Círculos e relatórios": "Circles and reports",
    "Diário, notificações e ranking": "Diary, notifications and ranking",
    "Navegação social": "Social navigation",
    "Seção atual": "Current section",
    "Comunidade e comentários da análise": "Community and comments on the analysis",
    "Salvar análises, notícias e coleções": "Save analyses, news and collections",
    "Framing colaborativo, debate e revisão humana da IA": "Collaborative framing, debate and human review of AI",
    "Mensagens diretas": "Direct messages",
    "Research Circles e relatórios colaborativos": "Research circles and collaborative reports",
    "Diário da diáspora, notificações e ranking": "Diaspora diary, notifications and ranking",
    "Salvar notícia da seleção": "Save article from the selection",
    "Comentários": "Comments",
    "Análises salvas": "Saved analyses",
    "Notícias salvas": "Saved news",
    "Minhas estatísticas": "My statistics",
    "Encontrar pesquisadores": "Find researchers",
    "Buscar por username, nome ou instituição": "Search by username, name or institution",
    "Seguir": "Follow",
    "Seguidores": "Followers",
    "Escrever comentário público": "Write a public comment",
    "Publicar comentário": "Post comment",
    "Feed geral da comunidade": "General community feed",
    "Mapa de vozes": "Voice map",
    "Comentários por país de destino": "Comments by destination country",
    "Nota para salvar esta análise": "Note for saving this analysis",
    "Salvar análise atual": "Save current analysis",
    "Nome da coleção": "Collection name",
    "Descrição": "Description",
    "Coleção pública": "Public collection",
    "Criar coleção": "Create collection",
    "Escolha uma notícia": "Choose an article",
    "Nota privada sobre a notícia": "Private note about the article",
    "Salvar notícia": "Save article",
    "Minhas análises e notícias salvas": "My saved analyses and articles",
    "Framing Battle: algoritmo × humanos": "Framing Battle: algorithm × humans",
    "Notícia para classificar": "Article to classify",
    "Qual é o framing dominante?": "What is the dominant frame?",
    "Justificativa opcional": "Optional justification",
    "Votar framing": "Vote on framing",
    "Votos humanos de framing": "Human framing votes",
    "Debate Mode": "Debate Mode",
    "Afirmação para debate": "Statement for debate",
    "Criar debate desta análise": "Create debate for this analysis",
    "Sua posição": "Your position",
    "Concordo": "Agree",
    "Discordo": "Disagree",
    "Depende": "It depends",
    "Justificativa": "Justification",
    "Votar no debate": "Vote in the debate",
    "Revisão humana de IA / Story Mode": "Human review of AI / Story Mode",
    "A IA interpretou bem?": "Did the AI interpret it well?",
    "Comentário sobre a interpretação da IA": "Comment on the AI interpretation",
    "Salvar avaliação da IA": "Save AI evaluation",
    "Nova conversa": "New conversation",
    "Username da pessoa": "Person's username",
    "Criar conversa": "Create conversation",
    "Escolha uma conversa": "Choose a conversation",
    "Mensagem": "Message",
    "Enviar": "Send",
    "Enviar mensagem": "Send message",
    "Criar círculo de pesquisa": "Create research circle",
    "Título do círculo": "Circle title",
    "Invisibilidade midiática": "Media invisibility",
    "Criar círculo": "Create circle",
    "Círculos disponíveis": "Available circles",
    "Entrar neste círculo": "Join this circle",
    "Postar no círculo": "Post in the circle",
    "Publicar no círculo": "Publish in the circle",
    "Título do relatório colaborativo": "Collaborative report title",
    "Criar relatório": "Create report",
    "Diário da diáspora": "Diaspora diary",
    "Título da reflexão": "Reflection title",
    "Reflexão qualitativa": "Qualitative reflection",
    "Tornar reflexão pública": "Make reflection public",
    "Salvar reflexão": "Save reflection",
    "Notificações": "Notifications",
    "Ranking de comentários úteis": "Useful comments ranking",
    # Status / messages
    "Perfil atualizado.": "Profile updated.",
    "Perfil salvo com sucesso.": "Profile saved successfully.",
    "Conta criada com sucesso.": "Account created successfully.",
    "Login realizado com sucesso.": "Logged in successfully.",
    "Conta criada. Confirme seu email e depois faça login.": "Account created. Confirm your email and then log in.",
    "Não foi possível criar a conta.": "The account could not be created.",
    "Comentário publicado.": "Comment posted.",
    "Ainda não há comentários nesta análise.": "There are no comments on this analysis yet.",
    "Análise salva.": "Analysis saved.",
    "Notícia salva.": "Article saved.",
    "Coleção criada.": "Collection created.",
    "Voto registrado.": "Vote registered.",
    "Debate criado.": "Debate created.",
    "Voto salvo.": "Vote saved.",
    "Avaliação salva.": "Evaluation saved.",
    "Conversa criada.": "Conversation created.",
    "Círculo criado.": "Circle created.",
    "Você entrou no círculo.": "You joined the circle.",
    "Relatório criado.": "Report created.",
    "Reflexão salva.": "Reflection saved.",
    "Sem notificações.": "No notifications.",
    "Ainda não há reações suficientes para ranking.": "There are not enough reactions for a ranking yet.",
    "Caso da semana indisponível.": "Case of the week unavailable.",
    "Nenhuma notícia filtrada para salvar.": "No filtered article to save.",
    "Nenhuma notícia filtrada para votar framing.": "No filtered article available for framing voting.",
    "Você ainda não tem conversas.": "You do not have conversations yet.",
    "Usuário não encontrado.": "User not found.",
    "Estatísticas indisponíveis agora.": "Statistics are currently unavailable.",
    "A camada social ainda não está configurada. Adicione SUPABASE_URL e SUPABASE_ANON_KEY nos Secrets do Streamlit.": "The social layer is not configured yet. Add SUPABASE_URL and SUPABASE_ANON_KEY to Streamlit Secrets.",
    "O que falta configurar?": "What still needs to be configured?",
    "Crie um projeto no Supabase, rode o SQL das tabelas sociais e adicione as chaves no Streamlit Secrets.": "Create a Supabase project, run the social tables SQL and add the keys to Streamlit Secrets.",
    # Method / glossary / researcher mode
    "Perguntas para discussão em sala": "Classroom discussion questions",
    "Modo pesquisador": "Researcher mode",
    "Glossário interativo": "Interactive glossary",
    "Sobre o projeto": "About the project",
    "Diáspora": "Diaspora",
    "Invisibilidade midiática": "Media invisibility",
    "Framing / enquadramento": "Framing",
    "Proxy demográfico": "Demographic proxy",
    "Busca semântica": "Semantic search",
    "Unidade de análise": "Unit of analysis",
    "Fonte jornalística": "News source",
    "Fonte demográfica": "Demographic source",
    "Variável de tom": "Tone variable",
    "Variável de invisibilidade": "Invisibility variable",
    "Classificação de framing": "Framing classification",
    "Limitação principal": "Main limitation",
}

# Replace fragments inside longer strings / f-strings / markdown / reports.
FRAGMENT_PT_EN: dict[str, str] = {
    "Resumo por IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit.": "AI summary unavailable: add ANTHROPIC_API_KEY to Streamlit Secrets.",
    "Story Mode com IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit.": "AI Story Mode unavailable: add ANTHROPIC_API_KEY to Streamlit Secrets.",
    "Não foi possível gerar o resumo por IA. Erro:": "Could not generate the AI summary. Error:",
    "Não foi possível gerar a narrativa por IA. Erro:": "Could not generate the AI narrative. Error:",
    "Não há tom médio disponível para esta seleção.": "There is no average tone available for this selection.",
    "A cobertura apresenta tom médio negativo.": "The coverage has a negative average tone.",
    "A cobertura apresenta tom médio positivo.": "The coverage has a positive average tone.",
    "A cobertura apresenta tom médio próximo de neutro.": "The coverage has an average tone close to neutral.",
    "Não há notícias disponíveis para gerar insights com os filtros atuais.": "There are no news items available to generate insights with the current filters.",
    "A seleção contém": "The selection contains",
    "notícias sobre": "news items about",
    "O enquadramento predominante identificado é:": "The dominant identified frame is:",
    "O diagnóstico de invisibilidade é:": "The invisibility diagnosis is:",
    "A diversidade de fontes é baixa: poucas fontes concentram a cobertura.": "Source diversity is low: a few sources concentrate the coverage.",
    "A cobertura apresenta alta diversidade de fontes jornalísticas.": "The coverage shows high diversity of news sources.",
    "A cobertura aparece distribuída entre": "Coverage is distributed between",
    "Não há cobertura suficiente para construir uma narrativa sobre": "There is not enough coverage to build a narrative about",
    "aparece no corpus por meio de": "appears in the corpus through",
    "notícias filtradas": "filtered news items",
    "O enquadramento predominante é": "The dominant frame is",
    "o que sugere que a cobertura tende a organizar essa comunidade principalmente a partir desse tema": "which suggests that coverage tends to organize this community mainly through this theme",
    "O tom médio da cobertura é": "The average tone of the coverage is",
    "portanto": "therefore",
    "O índice proxy de invisibilidade é": "The proxy invisibility index is",
    "classificado como": "classified as",
    "Isso indica que a visibilidade midiática deve ser interpretada em relação ao peso demográfico e não apenas ao número absoluto de notícias.": "This indicates that media visibility should be interpreted in relation to demographic weight, not only the absolute number of news items.",
    "Em termos comunicacionais": "In communication terms",
    "o resultado ajuda a observar se a mídia trata a diáspora como sujeito social complexo": "the result helps observe whether the media treats the diaspora as a complex social subject",
    "ou se ela aparece apenas em contextos específicos, como trabalho, crise, segurança, economia ou cultura.": "or whether it appears only in specific contexts such as labor, crisis, security, economy or culture.",
    "Não há dados suficientes para o mapa crítico.": "There is not enough data for the critical map.",
    "Nenhuma notícia encontrada com esses filtros.": "No news found with these filters.",
    "Nenhum dado disponível para a seleção.": "No data available for this selection.",
    "Nenhum dado disponível para fontes e baseline.": "No data available for sources and baseline.",
    "Nenhuma notícia disponível com os filtros atuais.": "No news available with the current filters.",
    "Erro na busca semântica:": "Semantic search error:",
    "Nenhuma seleção foi salva no histórico ainda. Use o botão na barra lateral.": "No selection has been saved in the history yet. Use the button in the sidebar.",
    "Pasta data não encontrada": "Data folder not found",
    "Banco SQLite não encontrado": "SQLite database not found",
    "Arquivo de embeddings não encontrado": "Embeddings file not found",
    "Camada social não instalada: adicione social_layer.py ao projeto.": "Social layer not installed: add social_layer.py to the project.",
    "Camada social temporariamente indisponível:": "Social layer temporarily unavailable:",
    "Erro ao entrar:": "Login error:",
    "Erro ao criar conta:": "Error creating account:",
    "Erro ao salvar perfil:": "Error saving profile:",
    "Erro ao comentar:": "Error commenting:",
    "Erro ao enviar:": "Error sending:",
    "Erro:": "Error:",
    "Usuário": "User",
    "Logado como": "Logged in as",
    "começou a seguir você.": "started following you.",
    "Seu comentário recebeu reação": "Your comment received reaction",
    "Você recebeu uma nova conversa.": "You received a new conversation.",
    "Nova mensagem direta recebida.": "New direct message received.",
    "Você foi adicionado ao relatório:": "You were added to the report:",
    "Caso crítico sugerido:": "Suggested critical case:",
    "comentários": "comments",
    "comentário": "comment",
    "reações": "reactions",
    # Report sections
    "## Seleção": "## Selection",
    "Comunidade:": "Community:",
    "País de destino:": "Destination country:",
    "Sentimento filtrado:": "Filtered sentiment:",
    "## Principais métricas": "## Main metrics",
    "Notícias encontradas:": "News found:",
    "Cobertura usada no índice:": "Coverage used in the index:",
    "Tom médio:": "Average tone:",
    "Enquadramento predominante:": "Dominant frame:",
    "Diversidade de fontes:": "Source diversity:",
    "Índice de invisibilidade:": "Invisibility index:",
    "Classificação do risco narrativo:": "Narrative risk classification:",
    "## 3 principais achados": "## 3 main findings",
    "## Recomendação de pesquisa": "## Research recommendation",
    "Investigar qualitativamente as notícias mais relevantes para entender se a comunidade é representada como sujeito social": "Qualitatively investigate the most relevant news items to understand whether the community is represented as a social subject",
    "como força de trabalho, como problema público, como ator econômico ou como presença cultural.": "as a workforce, as a public issue, as an economic actor or as a cultural presence.",
    "## Observação metodológica": "## Methodological note",
    "O índice comunidade × destino é um proxy comparativo.": "The community × destination index is a comparative proxy.",
    "Ele combina o tamanho global da diáspora de origem com o peso migratório do país de destino.": "It combines the global size of the origin diaspora with the migratory weight of the destination country.",
    "Ele não representa uma contagem bilateral exata de migrantes por origem e destino.": "It does not represent an exact bilateral count of migrants by origin and destination.",
}

VALUE_TRANSLATIONS: dict[str, str] = {
    # Sentiments / values
    "positivo": "positive",
    "negativo": "negative",
    "neutro": "neutral",
    "positive": "positive",
    "negative": "negative",
    "neutral": "neutral",
    # Frames
    "Trabalho e migração": "Labor and migration",
    "Racismo e discriminação": "Racism and discrimination",
    "Saúde e pandemia": "Health and pandemic",
    "Crime e segurança": "Crime and security",
    "Economia e negócios": "Economy and business",
    "Cultura e identidade": "Culture and identity",
    "Política internacional": "International politics",
    "Enquadramento geral": "General framing",
    # Risks
    "Risco não disponível": "Risk unavailable",
    "Risco não calculável": "Risk not calculable",
    "Invisibilidade crítica": "Critical invisibility",
    "Alta invisibilidade": "High invisibility",
    "Invisibilidade moderada": "Moderate invisibility",
    "Baixa invisibilidade": "Low invisibility",
    "Risco narrativo crítico": "Critical narrative risk",
    "Risco narrativo alto": "High narrative risk",
    "Risco narrativo moderado": "Moderate narrative risk",
    "Risco narrativo baixo": "Low narrative risk",
    # Periods and dimensions
    "Pré-pandemia": "Pre-pandemic",
    "Pandemia": "Pandemic",
    "Pós-pandemia": "Post-pandemic",
    "Volume": "Volume",
    "Tom positivo": "Positive tone",
    "Diversidade de fontes": "Source diversity",
    "Diversidade de enquadramentos": "Frame diversity",
    "Presença temporal": "Temporal presence",
    # Positions / ratings / reactions
    "Sim": "Yes",
    "Não": "No",
    "Parcialmente": "Partially",
    "Concordo": "Agree",
    "Discordo": "Disagree",
    "Depende": "It depends",
    "📌 útil": "📌 useful",
    "🤔 interessante": "🤔 interesting",
    "⚠️ revisar": "⚠️ review",
    "✅ concordo": "✅ agree",
    "🧠 insight": "🧠 insight",
    "não identificado": "not identified",
    "não disponível": "not available",
    "Fonte desconhecida": "Unknown source",
}


def get_lang() -> str:
    if "lang" not in st.session_state:
        st.session_state["lang"] = DEFAULT_LANG
    return st.session_state.get("lang", DEFAULT_LANG)


def t(key: str) -> str:
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    lang = get_lang()
    return entry.get(lang, entry.get(DEFAULT_LANG, key))


def value_label(value: Any) -> str:
    text = str(value)
    if get_lang() != "en":
        return text
    return VALUE_TRANSLATIONS.get(text, UI_PT_EN.get(text, text))


def ui(text: Any) -> Any:
    """Translate visible strings to English when English is selected."""
    if not isinstance(text, str) or get_lang() != "en":
        return text
    if text in UI_PT_EN:
        return UI_PT_EN[text]
    if text in VALUE_TRANSLATIONS:
        return VALUE_TRANSLATIONS[text]
    out = text
    # replace longer fragments first to avoid partial collisions
    merged = {**FRAGMENT_PT_EN, **UI_PT_EN, **VALUE_TRANSLATIONS}
    for pt, en in sorted(merged.items(), key=lambda kv: len(kv[0]), reverse=True):
        if pt in out:
            out = out.replace(pt, en)
    return out


def translate_options(options: Any):
    if isinstance(options, (list, tuple)):
        return options
    return options


def _translate_dataframe(data: Any) -> Any:
    if get_lang() != "en":
        return data
    try:
        if isinstance(data, pd.DataFrame):
            df = data.copy()
            df.columns = [ui(str(c)) for c in df.columns]
            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].map(lambda x: value_label(x) if isinstance(x, str) else x)
            return df
    except Exception:
        return data
    return data


def _translate_plotly_fig(fig: Any) -> Any:
    if get_lang() != "en":
        return fig
    try:
        if getattr(fig, "layout", None) is not None:
            if fig.layout.title and fig.layout.title.text:
                fig.update_layout(title_text=ui(fig.layout.title.text))
            if fig.layout.xaxis and fig.layout.xaxis.title and fig.layout.xaxis.title.text:
                fig.update_xaxes(title_text=ui(fig.layout.xaxis.title.text))
            if fig.layout.yaxis and fig.layout.yaxis.title and fig.layout.yaxis.title.text:
                fig.update_yaxes(title_text=ui(fig.layout.yaxis.title.text))
        for tr in getattr(fig, "data", []):
            if getattr(tr, "name", None):
                tr.name = value_label(tr.name)
    except Exception:
        pass
    return fig


def install_i18n_patches() -> None:
    """Patch common Streamlit and Plotly display calls after the language selector is rendered."""
    global _PATCHED
    if _PATCHED:
        return
    _PATCHED = True

    def patch_function(obj: Any, name: str, kind: str = "first_arg"):
        if not hasattr(obj, name):
            return
        original = getattr(obj, name)
        if getattr(original, "_i18n_patched", False):
            return

        @wraps(original)
        def wrapper(*args, **kwargs):
            args = list(args)
            if kind == "write":
                args = [ui(a) if isinstance(a, str) else a for a in args]
            elif kind == "dataframe":
                if args:
                    args[0] = _translate_dataframe(args[0])
                elif "data" in kwargs:
                    kwargs["data"] = _translate_dataframe(kwargs["data"])
            elif kind == "plotly_chart":
                if args:
                    args[0] = _translate_plotly_fig(args[0])
                elif "figure_or_data" in kwargs:
                    kwargs["figure_or_data"] = _translate_plotly_fig(kwargs["figure_or_data"])
            elif kind in {"select", "radio"}:
                if args and isinstance(args[0], str):
                    args[0] = ui(args[0])
                elif "label" in kwargs:
                    kwargs["label"] = ui(kwargs["label"])
                # Display translated labels but return original values.
                if "format_func" not in kwargs:
                    kwargs["format_func"] = lambda x: value_label(x)
            elif kind == "metric":
                if args and isinstance(args[0], str):
                    args[0] = ui(args[0])
                if len(args) > 1 and isinstance(args[1], str):
                    args[1] = value_label(args[1])
                if "label" in kwargs:
                    kwargs["label"] = ui(kwargs["label"])
                if "value" in kwargs and isinstance(kwargs["value"], str):
                    kwargs["value"] = value_label(kwargs["value"])
            else:
                if args and isinstance(args[0], str):
                    args[0] = ui(args[0])
                elif "label" in kwargs:
                    kwargs["label"] = ui(kwargs["label"])
                elif "body" in kwargs:
                    kwargs["body"] = ui(kwargs["body"])
                elif "text" in kwargs:
                    kwargs["text"] = ui(kwargs["text"])

                for key in ("placeholder", "help"):
                    if key in kwargs and isinstance(kwargs[key], str):
                        kwargs[key] = ui(kwargs[key])
            return original(*args, **kwargs)

        wrapper._i18n_patched = True
        setattr(obj, name, wrapper)

    # Patch top-level Streamlit calls.
    for nm in ["markdown", "subheader", "header", "title", "caption", "info", "warning", "success", "error"]:
        patch_function(st, nm)
    patch_function(st, "write", "write")
    patch_function(st, "dataframe", "dataframe")
    patch_function(st, "plotly_chart", "plotly_chart")
    for nm in ["button", "text_input", "text_area", "checkbox", "form_submit_button", "download_button", "popover", "toggle", "date_input", "slider"]:
        patch_function(st, nm)
    for nm in ["selectbox", "radio"]:
        patch_function(st, nm, "select")
    patch_function(st, "metric", "metric")

    # Patch DeltaGenerator methods (sidebar, columns, containers, forms, tabs, popovers).
    try:
        from streamlit.delta_generator import DeltaGenerator

        for nm in ["markdown", "subheader", "header", "title", "caption", "info", "warning", "success", "error"]:
            patch_function(DeltaGenerator, nm)
        patch_function(DeltaGenerator, "write", "write")
        patch_function(DeltaGenerator, "dataframe", "dataframe")
        patch_function(DeltaGenerator, "plotly_chart", "plotly_chart")
        for nm in ["button", "text_input", "text_area", "checkbox", "form_submit_button", "download_button", "popover", "toggle", "date_input", "slider"]:
            patch_function(DeltaGenerator, nm)
        for nm in ["selectbox", "radio"]:
            patch_function(DeltaGenerator, nm, "select")
        patch_function(DeltaGenerator, "metric", "metric")
    except Exception:
        pass

    # Patch Plotly Express constructors so titles/labels are translated before rendering.
    try:
        import plotly.express as px

        for nm in ["line", "bar", "pie", "scatter", "choropleth", "line_polar"]:
            if hasattr(px, nm):
                original = getattr(px, nm)
                if getattr(original, "_i18n_patched", False):
                    continue

                @wraps(original)
                def px_wrapper(*args, _original=original, **kwargs):
                    if "title" in kwargs and isinstance(kwargs["title"], str):
                        kwargs["title"] = ui(kwargs["title"])
                    if "labels" in kwargs and isinstance(kwargs["labels"], dict):
                        kwargs["labels"] = {k: ui(v) if isinstance(v, str) else v for k, v in kwargs["labels"].items()}
                    return _original(*args, **kwargs)

                px_wrapper._i18n_patched = True
                setattr(px, nm, px_wrapper)
    except Exception:
        pass


def language_selector() -> str:
    if "lang" not in st.session_state:
        st.session_state["lang"] = DEFAULT_LANG

    codes = list(LANGUAGES.keys())
    current_index = codes.index(st.session_state.get("lang", DEFAULT_LANG))
    choice = st.selectbox(
        "🌐",
        options=codes,
        index=current_index,
        format_func=lambda code: LANGUAGES.get(code, code),
        label_visibility="collapsed",
        key="lang_selectbox",
    )
    st.session_state["lang"] = choice
    install_i18n_patches()
    return choice



# ============================================================
# EXTRA COMPLETE UI TRANSLATIONS — generated final pass
# ============================================================

# These updates cover visible text that was still hardcoded in app.py and social_layer.py.
UI_PT_EN.update({
    # General / statuses
    "Risco não disponível": "Risk not available",
    "Risco não calculável": "Risk cannot be calculated",
    "Risco narrativo crítico": "Critical narrative risk",
    "Risco narrativo alto": "High narrative risk",
    "Risco narrativo moderado": "Moderate narrative risk",
    "Risco narrativo baixo": "Low narrative risk",
    "Invisibilidade crítica": "Critical invisibility",
    "Alta invisibilidade": "High invisibility",
    "Invisibilidade moderada": "Moderate invisibility",
    "Baixa invisibilidade": "Low invisibility",
    "Diagnóstico": "Diagnosis",
    "Principais achados": "Main findings",
    "Modo apresentação": "Presentation mode",
    "Story Mode": "Story Mode",
    "Narrative Risk": "Narrative Risk",
    "Cobertura encontrada": "Coverage found",
    "Índice de invisibilidade": "Invisibility index",
    "Proxy demográfico": "Demographic proxy",

    # Tone / insight sentences
    "Não há tom médio disponível para esta seleção.": "No average tone is available for this selection.",
    "A cobertura apresenta tom médio negativo.": "The coverage has a negative average tone.",
    "A cobertura apresenta tom médio positivo.": "The coverage has a positive average tone.",
    "A cobertura apresenta tom médio próximo de neutro.": "The coverage has an average tone close to neutral.",
    "Não há notícias disponíveis para gerar insights com os filtros atuais.": "There are no news items available to generate insights with the current filters.",
    "Não há cobertura suficiente para construir uma narrativa sobre": "There is not enough coverage to build a narrative about",
    "não identificado": "not identified",
    "não disponível": "not available",
    "Fonte desconhecida": "Unknown source",

    # App tabs / titles
    "Mapa crítico de invisibilidade": "Critical invisibility map",
    "Radar da cobertura e Narrative Risk Score": "Coverage radar and Narrative Risk Score",
    "Linha do tempo, pandemia e silêncio midiático": "Timeline, pandemic and media silence",
    "Fontes jornalísticas, diversidade e baseline": "News sources, diversity and baseline",
    "Comparações e rankings": "Comparisons and rankings",
    "Story Mode e relatórios": "Story Mode and reports",
    "Sala de aula, modo pesquisador, glossário e sobre": "Classroom, researcher mode, glossary and about",
    "Top 5 hotspots críticos": "Top 5 critical hotspots",
    "Eventos-chave para leitura da cobertura": "Key events for reading the coverage",
    "Antes, durante e depois da pandemia": "Before, during and after the pandemic",
    "Silence Detector": "Silence Detector",
    "Top fontes jornalísticas": "Top news sources",
    "Media Diversity Index": "Media Diversity Index",
    "Comparação com baseline geral": "Comparison with the general baseline",
    "Comparar duas comunidades no mesmo país": "Compare two communities in the same country",
    "Comparar uma comunidade em dois países": "Compare one community across two countries",
    "Visibilidade × tom": "Visibility × tone",
    "Visibilidade × tom médio": "Visibility × average tone",
    "Ranking crítico": "Critical ranking",
    "Executive Briefing": "Executive Briefing",
    "Relatório gerado automaticamente": "Automatically generated report",
    "Baixar briefing em Markdown": "Download briefing as Markdown",
    "Histórico de consultas nesta sessão": "Search history in this session",
    "Nenhuma seleção foi salva no histórico ainda. Use o botão na barra lateral.": "No selection has been saved to the history yet. Use the button in the sidebar.",
    "Nenhuma notícia encontrada com esses filtros.": "No news item was found with these filters.",
    "Não há dados suficientes para o mapa crítico.": "There is not enough data for the critical map.",
    "Nenhum dado disponível para a seleção.": "No data available for the selection.",
    "Nenhum dado disponível para fontes e baseline.": "No data available for sources and baseline.",
    "Digite uma consulta ou escolha uma pergunta sugerida.": "Type a query or choose a suggested question.",
    "Nenhuma notícia disponível com os filtros atuais.": "No news item is available with the current filters.",
    "Gerar Story Mode com IA": "Generate Story Mode with AI",
    "Narrativa por IA": "AI narrative",

    # Chart titles / labels
    "Distribuição do sentimento": "Sentiment distribution",
    "Enquadramentos predominantes": "Dominant frames",
    "Volume mensal": "Monthly volume",
    "Tom médio mensal da cobertura": "Monthly average tone of coverage",
    "Hotspots de invisibilidade": "Invisibility hotspots",
    "Radar da cobertura": "Coverage radar",
    "Volume": "Volume",
    "Tom positivo": "Positive tone",
    "Diversidade de enquadramentos": "Frame diversity",
    "Presença temporal": "Temporal presence",
    "Mês": "Month",
    "Número de notícias": "Number of news items",
    "Mês": "Month",
    "Fase": "Phase",
    "Cobertura por fase histórica": "Coverage by historical phase",
    "Fontes que mais aparecem na seleção": "Sources that appear most in the selection",
    "Invisibilidade comparada em": "Invisibility compared in",
    "Invisibilidade de": "Invisibility of",
    "Volume de cobertura": "Coverage volume",
    "Tom médio": "Average tone",

    # Comparison controls
    "País para comparação": "Country for comparison",
    "Comunidade A": "Community A",
    "Comunidade B": "Community B",
    "Comunidade para comparação entre países": "Community for country comparison",
    "País A": "Country A",
    "País B": "Country B",
    "Ranking": "Ranking",
    "Top 5 maior invisibilidade": "Top 5 highest invisibility",
    "Top 5 maior cobertura": "Top 5 highest coverage",
    "Top 5 menor invisibilidade": "Top 5 lowest invisibility",

    # Time / pandemic
    "Pré-pandemia": "Pre-pandemic",
    "Pandemia": "Pandemic",
    "Pós-pandemia": "Post-pandemic",
    "Pré-pandemia": "Pre-pandemic",
    "Pandemia de Covid-19": "Covid-19 pandemic",
    "Debates sobre racismo anti-asiático": "Debates on anti-Asian racism",
    "Reabertura e reorganização migratória": "Reopening and migratory reorganization",
    "Normalização pós-pandemia": "Post-pandemic normalization",
    "Foram encontrados períodos sem cobertura no intervalo analisado.": "Periods with no coverage were found in the analyzed interval.",
    "Não foram detectados longos períodos de silêncio dentro do intervalo filtrado.": "No long periods of silence were detected within the filtered interval.",

    # Researcher/classroom/glossary
    "Perguntas para discussão em sala": "Classroom discussion questions",
    "Modo pesquisador": "Researcher mode",
    "Glossário interativo": "Interactive glossary",
    "Sobre o projeto": "About the project",
    "O que significa uma comunidade ser numerosa, mas pouco coberta pela mídia?": "What does it mean for a community to be large but receive little media coverage?",
    "A cobertura negativa ainda pode ser considerada uma forma de visibilidade?": "Can negative coverage still be considered a form of visibility?",
    "Em quais contextos a mídia tende a tornar uma diáspora visível?": "In what contexts does the media tend to make a diaspora visible?",
    "Quais temas aparecem mais: cultura, trabalho, crise, crime, economia ou política?": "Which themes appear more often: culture, labor, crisis, crime, economy or politics?",
    "O silêncio midiático também é uma forma de representação?": "Is media silence also a form of representation?",
    "Que limitações existem ao transformar cobertura jornalística em números?": "What limitations exist when transforming news coverage into numbers?",
    "Unidade de análise": "Unit of analysis",
    "Fonte jornalística": "News source",
    "Fonte demográfica": "Demographic source",
    "Variável de tom": "Tone variable",
    "Variável de invisibilidade": "Invisibility variable",
    "Classificação de framing": "Framing classification",
    "Limitação principal": "Main limitation",
    "Descrição": "Description",
    "Elemento": "Element",
    "Diáspora": "Diaspora",
    "Framing / enquadramento": "Framing",
    "Busca semântica": "Semantic search",

    # Report
    "Seleção": "Selection",
    "Comunidade": "Community",
    "País de destino": "Destination country",
    "Sentimento filtrado": "Filtered sentiment",
    "Principais métricas": "Main metrics",
    "Notícias encontradas": "News found",
    "Cobertura usada no índice": "Coverage used in the index",
    "Enquadramento predominante": "Dominant frame",
    "Diversidade de fontes": "Source diversity",
    "Índice de invisibilidade": "Invisibility index",
    "Classificação do risco narrativo": "Narrative risk classification",
    "3 principais achados": "3 main findings",
    "Recomendação de pesquisa": "Research recommendation",
    "Observação metodológica": "Methodological note",

    # Social layer auth/account
    "Logado como": "Logged in as",
    "Sair da conta": "Log out",
    "Erro ao entrar": "Error logging in",
    "Erro ao criar conta": "Error creating account",
    "Username": "Username",
    "URL do avatar/foto": "Avatar/photo URL",
    "Perfil atualizado.": "Profile updated.",
    "Erro ao salvar perfil": "Error saving profile",
    "Encontrar pesquisadores": "Find researchers",
    "Buscar por username, nome ou instituição": "Search by username, name or institution",
    "Seguir": "Follow",
    "Seguindo.": "Following.",
    "Minhas estatísticas": "My statistics",
    "Comentários": "Comments",
    "Análises salvas": "Saved analyses",
    "Notícias salvas": "Saved news",
    "Seguidores": "Followers",
    "Estatísticas indisponíveis agora.": "Statistics are currently unavailable.",

    # Social comments/feed
    "Comunidade e comentários da análise": "Community and comments on the analysis",
    "Discussão atual": "Current discussion",
    "Escrever comentário público": "Write a public comment",
    "Publicar comentário": "Post comment",
    "Erro ao comentar": "Error commenting",
    "Ainda não há comentários nesta análise.": "There are no comments on this analysis yet.",
    "Usuário": "User",
    "Feed geral da comunidade": "General community feed",
    "Mapa de vozes": "Voice map",
    "Comentários por país de destino": "Comments by destination country",

    # Save/collections
    "Salvar análises, notícias e coleções": "Save analyses, news and collections",
    "Nota para salvar esta análise": "Note for saving this analysis",
    "Salvar análise atual": "Save current analysis",
    "Nome da coleção": "Collection name",
    "Coleção pública": "Public collection",
    "Criar coleção": "Create collection",
    "Coleção criada.": "Collection created.",
    "Salvar notícia da seleção": "Save article from the selection",
    "Nenhuma notícia filtrada para salvar.": "No filtered article to save.",
    "Escolha uma notícia": "Choose an article",
    "Nota privada sobre a notícia": "Private note about the article",
    "Salvar notícia": "Save article",
    "Minhas análises e notícias salvas": "My saved analyses and articles",

    # Framing/debates/AI review
    "Framing colaborativo, debate e revisão humana da IA": "Collaborative framing, debate and human review of AI",
    "Framing Battle: algoritmo × humanos": "Framing Battle: algorithm × humans",
    "Nenhuma notícia filtrada para votar framing.": "No filtered article available for framing voting.",
    "Notícia para classificar": "Article to classify",
    "Qual é o framing dominante?": "What is the dominant frame?",
    "Justificativa opcional": "Optional justification",
    "Votar framing": "Vote on framing",
    "Voto registrado.": "Vote registered.",
    "Votos humanos de framing": "Human framing votes",
    "Debate Mode": "Debate Mode",
    "Afirmação para debate": "Statement for debate",
    "Criar debate desta análise": "Create debate for this analysis",
    "Debate criado.": "Debate created.",
    "Sua posição": "Your position",
    "Justificativa": "Justification",
    "Votar no debate": "Vote in the debate",
    "Voto salvo.": "Vote saved.",
    "Revisão humana de IA / Story Mode": "Human review of AI / Story Mode",
    "A IA interpretou bem?": "Did the AI interpret it well?",
    "Sim": "Yes",
    "Parcialmente": "Partially",
    "Não": "No",
    "Comentário sobre a interpretação da IA": "Comment on the AI interpretation",
    "Salvar avaliação da IA": "Save AI evaluation",
    "Avaliação salva.": "Evaluation saved.",

    # Messages
    "Mensagens diretas": "Direct messages",
    "Nova conversa": "New conversation",
    "Username da pessoa": "Person's username",
    "Criar conversa": "Create conversation",
    "Usuário não encontrado.": "User not found.",
    "Você recebeu uma nova conversa.": "You received a new conversation.",
    "Conversa criada.": "Conversation created.",
    "Você ainda não tem conversas.": "You do not have conversations yet.",
    "Escolha uma conversa": "Choose a conversation",
    "Mensagem": "Message",
    "Enviar": "Send",
    "Nova mensagem direta recebida.": "New direct message received.",
    "Erro ao enviar": "Error sending",

    # Circles/reports
    "Research Circles e relatórios colaborativos": "Research circles and collaborative reports",
    "Criar círculo de pesquisa": "Create research circle",
    "Título do círculo": "Circle title",
    "Invisibilidade midiática": "Media invisibility",
    "Criar círculo": "Create circle",
    "Círculo criado.": "Circle created.",
    "Círculos disponíveis": "Available circles",
    "Entrar neste círculo": "Join this circle",
    "Você entrou no círculo.": "You joined the circle.",
    "Postar no círculo": "Post in the circle",
    "Publicar no círculo": "Publish in the circle",
    "Título do relatório colaborativo": "Collaborative report title",
    "Criar relatório": "Create report",
    "Relatório criado.": "Report created.",
    "Relatório": "Report",
    "Sem texto ainda.": "No text yet.",
    "Você foi adicionado ao relatório": "You were added to the report",

    # Diary/notifications/ranking
    "Diário da diáspora, notificações e ranking": "Diaspora diary, notifications and ranking",
    "Diário da diáspora": "Diaspora diary",
    "Título da reflexão": "Reflection title",
    "Reflexão qualitativa": "Qualitative reflection",
    "Tornar reflexão pública": "Make reflection public",
    "Salvar reflexão": "Save reflection",
    "Reflexão salva.": "Reflection saved.",
    "Notificações": "Notifications",
    "Marcar todas como lidas": "Mark all as read",
    "Sem notificações.": "No notifications.",
    "Ranking de comentários úteis": "Useful comments ranking",
    "Ainda não há reações suficientes para ranking.": "There are not enough reactions for a ranking yet.",
    "Caso crítico sugerido": "Suggested critical case",
    "Sem dados para caso da semana.": "No data for the case of the week.",
    "Caso da semana indisponível.": "Case of the week unavailable.",

    # Common errors
    "Erro": "Error",
    "Erro:": "Error:",
    "Erro ao comentar": "Error commenting",
    "Erro ao salvar perfil": "Error saving profile",
    "Erro ao enviar": "Error sending",
})

VALUE_TRANSLATIONS.update({
    "Trabalho e migração": "Labor and migration",
    "Racismo e discriminação": "Racism and discrimination",
    "Saúde e pandemia": "Health and pandemic",
    "Crime e segurança": "Crime and security",
    "Economia e negócios": "Economy and business",
    "Cultura e identidade": "Culture and identity",
    "Política internacional": "International politics",
    "Enquadramento geral": "General framing",
    "Invisibilidade crítica": "Critical invisibility",
    "Alta invisibilidade": "High invisibility",
    "Invisibilidade moderada": "Moderate invisibility",
    "Baixa invisibilidade": "Low invisibility",
    "Risco narrativo crítico": "Critical narrative risk",
    "Risco narrativo alto": "High narrative risk",
    "Risco narrativo moderado": "Moderate narrative risk",
    "Risco narrativo baixo": "Low narrative risk",
    "Risco não disponível": "Risk not available",
    "Risco não calculável": "Risk cannot be calculated",
    "Pré-pandemia": "Pre-pandemic",
    "Pandemia": "Pandemic",
    "Pós-pandemia": "Post-pandemic",
    "positivo": "positive",
    "negativo": "negative",
    "neutro": "neutral",
    "📌 útil": "📌 useful",
    "🤔 interessante": "🤔 interesting",
    "⚠️ revisar": "⚠️ review",
    "✅ concordo": "✅ agree",
    "🧠 insight": "🧠 insight",
    "Sim": "Yes",
    "Parcialmente": "Partially",
    "Não": "No",
    "Concordo": "Agree",
    "Discordo": "Disagree",
    "Depende": "It depends",
})

FRAGMENT_PT_EN.update({
    # AI / generated text
    "Resumo por IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit.": "AI summary unavailable: add ANTHROPIC_API_KEY to Streamlit Secrets.",
    "Story Mode com IA indisponível: adicione ANTHROPIC_API_KEY nos Secrets do Streamlit.": "AI Story Mode unavailable: add ANTHROPIC_API_KEY to Streamlit Secrets.",
    "Não foi possível gerar o resumo por IA. Erro:": "Could not generate the AI summary. Error:",
    "Não foi possível gerar a narrativa por IA. Erro:": "Could not generate the AI narrative. Error:",
    "Não há notícias disponíveis para gerar insights com os filtros atuais.": "There are no news items available to generate insights with the current filters.",
    "A seleção contém": "The selection contains",
    "notícias sobre": "news items about",
    "O enquadramento predominante identificado é:": "The dominant identified frame is:",
    "O diagnóstico de invisibilidade é:": "The invisibility diagnosis is:",
    "A diversidade de fontes é baixa: poucas fontes concentram a cobertura.": "Source diversity is low: a few sources concentrate the coverage.",
    "A cobertura apresenta alta diversidade de fontes jornalísticas.": "The coverage shows high diversity of news sources.",
    "A cobertura aparece distribuída entre": "Coverage is distributed between",
    "Não há cobertura suficiente para construir uma narrativa sobre": "There is not enough coverage to build a narrative about",
    "A comunidade": "The community",
    "aparece no corpus por meio de": "appears in the corpus through",
    "notícias filtradas": "filtered news items",
    "O enquadramento predominante é": "The dominant frame is",
    "o que sugere que a cobertura tende a organizar essa comunidade principalmente a partir desse tema.": "which suggests that coverage tends to organize this community mainly around this theme.",
    "O tom médio da cobertura é": "The average tone of coverage is",
    "portanto": "therefore",
    "O índice proxy de invisibilidade é": "The proxy invisibility index is",
    "classificado como": "classified as",
    "Isso indica que a visibilidade midiática deve ser interpretada em relação ao peso demográfico e não apenas ao número absoluto de notícias.": "This indicates that media visibility should be interpreted in relation to demographic weight and not only the absolute number of news items.",
    "Em termos comunicacionais": "In communication terms",
    "o resultado ajuda a observar se a mídia trata a diáspora como sujeito social complexo": "the result helps observe whether the media treats the diaspora as a complex social subject",
    "ou se ela aparece apenas em contextos específicos, como trabalho, crise, segurança, economia ou cultura.": "or whether it only appears in specific contexts such as labor, crisis, security, economy or culture.",

    # Report text
    "## Seleção": "## Selection",
    "## Principais métricas": "## Main metrics",
    "## 3 principais achados": "## 3 main findings",
    "## Recomendação de pesquisa": "## Research recommendation",
    "## Observação metodológica": "## Methodological note",
    "Comunidade:": "Community:",
    "País de destino:": "Destination country:",
    "Sentimento filtrado:": "Filtered sentiment:",
    "Notícias encontradas:": "News found:",
    "Cobertura usada no índice:": "Coverage used in the index:",
    "Tom médio:": "Average tone:",
    "Enquadramento predominante:": "Dominant frame:",
    "Diversidade de fontes:": "Source diversity:",
    "Proxy demográfico:": "Demographic proxy:",
    "Índice de invisibilidade:": "Invisibility index:",
    "Classificação do risco narrativo:": "Narrative risk classification:",
    "Investigar qualitativamente as notícias mais relevantes para entender se a comunidade é representada como sujeito social": "Qualitatively investigate the most relevant news items to understand whether the community is represented as a social subject",
    "como força de trabalho, como problema público, como ator econômico ou como presença cultural.": "as a workforce, as a public issue, as an economic actor or as a cultural presence.",
    "O índice comunidade × destino é um proxy comparativo.": "The community × destination index is a comparative proxy.",
    "Ele combina o tamanho global da diáspora de origem com o peso migratório do país de destino.": "It combines the global size of the origin diaspora with the migratory weight of the destination country.",
    "Ele não representa uma contagem bilateral exata de migrantes por origem e destino.": "It does not represent an exact bilateral count of migrants by origin and destination.",

    # Long method boxes / explanations
    "O mapa mostra hotspots de invisibilidade por país de destino.": "The map shows invisibility hotspots by destination country.",
    "Países mais escuros indicam maior invisibilidade relativa.": "Darker countries indicate higher relative invisibility.",
    "O índice aumenta quando há uma combinação de presença demográfica relevante e pouca cobertura midiática encontrada no corpus.": "The index increases when relevant demographic presence combines with little media coverage found in the corpus.",
    "O Narrative Risk Score combina invisibilidade, tom negativo, enquadramentos sensíveis e baixa diversidade de fontes.": "The Narrative Risk Score combines invisibility, negative tone, sensitive frames and low source diversity.",
    "Não. Ele é um indicador comparativo. Serve para orientar análise crítica, não para substituir leitura qualitativa das notícias.": "No. It is a comparative indicator. It helps guide critical analysis, not replace qualitative reading of the news.",
    "Valores abaixo de 0 indicam cobertura mais negativa": "Values below 0 indicate more negative coverage",
    "valores próximos de 0 indicam tom neutro": "values close to 0 indicate neutral tone",
    "valores acima de 0 indicam cobertura mais positiva": "values above 0 indicate more positive coverage",

    # Social fragments/errors
    "Logado como": "Logged in as",
    "Erro ao entrar:": "Error logging in:",
    "Erro ao criar conta:": "Error creating account:",
    "Erro ao salvar perfil:": "Error saving profile:",
    "Erro ao comentar:": "Error commenting:",
    "Erro ao enviar:": "Error sending:",
    "Erro:": "Error:",
    "em": "in",
    "começou a seguir você.": "started following you.",
    "Seu comentário recebeu reação": "Your comment received reaction",
    "Você recebeu uma nova conversa.": "You received a new conversation.",
    "Nova mensagem direta recebida.": "New direct message received.",
    "Você foi adicionado ao relatório:": "You were added to the report:",
    "automático:": "automatic:",
    "Comentários por país de destino": "Comments by destination country",
    "comentários": "comments",
    "reações": "reactions",
    "votos": "votes",
    "tom médio": "average tone",
})

# Extra Portuguese fragments that appear inside markdown/html strings.
# They are intentionally fragment-based because many visible strings are f-strings.
_MORE_FRAGMENT_TRANSLATIONS = {
    "Notícias": "News",
    "Fonte": "Source",
    "Data": "Date",
    "Tom": "Tone",
    "Enquadramento": "Frame",
    "Abrir notícia": "Open article",
    "Comunidade": "Community",
    "Destino": "Destination",
    "Sentimento": "Sentiment",
    "Invisibilidade": "Invisibility",
    "Cobertura": "Coverage",
    "cobertura": "coverage",
    "mídia": "media",
    "jornalística": "news",
    "jornalísticas": "news",
    "midiática": "media",
    "midiático": "media",
    "diáspora": "diaspora",
    "diásporas": "diasporas",
    "asiática": "Asian",
    "asiáticas": "Asian",
    "país": "country",
    "países": "countries",
    "comunidade": "community",
    "comunidades": "communities",
    "fontes": "sources",
    "dados": "data",
    "análise": "analysis",
    "análises": "analyses",
    "notícia": "article",
    "notícias": "news items",
    "salvas": "saved",
    "salvo": "saved",
    "salva": "saved",
    "criada": "created",
    "criado": "created",
    "atual": "current",
    "atualizado": "updated",
    "reflexão": "reflection",
    "relatório": "report",
    "relatórios": "reports",
    "mensagem": "message",
    "mensagens": "messages",
    "coleção": "collection",
    "coleções": "collections",
    "círculo": "circle",
    "círculos": "circles",
    "debate": "debate",
    "debates": "debates",
    "ranking": "ranking",
}
for _pt, _en in _MORE_FRAGMENT_TRANSLATIONS.items():
    FRAGMENT_PT_EN.setdefault(_pt, _en)


# Upgrade the display translator so it also translates several fixed Portuguese UI fragments
# that are built dynamically, without changing internal database values.
_OLD_UI_FUNC = ui
def ui(text: Any) -> Any:  # type: ignore[override]
    if not isinstance(text, str) or get_lang() != "en":
        return text
    if text in UI_PT_EN:
        return UI_PT_EN[text]
    if text in VALUE_TRANSLATIONS:
        return VALUE_TRANSLATIONS[text]
    out = text
    merged = {**FRAGMENT_PT_EN, **UI_PT_EN, **VALUE_TRANSLATIONS}
    for pt, en in sorted(merged.items(), key=lambda kv: len(str(kv[0])), reverse=True):
        if isinstance(pt, str) and pt in out:
            out = out.replace(pt, str(en))
    return out

def value_label(value: Any) -> str:  # type: ignore[override]
    text = str(value)
    if get_lang() != "en":
        return text
    if text in VALUE_TRANSLATIONS:
        return VALUE_TRANSLATIONS[text]
    if text in UI_PT_EN:
        return UI_PT_EN[text]
    return ui(text)


# Add extra patches for Streamlit elements that were not covered by the first patcher.
_OLD_INSTALL_I18N_PATCHES = install_i18n_patches
_EXTRA_PATCHED = False

def install_i18n_patches() -> None:  # type: ignore[override]
    global _EXTRA_PATCHED
    _OLD_INSTALL_I18N_PATCHES()
    if _EXTRA_PATCHED:
        return
    _EXTRA_PATCHED = True

    def patch_function(obj: Any, name: str, kind: str = "first_arg"):
        if not hasattr(obj, name):
            return
        original = getattr(obj, name)
        if getattr(original, "_i18n_extra_patched", False):
            return

        @wraps(original)
        def wrapper(*args, **kwargs):
            args = list(args)
            if kind == "tabs":
                if args and isinstance(args[0], (list, tuple)):
                    args[0] = [ui(x) if isinstance(x, str) else x for x in args[0]]
                elif "tabs" in kwargs and isinstance(kwargs["tabs"], (list, tuple)):
                    kwargs["tabs"] = [ui(x) if isinstance(x, str) else x for x in kwargs["tabs"]]
            elif kind in {"select", "radio", "multiselect"}:
                if args and isinstance(args[0], str):
                    args[0] = ui(args[0])
                elif "label" in kwargs and isinstance(kwargs["label"], str):
                    kwargs["label"] = ui(kwargs["label"])
                if "format_func" not in kwargs:
                    kwargs["format_func"] = lambda x: value_label(x)
            else:
                if args and isinstance(args[0], str):
                    args[0] = ui(args[0])
                elif "label" in kwargs and isinstance(kwargs["label"], str):
                    kwargs["label"] = ui(kwargs["label"])
                elif "body" in kwargs and isinstance(kwargs["body"], str):
                    kwargs["body"] = ui(kwargs["body"])
                elif "text" in kwargs and isinstance(kwargs["text"], str):
                    kwargs["text"] = ui(kwargs["text"])
                for key in ("placeholder", "help"):
                    if key in kwargs and isinstance(kwargs[key], str):
                        kwargs[key] = ui(kwargs[key])
            return original(*args, **kwargs)

        wrapper._i18n_extra_patched = True
        setattr(obj, name, wrapper)

    for nm in ["expander", "popover"]:
        patch_function(st, nm)
    patch_function(st, "tabs", "tabs")
    for nm in ["selectbox", "radio", "multiselect"]:
        patch_function(st, nm, "select")

    try:
        from streamlit.delta_generator import DeltaGenerator
        for nm in ["expander", "popover"]:
            patch_function(DeltaGenerator, nm)
        for nm in ["selectbox", "radio", "multiselect"]:
            patch_function(DeltaGenerator, nm, "select")
    except Exception:
        pass

    # Strengthen Plotly Express translation: translate title, labels and object/category values.
    try:
        import plotly.express as px

        for nm in ["line", "bar", "pie", "scatter", "choropleth", "line_polar"]:
            if not hasattr(px, nm):
                continue
            original = getattr(px, nm)
            if getattr(original, "_i18n_complete_patched", False):
                continue

            @wraps(original)
            def px_wrapper(*args, _original=original, **kwargs):
                args = list(args)
                if args and isinstance(args[0], pd.DataFrame):
                    args[0] = _translate_dataframe(args[0])
                if "data_frame" in kwargs and isinstance(kwargs["data_frame"], pd.DataFrame):
                    kwargs["data_frame"] = _translate_dataframe(kwargs["data_frame"])
                if "title" in kwargs and isinstance(kwargs["title"], str):
                    kwargs["title"] = ui(kwargs["title"])
                if "labels" in kwargs and isinstance(kwargs["labels"], dict):
                    kwargs["labels"] = {k: ui(v) if isinstance(v, str) else v for k, v in kwargs["labels"].items()}
                return _original(*args, **kwargs)

            px_wrapper._i18n_complete_patched = True
            setattr(px, nm, px_wrapper)
    except Exception:
        pass

