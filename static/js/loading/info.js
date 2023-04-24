// load content

function loadInfo(regions) {

    loadOptions(regions);
    var content = $("#content");

    regions.forEach(region => {
        var newRegion = loadRegion(region);
        content.append(newRegion);
    });

    $(".subtitles__option").click(function () {
        const section_id = $(this).attr("data-section");
        const sections = $(".regionsItem");

        if (section_id == "0") {
            sections.show();
        } else {
            sections.hide();
            $("#" + section_id).show();
        }
    });

    $('.mode__option').click(function () {
        var value = $(this).data('value');  
        if (value == "unis") {
            $(".uniTable").show()
            $(".shortTable").hide()
        } else if (value == "short") {
            $(".uniTable").hide()
            $(".shortTable").show()
        };
    });

    $(".templates__subtitles").css("border-bottom", "1px solid black");
    $(".shortTable").hide();
    $("#loader").hide();
};

// loading of content data
function loadOptions(regions) {
    var subtitles = $("#subtitles"),
        modes = $("#modes");

    var first_text = $("<a>", { href: "#", text: "All Regions" }),
        unisTableText = $("<a>", { href: "#", text: "Статистичні дані" }),
        shortTableText = $("<a>", { href: "#", text: "Зведені дані" });

    var first_elem = $("<li>", {
        class: "subtitles__option",
        "data-section": "0"
    }),
        unisTableElem = $("<li>", {
            class: "mode__option",
            "data-value": "unis"
        }),
        shortTableElem = $("<li>", {
            class: "mode__option",
            "data-value": "short"
        });

    first_elem.append(first_text);
    unisTableElem.append(unisTableText);
    shortTableElem.append(shortTableText);

    subtitles.append(first_elem);
    modes.append(unisTableElem, ' | ', shortTableElem)

    regions.forEach(region => {

        var sub_text = $("<a>", { href: "#", text: `${region.name}    ` });
        var sub_elem = $("<li>", {
            class: "subtitles__option",
            "data-section": region.id,
        });
        sub_elem.append(sub_text);
        subtitles.append(' / ', sub_elem);
    });
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

    region.specs.forEach(spec => {
        var newSpec = loadSpec(spec);
        newRegion.append(newSpec);
    });

    return newRegion;
};
