//var my = new ES('http://127.0.0.1:9200', '');
var timeline = function(pl, data) {
	  $.each(data, function(index, tramite) {
	  	var tempo = tramite['tempo'];
	  	for (var i=0;i<tempo;i++) {
	  		$("#"+pl+ " .timeline").append("<div class='dia "+tramite['unidade']+"'' title='"+tramite['unidade']+" - "+ tempo +" dias'></div>");
	  	}
	  });
	}

var render = function(q) {
	var query = SETTINGS['SERVER'] + 'monitor/_search?source=' + JSON.stringify(q)
	$.getJSON(query, function (data) {
	    r.clear();
	    $.each(data.hits.hits, function (index, t) {
	    	console.log(t);
	        r.append(t['_source']);
	        timeline(t['_source']['id'], t['_source']['tramite']);
	    });
	    $("#tempo").fadeIn("slow");
	});
}

$(document).ready(function () {
	r = Tempo.prepare("tempo");
	var q = {
      "query" : {
                "match_all" : {}
            },
        "size":10
    }
	render(q);

	$("#buscar button").click(function (e) {
		e.preventDefault();
		var search = $("#buscar input").val();
		var q = {
			"query" : {
				"query_string" : { 
					"query" : search,
					"fields" : ["ementa", "encerramento", "_id"],
					"default_operator" : "AND"
				},
			"size":10
			}
		}
		render(q);
	})
});