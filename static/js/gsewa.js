var complete=[0,0];
var cancel=[0,0];
$(document).ready(function(){
    
        var $dataRows=$("#complete tr:not('.totalData')");
            $dataRows.each(function() {
                $(this).find('.rowData').each(function(i){        
                    complete[i]+=parseFloat( $(this).html());
                });
            });
            
	$('#complete td.totalData').each(function(i){
    $(this).html(complete[i]);
});
    var $dataRows=$("#cancel tr:not('.totalData')");
            $dataRows.each(function() {
                $(this).find('.rowData').each(function(i){        
                    cancel[i]+=parseInt( $(this).html());
                });
            });
            
    $('#cancel td.totalData').each(function(i){
    $(this).html(cancel[i]);


});
	});