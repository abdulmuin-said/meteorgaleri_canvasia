SELECT "Id", "Ad", "Slug", "Sira", "AktifMi" FROM "Kategoriler" WHERE "Slug" = 'test-sehpa-ve-yan-mobilya';
SELECT "Id", "Baslik", "Slug", "UrunTipi", "KategoriId", "AnaSayfadaGoster", "OneCikanMi", "YeniUrunMu" FROM "Urunler" WHERE "Slug" = 'test-lina-metal-yan-sehpa';
SELECT "Id", "UrunId", "Olcu", "CerceveTipi", "SatisFiyati", "VarsayilanMi", "AktifMi" FROM "UrunSecenekleri" WHERE "UrunId" = (SELECT "Id" FROM "Urunler" WHERE "Slug" = 'test-lina-metal-yan-sehpa');
SELECT t."Ad", d."Deger" FROM "UrunOzellikDegerleri" d JOIN "UrunOzellikTanimlari" t ON t."Id" = d."UrunOzellikTanimiId" WHERE d."UrunId" = (SELECT "Id" FROM "Urunler" WHERE "Slug" = 'test-lina-metal-yan-sehpa') ORDER BY t."Sira";
