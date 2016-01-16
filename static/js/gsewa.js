var complete=[0,0];
var cancel=[0,0];
$(document).ready(function(){
    
        var $dataRows=$("#complete tr:not('.totalData')");
            $dataRows.each(function() {
                $(this).find('.rowData').each(function(i){        
                    complete[i]+=parseInt( $(this).html());
                });
            });
            
	$('#complete td.totalData').each(function(i){
    console.log(this);
    $(this).html(complete[i]);
});
    var $dataRows=$("#cancel tr:not('.totalData')");
            $dataRows.each(function() {
                $(this).find('.rowData').each(function(i){        
                    cancel[i]+=parseInt( $(this).html());
                });
            });
            
    $('#cancel td.totalData').each(function(i){
    console.log(this);
    $(this).html(cancel[i]);


});
	});