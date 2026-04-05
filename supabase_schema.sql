-- sendbox.fun reviews schema
-- Run this in Supabase SQL Editor (Database → SQL Editor → New query)

-- Reviews table
create table if not exists public.reviews (
  id uuid primary key default gen_random_uuid(),
  tool_id text not null,
  user_id uuid not null references auth.users(id) on delete cascade,
  user_email text not null,
  rating smallint not null check (rating >= 1 and rating <= 5),
  review_text text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now(),
  unique(tool_id, user_id)
);

create index if not exists idx_reviews_tool_id on public.reviews(tool_id);
create index if not exists idx_reviews_created_at on public.reviews(created_at desc);

-- Enable Row Level Security
alter table public.reviews enable row level security;

-- Anyone can read reviews (public data)
drop policy if exists "Reviews are viewable by everyone" on public.reviews;
create policy "Reviews are viewable by everyone"
  on public.reviews for select
  using (true);

-- Authenticated users can insert their own reviews
drop policy if exists "Users can insert their own reviews" on public.reviews;
create policy "Users can insert their own reviews"
  on public.reviews for insert
  with check (auth.uid() = user_id);

-- Users can update their own reviews only
drop policy if exists "Users can update own reviews" on public.reviews;
create policy "Users can update own reviews"
  on public.reviews for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- Users can delete their own reviews only
drop policy if exists "Users can delete own reviews" on public.reviews;
create policy "Users can delete own reviews"
  on public.reviews for delete
  using (auth.uid() = user_id);

-- Aggregate view for fast rating lookups
create or replace view public.tool_ratings as
  select
    tool_id,
    round(avg(rating)::numeric, 1) as avg_rating,
    count(*) as review_count
  from public.reviews
  group by tool_id;

grant select on public.tool_ratings to anon, authenticated;

-- Auto-update updated_at on modifications
create or replace function public.handle_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists on_reviews_updated on public.reviews;
create trigger on_reviews_updated
  before update on public.reviews
  for each row execute function public.handle_updated_at();
