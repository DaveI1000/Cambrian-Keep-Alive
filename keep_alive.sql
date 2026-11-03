-- Run separately in the SQL Editor of Cambrian Rota and Cambrian TSR.
-- This table is independent of the existing applications.
create table if not exists public.keep_alive (
  id integer primary key check (id = 1),
  status integer not null default 0 check (status in (0,1)),
  last_updated timestamptz not null default now(),
  update_count bigint not null default 0
);
insert into public.keep_alive(id,status,update_count)
values (1,0,0) on conflict (id) do nothing;

-- Only the service-role key used by the private scheduled workflow can access it.
alter table public.keep_alive enable row level security;
revoke all on public.keep_alive from anon, authenticated;
grant select, update on public.keep_alive to service_role;
