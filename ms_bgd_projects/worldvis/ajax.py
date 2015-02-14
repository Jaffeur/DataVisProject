from dajaxice.decorators import dajaxice_register
import models
import json 

list_countries_a = ["AFG","ALB","DZA","ASM","AND","AGO","AIA","ATA","ATG","ARG","ARM","ABW","AUS","AUT","AZE","BHS","BHR","ISL","BGD","BRB","BLR","BEL","BLZ","BEN","BMU","BTN","BOL","BIH","BWA","BVT","BRA","IOT","BRN","BGR","BFA","BDI","KHM","CMR","CAN","CPV","CYM","CAF","TCD","CHL","CHN","CXR","CCK","COL","COM","COD","COG","COK","CRI","CIV","HRV","CUB","CYP","CZE","DNK","DJI","DMA","DOM","ECU","EGY","SLV","GNQ","ERI","EST","ETH","FLK","FRO","FJI","FIN","FRA","GUF","PYF","ATF","GAB","GMB","GEO","DEU","GHA","GIB","GRC","GRL","GRD","GLP","GUM","GTM","GIN","GNB","GUY","HTI","HMD","HND","HKG","HUN","ISL","IND","IDN","IRN","IRQ","IRL","ISR","ITA","JAM","JPN","JEY","JON","JOR","KAZ","KEN","KIR","PRK","KOR","KWT","KGZ","LAO","LVA","LBN","LSO","LBR","LBY","LIE","LTU","LUX","MAC","MKD","MDG","MWI","MYS","MDV","MLI","MLT","MHL","MTQ","MRT","MUS","MYT","MEX","FSM","MDA","MCO","MNG","MSR","MAR","MOZ","NAM","NRU","NPL","NLD","ANT","NCL","NZL","NIC","NER","NGA","NIU","NFK","MNP","NOR","OMN","PAK","PLW","PAN","PNG","PRY","PER","PHL","POL","PRT","PRI","QAT","REU","ROU","RUS","RWA","SHN","KNA","LCA","SPM","VCT","WSM","SMR","STP","SAU","SEN","SCG","SYC","SLE","SGP","SVK","SVN","SLB","SOM","ZAF","SGS","ESP","LKA","SDN","SUR","SJM","SWZ","SWE","CHE","SYR","TWN","TJK","TZA","THA","TGO","TKL","TON","TTO","TUN","TUR","TKM","TCA","TUV","UGA","UKR","ARE","GRB","USA","URY","UZB","VUT","VEN","VNM","VGB","WLF","ESH","YEM","ZMB","ZWE"]


@dajaxice_register
def notify_features(request, form):
	countries, features = get_features_lists(form)
	clusters = models.clusterKMeans(countries,features,2)	
	print clusters									
	return json.dumps(clusters)

def get_features_lists(json):
	countries = list()
	features = list()
	for elem in json:
		if elem['name'] == "country" and elem['value'] in list_countries_a:
			countries.append(elem['value'])
		if elem['name'] == "feature":
			features.append(elem['value'])
	return countries, features
