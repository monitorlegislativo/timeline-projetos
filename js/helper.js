var memory;

function ES (server, index) {
	this.debug = false
	this.base_url = server + index;
	this.query = function(q) {
		if (this.debug) {
			console.log(JSON.stringify(q));
		}
		return JSON.stringify(q);
	}

	this.load = function(q) { 
	 $.ajax({  
    	url: this.base_url + '/_search?source=' + JSON.stringify(q),  
    	dataType: 'json',
    	async: false,  
    	success: function(data) {
			memory = $.map(data.hits.hits, function (n, i) { 
				var empresa = n._source
				return empresa
			});
		}
	});
	}
}