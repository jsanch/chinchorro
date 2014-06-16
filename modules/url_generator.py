import urllib.parse
from itertools import chain

YEARS = [2009,2010,2011,2012,2013,2014]
MAX_OFFICE_ID = 9999

def parse_har():
    with open('form.data') as har:
        data = dict(urllib.parse.parse_qsl(har.read()))
    return data

def get_document_id(data):
    return data['ctl00$contenidoArriba$txtNoDocumento1']

def get_oficina_id(data):
    return data['ctl00$contenidoArriba$ddlOficinas'].strip()

def get_year(data):
    return int(data['ctl00$contenidoArriba$txtAnioDocumento'])

def get_page(data):
    if '__EVENTARGUMENT' and '__EVENTTARGET' in data.keys():
        page = data['__EVENTARGUMENT']
        return int(page.split('$')[1])
    else:
        return 1

def increment_page(data):
    if get_page(data) != 1:
        data['__EVENTARGUMENT'] = '$'.join(['Page',str(get_page(data) + 1)])
    else:
        data['__EVENTARGUMENT'] = 'Page$2'
    data['__EVENTTARGET'] = 'ctl00$contenidoAbajo$gvTramitesBusqueda'
    data['__PREVIOUSPAGE'] = 'znfKQht05vqVnKpMOyjEijPVxrtHk6Z6ErFzt0IkgZI1'
    if 'ctl00$contenidoArriba$Buscar' in data.keys(): del data['ctl00$contenidoArriba$Buscar']
    return data

def set_event_validation(data,event_validation):
    data['__EVENTVALIDATION'] = event_validation
    return data

def set_view_state(data,view_state):
    data['__VIEWSTATE'] = view_state
    return data

def set_document_id(data,document_id):
    data['ctl00$contenidoArriba$txtNoDocumento1'] = document_id
    return data

def set_year(data,year):
    data['ctl00$contenidoArriba$txtAnioDocumento'] = int(year)
    return data

def set_oficina_id(data,oficina_id):
    data['ctl00$contenidoArriba$ddlOficinas'] = str(oficina_id).ljust(10)
    return data

def get_doc_type(data):
    return data['ctl00$contenidoArriba$ddlDocumento']

def set_doc_type(data,doc_type):
    data['ctl00$contenidoArriba$ddlDocumento'] = doc_type
    return data

def generate_data_for_office_and_year(data,oficina_id,year):
    data = set_oficina_id(data,oficina_id)
    data = set_year(data,year)
    for i in range(0,MAX_OFFICE_ID):
        data = set_document_id(data,i)
        yield data

def generate_data_for_office(data,oficina_id):
    generators = []
    for year in YEARS:
        generators.append(generate_data_for_office_and_year(data,oficina_id,year))
    return chain(*generators)
