using System;
using System.Collections.Generic;
using System.Globalization;
using System.Threading.Tasks;
using Iyzipay;
using Iyzipay.Model;
using Iyzipay.Request;
using KanvasProje.Service.Interfaces;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace KanvasProje.Service.Services
{
    /// <summary>
    /// İyzico ödeme altyapısı implementasyonu.
    /// IPaymentService arayüzünü uygular; böylece Controller ve iş mantığı
    /// doğrudan İyzico'ya bağımlı olmaz.
    /// </summary>
    public class IyzicoPaymentService : IPaymentService
    {
        private readonly IConfiguration _config;
        private readonly ILogger<IyzicoPaymentService> _logger;

        public IyzicoPaymentService(IConfiguration config, ILogger<IyzicoPaymentService> logger)
        {
            _config = config;
            _logger = logger;
        }

        private Options GetOptions()
        {
            return new Options
            {
                ApiKey = _config["Iyzico:ApiKey"] ?? throw new InvalidOperationException("Iyzico:ApiKey yapılandırılmamış."),
                SecretKey = _config["Iyzico:SecretKey"] ?? throw new InvalidOperationException("Iyzico:SecretKey yapılandırılmamış."),
                BaseUrl = _config["Iyzico:BaseUrl"] ?? "https://sandbox-api.iyzipay.com"
            };
        }

        public Task<PaymentInitResult> InitializeCheckoutAsync(PaymentInitRequest request)
        {
            try
            {
                var options = GetOptions();

                var formRequest = new CreateCheckoutFormInitializeRequest
                {
                    Locale = Locale.TR.ToString(),
                    ConversationId = request.OrderId,
                    Price = request.TotalPrice.ToString("F2", CultureInfo.InvariantCulture),
                    PaidPrice = request.PaidPrice.ToString("F2", CultureInfo.InvariantCulture),
                    Currency = Currency.TRY.ToString(),
                    BasketId = request.OrderId,
                    PaymentGroup = PaymentGroup.PRODUCT.ToString(),
                    CallbackUrl = request.CallbackUrl,
                    EnabledInstallments = new List<int> { 1, 2, 3, 6, 9, 12 }
                };

                // Alıcı bilgileri
                formRequest.Buyer = new Buyer
                {
                    Id = request.BuyerId,
                    Name = request.BuyerName,
                    Surname = request.BuyerSurname,
                    GsmNumber = NormalizePhone(request.BuyerPhone),
                    Email = request.BuyerEmail,
                    IdentityNumber = "11111111111",
                    LastLoginDate = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
                    RegistrationDate = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
                    RegistrationAddress = request.BuyerAddress,
                    Ip = request.BuyerIp,
                    City = request.BuyerCity,
                    Country = "Turkey",
                    ZipCode = "34000"
                };

                // Teslimat adresi
                var address = new Address
                {
                    ContactName = $"{request.BuyerName} {request.BuyerSurname}",
                    City = request.BuyerCity,
                    Country = "Turkey",
                    Description = request.BuyerAddress,
                    ZipCode = "34000"
                };
                formRequest.ShippingAddress = address;
                formRequest.BillingAddress = address;

                // Sepet kalemleri
                var basketItems = new List<BasketItem>();
                foreach (var item in request.BasketItems)
                {
                    basketItems.Add(new BasketItem
                    {
                        Id = item.Id,
                        Name = item.Name,
                        Category1 = item.Category,
                        ItemType = BasketItemType.PHYSICAL.ToString(),
                        Price = item.Price.ToString("F2", CultureInfo.InvariantCulture)
                    });
                }
                formRequest.BasketItems = basketItems;

                var result = CheckoutFormInitialize.Create(formRequest, options);

                if (result.Status == "success")
                {
                    _logger.LogInformation("İyzico checkout başlatıldı. OrderId={OrderId}, Token={Token}", request.OrderId, result.Token);
                    return Task.FromResult(new PaymentInitResult
                    {
                        Success = true,
                        CheckoutFormContent = result.CheckoutFormContent,
                        Token = result.Token
                    });
                }

                _logger.LogWarning("İyzico checkout başarısız. OrderId={OrderId}, Hata={ErrorMessage}", request.OrderId, result.ErrorMessage);
                return Task.FromResult(new PaymentInitResult
                {
                    Success = false,
                    ErrorMessage = result.ErrorMessage,
                    ErrorCode = result.ErrorCode
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "İyzico checkout sırasında beklenmeyen hata. OrderId={OrderId}", request.OrderId);
                return Task.FromResult(new PaymentInitResult
                {
                    Success = false,
                    ErrorMessage = "Ödeme sistemiyle bağlantı kurulamadı. Lütfen daha sonra tekrar deneyin."
                });
            }
        }

        public Task<PaymentVerifyResult> VerifyPaymentAsync(string token)
        {
            try
            {
                var options = GetOptions();
                var request = new RetrieveCheckoutFormRequest { Token = token };
                var result = CheckoutForm.Retrieve(request, options);

                if (result.PaymentStatus == "SUCCESS")
                {
                    _logger.LogInformation(
                        "Ödeme doğrulandı. PaymentId={PaymentId}, Tutar={PaidPrice}, Taksit={Installment}",
                        result.PaymentId, result.PaidPrice, result.Installment);

                    return Task.FromResult(new PaymentVerifyResult
                    {
                        Success = true,
                        PaymentId = result.PaymentId,
                        ConversationId = result.ConversationId,
                        PaidPrice = decimal.TryParse(result.PaidPrice, CultureInfo.InvariantCulture, out var paid) ? paid : 0,
                        Installment = result.Installment,
                        CardAssociation = result.CardAssociation,
                        CardFamily = result.CardFamily,
                        BinNumber = result.BinNumber,
                        LastFourDigits = result.LastFourDigits
                    });
                }

                _logger.LogWarning(
                    "Ödeme doğrulama başarısız. Token={Token}, Status={Status}, Hata={ErrorMessage}",
                    token, result.PaymentStatus, result.ErrorMessage);

                return Task.FromResult(new PaymentVerifyResult
                {
                    Success = false,
                    ErrorMessage = result.ErrorMessage,
                    ErrorCode = result.ErrorCode
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ödeme doğrulama sırasında beklenmeyen hata. Token={Token}", token);
                return Task.FromResult(new PaymentVerifyResult
                {
                    Success = false,
                    ErrorMessage = "Ödeme doğrulama sırasında bir hata oluştu."
                });
            }
        }

        /// <summary>
        /// Telefon numarasını İyzico formatına çevirir (+905xxxxxxxxx)
        /// </summary>
        private static string NormalizePhone(string? phone)
        {
            if (string.IsNullOrWhiteSpace(phone)) return "+905000000000";

            var digits = new string(phone.Where(char.IsDigit).ToArray());

            if (digits.StartsWith("90") && digits.Length == 12)
                return "+" + digits;

            if (digits.StartsWith("0") && digits.Length == 11)
                return "+9" + digits;

            if (digits.Length == 10)
                return "+90" + digits;

            return "+90" + digits;
        }
    }
}
