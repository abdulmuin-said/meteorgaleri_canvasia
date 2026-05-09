import os

# 1. Fix Iletisim.cshtml
iletisim_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Kurumsal\Iletisim.cshtml"
with open(iletisim_path, "r", encoding="utf-8") as f:
    iletisim = f.read()

# Replace the form with AJAX ready form
old_form = """            <form asp-action="Iletisim" asp-controller="Kurumsal" method="post" class="space-y-5">
                @Html.AntiForgeryToken()
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Ad Soyad</label>
                        <input name="AdSoyad" type="text" required placeholder="Adınız Soyadınız"
                               class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3]" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">E-posta</label>
                        <input name="Eposta" type="email" required placeholder="ornek@mail.com"
                               class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3]" />
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Konu</label>
                    <input name="Konu" type="text" required placeholder="Mesajınızın konusu"
                           class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3]" />
                </div>
                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Mesaj</label>
                    <textarea name="Mesaj" rows="5" required placeholder="Mesajınızı yazın..."
                              class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none resize-none bg-[#fcf9f3]"></textarea>
                </div>
                <button type="submit"
                        class="w-full bg-[#313511] text-white py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
                    Gönder
                </button>
            </form>"""

new_form = """            <form id="contactForm" asp-action="IletisimGonder" asp-controller="Kurumsal" method="post" class="space-y-5">
                @Html.AntiForgeryToken()
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Ad Soyad</label>
                        <input name="AdSoyad" type="text" required placeholder="Adınız Soyadınız"
                               class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] transition-colors" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">E-posta</label>
                        <input name="Email" type="email" required placeholder="ornek@mail.com"
                               class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] transition-colors" />
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Konu</label>
                    <input name="Konu" type="text" required placeholder="Mesajınızın konusu"
                           class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] transition-colors" />
                </div>
                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Mesaj</label>
                    <textarea name="Mesaj" rows="5" required placeholder="Mesajınızı yazın..."
                              class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none resize-none bg-[#fcf9f3] transition-colors"></textarea>
                </div>
                <button type="submit" id="contactSubmitBtn"
                        class="w-full bg-[#313511] text-white py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors flex items-center justify-center gap-2">
                    <i class="fas fa-paper-plane"></i> Gönder
                </button>
            </form>

            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const form = document.getElementById('contactForm');
                    if (form) {
                        form.addEventListener('submit', function(e) {
                            e.preventDefault();
                            
                            const btn = document.getElementById('contactSubmitBtn');
                            const originalContent = btn.innerHTML;
                            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gönderiliyor...';
                            btn.disabled = true;

                            const formData = new FormData(form);
                            
                            fetch(form.action, {
                                method: 'POST',
                                body: formData
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    if (window.showToast) {
                                        window.showToast(data.message || 'Mesajınız başarıyla iletildi.', 'success');
                                    }
                                    form.reset();
                                } else {
                                    if (window.showToast) {
                                        window.showToast(data.message || 'Bir hata oluştu.', 'error');
                                    }
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                if (window.showToast) {
                                    window.showToast('Bağlantı hatası oluştu. Lütfen tekrar deneyin.', 'error');
                                }
                            })
                            .finally(() => {
                                btn.innerHTML = originalContent;
                                btn.disabled = false;
                            });
                        });
                    }
                });
            </script>"""

iletisim = iletisim.replace(old_form, new_form)
with open(iletisim_path, "w", encoding="utf-8") as f:
    f.write(iletisim)


# 2. Fix IyzicoOdemeSayfasi.cshtml
iyzico_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Siparis\IyzicoOdemeSayfasi.cshtml"

new_iyzico = """@{
    ViewData["Title"] = "Güvenli Ödeme - Iyzico";
    Layout = "_Layout";
}

<!-- Breadcrumb -->
<div class="bg-[#f1ede7] border-b border-[#e5e2dc] py-4">
    <div class="container mx-auto px-4 flex items-center justify-center gap-4 text-xs tracking-widest uppercase">
        <span class="text-[#47473d] flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#e5e2dc] text-[#47473d] flex items-center justify-center font-bold">1</span> Sepet
        </span>
        <span class="text-[#e5e2dc]">/</span>
        <span class="text-[#47473d] flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#e5e2dc] text-[#47473d] flex items-center justify-center font-bold">2</span> Teslimat
        </span>
        <span class="text-[#e5e2dc]">/</span>
        <span class="text-[#313511] font-bold flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#313511] text-white flex items-center justify-center font-bold"><i class="fas fa-lock text-[10px]"></i></span> Ödeme Onayı
        </span>
    </div>
</div>

<div class="container mx-auto px-4 py-16">
    <div class="max-w-3xl mx-auto">
        <div class="bg-white border border-[#e5e2dc] rounded-lg shadow-sm overflow-hidden">
            <div class="border-b border-[#e5e2dc] bg-[#fcf9f3] py-5 px-6 flex items-center gap-3">
                <i class="fas fa-lock text-[#313511] text-2xl"></i>
                <div>
                    <h1 class="font-serif text-2xl text-[#313511] m-0">Güvenli Ödeme</h1>
                    <p class="text-xs text-[#47473d] mt-1">Kart bilgileriniz 256-bit SSL ile bankaya iletilir.</p>
                </div>
            </div>
            
            <div class="p-4 md:p-8">
                <!-- Iyzico Ödeme Formu -->
                <div id="iyzipay-checkout-form" class="responsive">
                    @Html.Raw(ViewBag.IyzicoContent)
                </div>
            </div>
        </div>
        
        <div class="text-center mt-6 text-[#47473d] text-sm flex items-center justify-center gap-2">
            <i class="fas fa-shield-alt text-[#b58735]"></i> Ödeme altyapısı <strong>Iyzico</strong> tarafından sağlanmaktadır.
        </div>
    </div>
</div>
"""

with open(iyzico_path, "w", encoding="utf-8") as f:
    f.write(new_iyzico)

print("Iletisim and Iyzico pages refactored.")
