---
name: Artisan Canvas
colors:
  surface: '#fcf9f3'
  surface-dim: '#dddad4'
  surface-bright: '#fcf9f3'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3ed'
  surface-container: '#f1ede7'
  surface-container-high: '#ebe8e2'
  surface-container-highest: '#e5e2dc'
  on-surface: '#1c1c18'
  on-surface-variant: '#47473d'
  inverse-surface: '#31302d'
  inverse-on-surface: '#f4f0ea'
  outline: '#78786c'
  outline-variant: '#c8c7b9'
  surface-tint: '#5d6139'
  primary: '#1c2001'
  on-primary: '#ffffff'
  primary-container: '#313511'
  on-primary-container: '#9a9e70'
  inverse-primary: '#c6ca99'
  secondary: '#7e5702'
  on-secondary: '#ffffff'
  secondary-container: '#ffc970'
  on-secondary-container: '#785300'
  tertiary: '#281631'
  on-tertiary: '#ffffff'
  tertiary-container: '#3e2b47'
  on-tertiary-container: '#ab92b4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2e6b3'
  primary-fixed-dim: '#c6ca99'
  on-primary-fixed: '#1a1e00'
  on-primary-fixed-variant: '#454a23'
  secondary-fixed: '#ffdeac'
  secondary-fixed-dim: '#f2be66'
  on-secondary-fixed: '#281900'
  on-secondary-fixed-variant: '#604100'
  tertiary-fixed: '#f5d9fe'
  tertiary-fixed-dim: '#d8bde1'
  on-tertiary-fixed: '#26142f'
  on-tertiary-fixed-variant: '#543f5d'
  background: '#fcf9f3'
  on-background: '#1c1c18'
  surface-variant: '#e5e2dc'
typography:
  display-xl:
    fontFamily: notoSerif
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: notoSerif
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: notoSerif
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: manrope
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.1em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 24px
  margin: 40px
  section-gap: 80px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

Bu tasarım sistemi, küratörlü bir sanat galerisinin sessiz özgüvenini ve sofistike duruşunu dijital ortama taşımayı hedefler. Temel odak noktası, ürünün (sanat eserinin) kendisidir; arayüz, eseri gölgelemek yerine onu çerçeveleyen şık ve minimal bir sahne görevi görür.

**Minimalizm ve Editoryal Estetik:** Geniş beyaz alanlar (whitespace), güçlü tipografik hiyerarşi ve asimetrik grid yapıları ile dergi kalitesinde bir deneyim sunulur. Gereksiz süslemelerden kaçınılarak, "az ama öz" felsefesi benimsenmiştir. Kullanıcıda uyandırılmak istenen duygu; güven, seçkinlik ve sanatsal derinliktir.

## Colors

Renk paleti, doğadan ve klasik sanat materyallerinden ilham alır. **Koyu Zeytin Yeşili (#313511)**, markanın köklü ve ciddi duruşunu temsil eden ana kurumsal renktir. **Hardal Altın (#b58735)**, dikkat çekilmesi gereken etkileşim noktalarında ve vurgularda premium bir dokunuş sağlar.

Arka planlarda kullanılan saf beyaz ve açık gri tonları, galerideki boş duvarları simgeler. Metin renklerinde tam siyah yerine çok koyu gri tonları tercih edilerek, Playfair Display tipografisinin okunabilirliği ve zarafeti korunmuştur.

## Typography

Tipografi seçimi, geleneksel zanaatkarlık ile modern kullanıcı deneyimi arasındaki köprüdür. 

- **Başlıklar (notoSerif):** "Playfair Display" karakterini yansıtan, editoryal bir derinliğe sahip serif yazı tipi. Büyük ölçekli kullanımlarda markanın premium algısını pekiştirir.
- **Gövde Metinleri (manrope):** "Lato"nun temizliğini ve modernliğini sunan sans-serif font. Uzun okumalarda gözü yormaz ve bilgi mimarisini net bir şekilde destekler.
- **Vurgular:** Küçük etiketlerde ve yardımcı metinlerde büyük harf (uppercase) ve geniş harf arası boşluk (letter-spacing) kullanılarak küratör notu estetiği oluşturulur.

## Layout & Spacing

Tasarım sistemi, nefes alan bir **sabit grid (fixed grid)** yapısı üzerine kuruludur. İçerik, maksimum 1280px genişliğindeki güvenli alanda toplanır. 

**Ritim:** 8px tabanlı bir spacing sistemi kullanılır. Ancak editoryal hissi güçlendirmek için bölümler arasındaki dikey boşluklar (section-gap) cömert tutulmuştur (80px+). Görseller ve metin blokları arasında asimetrik yerleşimler tercih edilerek statik bir e-ticaret görünümünden uzaklaşılır.

## Elevation & Depth

Bu tasarım sisteminde derinlik, gölgelerden ziyade **tonal katmanlar** ve **ince çizgiler** (low-contrast outlines) ile sağlanır. 

- **Katmanlama:** Kartlar ve konteynerler için gölge yerine `#f6f6f8` renginde zeminler veya 1px kalınlığında çok açık gri sınır çizgileri kullanılır.
- **Odak:** Yalnızca çok kritik aksiyonlarda (modal veya dropdown gibi) son derece yumuşak, fark edilmesi zor, yayılımı (blur) yüksek ve opaklığı düşük (#000000 %5) ambiyans gölgeleri tercih edilebilir.
- **Cam Etkisi:** Ürün detay sayfalarında, görselin üzerine binen metin bloklarında hafif bir backdrop-blur (buzlu cam) etkisi kullanılarak modern bir dokunuş eklenir.

## Shapes

Tasarım sisteminin imza niteliğindeki görsel öğesi, **yüksek yuvarlaklık (pill-shaped)** değerleridir. 

Keskin köşeli görseller ve tipografi ile kontrast oluşturması için etkileşimli öğelerde (butonlar, arama çubukları, etiketler) 40px ve üzeri border-radius kullanılır. Bu seçim, "sanat galerisi" ciddiyetini modern ve ulaşılabilir bir kullanıcı dostu yaklaşımla dengeler. Sanat eserlerini temsil eden görseller ise her zaman keskin (0px) köşelere sahip olmalıdır; bu, eserin orijinalliğini ve çerçeve yapısını korur.

## Components

**Butonlar:**
- **Primary:** Koyu Zeytin Yeşili (#313511) arka plan, beyaz metin. 40px köşe yuvarlaklığı. Hover durumunda Hardal Altın (#b58735) rengine yumuşak bir geçiş yapılır.
- **Secondary:** İnce zeytin yeşili çerçeve, zeytin yeşili metin, şeffaf arka plan.

**Girdi Alanları (Input Fields):**
- Altı çizili (border-bottom) veya çok hafif gri dolgulu, minimal tasarımlar. Odaklanıldığında (focus) alt çizgi Hardal Altın rengine döner.

**Kartlar (Cards):**
- Çerçevesiz, temiz beyaz zemin üzerine oturan, metinlerin görselin altında geniş boşluklarla yer aldığı editoryal kart yapısı.

**Çipler (Chips/Labels):**
- Koleksiyon isimleri veya sanatçı kategorileri için küçük, tamamı büyük harf ve pill-shaped yapıda düşük kontrastlı etiketler.

**Ek Bileşenler:**
- **Sanatçı İmzası:** Sanatçı isimleri için özel bir italik serif stil kullanımı.
- **Küratör Notu:** Ürün sayfalarında açık gri bloklar içinde sunulan, özel tipografik tırnak işaretleri içeren açıklama alanları.