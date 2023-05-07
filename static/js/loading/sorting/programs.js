
function getPrograms(uni) {

    var programsTable = $("<div>", { class: "templatesItem programsTable" }),
        programsTableObj = $("<div>", { class: "templatesItem__desc templatesItem__desc--table" }),
        newTableText = $("<div>", { class: "templatesItem__desc__text" });

    var newUniName =
        `<div class="templatesItem__desc__name">
      <span class="templatesItem__icon">
        <i class="fa-solid fa-building-columns"></i>
      </span>
      <span>${uni.name}</span>
    </div>`
    programsTableObj.html(newUniName);

    var table = $("<table>");
    var tableCol = $("<col>", {
        span: "1",
        style: "width: 35%;"
    });

    var firstRow = $("<tr>");
    var rowName = $("<th>", { text: "Освітня програма" });
    firstRow.append(rowName);
    table.append(tableCol, firstRow);

    uni.programs.forEach(program => {
        var row = $("<tr>");
        var program = $("<td>", { text: program });
        row.append(program);
        table.append(row);
    });

    newTableText.append(table);
    programsTableObj.append(newTableText);
    programsTable.append(programsTableObj);

    return programsTable;
    
};