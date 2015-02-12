from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import json as simplejson
import json

@dajaxice_register
def notify_features(request, form):
	dajax = Dajax()
	print str(form)

	return dajax.json()