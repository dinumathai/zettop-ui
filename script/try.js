$(document).ready(function() { 
  var eventSource;
  
  $("#create-btn").click(function() {
    $.ajax({
      url: '/saveconf',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      data: $("#config-json").val()
    }).fail(function(data) {
       alert("Failed to process input. Please validate the input json");
    }).done(function(data) {
       streamOutput(data.tmpFile);
    });
  });
  
  function streamOutput(fileName) {
	if(eventSource) {
		eventSource.close();
	}
	// For testing the steaming of output
    // eventSource = new EventSource("/stream/" + fileName + "/");
	eventSource = new EventSource("/executecmd/" + fileName + "/");
	$("#output").empty(); 
    eventSource.onmessage = function(event) {
      $("#output").append(event.data + "<br/>");
    }
  };

  $("#cancel-btn").click(function() { 
    eventSource.close();
  });

});