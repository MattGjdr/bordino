function updateQueryStringParameter(uri, key, value) {
	var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
	var separator = uri.indexOf('?') !== -1 ? "&" : "?";
	if (uri.match(re)) {
		return uri.replace(re, '$1' + key + "=" + value + '$2');
	}
	else {
		return uri + separator + key + "=" + value;
	}
}

function set_previous(val){
	url = window.location.href
	url = updateQueryStringParameter(url,"start",val)
	console.log(url)
	window.open(url,"_self")
}


$(document).ready(function() {
	function post_to_url(path, params, method) {
	    method = method || "post";

	    var form = document.createElement("form");
	    form.setAttribute("method", method);
	    form.setAttribute("action", path);

	    for(var key in params) {
	        if(params.hasOwnProperty(key) && params[key] !== "") {
	            var hiddenField = document.createElement("input");
	            hiddenField.setAttribute("type", "hidden");
	            hiddenField.setAttribute("name", key);
	            hiddenField.setAttribute("value", params[key]);

	            form.appendChild(hiddenField);
	         }
	    }

	    document.body.appendChild(form);
	    form.submit();
	}

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

	$(document).on('keypress',function(e) {
	    if(e.which == 13) {
	        search();
	    }
	});

	$( "#search" ).click(function() {
		search();
	});

	$( "#update" ).click(function() {
		console.log("update");
		// post_to_url('/update/'+$('#id').val(), {
		// 	title: $('#title').val(),
		//     date: $('#date').val(),
		//     location: $('#location').val(),
		//     content: $('#content').val(),
		//     comment: $('#comment').val(),
		//     edition: $('#edition').val(),
		//     translation: $('#translation').val(),
		//     studies: $('#studies').val(),
		//     author: $('#author').val(),
		//     latin: $('#latin').val(),
		//     chapter: $('#chapter').val(),
		//     keys: $('#keys').val(),
		//     material: $('#material').val()
		// }, 'get');

		post_to_url('/update/'+$('#id').val(), {
			xml: $('#xml').val(),
			imghash: $('#imghash').val(),
		}, 'get');
	});

	function search(){
		var options = [];
        $.each($("#multiselect option:selected"), function(){            
            options.push($(this).val());
        });
        console.log(options);
		//where to search
		console.log($('#collapseall').hasClass('in'));
		console.log($('#collapseimage').hasClass('in'));
		console.log($('#collapsetext').hasClass('in'));
		console.log($('#multiCollapseOptions').hasClass('in'));

		if ($('#multiCollapseOptions').hasClass('in') == false){
			//basic search
			console.log("basic search");

			post_to_url('/', {
				type: "basic",
			    q: $('#general-search').val(),
				keys: options
			}, 'get');
		}
		else{
			if ($('#collapseall').hasClass('in')){
				console.log("collapseall search");
				post_to_url('/', {
					type: "imgtxt",
				    title: $('#title_a').val(),
				    date: $('#date_a').val(),
				    location: $('#location_a').val(),
				    content: $('#content_a').val(),
				    comment: $('#comment_a').val(),
				    references: $('#references_a').val(),
				    keys: options
				}, 'get');
			}
			if ($('#collapseimage').hasClass('in')){
				console.log("collapseimage search");
				post_to_url('/', {
					type: "image",
				    title: $('#title_i').val(),
				    date: $('#date_i').val(),
				    location: $('#location_i').val(),
				    content: $('#content_i').val(),
				    comment: $('#comment_i').val(),
				    references: $('#references_i').val(),
				    material: $('#material_i').val(),
				    keys: options
				}, 'get');
			}
			if ($('#collapsetext').hasClass('in')){
				console.log("collapsetext search");
				post_to_url('/', {
					type: "text",
				    title: $('#title_t').val(),
				    date: $('#date_t').val(),
				    location: $('#location_t').val(),
				    content: $('#content_t').val(),
				    comment: $('#comment_t').val(),
				    references: $('#references_t').val(),
				    author: $('#author_t').val(),
				    latin: $('#latin_t').val(),
				    chapter: $('#chapter_t').val(),
				    keys: options
				}, 'get');
			}
		}
	}
});