//var my = new ES('http://127.0.0.1:9200', '');
var q = {}

var cargos = function(d, comissao) {
	var lq = {
      "query" : {
      	"nested" : {
        	"path" : "comissoes",
        	"query" : {
		      	"bool" : {
			      	"must" : [{
			      		"range" : {
			        		"i" : {
			    				"lte" : d.format("DD/MM/YYYY")
			    			}
			        	}},
			        	{"range" : {
			        		"f" : {
			   		     			"gte" : d.format("DD/MM/YYYY")
			        			}
			    	    	}	
			    	    }]
			    	}
		    	}
		    }
	    },
        "size":100,
        "from":0,
    }
    var query = SETTINGS['SERVER'] + 'vereadores/_search?source=' + JSON.stringify(lq);
    
    $.getJSON(query, function (data) {
    	$.each(data.hits.hits, function (index, t) {
    			$.each(t['_source'].comissoes, function (index, com) {
    				if (com.n == SETTINGS['MAPPING'][comissao]) {
    					var start = moment(com.i, "DD/MM/YYYY");
    					var end = moment(com.f, "DD/MM/YYYY");
    					var range = moment().range(start, end);
    					if (range.contains(d)) {
    						console.log(t['_source'].nome_parlamentar);
	        				console.log(t['_source'].comissoes[0]);
	        			}
    				}
    			});
    	});
	});
}

var timeline = function(pl, data) {
	  $.each(data, function(index, tramite) {
	  	var tempo = tramite['tempo'];
	  	c = tramite['data_ini'].split('/')
	  	var current = new Date(Number(c[2]), Number(c[1]), Number(c[0]));
	  	for (var i=0;i<tempo;i++) {
	  		$("#"+pl+ " .timeline").append("<div data-time='"+current.valueOf()+"' data-comissao='"+tramite['unidade']+"' class='dia "+tramite['unidade']+"'' title='"+tramite['unidade']+" - "+ tempo +" dias'></div>");
	  	current = new Date(current.setDate(current.getDate()+1));
	  	}
	  });
	}

var paginacao = function(direcao, q) {
	if (direcao == 'mais') { 
		q['from'] = q['from'] + q['size'];
	}
	else if (direcao == 'menos') {
		if (q['from']-q['size'] >= 0) {
			q['from'] = q['from'] - q['size'];
		}
	}
	return q;
}

var render = function(q) {
	var query = SETTINGS['SERVER'] + 'monitor/_search?source=' + JSON.stringify(q)
	$.getJSON(query, function (data) {
	    r.clear();
	    $.each(data.hits.hits, function (index, t) {
	        r.append(t['_source']);
	        timeline(t['_source']['id'], t['_source']['tramite']);
	    });
        $(".timeline .dia").click(function (e) {
			var d = moment(Number(e.target.getAttribute('data-time')));
			var com = e.target.getAttribute('data-comissao');
        	cargos(d, com);
	  	});
	    $("#tempo").fadeIn("slow");
	});
}

$(document).ready(function () {
	r = Tempo.prepare("tempo");
	q = {
      "query" : {
                "match_all" : {}
            },
        "size":10,
        "from":0
    }
	render(q);

	$("#buscar button").click(function (e) {
		e.preventDefault();
		var search = $("#buscar input").val();
		q = {
			"query" : {
				"query_string" : { 
					"query" : search,
					"fields" : ["ementa", "encerramento", "_id"],
					"default_operator" : "AND"
				},
			"size":10,
			"from":0
			}
		}
		render(q);
	})
});