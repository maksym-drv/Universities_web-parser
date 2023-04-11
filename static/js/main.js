// nav
$('.navToggle').click(function () {
  $('body').toggleClass('navActive');
});

// check task status
function checkTaskStatus (url) {
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function(data) {
      if (data.status == 'SUCCESS') {
        // the task is complete, handle the result
        loadContent(data.result);
      } else if (data.status == 'PENDING' || data.status == 'STARTED') {
        // the task is still running, check again later
        setTimeout(function() {
          checkTaskStatus(url);
        }, 1000);
      } else {
        console.log('The task failed.');
      }
    },
    error: function() {
      // handle the error
      console.log('An error occurred while checking the task status.');
    }
  });
}

// load content
function loadContent(regions) {

  loadSubtitles(regions);
  var content = $("#content");

  regions.forEach(region => {
    var newRegion = loadRegion(region);
    content.append(newRegion);
  });

  $(".subtitles__option").click(function() {
    const section_id = $(this).attr("data-section");
    const sections = $(".regionsItem");

    if (section_id == "0") {
      sections.show();
    } else {
      sections.hide();
      $("#" + section_id).show();
    }
  });
  
  $(".templates__subtitles").css("border-bottom", "1px solid black");
  $("#loader").hide();
};

// loading of content data
function loadSubtitles(regions) {
  var subtitles = $("#subtitles");

  var first_text = $("<a>", { href: "#", text: "All Regions" });
  var last_text = $("<a>", { href: "#", text: "Short data" });

  var first_elem = $("<li>", {
    class: "subtitles__option",
    "data-section": "0",
  });

  var last_elem = $("<li>", {
    class: "subtitles__option",
    "data-section": "short",
  });

  first_elem.append(first_text);
  last_elem.append(last_text);

  subtitles.append(first_elem);
  regions.forEach(region => {

    var sub_text = $("<a>", { href: "#", text: `${region.name}    ` });
    var sub_elem = $("<li>", {
      class: "subtitles__option",
      "data-section": region.id,
    });
    sub_elem.append(sub_text);
    subtitles.append(' / ', sub_elem);
  });
  subtitles.append(' / ', last_elem);
};

function loadRegion(region) {

  var newRegion = $("<div>", {
    class: "regionsItem",
    id: region.id
  });
  var regionIcon = $("<i>", { class: "fa-solid fa-mountain-sun" });
  var regionName = $("<h3>").append(regionIcon, ` ${region.name}`);
  newRegion.append(regionName);

  region.unis.forEach(uni => {
    var newUni = loadUni(uni);
    newRegion.append(newUni);
  });

  return newRegion;
};

function loadUni(uni) {
  var newUniItem = $("<div>", { class: "templatesItem" });

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

  var rowName         = $("<th>", {text: "Name"});
  var rowSpeciality   = $("<th>", {text: "Speciality"});
  var rowForm         = $("<th>", {text: "Form"});
  var rowApplications = $("<th>", {text: "Applications"});
  var rowBudget       = $("<th>", {text: "Enrolled (Budget)"});
  var rowContract     = $("<th>", {text: "Enrolled (Contract)"});
  var rowPrice        = $("<th>", {text: "Price"});
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

  var rowName         = $("<td>", {text: offer.name});
  var rowSpeciality   = $("<td>", {text: offer.id});
  var rowForm         = $("<td>", {text: offer.form});
  var rowApplications = $("<td>", {text: offer.applications});
  var rowBudget       = $("<td>", {text: offer.ob});
  var rowContract     = $("<td>", {text: offer.oc});
  var rowPrice        = $("<td>", {text: offer.price});

  row.append(rowName, rowSpeciality, rowForm, 
  rowApplications, rowBudget, rowContract, rowPrice);
  
  return row;
};