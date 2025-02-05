document.addEventListener("DOMContentLoaded", function () {
  let tables = document.querySelectorAll("table[id^='table-']");
  tables.forEach((table) => {
    $(table).DataTable({
      pageLength: 5,
      lengthMenu: [
        [5, 10, 25],
        [5, 10, 25],
      ],
      language: {
        sProcessing: "Procesando...",
        sLengthMenu: "Mostrar _MENU_ registros",
        sZeroRecords: "No se encontraron resultados",
        sEmptyTable: "Ningún dato disponible en esta tabla",
        sInfo:
          "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
        sInfoFiltered: "(filtrado de un total de _MAX_ registros)",
        sSearch: "Buscar:",
        oPaginate: {
          sFirst: "Primero",
          sPrevious: "Anterior",
          sNext: "Siguiente",
          sLast: "Último",
        },
        oAria: {
          sSortAscending: ": Ordenar ascendente",
          sSortDescending: ": Ordenar descendente",
        },
      },
    });
  });
});
