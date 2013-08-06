import json
from datetime import datetime
import pyes


def encerra():
	encerra_raw = open('../raw/encerra.txt', 'r')

	encerramentos = {}
	for a in encerra_raw.readlines()[2:]:
		try:
			b = a.split('#')
			if len(a.split('#')) == 5:
				pl = b[0] + '-' + b[1] + '-' + ''.join(b[2].split('/'))
			encerramentos[pl] = b[4].decode("iso-8859-1").strip()	
		except:
			print "error on " + pl
	return encerramentos

def projeta(encerramentos):
	arquivo = open('../raw/tramita.txt', 'r')
	projetos = {}
	for a in arquivo.readlines()[2:]:
		b = a.split('#')
		if len(a.split('#')) == 6:
			pl = b[0] + '-' + b[1] + '-' + ''.join(b[2].split('/'))
			tramite = {}
			try:
				tramite["data_ini"] = b[4]
				tramite["data_fim"] = b[5].strip()
				tramite["tempo"] = (datetime.strptime(b[5].strip(), "%d/%m/%Y") - datetime.strptime(b[4], "%d/%m/%Y")).days
			except:
				pass
			tramite["unidade"] = b[3]

			if projetos.has_key(pl):
				projetos[pl]['tramite'].append(tramite)
			else:
				projetos[pl] = { 'id' : pl }
				projetos[pl]['tramite'] = [tramite]
				if encerramentos.has_key(pl):
					projetos[pl]['encerramento'] = encerramentos[pl]
	return projetos

def write_json(arquivo, projetos):
	arquivo2 = open(arquivo, 'w')
	arquivo2.write(json.dumps(projetos, sort_keys=True, indent=4, separators=(',', ': ')))
	arquivo2.close()

def upa_neguim(projetos):
	print 'Connecting to ES...'
	conn = pyes.ES('http://127.0.0.1:9200')
	try:
		print 'Creating index...'
		conn.indices.create_index("monitor")
	except:
		pass

	mapping = {
		"data_fim" : { "type" : "string", "analyzer" : "keyword" },
		"data_ini" : { "type" : "date", "format" : "dd/MM/YYYY" }
    	}

	print 'Mapping...'
	conn.indices.put_mapping("projeto", {'properties': mapping}, ["monitor"])
    
	erros = 0
	print 'Indexing!'
	for v in projetos:
		p = projetos[v]
		conn.index(p, 'monitor', 'projeto', p['id'], bulk=True)
		try:
			conn.index(p, 'monitor', 'projeto', p['id'], bulk=True)
		except:
			print "erro"
			erros = erros + 1
	print erros

encerramentos = encerra()
projetos = projeta(encerramentos)
upa_neguim(projetos)
