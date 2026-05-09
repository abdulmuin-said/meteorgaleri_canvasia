using Microsoft.AspNetCore.Mvc;

namespace KanvasProje.Web.Areas.Admin.Controllers
{
    [Area("Admin")]
    public class YardimController : AdminBaseController
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
