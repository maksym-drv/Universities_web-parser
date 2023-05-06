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
        alert('Something went wrong :(\nPlease try again later.');
        console.log('The task failed.');
      }
    },
    error: function () {
      alert('Something went wrong :(\nPlease check your settings.');
    }
  });
}