$('#myDropdown').on('hide.bs.dropdown', function () {
    return false;
});

function setup_features(){
	var data = $('#set_features').serializeArray();
	Dajaxice.worldvis.notify_features(my_js_callback, {'form': data });
}

function setup_color(fills){
	$("#container").children().remove();


	map = new Datamap({
    element: document.getElementById('container'),
    scope: 'world',
    geographyConfig: {
        popupOnHover: false,
        highlightOnHover: false
    },
    fills: {
        'USA': '#1f77b4',
        'RUS': '#9467bd',
        'PRK': '#ff7f0e',
        'PRC': '#2ca02c',
        'IND': '#e377c2',
        'GBR': '#8c564b',
        'FRA': '#d62728',
        'PAK': '#7f7f7f',
        defaultFill: '#7A7A7A'
    },
    data: {
        'RUS': {fillKey: 'RUS'},
        'PRK': {fillKey: 'PRK'},
        'PRC': {fillKey: 'PRC'},
        'IND': {fillKey: 'IND'},
        'GBR': {fillKey: 'GBR'},
        'FRA': {fillKey: 'FRA'},
        'PAK': {fillKey: 'PAK'},
        'USA': {fillKey: 'USA'}
    }
});
}

function my_js_callback(data){
	var colors = ["#B03636","#363AB0", "#36B03E", "#AF8430", "#7F33B9"]
	fills_list = {};
	for (var i in data){
		var color = colors[i];
		var cluster_num = i;
		var countries = data[i]["countries"];
		var features = data[i]["features"];

		for (var i in countries){
			fills_list[countries[i]] = color;
		}
	}
	setup_color(fills_list);	
    //var clusters = data.clusters;
    //var cluster_json = JSON.parse(clusters);
    //alert(cluster_json.countries);
}





function color_cluster_map(cluster){
	alert("color");
}