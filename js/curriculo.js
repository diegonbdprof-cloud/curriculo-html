/*
 * Botão Imprimir.
 * Não lê formulário, não grava armazenamento e não faz pedido de rede.
 */
(function () {
  "use strict";

  var botao = document.querySelector("[data-acao='imprimir']");
  if (!botao) {
    return;
  }

  botao.addEventListener("click", function () {
    window.print();
  });
}());
