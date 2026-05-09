import os

layout_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml"
with open(layout_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """                }

                <a href="/Sepet" aria-label="Sepet" class="relative">"""

replacement = """                }

                <!-- Favoriler -->
                <a href="/Favori" aria-label="Favoriler" class="hover:text-red-500 transition-colors hidden md:block">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>
                </a>

                <a href="/Sepet" aria-label="Sepet" class="relative">"""

if target in content:
    content = content.replace(target, replacement)
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Layout successfully updated with Heart Icon!")
else:
    print("Target not found.")