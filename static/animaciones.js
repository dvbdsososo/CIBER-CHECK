(function () {
  var menosMovimiento = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1. Las secciones suben y aparecen cuando llegas a ellas */
  var items = document.querySelectorAll(".revela");

  if (menosMovimiento || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("visible"); });
  } else {
    var vigilante = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          vigilante.unobserve(e.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });

    items.forEach(function (el) { vigilante.observe(el); });
  }

  /* 2. El puntaje cuenta desde 0 hasta su valor */
  document.querySelectorAll("[data-contar]").forEach(function (el) {
    var meta = parseInt(el.getAttribute("data-contar"), 10);
    if (isNaN(meta) || menosMovimiento) { return; }

    var duracion = 1400;
    var retraso = 400;
    var inicio = null;
    el.textContent = "0";

    function paso(ahora) {
      if (inicio === null) { inicio = ahora; }
      var t = Math.min((ahora - inicio) / duracion, 1);
      var suave = 1 - Math.pow(1 - t, 4); /* frena suave al final */
      el.textContent = Math.round(meta * suave);
      if (t < 1) { requestAnimationFrame(paso); }
    }

    setTimeout(function () { requestAnimationFrame(paso); }, retraso);
  });

  /* 3. Botón "Analizar": avisa que está trabajando */
  var formulario = document.getElementById("formulario");
  var boton = document.getElementById("boton");
  var espera = document.getElementById("espera");

  if (formulario && boton) {
    formulario.addEventListener("submit", function () {
      boton.disabled = true;
      boton.textContent = "Analizando...";
      if (espera) { espera.hidden = false; }
    });

    /* Si regresan con la flecha del navegador, todo vuelve a funcionar */
    window.addEventListener("pageshow", function () {
      boton.disabled = false;
      boton.textContent = "Analizar";
      if (espera) { espera.hidden = true; }
    });
  }
})();
