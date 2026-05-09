# ==========================================
# Stage 1: Build
# ==========================================
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Proje dosyalarını kopyala ve restore et (cache optimizasyonu)
COPY KanvasProje.Core/KanvasProje.Core.csproj KanvasProje.Core/
COPY KanvasProje.Data/KanvasProje.Data.csproj KanvasProje.Data/
COPY KanvasProje.Service/KanvasProje.Service.csproj KanvasProje.Service/
COPY KanvasProje.Web/KanvasProje.Web.csproj KanvasProje.Web/
COPY KanvasProje.sln .

RUN dotnet restore KanvasProje.sln

# Tüm kaynak kodunu kopyala ve publish et
COPY . .
RUN dotnet publish KanvasProje.Web/KanvasProje.Web.csproj \
    -c Release \
    -o /app/publish \
    --no-restore

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

# Güvenlik: Root olmayan kullanıcı
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appgroup \
    && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Gerekli klasörleri oluştur
RUN mkdir -p /app/logs /app/App_Data /app/wwwroot/img/products /app/wwwroot/media/products/videos \
    && chown -R appuser:appgroup /app

# Publish çıktısını kopyala
COPY --from=build --chown=appuser:appgroup /app/publish .

# Ortam değişkenleri
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENV DOTNET_EnableDiagnostics=0

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

USER appuser
ENTRYPOINT ["dotnet", "KanvasProje.Web.dll"]
