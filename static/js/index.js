// DateRangePicker
var nowDate = new Date();
var today = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0);
$('.daterange').daterangepicker({
    "minDate": today,
});
// Auto complete
$(function () {
    $('.location').autoComplete({
        minLength: 1,
    });
    $('.location').on('autocomplete.select', function (evt, item) {
        console.log('select');
        // $('.basicAutoSelectSelected').html(JSON.stringify(item));
    });

    $('*[data-href]').on('click', function() {
        window.location = $(this).data("href");
    });
})

$('form').on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) {
    e.preventDefault();
    return false;
  }
});
// Auto close Alert
setTimeout(function() {
    $(".alert").alert('close');
}, 4000);