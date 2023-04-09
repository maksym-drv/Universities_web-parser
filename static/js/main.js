// nav
$('.navToggle').click(function () {
  $('body').toggleClass('navActive');
});

// menu subtitle
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