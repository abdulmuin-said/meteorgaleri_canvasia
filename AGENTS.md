# AGENTS.md — Canvasia (ASP.NET Core 8.0 e-commerce)

## Project overview

- **Stack**: ASP.NET Core 8.0 MVC + PostgreSQL + Tailwind CSS
- **Architecture**: Clean Architecture (4 projects: Web → Service → Data → Core)
- **Brand**: Canvasia (formerly MeteorGaleri)
- **UI**: Turkish language, Turkish-named DB entities/tables
- **No test project** — don't create one

## Core commands

```bash
# Local dev (DB in Docker, web on host)
docker-compose up -d db
cd KanvasProje.Web && dotnet watch run   # http://localhost:5002

# Full Docker stack
docker-compose build --no-cache && docker-compose up -d   # http://localhost:8080

# Build
dotnet build KanvasProje.sln

# Database
dotnet ef migrations add <Name> --project KanvasProje.Data --startup-project KanvasProje.Web
dotnet ef database update --project KanvasProje.Data --startup-project KanvasProje.Web

# Restore SQL dump
Get-Content kanvasdb_yedek.sql | docker exec -i kanvasproje-db psql -U kanvasuser -d kanvasdb

# CSS (Tailwind)
cd KanvasProje.Web && npm run watch:storefront-css
```

## DB conventions (PostgreSQL)

- Tables/columns use **Turkish PascalCase** and require **double quotes** in raw SQL:
  `"Urunler"`, `"Kategoriler"`, `"UrunResimleri"`, `"SepetItems"`, `"AspNetUsers"`
- Key property spellings: `Urun.Baslik` (not Ad/Name), `Urun.Slug`, `Urun.EtkinFiyat`, `UrunResim.ResimYolu` (not Url)

## Startup behavior quirks

- `secrets.json` loads DB connection string (gitignored)
- If Postgres unreachable at startup: **Hangfire + AbandonedCartService disabled** (not crash)
- `EnsureMissingMarch2026SchemaAsync` runs on every startup — hand-rolled idempotent migration for schema drift. If you add columns to `Urunler`, `Kategoriler`, `UrunSecenekleri`, or `UrunResimleri`, mirror them in that SQL block.

## Other

- iyzico payment is in sandbox mode (placeholder API key)
- Admin area at `/admin/*` (Area)
- Rate limiter: "auth" (10/5min IP), "general" (100/min IP)
- Maintenance mode via `ISiteSecurityService` middleware
- HTTPS redirect skipped when `DOTNET_RUNNING_IN_CONTAINER=true`

## Referenced docs

- `CLAUDE.md` — detailed architecture, runtime pipeline, naming conventions
- `PROJE_DOKUMANTASYONU.txt` — DB credentials, SQL restore commands, known issues