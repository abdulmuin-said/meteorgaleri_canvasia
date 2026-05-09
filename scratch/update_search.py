import re

file_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the old search dropdown logic
old_search_block = """                <div class="relative mr-2">
                    <button type="button" aria-label="Arama" onclick="document.getElementById('searchDropdown').classList.toggle('hidden'); document.getElementById('searchInput').focus();" class="flex items-center justify-center hover:text-[#b58735] transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 24 24"><path d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                    </button>
                    <!-- Search Dropdown -->
                    <div id="searchDropdown" class="hidden absolute top-full right-0 mt-4 w-72 bg-white border border-[#e5e2dc] shadow-lg rounded p-3 z-50">
                        <form asp-controller="Urun" asp-action="Index" method="get" class="flex items-center">
                            <input type="text" id="searchInput" name="s" placeholder="Ne aramıştınız?" class="flex-1 bg-[#fcf9f3] border border-[#e5e2dc] rounded px-3 py-2 text-sm focus:outline-none focus:border-[#313511] text-[#1c1c18]" />
                            <button type="submit" class="bg-[#313511] text-white px-4 py-2 ml-2 rounded text-xs uppercase tracking-widest hover:bg-[#1c2001] transition-colors">Ara</button>
                        </form>
                    </div>
                </div>"""

new_search_btn = """                <div class="relative mr-2">
                    <button type="button" aria-label="Arama" onclick="document.getElementById('fullscreenSearch').classList.remove('hidden'); document.getElementById('fullscreenSearch').classList.add('flex'); setTimeout(() => document.getElementById('fullscreenSearchInput').focus(), 100);" class="flex items-center justify-center hover:text-[#b58735] transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 24 24"><path d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                    </button>
                </div>"""

content = content.replace(old_search_block, new_search_btn)

# Remove the old jQuery outside click listener for searchDropdown
old_jquery = """            // Close search dropdown when clicking outside
            $(document).on('click', function(e) {
                var searchContainer = $('.relative.mr-2');
                if (!searchContainer.is(e.target) && searchContainer.has(e.target).length === 0) {
                    $('#searchDropdown').addClass('hidden');
                }
            });"""
content = content.replace(old_jquery, "")


# 2. Append the Fullscreen overlay right before </body>
fullscreen_overlay = """
    <!-- Fullscreen Search Overlay -->
    <div id="fullscreenSearch" class="fixed inset-0 z-[100] hidden bg-[#fcf9f3] bg-opacity-95 backdrop-blur-md flex-col items-center justify-center transition-opacity duration-300">
        <button type="button" onclick="document.getElementById('fullscreenSearch').classList.add('hidden'); document.getElementById('fullscreenSearch').classList.remove('flex');" class="absolute top-8 right-8 text-[#313511] hover:text-[#b58735] transition-colors z-[101]">
            <i class="fas fa-times text-4xl"></i>
        </button>
        <div class="w-full max-w-3xl px-6 relative">
            <p class="text-center text-xs tracking-widest uppercase text-[#47473d] mb-6 font-medium">Ne Aramıştınız?</p>
            <form asp-controller="Urun" asp-action="Index" method="get" class="relative">
                <input type="text" id="fullscreenSearchInput" name="s" placeholder="Ürün, koleksiyon veya renk arayın..." class="w-full bg-transparent border-0 border-b-2 border-[#e5e2dc] focus:ring-0 focus:border-[#313511] text-2xl md:text-4xl text-center text-[#1c1c18] pb-4 placeholder-gray-300 font-serif outline-none" autocomplete="off" />
                <button type="submit" class="absolute right-2 bottom-4 text-[#313511] hover:text-[#b58735] transition-colors">
                    <i class="fas fa-arrow-right text-2xl"></i>
                </button>
            </form>
        </div>
    </div>
"""

content = content.replace("</body>", fullscreen_overlay + "\n</body>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("_Layout.cshtml updated with fullscreen search overlay")
