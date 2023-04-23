// check task status

function checkTaskStatus (url, successAction) {
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function(data) {
      if (data.status == 'SUCCESS') {
        successAction(data.result);
      } else if (data.status == 'PENDING' || data.status == 'STARTED') {
        // the task is still running, check again later
        setTimeout(function() {
          checkTaskStatus(url, successAction);
        }, 1000);
      } else {
        console.log('The task failed.');
      }
    },
    error: function() {
      console.log('An error occurred while checking the task status.');
    }
  });
}