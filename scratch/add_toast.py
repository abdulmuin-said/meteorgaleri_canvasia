import re

layout_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml"

with open(layout_path, "r", encoding="utf-8") as f:
    layout = f.read()

# Add Toast Container
toast_container = """
    <!-- Toast Notification Container -->
    <div id="toastContainer" class="fixed bottom-4 left-4 z-[110] flex flex-col gap-3"></div>
"""
layout = layout.replace("<!-- Fullscreen Search Overlay -->", toast_container + "\n    <!-- Fullscreen Search Overlay -->")

# Add showToast JS function
toast_js = """
        window.showToast = function(message, type = 'success') {
            const container = document.getElementById('toastContainer');
            if (!container) return;

            const toast = document.createElement('div');
            toast.className = 'transform translate-y-10 opacity-0 transition-all duration-500 ease-out flex items-center gap-3 px-6 py-4 rounded shadow-lg backdrop-blur-md min-w-[300px] border-l-4';
            
            let iconHtml = '';
            if (type === 'success') {
                toast.classList.add('bg-[#fcf9f3]', 'bg-opacity-95', 'text-[#313511]', 'border-[#313511]');
                iconHtml = '<i class="fas fa-check-circle text-xl text-[#313511]"></i>';
            } else if (type === 'error') {
                toast.classList.add('bg-white', 'bg-opacity-95', 'text-red-800', 'border-red-600');
                iconHtml = '<i class="fas fa-exclamation-circle text-xl text-red-600"></i>';
            } else {
                toast.classList.add('bg-white', 'bg-opacity-95', 'text-blue-800', 'border-blue-600');
                iconHtml = '<i class="fas fa-info-circle text-xl text-blue-600"></i>';
            }

            toast.innerHTML = `
                ${iconHtml}
                <div class="flex-1">
                    <p class="font-medium text-sm tracking-wide font-sans">${message}</p>
                </div>
                <button onclick="this.parentElement.remove()" class="text-gray-400 hover:text-[#313511] transition-colors ml-4">
                    <i class="fas fa-times"></i>
                </button>
            `;

            container.appendChild(toast);

            // Trigger animation
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    toast.classList.remove('translate-y-10', 'opacity-0');
                    toast.classList.add('translate-y-0', 'opacity-100');
                });
            });

            // Auto remove
            setTimeout(() => {
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-10', 'opacity-0');
                setTimeout(() => toast.remove(), 500);
            }, 4000);
        };
"""

# Replace newsletter AJAX logic in layout
old_newsletter = """                    success: function(response) {
                        messageDiv.removeClass('hidden text-red-400 text-green-400');
                        if (response.success) {
                            messageDiv.addClass('text-green-400').text(response.message || 'Başarıyla abone oldunuz.');
                            $('#newsletterEmail').val('');
                        } else {
                            messageDiv.addClass('text-red-400').text(response.message || 'Bir hata oluştu.');
                        }
                        btn.text(originalBtnText).prop('disabled', false);
                    },
                    error: function() {
                        messageDiv.removeClass('hidden text-green-400').addClass('text-red-400').text('Bağlantı hatası oluştu.');
                        btn.text(originalBtnText).prop('disabled', false);
                    }"""

new_newsletter = """                    success: function(response) {
                        if (response.success) {
                            window.showToast(response.message || 'Başarıyla abone oldunuz.', 'success');
                            $('#newsletterEmail').val('');
                        } else {
                            window.showToast(response.message || 'Bir hata oluştu.', 'error');
                        }
                        btn.text(originalBtnText).prop('disabled', false);
                    },
                    error: function() {
                        window.showToast('Bağlantı hatası oluştu.', 'error');
                        btn.text(originalBtnText).prop('disabled', false);
                    }"""

layout = layout.replace(old_newsletter, new_newsletter)
layout = layout.replace("});\n    </script>", "});\n" + toast_js + "\n    </script>")

with open(layout_path, "w", encoding="utf-8") as f:
    f.write(layout)

# -----------------
# Detay.cshtml 
detay_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml"
with open(detay_path, "r", encoding="utf-8") as f:
    detay = f.read()

old_detay_ajax = """        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'RequestVerificationToken': token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.innerHTML = '<i class="fas fa-check"></i> Eklendi';
                this.style.background = '#4CAF50';
                this.style.borderColor = '#4CAF50';
                
                const cartCounter = document.getElementById('cartItemCount');
                if (cartCounter) {
                    let current = parseInt(cartCounter.innerText) || 0;
                    let added = parseInt(formData.get('Adet')) || 1;
                    cartCounter.innerText = current + added;
                }

                setTimeout(() => {
                    this.innerHTML = originalHtml;
                    this.style.background = '';
                    this.style.borderColor = '';
                    this.disabled = false;
                }, 2000);
            } else {
                alert(data.message || 'Hata oluştu');
                this.innerHTML = originalHtml;
                this.disabled = false;
            }
        })
        .catch(error => {
            console.error(error);
            alert('Bağlantı hatası');
            this.innerHTML = originalHtml;
            this.disabled = false;
        });"""

new_detay_ajax = """        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'RequestVerificationToken': token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (window.showToast) {
                    window.showToast('Ürün başarıyla sepetinize eklendi.', 'success');
                }
                
                const cartCounter = document.getElementById('cartItemCount');
                if (cartCounter) {
                    let current = parseInt(cartCounter.innerText) || 0;
                    let added = parseInt(formData.get('Adet')) || 1;
                    cartCounter.innerText = current + added;
                    
                    // Simple pop animation on the cart counter
                    cartCounter.classList.add('scale-150');
                    setTimeout(() => cartCounter.classList.remove('scale-150'), 300);
                }

                this.innerHTML = originalHtml;
                this.disabled = false;
            } else {
                if (window.showToast) {
                    window.showToast(data.message || 'Hata oluştu', 'error');
                } else {
                    alert(data.message || 'Hata oluştu');
                }
                this.innerHTML = originalHtml;
                this.disabled = false;
            }
        })
        .catch(error => {
            console.error(error);
            if (window.showToast) {
                window.showToast('Bağlantı hatası oluştu.', 'error');
            } else {
                alert('Bağlantı hatası');
            }
            this.innerHTML = originalHtml;
            this.disabled = false;
        });"""

detay = detay.replace(old_detay_ajax, new_detay_ajax)

with open(detay_path, "w", encoding="utf-8") as f:
    f.write(detay)

print("Toast system implemented in Layout and Detay.")
