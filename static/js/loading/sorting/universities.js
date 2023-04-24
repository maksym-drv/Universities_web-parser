
function loadUni(uni) {
    var newUniItem = $("<div>", { class: "templatesItem uniTable" });
    var newUniObj = $("<div>", { class: "templatesItem__desc templatesItem__desc--table" });

    var newUniName =
        `<div class="templatesItem__desc__name">
      <span class="templatesItem__icon">
        <i class="fa-solid fa-building-columns"></i>
      </span>
      <span>${uni.name}</span>
    </div>`
    newUniObj.html(newUniName);

    var newUniText = $("<div>", { class: "templatesItem__desc__text" });

    var table = $("<table>");

    var tableCol = $("<col>", {
        span: "1",
        style: "width: 35%;"
    });
    var firstRow = $("<tr>");

    var rowName = $("<th>", { text: "Name" });
    var rowSpeciality = $("<th>", { text: "Speciality" });
    var rowForm = $("<th>", { text: "Form" });
    var rowApplications = $("<th>", { text: "Applications" });
    var rowBudget = $("<th>", { text: "Enrolled (Budget)" });
    var rowContract = $("<th>", { text: "Enrolled (Contract)" });
    var rowPrice = $("<th>", { text: "Price" });
    firstRow.append(rowName, rowSpeciality, rowForm,
        rowApplications, rowBudget, rowContract, rowPrice);

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
    var rowForm = $("<td>", { text: offer.form });
    var rowApplications = $("<td>", { text: offer.applications });
    var rowBudget = $("<td>", { text: offer.ob });
    var rowContract = $("<td>", { text: offer.oc });
    var rowPrice = $("<td>", { text: offer.price });

    row.append(rowName, rowSpeciality, rowForm,
        rowApplications, rowBudget, rowContract, rowPrice);

    return row;
};