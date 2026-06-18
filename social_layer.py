"""
Invisible Diasporas Lab — Camada social colaborativa para Streamlit + Supabase.

Como usar no app.py:
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
"""

from __future__ import annotations

import re
from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.express as px
import streamlit as st
from supabase import create_client, Client

from language import t

SOCIAL_FRAMES = [
    "Trabalho e migração",
    "Racismo e discriminação",
    "Saúde e pandemia",
    "Crime e segurança",
    "Economia e negócios",
    "Cultura e identidade",
    "Política internacional",
    "Enquadramento geral",
]

REACTIONS = ["📌 útil", "🤔 interessante", "⚠️ revisar", "✅ concordo", "🧠 insight"]


def _slug(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9áéíóúâêôãõç]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "na"


def make_analysis_key(community: str, country: str, sentiment: str, start_date: Any, end_date: Any) -> str:
    return "|".join([
        _slug(community),
        _slug(country),
        _slug(sentiment),
        str(start_date),
        str(end_date),
    ])


def get_configured() -> bool:
    try:
        return bool(st.secrets.get("SUPABASE_URL")) and bool(st.secrets.get("SUPABASE_ANON_KEY"))
    except Exception:
        return False


def new_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


def get_sb() -> Optional[Client]:
    if not get_configured():
        return None
    if "sb_client" not in st.session_state:
        st.session_state["sb_client"] = new_supabase_client()
    return st.session_state["sb_client"]


def current_user() -> Optional[Dict[str, Any]]:
    return st.session_state.get("social_user")


def current_user_id() -> Optional[str]:
    user = current_user()
    return user.get("id") if user else None


def safe_data(resp: Any) -> List[Dict[str, Any]]:
    try:
        return resp.data or []
    except Exception:
        return []


def notify_user(sb: Client, user_id: str, type_: str, body: str) -> None:
    if not user_id:
        return
    try:
        sb.table("notifications").insert({
            "user_id": user_id,
            "type": type_,
            "body": body,
        }).execute()
    except Exception:
        pass


def ensure_profile(sb: Client, user_id: str, email: str = "") -> None:
    profile = safe_data(sb.table("profiles").select("id").eq("id", user_id).limit(1).execute())
    if profile:
        return

    base_username = (email.split("@")[0] if email else f"user_{user_id[:8]}").lower()
    username = re.sub(r"[^a-z0-9_]+", "_", base_username).strip("_") or f"user_{user_id[:8]}"

    try:
        sb.table("profiles").insert({
            "id": user_id,
            "username": username,
            "full_name": username,
            "bio": "",
            "institution": "",
            "interests": "",
        }).execute()
    except Exception:
        pass


def get_profile(sb: Client, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    user_id = user_id or current_user_id()
    if not user_id:
        return None
    data = safe_data(sb.table("profiles").select("*").eq("id", user_id).limit(1).execute())
    return data[0] if data else None


def render_auth_box() -> bool:
    """Returns True when the user is logged in."""
    if not get_configured():
        st.warning("A camada social ainda não está configurada. Adicione SUPABASE_URL e SUPABASE_ANON_KEY nos Secrets do Streamlit.")
        with st.expander("O que falta configurar?"):
            st.write("Crie um projeto no Supabase, rode o SQL das tabelas sociais e adicione as chaves no Streamlit Secrets.")
        return False

    sb = get_sb()
    user = current_user()

    if user:
        profile = get_profile(sb, user["id"])
        name = profile.get("full_name") or profile.get("username") if profile else user.get("email")
        st.sidebar.success(f"Logado como {name}")
        if st.sidebar.button("Sair da conta"):
            try:
                sb.auth.sign_out()
            except Exception:
                pass
            for key in ["social_user", "sb_client"]:
                st.session_state.pop(key, None)
            st.rerun()
        return True

    st.sidebar.markdown("---")
    st.sidebar.subheader("Conta social")
    mode = st.sidebar.radio("Acesso", ["Entrar", "Criar conta"], horizontal=True)
    email = st.sidebar.text_input("Email", key="social_email")
    password = st.sidebar.text_input("Senha", type="password", key="social_password")

    if mode == "Entrar":
        if st.sidebar.button("Entrar"):
            try:
                resp = sb.auth.sign_in_with_password({"email": email, "password": password})
                user_obj = resp.user
                if user_obj:
                    st.session_state["social_user"] = {"id": user_obj.id, "email": user_obj.email}
                    ensure_profile(sb, user_obj.id, user_obj.email or email)
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"Erro ao entrar: {e}")
    else:
        username = st.sidebar.text_input("Username", key="signup_username")
        full_name = st.sidebar.text_input("Nome", key="signup_fullname")
        if st.sidebar.button("Criar conta"):
            try:
                resp = sb.auth.sign_up({"email": email, "password": password})
                user_obj = resp.user
                session_obj = getattr(resp, "session", None)
                if user_obj and session_obj:
                    st.session_state["social_user"] = {"id": user_obj.id, "email": user_obj.email}
                    ensure_profile(sb, user_obj.id, user_obj.email or email)
                    sb.table("profiles").update({
                        "username": username or (email.split("@")[0] if email else None),
                        "full_name": full_name or username or email,
                    }).eq("id", user_obj.id).execute()
                    st.rerun()
                elif user_obj:
                    st.sidebar.info("Conta criada. Confirme seu email e depois faça login.")
                else:
                    st.sidebar.warning("Não foi possível criar a conta.")
            except Exception as e:
                st.sidebar.error(f"Erro ao criar conta: {e}")

    return False


def render_profile_tab(sb: Client) -> None:
    st.subheader("Meu perfil")
    user_id = current_user_id()
    profile = get_profile(sb, user_id) or {}

    with st.form("edit_profile"):
        username = st.text_input("Username", value=profile.get("username") or "")
        full_name = st.text_input("Nome completo", value=profile.get("full_name") or "")
        institution = st.text_input("Instituição", value=profile.get("institution") or "")
        interests = st.text_area("Interesses", value=profile.get("interests") or "")
        bio = st.text_area("Bio", value=profile.get("bio") or "")
        avatar_url = st.text_input("URL do avatar/foto", value=profile.get("avatar_url") or "")
        submitted = st.form_submit_button("Salvar perfil")

    if submitted:
        try:
            sb.table("profiles").update({
                "username": username,
                "full_name": full_name,
                "institution": institution,
                "interests": interests,
                "bio": bio,
                "avatar_url": avatar_url,
            }).eq("id", user_id).execute()
            st.success("Perfil atualizado.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar perfil: {e}")

    st.markdown("### Encontrar pesquisadores")
    query = st.text_input("Buscar por username, nome ou instituição")
    if query:
        users = safe_data(
            sb.table("profiles")
            .select("id, username, full_name, institution, interests, bio")
            .or_(f"username.ilike.%{query}%,full_name.ilike.%{query}%,institution.ilike.%{query}%")
            .limit(20)
            .execute()
        )
        for p in users:
            if p["id"] == user_id:
                continue
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{p.get('full_name') or p.get('username')}** · @{p.get('username')}  ")
                st.caption(f"{p.get('institution') or ''} · {p.get('interests') or ''}")
            with col2:
                if st.button("Seguir", key=f"follow_{p['id']}"):
                    try:
                        sb.table("follows").upsert({"follower_id": user_id, "followee_id": p["id"]}).execute()
                        notify_user(sb, p["id"], "follow", f"@{profile.get('username')} começou a seguir você.")
                        st.success("Seguindo.")
                    except Exception as e:
                        st.error(f"Erro: {e}")

    st.markdown("### Minhas estatísticas")
    c1, c2, c3, c4 = st.columns(4)
    try:
        comments = len(safe_data(sb.table("analysis_comments").select("id").eq("user_id", user_id).execute()))
        saved = len(safe_data(sb.table("saved_analyses").select("id").eq("user_id", user_id).execute()))
        articles = len(safe_data(sb.table("saved_articles").select("id").eq("user_id", user_id).execute()))
        followers = len(safe_data(sb.table("follows").select("follower_id").eq("followee_id", user_id).execute()))
        c1.metric("Comentários", comments)
        c2.metric("Análises salvas", saved)
        c3.metric("Notícias salvas", articles)
        c4.metric("Seguidores", followers)
    except Exception:
        st.info("Estatísticas indisponíveis agora.")


def render_comments_tab(sb: Client, context: Dict[str, Any]) -> None:
    st.subheader("Comunidade e comentários da análise")
    analysis_key = context["analysis_key"]
    user_id = current_user_id()
    profile = get_profile(sb, user_id) or {}

    st.markdown(
        f"**Discussão atual:** {context['community']} · {context['country']} · {context['sentiment']}"
    )

    with st.form("new_comment"):
        comment_text = st.text_area("Escrever comentário público")
        submitted = st.form_submit_button("Publicar comentário")
    if submitted and comment_text.strip():
        try:
            sb.table("analysis_comments").insert({
                "user_id": user_id,
                "community": context["community"],
                "destination_country": context["country"],
                "sentiment": context["sentiment"],
                "analysis_key": analysis_key,
                "comment_text": comment_text.strip(),
            }).execute()
            st.success("Comentário publicado.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao comentar: {e}")

    comments = safe_data(
        sb.table("analysis_comments")
        .select("id, user_id, comment_text, created_at, community, destination_country, sentiment, profiles(username, full_name, institution)")
        .eq("analysis_key", analysis_key)
        .order("created_at", desc=True)
        .limit(50)
        .execute()
    )

    if not comments:
        st.info("Ainda não há comentários nesta análise.")
    else:
        for c in comments:
            author = c.get("profiles") or {}
            st.markdown("---")
            st.markdown(f"**{author.get('full_name') or author.get('username') or 'Usuário'}** · {c.get('created_at', '')[:16]}")
            st.write(c["comment_text"])
            rcols = st.columns(len(REACTIONS))
            for i, reaction in enumerate(REACTIONS):
                with rcols[i]:
                    if st.button(reaction, key=f"react_{c['id']}_{reaction}"):
                        try:
                            sb.table("comment_reactions").upsert({
                                "comment_id": c["id"],
                                "user_id": user_id,
                                "reaction": reaction,
                            }).execute()
                            if c["user_id"] != user_id:
                                notify_user(sb, c["user_id"], "reaction", f"Seu comentário recebeu reação {reaction}.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

    st.markdown("### Feed geral da comunidade")
    feed = safe_data(
        sb.table("analysis_comments")
        .select("id, comment_text, created_at, community, destination_country, profiles(username, full_name)")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )
    for item in feed:
        author = item.get("profiles") or {}
        st.markdown(
            f"- **{author.get('full_name') or author.get('username') or 'Usuário'}** em "
            f"*{item.get('community')} · {item.get('destination_country')}*: {item.get('comment_text')}"
        )

    st.markdown("### Mapa de vozes")
    if feed:
        feed_df = pd.DataFrame(feed)
        voice_df = feed_df.groupby("destination_country").size().reset_index(name="comentários")
        fig = px.bar(voice_df, x="destination_country", y="comentários", title="Comentários por país de destino")
        st.plotly_chart(fig, use_container_width=True)


def render_save_collections_tab(sb: Client, context: Dict[str, Any], filtered: pd.DataFrame) -> None:
    st.subheader("Salvar análises, notícias e coleções")
    user_id = current_user_id()

    c1, c2 = st.columns(2)
    with c1:
        note = st.text_area("Nota para salvar esta análise")
        if st.button("Salvar análise atual"):
            try:
                sb.table("saved_analyses").insert({
                    "user_id": user_id,
                    "community": context["community"],
                    "destination_country": context["country"],
                    "sentiment": context["sentiment"],
                    "start_date": str(context["start_date"]),
                    "end_date": str(context["end_date"]),
                    "notes": note,
                }).execute()
                st.success("Análise salva.")
            except Exception as e:
                st.error(f"Erro: {e}")

    with c2:
        with st.form("new_collection"):
            title = st.text_input("Nome da coleção")
            description = st.text_area("Descrição")
            is_public = st.checkbox("Coleção pública")
            submitted = st.form_submit_button("Criar coleção")
        if submitted and title:
            try:
                sb.table("collections").insert({
                    "user_id": user_id,
                    "title": title,
                    "description": description,
                    "is_public": is_public,
                }).execute()
                st.success("Coleção criada.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

    st.markdown("### Salvar notícia da seleção")
    if filtered.empty:
        st.info("Nenhuma notícia filtrada para salvar.")
    else:
        options = filtered.sort_values("date", ascending=False).head(50).copy()
        options["label"] = options.apply(lambda r: f"{int(r['article_id'])} · {r['date'].date()} · {r['source']} · {r['url'][:70]}", axis=1)
        selected_label = st.selectbox("Escolha uma notícia", options["label"].tolist())
        selected = options[options["label"] == selected_label].iloc[0]
        article_note = st.text_area("Nota privada sobre a notícia")
        if st.button("Salvar notícia"):
            try:
                sb.table("saved_articles").upsert({
                    "user_id": user_id,
                    "article_id": int(selected["article_id"]),
                    "community": str(selected.get("community", "")),
                    "destination_country": str(selected.get("destination_country", "")),
                    "source": str(selected.get("source", "")),
                    "url": str(selected.get("url", "")),
                    "notes": article_note,
                }).execute()
                st.success("Notícia salva.")
            except Exception as e:
                st.error(f"Erro: {e}")

    st.markdown("### Minhas análises e notícias salvas")
    saved_a = safe_data(sb.table("saved_analyses").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(20).execute())
    saved_n = safe_data(sb.table("saved_articles").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(20).execute())

    if saved_a:
        st.write("**Análises salvas**")
        st.dataframe(pd.DataFrame(saved_a), use_container_width=True, hide_index=True)
    if saved_n:
        st.write("**Notícias salvas**")
        st.dataframe(pd.DataFrame(saved_n), use_container_width=True, hide_index=True)


def render_framing_debate_tab(sb: Client, context: Dict[str, Any], filtered: pd.DataFrame, story: str) -> None:
    st.subheader("Framing colaborativo, debate e revisão humana da IA")
    user_id = current_user_id()

    st.markdown("### Framing Battle: algoritmo × humanos")
    if filtered.empty:
        st.info("Nenhuma notícia filtrada para votar framing.")
    else:
        options = filtered.sort_values("date", ascending=False).head(50).copy()
        options["label"] = options.apply(lambda r: f"{int(r['article_id'])} · automático: {r.get('frame', 'n/d')} · {r['url'][:60]}", axis=1)
        selected_label = st.selectbox("Notícia para classificar", options["label"].tolist(), key="framing_article")
        selected = options[options["label"] == selected_label].iloc[0]
        frame = st.selectbox("Qual é o framing dominante?", SOCIAL_FRAMES)
        note = st.text_area("Justificativa opcional")
        if st.button("Votar framing"):
            try:
                sb.table("framing_votes").upsert({
                    "user_id": user_id,
                    "article_id": int(selected["article_id"]),
                    "frame": frame,
                    "note": note,
                }).execute()
                st.success("Voto registrado.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

        votes = safe_data(sb.table("framing_votes").select("frame").eq("article_id", int(selected["article_id"])).execute())
        if votes:
            vote_df = pd.DataFrame(votes).groupby("frame").size().reset_index(name="votos")
            fig = px.bar(vote_df, x="frame", y="votos", title="Votos humanos de framing")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Debate Mode")
    default_statement = f"A cobertura sobre {context['community']} em {context['country']} é invisível em relação ao seu peso demográfico."
    statement = st.text_input("Afirmação para debate", value=default_statement)
    if st.button("Criar debate desta análise"):
        try:
            sb.table("debates").insert({
                "creator_id": user_id,
                "analysis_key": context["analysis_key"],
                "statement": statement,
            }).execute()
            st.success("Debate criado.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

    debates = safe_data(sb.table("debates").select("*").eq("analysis_key", context["analysis_key"]).order("created_at", desc=True).limit(10).execute())
    for d in debates:
        with st.expander(d["statement"]):
            position = st.radio("Sua posição", ["Concordo", "Discordo", "Depende"], key=f"pos_{d['id']}", horizontal=True)
            justification = st.text_area("Justificativa", key=f"just_{d['id']}")
            if st.button("Votar no debate", key=f"vote_debate_{d['id']}"):
                try:
                    sb.table("debate_votes").upsert({
                        "debate_id": d["id"],
                        "user_id": user_id,
                        "position": position,
                        "justification": justification,
                    }).execute()
                    st.success("Voto salvo.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")
            votes = safe_data(sb.table("debate_votes").select("position, justification").eq("debate_id", d["id"]).execute())
            if votes:
                vote_df = pd.DataFrame(votes).groupby("position").size().reset_index(name="votos")
                st.dataframe(vote_df, use_container_width=True, hide_index=True)

    st.markdown("### Revisão humana de IA / Story Mode")
    rating = st.radio("A IA interpretou bem?", ["Sim", "Parcialmente", "Não"], horizontal=True)
    feedback = st.text_area("Comentário sobre a interpretação da IA", value="")
    if st.button("Salvar avaliação da IA"):
        try:
            sb.table("ai_feedback").insert({
                "user_id": user_id,
                "analysis_key": context["analysis_key"],
                "rating": rating,
                "feedback_text": feedback,
            }).execute()
            st.success("Avaliação salva.")
        except Exception as e:
            st.error(f"Erro: {e}")


def render_messages_tab(sb: Client) -> None:
    st.subheader("Mensagens diretas")
    user_id = current_user_id()

    st.markdown("### Nova conversa")
    username = st.text_input("Username da pessoa")
    if st.button("Criar conversa") and username:
        target = safe_data(sb.table("profiles").select("id, username").eq("username", username).limit(1).execute())
        if not target:
            st.error("Usuário não encontrado.")
        else:
            target_id = target[0]["id"]
            try:
                conv = safe_data(sb.table("conversations").insert({}).select("id").execute())[0]
                sb.table("conversation_members").insert([
                    {"conversation_id": conv["id"], "user_id": user_id},
                    {"conversation_id": conv["id"], "user_id": target_id},
                ]).execute()
                notify_user(sb, target_id, "dm", "Você recebeu uma nova conversa.")
                st.success("Conversa criada.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

    memberships = safe_data(sb.table("conversation_members").select("conversation_id").eq("user_id", user_id).execute())
    conv_ids = [m["conversation_id"] for m in memberships]
    if not conv_ids:
        st.info("Você ainda não tem conversas.")
        return

    conv_id = st.selectbox("Escolha uma conversa", conv_ids)
    messages = safe_data(
        sb.table("direct_messages")
        .select("id, sender_id, message_text, created_at, profiles(username, full_name)")
        .eq("conversation_id", conv_id)
        .order("created_at", desc=False)
        .limit(100)
        .execute()
    )
    for m in messages:
        author = m.get("profiles") or {}
        st.markdown(f"**{author.get('full_name') or author.get('username') or 'Usuário'}:** {m['message_text']}")
        st.caption(m.get("created_at", ""))

    with st.form("send_dm"):
        msg = st.text_area("Mensagem")
        submitted = st.form_submit_button("Enviar")
    if submitted and msg.strip():
        try:
            sb.table("direct_messages").insert({
                "conversation_id": conv_id,
                "sender_id": user_id,
                "message_text": msg.strip(),
            }).execute()
            # notifica outros membros
            members = safe_data(sb.table("conversation_members").select("user_id").eq("conversation_id", conv_id).execute())
            for m in members:
                if m["user_id"] != user_id:
                    notify_user(sb, m["user_id"], "dm", "Nova mensagem direta recebida.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")


def render_circles_reports_tab(sb: Client, context: Dict[str, Any]) -> None:
    st.subheader("Research Circles e relatórios colaborativos")
    user_id = current_user_id()

    st.markdown("### Criar círculo de pesquisa")
    with st.form("new_circle"):
        title = st.text_input("Título do círculo")
        theme = st.text_input("Tema", value="Invisibilidade midiática")
        desc = st.text_area("Descrição")
        submitted = st.form_submit_button("Criar círculo")
    if submitted and title:
        try:
            circle = safe_data(sb.table("research_circles").insert({
                "creator_id": user_id,
                "title": title,
                "theme": theme,
                "description": desc,
            }).select("id").execute())[0]
            sb.table("circle_members").insert({"circle_id": circle["id"], "user_id": user_id}).execute()
            st.success("Círculo criado.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

    circles = safe_data(sb.table("research_circles").select("*").order("created_at", desc=True).limit(20).execute())
    if circles:
        circle_labels = [f"{c['id']} · {c['title']} · {c.get('theme') or ''}" for c in circles]
        chosen = st.selectbox("Círculos disponíveis", circle_labels)
        circle_id = int(chosen.split(" · ")[0])
        if st.button("Entrar neste círculo"):
            try:
                sb.table("circle_members").upsert({"circle_id": circle_id, "user_id": user_id}).execute()
                st.success("Você entrou no círculo.")
            except Exception as e:
                st.error(f"Erro: {e}")

        with st.form("circle_post"):
            post_text = st.text_area("Postar no círculo")
            submitted = st.form_submit_button("Publicar no círculo")
        if submitted and post_text.strip():
            try:
                sb.table("circle_posts").insert({
                    "circle_id": circle_id,
                    "user_id": user_id,
                    "post_text": post_text.strip(),
                }).execute()
                st.success("Post publicado.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

        posts = safe_data(
            sb.table("circle_posts")
            .select("post_text, created_at, profiles(username, full_name)")
            .eq("circle_id", circle_id)
            .order("created_at", desc=True)
            .limit(30)
            .execute()
        )
        for p in posts:
            author = p.get("profiles") or {}
            st.markdown(f"**{author.get('full_name') or author.get('username') or 'Usuário'}:** {p['post_text']}")
            st.caption(p.get("created_at", ""))

    st.markdown("---")
    st.markdown("### Collab Report")
    with st.form("new_report"):
        report_title = st.text_input("Título do relatório colaborativo", value=f"Relatório — {context['community']} em {context['country']}")
        report_body = st.text_area("Texto inicial")
        submitted = st.form_submit_button("Criar relatório")
    if submitted and report_title:
        try:
            sb.table("collab_reports").insert({
                "owner_id": user_id,
                "title": report_title,
                "analysis_key": context["analysis_key"],
                "body": report_body,
            }).execute()
            st.success("Relatório criado.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

    reports = safe_data(sb.table("collab_reports").select("*").order("created_at", desc=True).limit(20).execute())
    for r in reports:
        with st.expander(r["title"]):
            st.write(r.get("body") or "Sem texto ainda.")
            collaborator_username = st.text_input("Adicionar colaborador por username", key=f"collab_user_{r['id']}")
            if st.button("Adicionar colaborador", key=f"add_collab_{r['id']}") and collaborator_username:
                target = safe_data(sb.table("profiles").select("id").eq("username", collaborator_username).limit(1).execute())
                if target:
                    try:
                        sb.table("report_collaborators").upsert({
                            "report_id": r["id"],
                            "user_id": target[0]["id"],
                            "role": "editor",
                        }).execute()
                        notify_user(sb, target[0]["id"], "report", f"Você foi adicionado ao relatório: {r['title']}")
                        st.success("Colaborador adicionado.")
                    except Exception as e:
                        st.error(f"Erro: {e}")
                else:
                    st.error("Usuário não encontrado.")


def render_diary_notifications_tab(sb: Client, context: Dict[str, Any]) -> None:
    st.subheader("Diário da diáspora, notificações e ranking")
    user_id = current_user_id()

    st.markdown("### Diário da diáspora")
    with st.form("diary"):
        title = st.text_input("Título da reflexão")
        body = st.text_area("Reflexão qualitativa")
        public = st.checkbox("Tornar reflexão pública")
        submitted = st.form_submit_button("Salvar reflexão")
    if submitted and body.strip():
        try:
            sb.table("diary_entries").insert({
                "user_id": user_id,
                "community": context["community"],
                "destination_country": context["country"],
                "title": title,
                "body": body.strip(),
                "is_public": public,
            }).execute()
            st.success("Reflexão salva.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

    entries = safe_data(sb.table("diary_entries").select("*, profiles(username, full_name)").order("created_at", desc=True).limit(20).execute())
    for entry in entries:
        with st.expander(entry.get("title") or "Reflexão"):
            author = entry.get("profiles") or {}
            st.caption(f"{author.get('full_name') or author.get('username') or 'Usuário'} · {entry.get('community')} · {entry.get('destination_country')}")
            st.write(entry.get("body"))

    st.markdown("### Notificações")
    notes = safe_data(sb.table("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(30).execute())
    if notes:
        for n in notes:
            prefix = "✅" if n.get("read") else "🔔"
            st.write(f"{prefix} {n.get('body')} — {n.get('created_at', '')[:16]}")
        if st.button("Marcar todas como lidas"):
            sb.table("notifications").update({"read": True}).eq("user_id", user_id).execute()
            st.rerun()
    else:
        st.info("Sem notificações.")

    st.markdown("### Ranking de comentários úteis")
    reactions = safe_data(
        sb.table("comment_reactions")
        .select("comment_id, reaction, analysis_comments(comment_text, community, destination_country, profiles(username, full_name))")
        .execute()
    )
    if reactions:
        rows = []
        for r in reactions:
            c = r.get("analysis_comments") or {}
            author = c.get("profiles") or {}
            rows.append({
                "comment_id": r.get("comment_id"),
                "comentário": c.get("comment_text"),
                "autor": author.get("full_name") or author.get("username"),
                "contexto": f"{c.get('community')} · {c.get('destination_country')}",
            })
        rank = pd.DataFrame(rows).groupby(["comment_id", "comentário", "autor", "contexto"]).size().reset_index(name="reações")
        st.dataframe(rank.sort_values("reações", ascending=False).head(10), use_container_width=True, hide_index=True)
    else:
        st.info("Ainda não há reações suficientes para ranking.")


def render_case_of_week(articles: pd.DataFrame) -> None:
    st.markdown("### Invisible Case of the Week")
    if articles is None or articles.empty:
        st.info("Sem dados para caso da semana.")
        return
    try:
        case = (
            articles.groupby(["community", "destination_country"])
            .agg(noticias=("url", "count"), tom_medio=("tone", "mean"))
            .reset_index()
            .sort_values(["noticias", "tom_medio"], ascending=[True, True])
            .head(1)
        )
        if not case.empty:
            r = case.iloc[0]
            st.warning(
                f"Caso crítico sugerido: {r['community']} em {r['destination_country']} — "
                f"{int(r['noticias'])} notícias, tom médio {r['tom_medio']:.2f}."
            )
    except Exception:
        st.info("Caso da semana indisponível.")


def render_social_layer(
    selected_community: str,
    selected_country: str,
    selected_sentiment: str,
    start_date: Any,
    end_date: Any,
    filtered: pd.DataFrame,
    articles: pd.DataFrame,
    story: str = "",
) -> None:
    """Renderiza toda a camada social no fim do app.py."""
    st.markdown("---")
    st.header("🌐 Camada colaborativa")
    st.caption("Contas, perfis, comentários, mensagens, coleções, debates e análise humana colaborativa.")

    logged_in = render_auth_box()
    if not logged_in:
        st.info("Entre ou crie uma conta para usar a camada colaborativa.")
        return

    sb = get_sb()
    context = {
        "community": selected_community,
        "country": selected_country,
        "sentiment": selected_sentiment,
        "start_date": start_date,
        "end_date": end_date,
        "analysis_key": make_analysis_key(selected_community, selected_country, selected_sentiment, start_date, end_date),
    }

    render_case_of_week(articles)

    # ============================================================
    # MENU DE PERFIL NO TOPO DIREITO
    # ============================================================

    if "social_page" not in st.session_state:
        st.session_state["social_page"] = "Meu perfil"

    st.markdown(
        """
        <style>
        .social-topbar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-top: -0.5rem;
            margin-bottom: 1rem;
        }

        div[data-testid="stPopover"] > button {
            border-radius: 999px !important;
            border: 1px solid #eadccf !important;
            background-color: #fffaf3 !important;
            color: #2b2520 !important;
            padding: 0.55rem 1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
        }

        div[data-testid="stPopover"] > button:hover {
            border-color: #b7835a !important;
            color: #b7835a !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    top_left, top_right = st.columns([5, 1])

    with top_left:
        st.markdown("### 🌐 Camada colaborativa")

    with top_right:
        with st.popover(t("profile_menu"), use_container_width=True):
            st.markdown(f"#### {t('social_navigation')}")

            if st.button(f"👤 {t('social_profile')}", use_container_width=True):
                st.session_state["social_page"] = "Meu perfil"

            if st.button(f"💬 {t('social_comments')}", use_container_width=True):
                st.session_state["social_page"] = "Comentários e feed"

            if st.button(f"📌 {t('social_save')}", use_container_width=True):
                st.session_state["social_page"] = "Salvar e coleções"

            if st.button(f"🧠 {t('social_framing')}", use_container_width=True):
                st.session_state["social_page"] = "Framing e debates"

            if st.button(f"✉️ {t('social_messages')}", use_container_width=True):
                st.session_state["social_page"] = "Mensagens"

            if st.button(f"🌀 {t('social_circles')}", use_container_width=True):
                st.session_state["social_page"] = "Círculos e relatórios"

            if st.button(f"📓 {t('social_diary')}", use_container_width=True):
                st.session_state["social_page"] = "Diário, notificações e ranking"

    page_labels = {
        "Meu perfil": t("social_profile"),
        "Comentários e feed": t("social_comments"),
        "Salvar e coleções": t("social_save"),
        "Framing e debates": t("social_framing"),
        "Mensagens": t("social_messages"),
        "Círculos e relatórios": t("social_circles"),
        "Diário, notificações e ranking": t("social_diary"),
    }

    st.caption(f"{t('current_section')}: {page_labels.get(st.session_state['social_page'], st.session_state['social_page'])}")

    if st.session_state["social_page"] == "Meu perfil":
        render_profile_tab(sb)
    if st.session_state["social_page"] == "Comentários e feed":
        render_comments_tab(sb, context)
    if st.session_state["social_page"] == "Salvar e coleções":
        render_save_collections_tab(sb, context, filtered)
    if st.session_state["social_page"] == "Framing e debates":
        render_framing_debate_tab(sb, context, filtered, story)
    if st.session_state["social_page"] == "Mensagens":
        render_messages_tab(sb)
    if st.session_state["social_page"] == "Círculos e relatórios":
        render_circles_reports_tab(sb, context)
    if st.session_state["social_page"] == "Diário, notificações e ranking":
        render_diary_notifications_tab(sb, context)
