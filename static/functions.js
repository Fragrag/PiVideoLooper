$(function () {
  $('a#launch_video').bind('click', function () {
    $.getJSON('/launch_video',
      function (data) {
        //do nothing
      });
    return false;
  });
});

$(function () {
  $('a#kill_video').bind('click', function () {
    $.getJSON('/kill_video',
      function (data) {
        //do nothing
      });
    return false;
  });
});

$(function () {
  $('a#restart_video').bind('click', function () {
    $.getJSON('/restart_video',
      function (data) {
        //do nothing
      });
    return false;
  });
});

$(function () {
  $('a#reboot').bind('click', function () {
    $.getJSON('/reboot',
      function (data) {
        //do nothing
      });
    return false;
  });
});