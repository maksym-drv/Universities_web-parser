// load content

function loadInfo(result) {
    
    const regions = result.regions,
        files = result.files;

    loadFiles(files);
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
            $(".programsTable").hide()
        } else if (value == "short") {
            $(".uniTable").hide()
            $(".shortTable").show()
            $(".programsTable").hide()
        } else if (value == "programs") {
            $(".uniTable").hide()
            $(".shortTable").hide()
            $(".programsTable").show()
        };
    });

    $(".template__title").show();
    $(".templates__subtitles").css("border-bottom", "1px solid black");
    $(".templates__subtitles").show();
    $(".shortTable").hide();
    $(".programsTable").hide()
    $("#loader").hide();
};

// loading of content data
function loadOptions(regions) {
    var subtitles = $("#subtitles");

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

function loadFiles(files) {

    files.forEach(file => {
        var newFile = $('<li>').append(
            $('<a>', {
                href: file.url,
                class: "button",
                text: file.text
            })
        );
        $('#nav li:nth-child(3)').after(newFile);
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

    region.static.forEach(uni => {
        var newUni = loadUni(uni);
        newRegion.append(newUni);
    });

    region.short.forEach(spec => {
        var newShortTable = getShortTable(spec);
        newRegion.append(newShortTable);
    });

    region.static.forEach(uni => {
        var newPrograms = getPrograms(uni);
        newRegion.append(newPrograms);
    });

    return newRegion;
};
