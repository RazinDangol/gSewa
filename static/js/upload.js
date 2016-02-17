
var status_url;
$('#upload').dmUploader({
	url: '/process',
    dataType: 'json',
    onComplete: function(){
    	console.log("Upload complete");
     },
	 
    onUploadSuccess: function(id,data){
    	status_url = data.location;
       	console.log(status_url);
        $('div#upload').html("<div id='processing'><h2>Processing... Please wait</h2><img src='../static/loader.gif' style='width:70px;height:70px;'></div>");
		//Polling the server if the processing task is completed or not	
     	Poll();
    	function Poll(){
    		$.getJSON(status_url, function(data) {
         	// process results here
        		if(data.state ==="SUCCESS"){
          			console.log('Success');
                console.log('Queuing Background Missing job');
                $.get('/job/missing');
          			window.location.href = '/payment/all';
        		}
        		else{
        			setTimeout(Poll,3000);
      			}

    		});
		}
	}
});
     