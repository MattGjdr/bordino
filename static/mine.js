$(document).ready(function() {
	

	$('#multiselect').multiselect({
		buttonWidth : '100%',
		includeSelectAllOption : true,
		enableFiltering : true,
		numberDisplayed: 8,
		nonSelectedText: 'You might choose some research keys'
	});

	$('#multiCollapseOptions').on('shown.bs.collapse', function () {
   		console.log("Opened")
   		$('#general-search').prop('disabled', true);
	});

	$('#multiCollapseOptions').on('hidden.bs.collapse', function () {
	   console.log("Closed")
	   $('#general-search').prop('disabled', false);
	});


	$( "#search" ).click(function() {
		var options = [];
        $.each($("#multiselect option:selected"), function(){            
            options.push($(this).val());
        });
        console.log(options);
		console.log($('#general-search').val());

		//where to search
		console.log($('#collapseall').hasClass('in'));
		console.log($('#collapseimage').hasClass('in'));
		console.log($('#collapsetext').hasClass('in'));
		console.log($('#multiCollapseOptions').hasClass('in'));
		if ($('#multiCollapseOptions').hasClass('in') == false){
			//basic search
			console.log("basic search");
		}
		else{
			if ($('#collapseall').hasClass('in')){
				console.log("collapseall search");
			}
			if ($('#collapseimage').hasClass('in')){
				console.log("collapseimage search");
			}
			if ($('#collapsetext').hasClass('in')){
				console.log("collapsetext search");
			}
		}
	});

	$( "#search-options" ).click(function() {
		alert( "Handlllller for .click() called." );
	});

	$( "#search-options-images" ).click(function() {
		alert( "Handler for .click() called." );
	});

	$( "#search-options-texts" ).click(function() {
		alert( "Handler for .click() called." );
	});
});