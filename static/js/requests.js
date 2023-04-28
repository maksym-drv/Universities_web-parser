// check task status

function checkTaskStatus(url, csrftoken,
  successAction, request_data = {}) {
  $.ajax({
    url: url,
    type: 'post',
    headers: { 'X-CSRFToken': csrftoken },
    data: request_data,
    dataType: 'json',
    success: function (data) {
      if (data.status == 'SUCCESS') {
        successAction(data.result);
      } else if (data.status == 'PENDING' || data.status == 'STARTED') {
        // the task is still running, check again later
        setTimeout(function () {
          checkTaskStatus(url, csrftoken, successAction, request_data);
        }, 1000);
      } else {
        console.log('The task failed.');
      }
    },
    error: function () {
      console.log('An error occurred while checking the task status.');
    }
  });
}