// Diálogo "gerenciar cookies" — compartilhado por todas as páginas.
// Este site não usa cookies de rastreamento/analytics; o diálogo existe para
// ser transparente sobre isso e por convenção de rodapé.
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var openers = document.querySelectorAll('[data-open-cookies]');
    var dialog = document.getElementById('cookieDialog');
    if (!dialog) return;
    openers.forEach(function (btn) {
      btn.addEventListener('click', function () { dialog.showModal(); });
    });
    var closeBtn = dialog.querySelector('[data-close-cookies]');
    if (closeBtn) closeBtn.addEventListener('click', function () { dialog.close(); });
  });
})();
