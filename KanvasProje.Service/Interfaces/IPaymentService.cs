using System.Threading.Tasks;

namespace KanvasProje.Service.Interfaces
{
    /// <summary>
    /// Ödeme altyapısı için soyut arayüz.
    /// İyzico bugün kullanılıyor ancak yarın Stripe, PayTR vb. ile değiştirilebilir.
    /// </summary>
    public interface IPaymentService
    {
        /// <summary>
        /// Checkout formu başlatır ve ödeme sayfası HTML'ini döner.
        /// </summary>
        Task<PaymentInitResult> InitializeCheckoutAsync(PaymentInitRequest request);

        /// <summary>
        /// Callback sonrası ödeme sonucunu doğrular.
        /// </summary>
        Task<PaymentVerifyResult> VerifyPaymentAsync(string token);
    }

    public class PaymentInitRequest
    {
        public string OrderId { get; set; } = string.Empty;
        public decimal TotalPrice { get; set; }
        public decimal PaidPrice { get; set; }
        public string CallbackUrl { get; set; } = string.Empty;

        // Alıcı bilgileri
        public string BuyerId { get; set; } = string.Empty;
        public string BuyerName { get; set; } = string.Empty;
        public string BuyerSurname { get; set; } = string.Empty;
        public string BuyerEmail { get; set; } = string.Empty;
        public string BuyerPhone { get; set; } = string.Empty;
        public string BuyerAddress { get; set; } = string.Empty;
        public string BuyerCity { get; set; } = string.Empty;
        public string BuyerIp { get; set; } = string.Empty;

        // Sepet kalemleri
        public List<PaymentBasketItem> BasketItems { get; set; } = new();
    }

    public class PaymentBasketItem
    {
        public string Id { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public decimal Price { get; set; }
    }

    public class PaymentInitResult
    {
        public bool Success { get; set; }
        public string? CheckoutFormContent { get; set; }
        public string? Token { get; set; }
        public string? ErrorMessage { get; set; }
        public string? ErrorCode { get; set; }
    }

    public class PaymentVerifyResult
    {
        public bool Success { get; set; }
        public string? PaymentId { get; set; }
        public string? ConversationId { get; set; }
        public decimal PaidPrice { get; set; }
        public string? ErrorMessage { get; set; }
        public string? ErrorCode { get; set; }
        public int? Installment { get; set; }
        public string? CardAssociation { get; set; }
        public string? CardFamily { get; set; }
        public string? BinNumber { get; set; }
        public string? LastFourDigits { get; set; }
    }
}
