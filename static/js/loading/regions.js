// load content

function loadRegions(regions) {

    var content = $("#regions");

    regions.forEach(region => {

        var newRegioLabel = $("<label>",
            {
                for: "option",
                text: region.name
            }
        );

        var newRegionCheck = $("<input>",
            {
                id: region.id,
                class: "form__option",
                type: "checkbox"
            }
        );

        var newRegion = $("<summary>").append(
            newRegioLabel, "  ", newRegionCheck);
        var newUnis = loadUnis(
            region.unis,
            region.id
        );

        newRegion = $("<details>", {
            class: "form__regions"
        }).append(
            newRegion,
            newUnis
        );

        content.append(newRegion);
    });

    setCheckboxes();
    setBehavior();
    $(".form__box").show();
    $("#loader").hide();
};

function loadUnis(unis, region_id) {

    newUnis = $("<ol>");

    unis.forEach(uni => {

        var newUni = $("<input>",
            {
                class: "form__suboption",
                type: "checkbox",
                name: "university",
                value: uni.university_id,
                "data-option": region_id,
            }
        );

        if (uni.checkbox) {
            newUni.prop("checked", true);
        };

        newUni = $("<label>").append(newUni, ` ${uni.university_name}`);
        newUni = $("<li>").append(newUni);
        newUnis.append(newUni);
    });

    return newUnis;
};