/* Global behaviour: close the mobile menu on link click */
(function () {
    "use strict";

    var menu = document.getElementById("mainNav");
    if (!menu || typeof bootstrap === "undefined") return;

    menu.querySelectorAll("a.nav-link").forEach(function (link) {
        link.addEventListener("click", function () {
            var instance = bootstrap.Collapse.getInstance(menu);
            if (instance && menu.classList.contains("show")) instance.hide();
        });
    });
})();
