BEGIN;

CREATE OR REPLACE FUNCTION public.tr_slugify(input_text text)
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT trim(
        both '-'
        FROM regexp_replace(
            lower(
                translate(
                    coalesce(input_text, ''),
                    'ÇçĞğİIıÖöŞşÜü',
                    'CcGgIIiOoSsUu'
                )
            ),
            '[^a-z0-9]+',
            '-',
            'g'
        )
    );
$$;

ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "AltMetin" text NOT NULL DEFAULT '';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "Baslik" text NOT NULL DEFAULT '';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "Etiketler" text NOT NULL DEFAULT '';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "MedyaAlani" text NOT NULL DEFAULT 'Galeri';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "MedyaTipi" text NOT NULL DEFAULT 'Gorsel';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "MobilResimYolu" text NOT NULL DEFAULT '';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "Sira" integer NOT NULL DEFAULT 0;
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "ThumbnailYolu" text NOT NULL DEFAULT '';
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "UrunSecenekId" integer NULL;
ALTER TABLE "UrunResimleri" ADD COLUMN IF NOT EXISTS "VideoUrl" text NOT NULL DEFAULT '';

CREATE INDEX IF NOT EXISTS "IX_UrunResimleri_UrunId_Sira"
    ON "UrunResimleri" ("UrunId", "Sira");

UPDATE "Kategoriler" k
SET
    "Slug" = CASE
        WHEN coalesce(nullif(btrim(k."Slug"), ''), '') = '' THEN public.tr_slugify(k."Ad")
        ELSE k."Slug"
    END,
    "GorselUrl" = CASE
        WHEN coalesce(nullif(btrim(k."GorselUrl"), ''), '') = '' THEN coalesce((
            SELECT u."AnaGorselUrl"
            FROM "Urunler" u
            WHERE u."KategoriId" = k."Id"
              AND NOT u."SilindiMi"
              AND coalesce(nullif(btrim(u."AnaGorselUrl"), ''), '') <> ''
            ORDER BY u."Sira", u."Id"
            LIMIT 1
        ), '')
        ELSE k."GorselUrl"
    END,
    "BannerUrl" = CASE
        WHEN coalesce(nullif(btrim(k."BannerUrl"), ''), '') = '' THEN coalesce((
            SELECT u."AnaGorselUrl"
            FROM "Urunler" u
            WHERE u."KategoriId" = k."Id"
              AND NOT u."SilindiMi"
              AND coalesce(nullif(btrim(u."AnaGorselUrl"), ''), '') <> ''
            ORDER BY u."Sira", u."Id"
            LIMIT 1
        ), '')
        ELSE k."BannerUrl"
    END,
    "SeoTitle" = CASE
        WHEN coalesce(nullif(btrim(k."SeoTitle"), ''), '') = '' THEN k."Ad" || ' | Canvasia'
        ELSE k."SeoTitle"
    END,
    "SeoDescription" = CASE
        WHEN coalesce(nullif(btrim(k."SeoDescription"), ''), '') = '' THEN k."Ad" || ' kategorisindeki ürünleri keşfedin.'
        ELSE k."SeoDescription"
    END,
    "UstMetin" = CASE
        WHEN coalesce(nullif(btrim(k."UstMetin"), ''), '') = '' THEN k."Ad" || ' kategorisindeki ürünleri inceleyin.'
        ELSE k."UstMetin"
    END,
    "AltMetin" = CASE
        WHEN coalesce(nullif(btrim(k."AltMetin"), ''), '') = '' THEN k."Ad" || ' kategorisinde farklı ölçü ve tasarımları değerlendirebilirsiniz.'
        ELSE k."AltMetin"
    END,
    "KampanyaEtiketi" = CASE
        WHEN coalesce(nullif(btrim(k."KampanyaEtiketi"), ''), '') = '' THEN 'Seçili Koleksiyon'
        ELSE k."KampanyaEtiketi"
    END
WHERE NOT k."SilindiMi";

UPDATE "Urunler" u
SET
    "KisaAd" = CASE
        WHEN coalesce(nullif(btrim(u."KisaAd"), ''), '') = '' THEN left(u."Baslik", 80)
        ELSE u."KisaAd"
    END,
    "SKU" = CASE
        WHEN coalesce(nullif(btrim(u."SKU"), ''), '') = '' THEN 'URN-' || lpad(u."Id"::text, 6, '0')
        ELSE u."SKU"
    END,
    "Barkod" = CASE
        WHEN coalesce(nullif(btrim(u."Barkod"), ''), '') = '' THEN 'URN-' || lpad(u."Id"::text, 6, '0')
        ELSE u."Barkod"
    END,
    "Marka" = CASE
        WHEN coalesce(nullif(btrim(u."Marka"), ''), '') = '' THEN 'Canvasia'
        ELSE u."Marka"
    END,
    "Etiketler" = CASE
        WHEN coalesce(nullif(btrim(u."Etiketler"), ''), '') = '' THEN concat_ws(', ', k."Ad", 'kanvas tablo')
        ELSE u."Etiketler"
    END,
    "KisaAciklama" = CASE
        WHEN coalesce(nullif(btrim(u."KisaAciklama"), ''), '') = '' THEN 'Özel ölçü seçenekleriyle hazırlanan dekoratif kanvas tablo.'
        ELSE u."KisaAciklama"
    END,
    "Aciklama" = CASE
        WHEN coalesce(nullif(btrim(u."Aciklama"), ''), '') = '' THEN u."Baslik" || ' ürünü, yaşam alanlarında dekoratif kullanım için hazırlanan premium kanvas tablo koleksiyonunun parçasıdır.'
        ELSE u."Aciklama"
    END,
    "TeknikOzellikler" = CASE
        WHEN coalesce(nullif(btrim(u."TeknikOzellikler"), ''), '') = '' THEN E'Yüksek çözünürlüklü baskı\nKanvas yüzey\nFarklı ölçü seçenekleri'
        ELSE u."TeknikOzellikler"
    END,
    "MalzemeBilgisi" = CASE
        WHEN coalesce(nullif(btrim(u."MalzemeBilgisi"), ''), '') = '' THEN 'Yüksek kaliteli kanvas kumaş ve dayanıklı şase malzemesi kullanılır.'
        ELSE u."MalzemeBilgisi"
    END,
    "BakimTalimati" = CASE
        WHEN coalesce(nullif(btrim(u."BakimTalimati"), ''), '') = '' THEN 'Nemli olmayan yumuşak bez ile nazikçe temizleyiniz. Doğrudan su ve kimyasal temasından kaçınınız.'
        ELSE u."BakimTalimati"
    END,
    "PaketlemeBilgisi" = CASE
        WHEN coalesce(nullif(btrim(u."PaketlemeBilgisi"), ''), '') = '' THEN 'Ürün koruyucu ambalaj ile paketlenerek gönderilir.'
        ELSE u."PaketlemeBilgisi"
    END,
    "UretimSuresiGun" = CASE
        WHEN u."UretimSuresiGun" <= 0 THEN 3
        ELSE u."UretimSuresiGun"
    END,
    "KargoyaVerilisSuresiGun" = CASE
        WHEN u."KargoyaVerilisSuresiGun" <= 0 THEN 2
        ELSE u."KargoyaVerilisSuresiGun"
    END,
    "TahminiTeslimSuresiGun" = CASE
        WHEN u."TahminiTeslimSuresiGun" <= 0 THEN 5
        ELSE u."TahminiTeslimSuresiGun"
    END,
    "MinSiparisAdedi" = CASE
        WHEN u."MinSiparisAdedi" < 1 THEN 1
        ELSE u."MinSiparisAdedi"
    END,
    "MaxSiparisAdedi" = CASE
        WHEN u."MaxSiparisAdedi" IS NOT NULL AND u."MaxSiparisAdedi" < GREATEST(u."MinSiparisAdedi", 1) THEN GREATEST(u."MinSiparisAdedi", 1)
        ELSE u."MaxSiparisAdedi"
    END
FROM "Kategoriler" k
WHERE k."Id" = u."KategoriId"
  AND NOT u."SilindiMi";

UPDATE "UrunSecenekleri" s
SET
    "VaryantSku" = CASE
        WHEN coalesce(nullif(btrim(s."VaryantSku"), ''), '') = '' THEN coalesce(nullif(btrim(u."SKU"), ''), 'URN-' || lpad(u."Id"::text, 6, '0')) || '-VAR-' || lpad(s."Id"::text, 6, '0')
        ELSE s."VaryantSku"
    END,
    "GorselUrl" = CASE
        WHEN coalesce(nullif(btrim(s."GorselUrl"), ''), '') = '' THEN coalesce((
            SELECT r."ResimYolu"
            FROM "UrunResimleri" r
            WHERE r."UrunId" = s."UrunId"
              AND NOT r."SilindiMi"
            ORDER BY r."VarsayilanMi" DESC, r."Id"
            LIMIT 1
        ), u."AnaGorselUrl", s."GorselUrl")
        ELSE s."GorselUrl"
    END,
    "MalzemeTuru" = CASE
        WHEN coalesce(nullif(btrim(s."MalzemeTuru"), ''), '') = '' THEN 'Kanvas Baskı'
        ELSE s."MalzemeTuru"
    END,
    "CerceveRengi" = CASE
        WHEN coalesce(nullif(btrim(s."CerceveRengi"), ''), '') = '' THEN 'Standart'
        ELSE s."CerceveRengi"
    END,
    "Yon" = CASE
        WHEN coalesce(nullif(btrim(s."Yon"), ''), '') = '' THEN
            CASE
                WHEN lower(s."Olcu") LIKE '%yatay%' THEN 'Yatay'
                WHEN lower(s."Olcu") LIKE '%dikey%' THEN 'Dikey'
                WHEN lower(s."Olcu") LIKE '%kare%' THEN 'Kare'
                ELSE 'Standart'
            END
        ELSE s."Yon"
    END,
    "ParcaSayisi" = CASE
        WHEN s."ParcaSayisi" <= 0 THEN 1
        ELSE s."ParcaSayisi"
    END,
    "MaliyetFiyati" = CASE
        WHEN s."MaliyetFiyati" <= 0 THEN CASE WHEN u."Maliyet" > 0 THEN u."Maliyet" ELSE round((s."SatisFiyati" * 0.60)::numeric, 2) END
        ELSE s."MaliyetFiyati"
    END,
    "UretimSuresiGun" = CASE
        WHEN s."UretimSuresiGun" <= 0 THEN GREATEST(u."UretimSuresiGun", 3)
        ELSE s."UretimSuresiGun"
    END,
    "Desi" = CASE
        WHEN s."Desi" <= 0 THEN 1
        ELSE s."Desi"
    END
FROM "Urunler" u
WHERE u."Id" = s."UrunId"
  AND NOT s."SilindiMi";

WITH first_variant AS (
    SELECT DISTINCT ON (s."UrunId")
        s."Id",
        s."UrunId"
    FROM "UrunSecenekleri" s
    WHERE NOT s."SilindiMi"
      AND s."AktifMi"
    ORDER BY s."UrunId", s."VarsayilanMi" DESC, s."Sira", s."Id"
),
missing_default AS (
    SELECT fv."Id"
    FROM first_variant fv
    WHERE NOT EXISTS (
        SELECT 1
        FROM "UrunSecenekleri" x
        WHERE x."UrunId" = fv."UrunId"
          AND NOT x."SilindiMi"
          AND x."VarsayilanMi"
    )
)
UPDATE "UrunSecenekleri" s
SET "VarsayilanMi" = true
FROM missing_default md
WHERE s."Id" = md."Id";

UPDATE "Urunler" u
SET "StokDurumu" = CASE
    WHEN EXISTS (
        SELECT 1
        FROM "UrunSecenekleri" s
        WHERE s."UrunId" = u."Id"
          AND NOT s."SilindiMi"
          AND s."AktifMi"
          AND s."StokAdedi" > 0
    ) THEN 'Stokta'
    WHEN EXISTS (
        SELECT 1
        FROM "UrunSecenekleri" s
        WHERE s."UrunId" = u."Id"
          AND NOT s."SilindiMi"
          AND s."AktifMi"
          AND s."OnSipariseAcikMi"
    ) THEN 'OnSiparis'
    ELSE 'Tukendi'
END
WHERE NOT u."SilindiMi";

UPDATE "UrunResimleri" r
SET
    "Baslik" = CASE
        WHEN coalesce(nullif(btrim(r."Baslik"), ''), '') = '' THEN 'Galeri Görseli'
        ELSE r."Baslik"
    END,
    "AltMetin" = CASE
        WHEN coalesce(nullif(btrim(r."AltMetin"), ''), '') = '' THEN coalesce(nullif(btrim(u."Baslik"), ''), 'Ürün görseli')
        ELSE r."AltMetin"
    END,
    "MedyaTipi" = CASE
        WHEN coalesce(nullif(btrim(r."MedyaTipi"), ''), '') = '' THEN 'Gorsel'
        ELSE r."MedyaTipi"
    END,
    "MedyaAlani" = CASE
        WHEN coalesce(nullif(btrim(r."MedyaAlani"), ''), '') = '' THEN 'Galeri'
        ELSE r."MedyaAlani"
    END,
    "VideoUrl" = coalesce(r."VideoUrl", ''),
    "ThumbnailYolu" = CASE
        WHEN coalesce(nullif(btrim(r."ThumbnailYolu"), ''), '') = '' THEN coalesce(r."ResimYolu", '')
        ELSE r."ThumbnailYolu"
    END,
    "MobilResimYolu" = CASE
        WHEN coalesce(nullif(btrim(r."MobilResimYolu"), ''), '') = '' THEN coalesce(r."ResimYolu", '')
        ELSE r."MobilResimYolu"
    END,
    "Etiketler" = CASE
        WHEN coalesce(nullif(btrim(r."Etiketler"), ''), '') = '' THEN coalesce(nullif(btrim(u."Etiketler"), ''), 'galeri')
        ELSE r."Etiketler"
    END
FROM "Urunler" u
WHERE u."Id" = r."UrunId"
  AND NOT r."SilindiMi";

WITH ranked_media AS (
    SELECT
        r."Id",
        row_number() OVER (
            PARTITION BY r."UrunId"
            ORDER BY r."VarsayilanMi" DESC, r."Id"
        ) - 1 AS new_order
    FROM "UrunResimleri" r
    WHERE NOT r."SilindiMi"
)
UPDATE "UrunResimleri" r
SET "Sira" = rm.new_order
FROM ranked_media rm
WHERE r."Id" = rm."Id";

WITH first_media AS (
    SELECT DISTINCT ON (r."UrunId")
        r."Id",
        r."UrunId"
    FROM "UrunResimleri" r
    WHERE NOT r."SilindiMi"
    ORDER BY r."UrunId", r."VarsayilanMi" DESC, r."Sira", r."Id"
),
missing_media_default AS (
    SELECT fm."Id"
    FROM first_media fm
    WHERE NOT EXISTS (
        SELECT 1
        FROM "UrunResimleri" x
        WHERE x."UrunId" = fm."UrunId"
          AND NOT x."SilindiMi"
          AND x."VarsayilanMi"
    )
)
UPDATE "UrunResimleri" r
SET "VarsayilanMi" = true
FROM missing_media_default md
WHERE r."Id" = md."Id";

INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
SELECT '20260313235500_AddAdvancedProductMedia', '9.0.0'
WHERE NOT EXISTS (
    SELECT 1
    FROM "__EFMigrationsHistory"
    WHERE "MigrationId" = '20260313235500_AddAdvancedProductMedia'
);

COMMIT;
