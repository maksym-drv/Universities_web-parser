
function loadSpec(spec) {

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
        <th>Мін. заочна </th>
        <th>Макс. денна </th>
    </tr>
    <tr>
        <td rowspan="2">${spec.name}</td>
        <td>Денна</td>
        <td>${spec.fulltime_apps}</td>
        <td>${spec.fulltime_budget}</td>
        <td>${spec.fulltime_contract}</td>
        <td rowspan="2">${spec.enrolled}</td>
        <td rowspan="2">${spec.min_price}</td>
        <td rowspan="2">${spec.max_price} </td>
    </tr>
    <tr>
        <td>Заочна</td>
        <td>${spec.parttime_apps}</td>
        <td>${spec.parttime_budget}</td>
        <td>${spec.parttime_contract}</td>
    </tr>
    <tr>
        <td></td>
        <td>Всього:</td>
        <td>${spec.apps}</td>
        <td>${spec.budget}</td>
        <td>${spec.contract}</td>
        <td></td>
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