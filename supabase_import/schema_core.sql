drop table if exists public."articles" cascade;
create table public."articles" (
  "article_id" integer,
  "date" text,
  "year" integer,
  "month" text,
  "community" text,
  "destination_country" double precision,
  "iso3" text,
  "source" text,
  "domain" text,
  "tone" double precision,
  "sentiment" text,
  "url" text,
  "text_proxy" text
);

alter table public."articles" enable row level security;
create policy "public can read articles" on public."articles" for select to anon using (true);

drop table if exists public."migration_destination" cascade;
create table public."migration_destination" (
  "destination_country" double precision,
  "iso3" text,
  "undesa_name" text,
  "undesa_location_code" integer,
  "destination_migrant_stock_2020" double precision,
  "destination_total_population_2020" double precision,
  "migrant_share_population_2020" double precision
);

alter table public."migration_destination" enable row level security;
create policy "public can read migration_destination" on public."migration_destination" for select to anon using (true);

drop table if exists public."migration_origin" cascade;
create table public."migration_origin" (
  "community" text,
  "undesa_origin_names" text,
  "origin_location_codes" text,
  "origin_global_migrant_stock_2020" double precision
);

alter table public."migration_origin" enable row level security;
create policy "public can read migration_origin" on public."migration_origin" for select to anon using (true);
