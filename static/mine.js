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
	//https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
	function getParameterByName(name, url) {
	    if (!url) url = window.location.href;
	    name = name.replace(/[\[\]]/g, '\\$&');
	    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
	        results = regex.exec(url);
	    if (!results) return null;
	    if (!results[2]) return '';
	    return decodeURIComponent(results[2].replace(/\+/g, ' '));
	}

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

	if (getParameterByName("keys"))
	{
		$("#multiselect").val(getParameterByName("keys").split(','))
		$("#multiselect").trigger("change");
	}
	
	if (getParameterByName("t") == "basic")
	{
		$('#general-search').val(getParameterByName("q"));
	}
	else
	{
		// $("#multiCollapseOptions").collapse("show");
		// $('#collapseall').collapse('hide')
		// $('#collapseimage').collapse('hide')
		// $('#collapsetext').collapse('hide')

		if (getParameterByName("t") == "imgtxt")
		{
			// $('#collapseall').collapse('toggle')

			$('#title_a').val(getParameterByName("title"))
		    $('#date_a').val(getParameterByName("date"))
		    $('#location_a').val(getParameterByName("location"))
		    $('#content_a').val(getParameterByName("content"))
		    $('#comment_a').val(getParameterByName("comment"))
		    $('#references_a').val(getParameterByName("references"))
		    $('#type_a').val(getParameterByName("type"))
		}
		if (getParameterByName("t") == "image")
		{
			// $('#collapseimage').collapse('toggle')

			$('#title_i').val(getParameterByName("title"))
		    $('#date_i').val(getParameterByName("date"))
		    $('#location_i').val(getParameterByName("location"))
		    $('#content_i').val(getParameterByName("content"))
		    $('#comment_i').val(getParameterByName("comment"))
		    $('#references_i').val(getParameterByName("references"))
		    $('#type_i').val(getParameterByName("type"))
		}
		if (getParameterByName("t") == "text")
		{
			// $('#collapsetext').collapse('toggle')

			$('#title_t').val(getParameterByName("title"))
		    $('#date_t').val(getParameterByName("date"))
		    $('#location_t').val(getParameterByName("location"))
		    $('#content_t').val(getParameterByName("content"))
		    $('#comment_t').val(getParameterByName("comment"))
		    $('#references_t').val(getParameterByName("references"))
		    $('#author_t').val(getParameterByName("author"))
		    $('#latin_t').val(getParameterByName("latin"))
		    $('#chapter_t').val(getParameterByName("chapter"))
		    $('#type_t').val(getParameterByName("type"))
		}
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
		

		if ($('#imghash').val() === undefined)
		{
			post_to_url('/update/txt/'+$('#id').val(), {
				xml: $('#xml').val()
			}, 'get');
		}
		else
		{
			post_to_url('/update/img/'+$('#id').val(), {
				xml: $('#xml').val()
			}, 'get');
		}
		
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
				t: "basic",
			    q: $('#general-search').val(),
				keys: options
			}, 'get');
		}
		else{
			if ($('#collapseall').hasClass('in')){
				console.log("collapseall search");
				post_to_url('/', {
					t: "imgtxt",
				    title: $('#title_a').val(),
				    date: $('#date_a').val(),
				    location: $('#location_a').val(),
				    content: $('#content_a').val(),
				    comment: $('#comment_a').val(),
				    references: $('#references_a').val(),
				    type: $('#type_a').val(),
				    keys: options
				}, 'get');
			}
			if ($('#collapseimage').hasClass('in')){
				console.log("collapseimage search");
				post_to_url('/', {
					t: "image",
				    title: $('#title_i').val(),
				    date: $('#date_i').val(),
				    location: $('#location_i').val(),
				    content: $('#content_i').val(),
				    comment: $('#comment_i').val(),
				    references: $('#references_i').val(),
				    type: $('#type_i').val(),
				    keys: options
				}, 'get');
			}
			if ($('#collapsetext').hasClass('in')){
				console.log("collapsetext search");
				post_to_url('/', {
					t: "text",
				    title: $('#title_t').val(),
				    date: $('#date_t').val(),
				    location: $('#location_t').val(),
				    content: $('#content_t').val(),
				    comment: $('#comment_t').val(),
				    references: $('#references_t').val(),
				    author: $('#author_t').val(),
				    latin: $('#latin_t').val(),
				    chapter: $('#chapter_t').val(),
				    type: $('#type_t').val(),
				    keys: options
				}, 'get');
			}
		}
	}
});