
function loadUni(uni) {
    var newUniItem = $("<div>", { class: "templatesItem uniTable" }),
        newUniObj = $("<div>", { class: "templatesItem__desc templatesItem__desc--table" }),
        newUniText = $("<div>", { class: "templatesItem__desc__text" });

    var newUniName =
        `<div class="templatesItem__desc__name">
      <span class="templatesItem__icon">
        <i class="fa-solid fa-building-columns"></i>
      </span>
      <span>${uni.name}</span>
    </div>`
    newUniObj.html(newUniName);

    var table = $("<table>");

    var tableCol = $("<col>", {
        span: "1",
        style: "width: 35%;"
    });
    var firstRow = $("<tr>");

    var rowName = $("<th>", { text: "Назва пропозиції" });
    var rowSpeciality = $("<th>", { text: "Спеціальність" });
    var rowProgram = $("<th>", { text: "Освітня програма" });
    var rowForm = $("<th>", { text: "Форма навчання" });
    var rowApps = $("<th>", { text: "Кількість заяв" });
    var rowBudget = $("<th>", { text: "Зараховано (бюджет)" });
    var rowContract = $("<th>", { text: "Зараховано (контракт)" });
    var rowPrice = $("<th>", { text: "Вартість навчання" });
    firstRow.append(rowName, rowSpeciality, rowProgram,
        rowForm, rowApps, rowBudget, rowContract, rowPrice);

    table.append(tableCol, firstRow)

    uni.offers.forEach(offer => {
        var newOffer = loadOffer(offer);
        table.append(newOffer);
    });

    newUniText.append(table);
    newUniObj.append(newUniText);
    newUniItem.append(newUniObj);

    return newUniItem;

};

function loadOffer(offer) {
    var row = $("<tr>");

    var rowName = $("<td>", { text: offer.name });
    var rowSpeciality = $("<td>", { text: offer.id });
    var rowProgram = $("<td>", { text: offer.program });
    var rowForm = $("<td>", { text: offer.form });
    var rowApps = $("<td>", { text: offer.apps });
    var rowBudget = $("<td>", { text: offer.ob });
    var rowContract = $("<td>", { text: offer.oc });
    var rowPrice = $("<td>", { text: offer.price });

    row.append(rowName, rowSpeciality, rowProgram, rowForm,
        rowApps, rowBudget, rowContract, rowPrice);

    return row;
};