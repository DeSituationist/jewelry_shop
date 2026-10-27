(function () {
    "use strict";

    document.querySelectorAll("[data-stone-tabs]").forEach(function (root) {
        var list = root.querySelector("[data-tabs-list]");
        var prev = root.querySelector("[data-tabs-prev]");
        var next = root.querySelector("[data-tabs-next]");
        if (!list || !prev || !next) return;

        function update() {
            var max = list.scrollWidth - list.clientWidth;
            prev.disabled = list.scrollLeft <= 1;
            next.disabled = list.scrollLeft >= max - 1;
        }

        function step(dir) {
            list.scrollBy({ left: dir * list.clientWidth * 0.8, behavior: "smooth" });
        }

        prev.addEventListener("click", function () { step(-1); });
        next.addEventListener("click", function () { step(1); });
        list.addEventListener("scroll", update, { passive: true });
        window.addEventListener("resize", update);

        var active = list.querySelector(".active");
        if (active) {
            list.scrollLeft = active.offsetLeft - (list.clientWidth - active.offsetWidth) / 2;
        }
        update();
    });
})();
