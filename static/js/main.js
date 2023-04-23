// nav
$('.navToggle').click(function () {
  $('body').toggleClass('navActive');
});

function checkAll() {
  var checkall = $('#allRegions'),
    allSuboptions = $('.form__suboption').length,
    allChecked = $('.form__suboption:checked').length;

  checkall.prop({
    'checked': allChecked > 0,
    'indeterminate': allChecked > 0 && allChecked < allSuboptions
  });
};

function setCheckboxes() {
  $('.form__option').each(function () {
    var region_id = this.id;
    var checkedCount = $(`[data-option="${region_id}"]:checked`).length,
      checkboxes = $(`[data-option="${region_id}"]`).length;

    $(this).prop({
      'checked': checkedCount > 0,
      'indeterminate': checkedCount > 0 && checkedCount < checkboxes
    });
  });
  checkAll()
};

function setBehavior() {
  $('#allRegions').click(function () {
    var options = $('.form__option'),
      suboptions = $('.form__suboption');
    options.prop('checked', this.checked);
    suboptions.prop('checked', this.checked);
  });

  $('.form__suboption').click(function () {
    var region_id = $(this).data('option');
    var checkedCount = $(`[data-option="${region_id}"]:checked`).length,
      checkboxes = $(`[data-option="${region_id}"]`).length,
      checkregion = $(`#${region_id}`);

    checkregion.prop({
      'checked': checkedCount > 0,
      'indeterminate': checkedCount > 0 && checkedCount < checkboxes
    });

    checkAll();
  });

  $('.form__option').click(function (option) {
    var region_id = this.id;
    var checkboxes = $(`[data-option="${region_id}"]`);
    checkboxes.prop('checked', this.checked);

    checkAll();
  });
};
