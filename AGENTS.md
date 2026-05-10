# AGENTS.md — Canvasia (ASP.NET Core 8.0 e-commerce)

## Project overview

- **Stack**: ASP.NET Core 8.0 MVC + PostgreSQL + Tailwind CSS
- **Architecture**: Clean Architecture (4 projects: Web → Service → Data → Core)
- **Brand**: Canvasia (formerly MeteorGaleri)
- **UI**: Turkish language, Turkish-named DB entities/tables

## Quick start

```bash
# Dev: DB in Docker, web on host
docker-compose up -d db
cd KanvasProje.Web && dotnet watch run   # http://localhost:5002

# Full Docker
docker-compose build --no-cache && docker-compose up -d   # http://localhost:8080
```

## Critical gotchas (would likely miss these)

1. **Database unreachable at startup** → App doesn't crash, but Hangfire + AbandonedCartService are disabled. Check logs if background jobs aren't running.

2. **Dual migration system** → EF migrations + `EnsureMissingMarch2026SchemaAsync` (hand-rolled SQL block). If you add columns to `Urunler`, `Kategoriler`, `UrunSecenekleri`, or `UrunResimleri`, mirror them in that SQL block or prod will diverge.

3. **Turkish PascalCase + quotes** → All raw SQL needs double quotes: `"Urunler"`, `"Kategoriler"`, `"UrunResimleri"`.

4. **Property name traps**:
   - `Urun.Baslik` — NOT "Ad" or "Name"
   - `UrunResim.ResimYolu` — NOT "Url" or "ImageUrl"
   - `Urun.EtkinFiyat`, `Urun.IndirimVarMi`, `Urun.SilindiMi`

5. **secrets.json** — Contains DB connection string, gitignored. Required for local dev.

6. **iyzico in sandbox** — Placeholder API key in appsettings.json. Don't test real payments.

7. **Rate limiter** — "auth" (10/5min IP), "general" (100/min IP). Will lock you out during testing.

8. **Maintenance mode** — `ISiteSecurityService` middleware blocks non-admin traffic when enabled.

## Commands

```bash
# Build
dotnet build KanvasProje.sln

# Migration
dotnet ef migrations add <Name> --project KanvasProje.Data --startup-project KanvasProje.Web
dotnet ef database update --project KanvasProje.Data --startup-project KanvasProje.Web

# Tailwind CSS
cd KanvasProje.Web && npm run watch:storefront-css
```

## Key URLs

- Public: `/Urun`, `/Urun/Detay/{slug}-{id}`, `/Sepet`, `/Siparis/Odeme`, `/Hesap/GirisYap`, `/admin/*` (Area)
- Hangfire: `/admin/hangfire` (local only)

## DB conventions

- Tables/columns use **Turkish PascalCase** with double quotes in raw SQL
- Default connection: `Host=localhost;Port=5432;Database=kanvasdb;Username=kanvasuser;Password=changeme_in_production`

## What NOT to do

- Don't create a test project (none exists in solution)
- Don't use Linux shell commands (PowerShell 5.1)
- Don't commit secrets.json or real credentials to git