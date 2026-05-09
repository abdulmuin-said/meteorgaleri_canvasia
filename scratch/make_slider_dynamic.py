import re

with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Home\Index.cshtml', 'r', encoding='utf-8') as f:
    content = f.read()

slider_html = """@if (homePageSettings.Hero.Enabled && homePageSettings.Hero.DesktopSlides.Any())
{
<!-- BEGIN: HeroSection - Otomatik Slider -->
<section class="relative w-full h-[600px] md:h-[700px] overflow-hidden" id="heroSlider">

    <!-- Slayt Görselleri -->
    <div id="heroTrack" class="flex h-full transition-transform duration-700 ease-in-out will-change-transform">

        @for (int i = 0; i < homePageSettings.Hero.DesktopSlides.Count; i++)
        {
            var slide = homePageSettings.Hero.DesktopSlides[i];
            <div class="hero-slide relative flex-shrink-0 w-full h-full">
                <img src="@(string.IsNullOrEmpty(slide.ImageUrl) ? "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1600&q=80&auto=format&fit=crop" : slide.ImageUrl)" 
                     alt="@slide.Title" class="absolute inset-0 w-full h-full object-cover">
                <div class="absolute inset-0 bg-gradient-to-r from-black/60 via-black/25 to-transparent"></div>
                <div class="absolute inset-0 flex items-center">
                    <div class="container mx-auto px-8 md:px-16">
                        @if (!string.IsNullOrEmpty(slide.Subtitle))
                        {
                            <p class="text-xs text-[#c6ca99] tracking-[0.3em] uppercase mb-4 font-light hero-subtitle">@slide.Subtitle</p>
                        }
                        @if (!string.IsNullOrEmpty(slide.Title))
                        {
                            <h2 class="font-serif text-5xl md:text-7xl lg:text-8xl text-white mb-5 tracking-wider leading-none hero-title">@Html.Raw(slide.Title.Replace("\\n", "<br>"))</h2>
                        }
                        @if (!string.IsNullOrEmpty(slide.Description))
                        {
                            <p class="text-base md:text-lg font-light mb-8 tracking-wide text-white/80 max-w-md hero-desc">@slide.Description</p>
                        }
                        @if (!string.IsNullOrEmpty(slide.ButtonText))
                        {
                            <a href="@(string.IsNullOrEmpty(slide.ButtonUrl) ? "/Urun" : slide.ButtonUrl)" class="inline-block border border-white text-white px-8 py-3 text-xs tracking-[0.2em] hover:bg-white hover:text-[#313511] transition-all duration-300 uppercase rounded-full hero-btn">
                                @slide.ButtonText
                            </a>
                        }
                    </div>
                </div>
            </div>
        }

    </div>

    <!-- Ok Butonları (Sol / Sağ) -->
    <button id="heroPrev" onclick="heroSlide(-1)" aria-label="Önceki slayt"
            class="absolute left-4 md:left-8 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full bg-white/20 backdrop-blur-sm text-white flex items-center justify-center hover:bg-white/40 transition-all duration-300 group">
        <svg class="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/>
        </svg>
    </button>
    <button id="heroNext" onclick="heroSlide(1)" aria-label="Sonraki slayt"
            class="absolute right-4 md:right-8 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full bg-white/20 backdrop-blur-sm text-white flex items-center justify-center hover:bg-white/40 transition-all duration-300 group">
        <svg class="w-5 h-5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
        </svg>
    </button>

    <!-- Nokta İndikatörler -->
    <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2" id="heroDots">
        @for (int i = 0; i < homePageSettings.Hero.DesktopSlides.Count; i++)
        {
            <button onclick="heroGoTo(@i)" class="hero-dot w-1.5 h-1.5 rounded-full bg-white/50 transition-all duration-300" aria-label="Slayt @(i+1)"></button>
        }
    </div>

    <!-- İlerleme Çubuğu -->
    <div class="absolute bottom-0 left-0 h-0.5 bg-white/30 w-full z-20">
        <div id="heroProgress" class="h-full bg-[#c6ca99] transition-none" style="width: 0%"></div>
    </div>

</section>
<!-- END: HeroSection -->
}"""

# Replace HTML
content = re.sub(r'<!-- BEGIN: HeroSection - Otomatik Slider -->.*?<!-- END: HeroSection -->', slider_html, content, flags=re.DOTALL)

# Replace Javascript count
js_pattern = r'const TOTAL = 3;'
js_replacement = 'const TOTAL = @(homePageSettings.Hero.DesktopSlides.Count > 0 ? homePageSettings.Hero.DesktopSlides.Count : 1);'
content = content.replace(js_pattern, js_replacement)

with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Home\Index.cshtml', 'w', encoding='utf-8') as f:
    f.write(content)

print('Frontend Slider is now dynamic!')
