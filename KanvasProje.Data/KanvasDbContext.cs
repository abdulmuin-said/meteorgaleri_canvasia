using KanvasProje.Core.Varliklar;
using KanvasProje.Core.Models;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace KanvasProje.Data
{
    // DbContext yerine IdentityDbContext<AppUser> yapıyoruz
    public class KanvasDbContext : IdentityDbContext<AppUser>
    {
        public KanvasDbContext(DbContextOptions<KanvasDbContext> options) : base(options)
        {
        }

        public DbSet<Urun> Urunler { get; set; }
        public DbSet<Kategori> Kategoriler { get; set; }
        public DbSet<UrunSecenek> UrunSecenekleri { get; set; }
        public DbSet<UrunOzellikTanimi> UrunOzellikTanimlari { get; set; }
        public DbSet<UrunOzellikDegeri> UrunOzellikDegerleri { get; set; }
        public DbSet<Siparis> Siparisler { get; set; }
        public DbSet<SiparisDetay> SiparisDetaylari { get; set; }
        public DbSet<KargoFirmasi> KargoFirmalari { get; set; }
        public DbSet<Adres> Adresler { get; set; }
        // ... diğer DbSetler ...
        public DbSet<UrunResim> UrunResimleri { get; set; }
        public DbSet<Favori> Favoriler { get; set; }
        public DbSet<ZiyaretciLog> ZiyaretciLoglari { get; set; }
        public DbSet<KurumsalSayfa> KurumsalSayfalar { get; set; }
        public DbSet<IadeTalebi> IadeTalepleri { get; set; }
        public DbSet<Kupon> Kuponlar { get; set; }
        public DbSet<Yorum> Yorumlar { get; set; }
        public DbSet<BultenAboneligi> BultenAbonelikleri { get; set; }
        public DbSet<IletisimMesaj> IletisimMesajlari { get; set; }
        public DbSet<SenTasarla> SenTasarla { get; set;}
        
        public DbSet<SiteAyarlari> SiteAyarlari { get; set; }
        
        public DbSet<Slayt> Slaytlar { get; set; }
        
        // PHASE 8: Database-backed Cart System
        public DbSet<Sepet> Sepetler { get; set; }
        public DbSet<SepetItem> SepetItems { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Identity tablolarının (AspNetUsers vs.) oluşması için bu satır ZORUNLU!
            base.OnModelCreating(modelBuilder);

            // Bizim eski ayarlar (Soft Delete vs.)
            modelBuilder.Entity<Urun>().HasQueryFilter(x => !x.SilindiMi);
            modelBuilder.Entity<Kategori>().HasQueryFilter(x => !x.SilindiMi);
            modelBuilder.Entity<UrunResim>().HasQueryFilter(x => !x.SilindiMi);
            modelBuilder.Entity<UrunOzellikTanimi>().HasQueryFilter(x => !x.SilindiMi);

            modelBuilder.Entity<UrunSecenek>()
                .HasOne(us => us.Urun)
                .WithMany(u => u.UrunSecenek)
                .HasForeignKey(us => us.UrunId) // UrunId kolonunu kullanmaya zorla
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<UrunOzellikDegeri>()
                .HasOne(od => od.Urun)
                .WithMany(u => u.UrunOzellikleri)
                .HasForeignKey(od => od.UrunId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<UrunOzellikDegeri>()
                .HasOne(od => od.UrunOzellikTanimi)
                .WithMany(ot => ot.UrunOzellikDegerleri)
                .HasForeignKey(od => od.UrunOzellikTanimiId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<Kategori>()
                .HasOne(k => k.ParentKategori)
                .WithMany(k => k.AltKategoriler)
                .HasForeignKey(k => k.ParentKategoriId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<UrunOzellikTanimi>()
                .HasIndex(x => new { x.UrunTipi, x.Kod })
                .IsUnique();

            modelBuilder.Entity<Urun>()
                .HasIndex(x => x.Slug)
                .HasFilter("\"Slug\" IS NOT NULL AND \"Slug\" <> ''");

            modelBuilder.Entity<Kategori>()
                .HasIndex(x => x.Slug)
                .HasFilter("\"Slug\" IS NOT NULL AND \"Slug\" <> ''");

            modelBuilder.Entity<UrunResim>()
                .HasIndex(x => new { x.UrunId, x.Sira });

            modelBuilder.Entity<KargoFirmasi>()
                .HasIndex(x => x.Kod)
                .IsUnique();
        }
    }
}
