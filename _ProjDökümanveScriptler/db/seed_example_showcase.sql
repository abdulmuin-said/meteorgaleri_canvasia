BEGIN;

ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "KisaAciklama" text NOT NULL DEFAULT '';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "Slug" text;
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "BannerUrl" text;
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "SeoTitle" text NOT NULL DEFAULT '';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "SeoDescription" text NOT NULL DEFAULT '';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "UstMetin" text NOT NULL DEFAULT '';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "AltMetin" text NOT NULL DEFAULT '';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "KampanyaEtiketi" text NOT NULL DEFAULT '';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "UrunSiralamaTipi" text NOT NULL DEFAULT 'manual';
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "Sira" integer NOT NULL DEFAULT 0;
ALTER TABLE "Kategoriler" ADD COLUMN IF NOT EXISTS "ParentKategoriId" integer;

CREATE INDEX IF NOT EXISTS "IX_Kategoriler_ParentKategoriId" ON "Kategoriler" ("ParentKategoriId");
CREATE INDEX IF NOT EXISTS "IX_Kategoriler_Slug" ON "Kategoriler" ("Slug");

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'FK_Kategoriler_Kategoriler_ParentKategoriId'
    ) THEN
        ALTER TABLE "Kategoriler"
            ADD CONSTRAINT "FK_Kategoriler_Kategoriler_ParentKategoriId"
            FOREIGN KEY ("ParentKategoriId")
            REFERENCES "Kategoriler" ("Id")
            ON DELETE RESTRICT;
    END IF;
END $$;

ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "KisaAd" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "SKU" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "Barkod" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "Marka" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "Etiketler" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "KisaAciklama" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "TeknikOzellikler" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "MalzemeBilgisi" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "BakimTalimati" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "PaketlemeBilgisi" text NOT NULL DEFAULT '';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "StokDurumu" text NOT NULL DEFAULT 'Stokta';
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "IndirimliFiyat" numeric;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "Maliyet" numeric NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "KdvOrani" numeric NOT NULL DEFAULT 20;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "UretimSuresiGun" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "KargoyaVerilisSuresiGun" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "TahminiTeslimSuresiGun" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "AktifMi" boolean NOT NULL DEFAULT TRUE;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "OneCikanMi" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "YeniUrunMu" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "KampanyaliMi" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "AnaSayfadaGoster" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "Sira" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "GoruntulenmeSayisi" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "SatisSayisi" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "FavoriSayisi" integer NOT NULL DEFAULT 0;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "MinSiparisAdedi" integer NOT NULL DEFAULT 1;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "MaxSiparisAdedi" integer;
ALTER TABLE "Urunler" ADD COLUMN IF NOT EXISTS "UrunTipi" text NOT NULL DEFAULT 'Genel';

CREATE INDEX IF NOT EXISTS "IX_Urunler_SKU" ON "Urunler" ("SKU");

ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "CerceveRengi" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "CerceveKalinligi" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "MalzemeTuru" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "Yon" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "ParcaSayisi" integer NOT NULL DEFAULT 1;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "VaryantSku" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "KisilestirmeMetni" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "OzelTasarimNotu" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "FiyatFarki" numeric NOT NULL DEFAULT 0;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "GorselUrl" text NOT NULL DEFAULT '';
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "AktifMi" boolean NOT NULL DEFAULT TRUE;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "VarsayilanMi" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "TukeninceGizle" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "OnSipariseAcikMi" boolean NOT NULL DEFAULT FALSE;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "Sira" integer NOT NULL DEFAULT 0;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "UretimSuresiGun" integer NOT NULL DEFAULT 0;
ALTER TABLE "UrunSecenekleri" ADD COLUMN IF NOT EXISTS "Desi" numeric NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS "UrunOzellikTanimlari"
(
    "Id" integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    "Ad" text NOT NULL,
    "Kod" text NOT NULL,
    "UrunTipi" text NOT NULL,
    "AlanTipi" text NOT NULL,
    "YardimMetni" text NOT NULL DEFAULT '',
    "Secenekler" text NOT NULL DEFAULT '',
    "FiltredeGoster" boolean NOT NULL DEFAULT FALSE,
    "DetaySayfasindaGoster" boolean NOT NULL DEFAULT TRUE,
    "TeknikTablodaGoster" boolean NOT NULL DEFAULT TRUE,
    "AktifMi" boolean NOT NULL DEFAULT TRUE,
    "Sira" integer NOT NULL DEFAULT 0,
    "OlusturulmaTarihi" timestamp with time zone NOT NULL DEFAULT NOW(),
    "SilindiMi" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS "UrunOzellikDegerleri"
(
    "Id" integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    "UrunId" integer NOT NULL,
    "UrunOzellikTanimiId" integer NOT NULL,
    "Deger" text NOT NULL DEFAULT '',
    "OlusturulmaTarihi" timestamp with time zone NOT NULL DEFAULT NOW(),
    "SilindiMi" boolean NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS "IX_UrunOzellikDegerleri_UrunId" ON "UrunOzellikDegerleri" ("UrunId");
CREATE INDEX IF NOT EXISTS "IX_UrunOzellikDegerleri_UrunOzellikTanimiId" ON "UrunOzellikDegerleri" ("UrunOzellikTanimiId");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_UrunOzellikTanimlari_UrunTipi_Kod" ON "UrunOzellikTanimlari" ("UrunTipi", "Kod");

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'FK_UrunOzellikDegerleri_UrunOzellikTanimlari_UrunOzellikTanimiId'
    ) THEN
        ALTER TABLE "UrunOzellikDegerleri"
            ADD CONSTRAINT "FK_UrunOzellikDegerleri_UrunOzellikTanimlari_UrunOzellikTanimiId"
            FOREIGN KEY ("UrunOzellikTanimiId")
            REFERENCES "UrunOzellikTanimlari" ("Id")
            ON DELETE CASCADE;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'FK_UrunOzellikDegerleri_Urunler_UrunId'
    ) THEN
        ALTER TABLE "UrunOzellikDegerleri"
            ADD CONSTRAINT "FK_UrunOzellikDegerleri_Urunler_UrunId"
            FOREIGN KEY ("UrunId")
            REFERENCES "Urunler" ("Id")
            ON DELETE CASCADE;
    END IF;
END $$;

INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
SELECT '20260313145500_ExpandCatalogMetadata', '9.0.0'
WHERE NOT EXISTS (
    SELECT 1 FROM "__EFMigrationsHistory" WHERE "MigrationId" = '20260313145500_ExpandCatalogMetadata'
);

INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
SELECT '20260313164000_ExpandProductVariants', '9.0.0'
WHERE NOT EXISTS (
    SELECT 1 FROM "__EFMigrationsHistory" WHERE "MigrationId" = '20260313164000_ExpandProductVariants'
);

INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
SELECT '20260313183000_AddDynamicProductFeatures', '9.0.0'
WHERE NOT EXISTS (
    SELECT 1 FROM "__EFMigrationsHistory" WHERE "MigrationId" = '20260313183000_AddDynamicProductFeatures'
);

INSERT INTO "UrunOzellikTanimlari"
(
    "Ad",
    "Kod",
    "UrunTipi",
    "AlanTipi",
    "YardimMetni",
    "Secenekler",
    "FiltredeGoster",
    "DetaySayfasindaGoster",
    "TeknikTablodaGoster",
    "AktifMi",
    "Sira",
    "OlusturulmaTarihi",
    "SilindiMi"
)
VALUES
    ('Renk', 'genel_renk', 'Genel', 'text', '', '', TRUE, TRUE, TRUE, TRUE, 10, NOW(), FALSE),
    ('Stil', 'genel_stil', 'Genel', 'select', '', E'Modern\nMinimal\nKlasik\nRustik\nEndustriyel', TRUE, TRUE, TRUE, TRUE, 20, NOW(), FALSE),
    ('Kullanim Alani', 'genel_kullanim_alani', 'Genel', 'select', '', E'Salon\nYatak Odasi\nOfis\nMutfak\nKoridor', TRUE, TRUE, TRUE, TRUE, 30, NOW(), FALSE),
    ('Govde Malzemesi', 'mobilya_govde_malzeme', 'SehpaMobilya', 'text', '', '', TRUE, TRUE, TRUE, TRUE, 610, NOW(), FALSE),
    ('Ayak Malzemesi', 'mobilya_ayak_malzeme', 'SehpaMobilya', 'text', '', '', TRUE, TRUE, TRUE, TRUE, 620, NOW(), FALSE),
    ('Tasima Kapasitesi', 'mobilya_tasima_kapasitesi', 'SehpaMobilya', 'text', '', '', FALSE, TRUE, TRUE, TRUE, 630, NOW(), FALSE),
    ('Kurulum Durumu', 'mobilya_kurulum', 'SehpaMobilya', 'select', '', E'Demonte\nHazir Kurulu', TRUE, TRUE, TRUE, TRUE, 640, NOW(), FALSE)
ON CONFLICT ("UrunTipi", "Kod") DO UPDATE
SET
    "Ad" = EXCLUDED."Ad",
    "AlanTipi" = EXCLUDED."AlanTipi",
    "YardimMetni" = EXCLUDED."YardimMetni",
    "Secenekler" = EXCLUDED."Secenekler",
    "FiltredeGoster" = EXCLUDED."FiltredeGoster",
    "DetaySayfasindaGoster" = EXCLUDED."DetaySayfasindaGoster",
    "TeknikTablodaGoster" = EXCLUDED."TeknikTablodaGoster",
    "AktifMi" = EXCLUDED."AktifMi",
    "Sira" = EXCLUDED."Sira";

DO $$
DECLARE
    existing_product_id integer;
    existing_category_id integer;
    category_id integer;
    product_id integer;
BEGIN
    SELECT "Id" INTO existing_product_id
    FROM "Urunler"
    WHERE "Slug" = 'test-lina-metal-yan-sehpa'
    LIMIT 1;

    IF existing_product_id IS NOT NULL THEN
        DELETE FROM "UrunOzellikDegerleri" WHERE "UrunId" = existing_product_id;
        DELETE FROM "UrunResimleri" WHERE "UrunId" = existing_product_id;
        DELETE FROM "UrunSecenekleri" WHERE "UrunId" = existing_product_id;
        DELETE FROM "Urunler" WHERE "Id" = existing_product_id;
    END IF;

    SELECT "Id" INTO existing_category_id
    FROM "Kategoriler"
    WHERE "Slug" = 'test-sehpa-ve-yan-mobilya'
    LIMIT 1;

    IF existing_category_id IS NOT NULL THEN
        DELETE FROM "Kategoriler" WHERE "Id" = existing_category_id;
    END IF;

    INSERT INTO "Kategoriler"
    (
        "Ad",
        "KisaAciklama",
        "Aciklama",
        "Slug",
        "GorselUrl",
        "BannerUrl",
        "SeoTitle",
        "SeoDescription",
        "UstMetin",
        "AltMetin",
        "KampanyaEtiketi",
        "UrunSiralamaTipi",
        "Sira",
        "AktifMi",
        "ParentKategoriId",
        "OlusturulmaTarihi",
        "SilindiMi"
    )
    VALUES
    (
        'Test Sehpa ve Yan Mobilya',
        'Yeni kategori altyapisini gostermek icin olusturulan test kategorisi.',
        'Bu kategori, ileride yeni urun aileleri eklenirken sistemin sabit kategoriye bagli kalmadigini gostermek icin olusturuldu.',
        'test-sehpa-ve-yan-mobilya',
        'https://placehold.co/800x800/e7ded3/4f3f39/png?text=Test+Kategori',
        'https://placehold.co/1600x600/e7ded3/4f3f39/png?text=Test+Sehpa+Kategorisi',
        'Test Sehpa ve Yan Mobilya',
        'Yeni kategori ekleme altyapisini gosteren test kategori kaydi.',
        'Kategori ust metni: yeni kategori yapisi artik serbest buyuyebilir.',
        'Kategori alt metni: bu kayit, ornek urun ve varyasyonlari test etmek icin eklendi.',
        'Showcase Testi',
        'manual',
        1,
        TRUE,
        NULL,
        NOW(),
        FALSE
    )
    RETURNING "Id" INTO category_id;

    INSERT INTO "Urunler"
    (
        "Baslik",
        "KisaAd",
        "Slug",
        "UrlYolu",
        "SKU",
        "Barkod",
        "Marka",
        "UrunTipi",
        "Etiketler",
        "KisaAciklama",
        "Aciklama",
        "TeknikOzellikler",
        "MalzemeBilgisi",
        "BakimTalimati",
        "PaketlemeBilgisi",
        "AnaGorselUrl",
        "StokDurumu",
        "Fiyat",
        "IndirimliFiyat",
        "Maliyet",
        "KdvOrani",
        "UretimSuresiGun",
        "KargoyaVerilisSuresiGun",
        "TahminiTeslimSuresiGun",
        "AktifMi",
        "OneCikanMi",
        "YeniUrunMu",
        "KampanyaliMi",
        "AnaSayfadaGoster",
        "Sira",
        "GoruntulenmeSayisi",
        "SatisSayisi",
        "FavoriSayisi",
        "MinSiparisAdedi",
        "MaxSiparisAdedi",
        "KategoriId",
        "OlusturulmaTarihi",
        "SilindiMi"
    )
    VALUES
    (
        'TEST Lina Metal Yan Sehpa',
        'Lina Yan Sehpa',
        'test-lina-metal-yan-sehpa',
        'test-lina-metal-yan-sehpa',
        'TST-SEHPA-LINA',
        '8690000000001',
        'Test Studio',
        'SehpaMobilya',
        'test,sehpa,mobilya,showcase',
        'Yeni urun veri modeli, varyasyon ve dinamik ozellik setini gosteren ornek urun.',
        '<p>Bu urun, yeni altyapiyi gormek icin eklenen ornek bir showcase kaydidir.</p><p>Varyasyon, teknik tablo, dinamik ozellik ve ana sayfa gosterimi birlikte test edilebilir.</p>',
        E'Govde: MDF uzeri ceviz kaplama\nAyak: Elektrostatik boyali metal\nTasima Kapasitesi: 35 kg\nKurulum: Demonte',
        'MDF uzeri ceviz kaplama tabla ve dayanikli metal ayak kullanilir.',
        'Nemli bez ile temizleyin. Asindirici kimyasal kullanmayin.',
        'Urun koruyucu kopuk ve cift kat koli ile sevk edilir.',
        'https://placehold.co/1200x1200/f5f1ea/5c4b44/png?text=TEST+Lina+Sehpa',
        'Stokta',
        4499,
        3999,
        2550,
        20,
        4,
        2,
        6,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        1,
        0,
        0,
        0,
        1,
        3,
        category_id,
        NOW(),
        FALSE
    )
    RETURNING "Id" INTO product_id;

    INSERT INTO "UrunResimleri"
    (
        "ResimYolu",
        "VarsayilanMi",
        "UrunId",
        "OlusturulmaTarihi",
        "SilindiMi"
    )
    VALUES
        ('https://placehold.co/1200x1200/f5f1ea/5c4b44/png?text=TEST+Lina+Sehpa', TRUE, product_id, NOW(), FALSE),
        ('https://placehold.co/1200x1200/ebe4da/5c4b44/png?text=TEST+Lina+Detay', FALSE, product_id, NOW(), FALSE);

    INSERT INTO "UrunSecenekleri"
    (
        "UrunId",
        "Olcu",
        "CerceveTipi",
        "CerceveRengi",
        "CerceveKalinligi",
        "MalzemeTuru",
        "Yon",
        "ParcaSayisi",
        "VaryantSku",
        "KisilestirmeMetni",
        "OzelTasarimNotu",
        "FiyatFarki",
        "SatisFiyati",
        "MaliyetFiyati",
        "StokAdedi",
        "UretimSuresiGun",
        "Desi",
        "GorselUrl",
        "AktifMi",
        "VarsayilanMi",
        "TukeninceGizle",
        "OnSipariseAcikMi",
        "Sira",
        "OlusturulmaTarihi",
        "SilindiMi"
    )
    VALUES
    (
        product_id,
        '45x45 cm',
        'Mat Siyah Ayak',
        'Siyah',
        '2 cm',
        'MDF Uzeri Kaplama',
        'Yuvarlak',
        1,
        'TST-SEHPA-LINA-45',
        '',
        'Salon ve oturma odasi icin ideal.',
        0,
        3499,
        2100,
        8,
        4,
        12,
        'https://placehold.co/1200x1200/f5f1ea/5c4b44/png?text=TEST+45x45',
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        1,
        NOW(),
        FALSE
    ),
    (
        product_id,
        '60x60 cm',
        'Ceviz Ahsap Ayak',
        'Ceviz',
        '2.5 cm',
        'MDF Uzeri Kaplama',
        'Kare',
        1,
        'TST-SEHPA-LINA-60',
        '',
        'Daha genis ust yuzey isteyen musteriler icin.',
        800,
        4299,
        2550,
        4,
        5,
        16,
        'https://placehold.co/1200x1200/ebe4da/5c4b44/png?text=TEST+60x60',
        TRUE,
        FALSE,
        FALSE,
        TRUE,
        2,
        NOW(),
        FALSE
    );

    INSERT INTO "UrunOzellikDegerleri"
    (
        "UrunId",
        "UrunOzellikTanimiId",
        "Deger",
        "OlusturulmaTarihi",
        "SilindiMi"
    )
    SELECT
        product_id,
        definition_id,
        definition_value,
        NOW(),
        FALSE
    FROM
    (
        SELECT "Id" AS definition_id, 'Ceviz' AS definition_value
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'Genel' AND "Kod" = 'genel_renk'
        UNION ALL
        SELECT "Id", 'Modern'
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'Genel' AND "Kod" = 'genel_stil'
        UNION ALL
        SELECT "Id", 'Salon'
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'Genel' AND "Kod" = 'genel_kullanim_alani'
        UNION ALL
        SELECT "Id", 'MDF uzeri ceviz kaplama'
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'SehpaMobilya' AND "Kod" = 'mobilya_govde_malzeme'
        UNION ALL
        SELECT "Id", 'Elektrostatik boyali metal'
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'SehpaMobilya' AND "Kod" = 'mobilya_ayak_malzeme'
        UNION ALL
        SELECT "Id", '35 kg'
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'SehpaMobilya' AND "Kod" = 'mobilya_tasima_kapasitesi'
        UNION ALL
        SELECT "Id", 'Demonte'
        FROM "UrunOzellikTanimlari"
        WHERE "UrunTipi" = 'SehpaMobilya' AND "Kod" = 'mobilya_kurulum'
    ) AS feature_values;
END $$;

COMMIT;
