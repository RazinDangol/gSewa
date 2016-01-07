var totals=[0,0];
$(document).ready(function(){
    
        var $dataRows=$("#total tr:not('.totalData')");
            $dataRows.each(function() {
                $(this).find('.rowData').each(function(i){        
                    totals[i]+=parseInt( $(this).html());
                });
            });
            console.log(totals);
	$('#total td.totalData').each(function(i){
    console.log(this);
    $(this).html(totals[i]);
});
	});