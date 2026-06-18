-- Invisible Diasporas Lab — camada social colaborativa
-- Rode este arquivo no Supabase: SQL Editor → New query → Run

create extension if not exists "uuid-ossp";

-- =========================
-- PERFIS E SOCIAL GRAPH
-- =========================

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique,
  full_name text,
  bio text,
  institution text,
  interests text,
  avatar_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.follows (
  follower_id uuid references public.profiles(id) on delete cascade,
  followee_id uuid references public.profiles(id) on delete cascade,
  created_at timestamptz default now(),
  primary key (follower_id, followee_id),
  check (follower_id <> followee_id)
);

-- =========================
-- COMENTÁRIOS, REAÇÕES E FEED
-- =========================

create table if not exists public.analysis_comments (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  community text not null,
  destination_country text not null,
  sentiment text,
  analysis_key text not null,
  comment_text text not null,
  parent_id bigint references public.analysis_comments(id) on delete cascade,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.comment_reactions (
  id bigint generated always as identity primary key,
  comment_id bigint references public.analysis_comments(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  reaction text not null default '📌 útil',
  created_at timestamptz default now(),
  unique(comment_id, user_id, reaction)
);

-- =========================
-- SALVAR ANÁLISES, NOTÍCIAS E COLEÇÕES
-- =========================

create table if not exists public.saved_analyses (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  community text not null,
  destination_country text not null,
  sentiment text,
  start_date date,
  end_date date,
  notes text,
  created_at timestamptz default now()
);

create table if not exists public.saved_articles (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  article_id integer not null,
  community text,
  destination_country text,
  source text,
  url text,
  notes text,
  created_at timestamptz default now(),
  unique(user_id, article_id)
);

create table if not exists public.collections (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  title text not null,
  description text,
  is_public boolean default false,
  created_at timestamptz default now()
);

create table if not exists public.collection_items (
  id bigint generated always as identity primary key,
  collection_id bigint references public.collections(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  item_type text not null check (item_type in ('article','analysis','report')),
  article_id integer,
  analysis_key text,
  report_id bigint,
  note text,
  created_at timestamptz default now()
);

-- =========================
-- FRAMING COLABORATIVO E IA
-- =========================

create table if not exists public.framing_votes (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  article_id integer not null,
  frame text not null,
  note text,
  created_at timestamptz default now(),
  unique(user_id, article_id)
);

create table if not exists public.ai_feedback (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  analysis_key text not null,
  rating text not null,
  feedback_text text,
  created_at timestamptz default now()
);

-- =========================
-- MENSAGENS DIRETAS
-- =========================

create table if not exists public.conversations (
  id bigint generated always as identity primary key,
  created_at timestamptz default now()
);

create table if not exists public.conversation_members (
  conversation_id bigint references public.conversations(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  created_at timestamptz default now(),
  primary key (conversation_id, user_id)
);

create table if not exists public.direct_messages (
  id bigint generated always as identity primary key,
  conversation_id bigint references public.conversations(id) on delete cascade,
  sender_id uuid references public.profiles(id) on delete cascade,
  message_text text not null,
  created_at timestamptz default now()
);

-- =========================
-- GRUPOS, DIÁRIO, DEBATES E RELATÓRIOS COLABORATIVOS
-- =========================

create table if not exists public.research_circles (
  id bigint generated always as identity primary key,
  creator_id uuid references public.profiles(id) on delete cascade,
  title text not null,
  description text,
  theme text,
  created_at timestamptz default now()
);

create table if not exists public.circle_members (
  circle_id bigint references public.research_circles(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  created_at timestamptz default now(),
  primary key (circle_id, user_id)
);

create table if not exists public.circle_posts (
  id bigint generated always as identity primary key,
  circle_id bigint references public.research_circles(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  post_text text not null,
  created_at timestamptz default now()
);

create table if not exists public.diary_entries (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  community text,
  destination_country text,
  title text,
  body text not null,
  is_public boolean default false,
  created_at timestamptz default now()
);

create table if not exists public.debates (
  id bigint generated always as identity primary key,
  creator_id uuid references public.profiles(id) on delete cascade,
  analysis_key text not null,
  statement text not null,
  created_at timestamptz default now()
);

create table if not exists public.debate_votes (
  id bigint generated always as identity primary key,
  debate_id bigint references public.debates(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  position text not null check (position in ('Concordo','Discordo','Depende')),
  justification text,
  created_at timestamptz default now(),
  unique(debate_id, user_id)
);

create table if not exists public.collab_reports (
  id bigint generated always as identity primary key,
  owner_id uuid references public.profiles(id) on delete cascade,
  title text not null,
  analysis_key text,
  body text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.report_collaborators (
  report_id bigint references public.collab_reports(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  role text default 'editor',
  created_at timestamptz default now(),
  primary key (report_id, user_id)
);

create table if not exists public.report_comments (
  id bigint generated always as identity primary key,
  report_id bigint references public.collab_reports(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  comment_text text not null,
  created_at timestamptz default now()
);

-- =========================
-- NOTIFICAÇÕES
-- =========================

create table if not exists public.notifications (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  type text,
  body text,
  read boolean default false,
  created_at timestamptz default now()
);

-- =========================
-- ROW LEVEL SECURITY
-- =========================

alter table public.profiles enable row level security;
alter table public.follows enable row level security;
alter table public.analysis_comments enable row level security;
alter table public.comment_reactions enable row level security;
alter table public.saved_analyses enable row level security;
alter table public.saved_articles enable row level security;
alter table public.collections enable row level security;
alter table public.collection_items enable row level security;
alter table public.framing_votes enable row level security;
alter table public.ai_feedback enable row level security;
alter table public.conversations enable row level security;
alter table public.conversation_members enable row level security;
alter table public.direct_messages enable row level security;
alter table public.research_circles enable row level security;
alter table public.circle_members enable row level security;
alter table public.circle_posts enable row level security;
alter table public.diary_entries enable row level security;
alter table public.debates enable row level security;
alter table public.debate_votes enable row level security;
alter table public.collab_reports enable row level security;
alter table public.report_collaborators enable row level security;
alter table public.report_comments enable row level security;
alter table public.notifications enable row level security;

-- Perfis públicos, edição só pelo dono
create policy "profiles are public" on public.profiles for select using (true);
create policy "users insert own profile" on public.profiles for insert with check (auth.uid() = id);
create policy "users update own profile" on public.profiles for update using (auth.uid() = id) with check (auth.uid() = id);

-- Follows: usuários logados leem, cada usuário gerencia quem segue
create policy "authenticated read follows" on public.follows for select to authenticated using (true);
create policy "users follow as self" on public.follows for insert with check (auth.uid() = follower_id);
create policy "users unfollow as self" on public.follows for delete using (auth.uid() = follower_id);

-- Comentários e reações: leitura pública para logados, escrita própria
create policy "authenticated read comments" on public.analysis_comments for select to authenticated using (true);
create policy "users insert own comments" on public.analysis_comments for insert with check (auth.uid() = user_id);
create policy "users update own comments" on public.analysis_comments for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "users delete own comments" on public.analysis_comments for delete using (auth.uid() = user_id);

create policy "authenticated read comment reactions" on public.comment_reactions for select to authenticated using (true);
create policy "users insert own comment reactions" on public.comment_reactions for insert with check (auth.uid() = user_id);
create policy "users delete own comment reactions" on public.comment_reactions for delete using (auth.uid() = user_id);

-- Itens pessoais
create policy "users read own saved analyses" on public.saved_analyses for select using (auth.uid() = user_id);
create policy "users insert own saved analyses" on public.saved_analyses for insert with check (auth.uid() = user_id);
create policy "users delete own saved analyses" on public.saved_analyses for delete using (auth.uid() = user_id);

create policy "users read own saved articles" on public.saved_articles for select using (auth.uid() = user_id);
create policy "users insert own saved articles" on public.saved_articles for insert with check (auth.uid() = user_id);
create policy "users update own saved articles" on public.saved_articles for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "users delete own saved articles" on public.saved_articles for delete using (auth.uid() = user_id);

create policy "read public collections or own" on public.collections for select using (is_public = true or auth.uid() = user_id);
create policy "users insert own collections" on public.collections for insert with check (auth.uid() = user_id);
create policy "users update own collections" on public.collections for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "users delete own collections" on public.collections for delete using (auth.uid() = user_id);

create policy "read collection items if visible" on public.collection_items for select using (
  auth.uid() = user_id or exists (
    select 1 from public.collections c where c.id = collection_id and c.is_public = true
  )
);
create policy "users insert own collection items" on public.collection_items for insert with check (auth.uid() = user_id);
create policy "users delete own collection items" on public.collection_items for delete using (auth.uid() = user_id);

-- Framing e IA
create policy "authenticated read framing votes" on public.framing_votes for select to authenticated using (true);
create policy "users upsert own framing votes" on public.framing_votes for insert with check (auth.uid() = user_id);
create policy "users update own framing votes" on public.framing_votes for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "users read own ai feedback" on public.ai_feedback for select using (auth.uid() = user_id);
create policy "users insert own ai feedback" on public.ai_feedback for insert with check (auth.uid() = user_id);

-- Conversas e DMs: só membros
create policy "members read conversation rows" on public.conversations for select using (
  exists (select 1 from public.conversation_members cm where cm.conversation_id = id and cm.user_id = auth.uid())
);
create policy "authenticated create conversations" on public.conversations for insert to authenticated with check (true);

create policy "members read memberships" on public.conversation_members for select using (
  user_id = auth.uid() or exists (
    select 1 from public.conversation_members cm where cm.conversation_id = conversation_members.conversation_id and cm.user_id = auth.uid()
  )
);
create policy "authenticated insert memberships" on public.conversation_members for insert to authenticated with check (true);

create policy "members read messages" on public.direct_messages for select using (
  exists (select 1 from public.conversation_members cm where cm.conversation_id = direct_messages.conversation_id and cm.user_id = auth.uid())
);
create policy "members send messages" on public.direct_messages for insert with check (
  auth.uid() = sender_id and exists (select 1 from public.conversation_members cm where cm.conversation_id = direct_messages.conversation_id and cm.user_id = auth.uid())
);

-- Círculos
create policy "authenticated read circles" on public.research_circles for select to authenticated using (true);
create policy "users create circles" on public.research_circles for insert with check (auth.uid() = creator_id);
create policy "circle creators update" on public.research_circles for update using (auth.uid() = creator_id) with check (auth.uid() = creator_id);

create policy "authenticated read circle members" on public.circle_members for select to authenticated using (true);
create policy "users join as self" on public.circle_members for insert with check (auth.uid() = user_id);
create policy "users leave as self" on public.circle_members for delete using (auth.uid() = user_id);

create policy "authenticated read circle posts" on public.circle_posts for select to authenticated using (true);
create policy "circle members post" on public.circle_posts for insert with check (
  auth.uid() = user_id and exists (select 1 from public.circle_members cm where cm.circle_id = circle_posts.circle_id and cm.user_id = auth.uid())
);

-- Diário: público ou próprio
create policy "read public diary or own" on public.diary_entries for select using (is_public = true or auth.uid() = user_id);
create policy "users insert own diary" on public.diary_entries for insert with check (auth.uid() = user_id);
create policy "users update own diary" on public.diary_entries for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "users delete own diary" on public.diary_entries for delete using (auth.uid() = user_id);

-- Debates
create policy "authenticated read debates" on public.debates for select to authenticated using (true);
create policy "users create debates" on public.debates for insert with check (auth.uid() = creator_id);

create policy "authenticated read debate votes" on public.debate_votes for select to authenticated using (true);
create policy "users insert own debate votes" on public.debate_votes for insert with check (auth.uid() = user_id);
create policy "users update own debate votes" on public.debate_votes for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Relatórios colaborativos
create policy "read own or collaborator reports" on public.collab_reports for select using (
  auth.uid() = owner_id or exists (select 1 from public.report_collaborators rc where rc.report_id = id and rc.user_id = auth.uid())
);
create policy "users create own reports" on public.collab_reports for insert with check (auth.uid() = owner_id);
create policy "owners update reports" on public.collab_reports for update using (auth.uid() = owner_id) with check (auth.uid() = owner_id);

create policy "read collaborators if member" on public.report_collaborators for select using (
  user_id = auth.uid() or exists (select 1 from public.collab_reports cr where cr.id = report_id and cr.owner_id = auth.uid())
);
create policy "owners add collaborators" on public.report_collaborators for insert with check (
  exists (select 1 from public.collab_reports cr where cr.id = report_id and cr.owner_id = auth.uid())
);

create policy "read report comments if report member" on public.report_comments for select using (
  exists (
    select 1 from public.collab_reports cr
    where cr.id = report_id and (
      cr.owner_id = auth.uid() or exists (select 1 from public.report_collaborators rc where rc.report_id = report_comments.report_id and rc.user_id = auth.uid())
    )
  )
);
create policy "members add report comments" on public.report_comments for insert with check (
  auth.uid() = user_id and exists (
    select 1 from public.collab_reports cr
    where cr.id = report_id and (
      cr.owner_id = auth.uid() or exists (select 1 from public.report_collaborators rc where rc.report_id = report_comments.report_id and rc.user_id = auth.uid())
    )
  )
);

-- Notificações
create policy "users read own notifications" on public.notifications for select using (auth.uid() = user_id);
create policy "users update own notifications" on public.notifications for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "authenticated create notifications" on public.notifications for insert to authenticated with check (true);

-- Índices básicos
create index if not exists idx_comments_analysis_key on public.analysis_comments(analysis_key, created_at desc);
create index if not exists idx_saved_articles_user on public.saved_articles(user_id, created_at desc);
create index if not exists idx_framing_article on public.framing_votes(article_id);
create index if not exists idx_dm_conversation on public.direct_messages(conversation_id, created_at desc);
create index if not exists idx_notifications_user on public.notifications(user_id, read, created_at desc);
