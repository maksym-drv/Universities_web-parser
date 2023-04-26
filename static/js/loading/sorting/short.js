
function getShortTable(spec) {

    var shortTable = $("<div>", { class: "templatesItem shortTable" });
    var shortTableObj = $("<div>", { class: "templatesItem__desc templatesItem__desc--table" });
    var newTableText = $("<div>", { class: "templatesItem__desc__text" });

    var table = $("<table>");
    var tableCol = $("<col>", {
        span: "1",
        style: "width: 35%;"
    });

    var tableContent = 
    `<tr>
        <th rowspan="2">Спеціальність</th>
        <th rowspan="2">Форма навчання</th>
        <th rowspan="2">Кількість заяв</th>
        <th colspan="2">Зараховано</th>
        <th rowspan="2">Всього</th>
        <th colspan="2">Вартість навчання</th>
    </tr>
    <tr>
        <th>Бюджет</th>
        <th>Контракт</th>
        <th>Мінімальна</th>
        <th>Максимальна</th>
    </tr>
    <tr>
        <td rowspan="2">${spec.name}</td>
        <td>Денна</td>
        <td>${spec.fulltime_apps}</td>
        <td>${spec.fulltime_budget}</td>
        <td>${spec.fulltime_contract}</td>
        <td>${spec.fulltime}</td>
        <td>${spec.min_fulltime}</td>
        <td>${spec.max_fulltime} </td>
    </tr>
    <tr>
        <td>Заочна</td>
        <td>${spec.parttime_apps}</td>
        <td>${spec.parttime_budget}</td>
        <td>${spec.parttime_contract}</td>
        <td>${spec.parttime}</td>
        <td>${spec.min_parttime}</td>
        <td>${spec.max_parttime} </td>
    </tr>
    <tr>
        <td></td>
        <th>Всього:</th>
        <td>${spec.apps}</td>
        <td>${spec.budget}</td>
        <td>${spec.contract}</td>
        <th>${spec.enrolled}</th>
        <td></td>
        <td></td>
    </tr>`;

    table.append(tableCol);
    table.html(tableContent);

    newTableText.append(table);
    shortTableObj.append(newTableText);
    shortTable.append(shortTableObj);

    return shortTable;
    
};