import json
projetos = json.load(open('tramita2.json', 'r'))

def conta(tipo):
	projetos_count = 0.0
	dias = {}
	for i in projetos:
		if projetos[i].has_key("encerramento") and projetos[i]['encerramento'] == tipo and i.split('-')[0] == 'PL':
			projetos_count += 1
			for b in projetos[i]['tramite']:
				if dias.has_key(b['unidade']) and b.has_key('tempo'):
					dias[b['unidade']] += b['tempo']
				else:
					if b.has_key('tempo'):
						dias[b['unidade']] = b['tempo']
	return dias, projetos_count

relatorio = {}
relatorio['promulgado'] = {}
relatorio['termino'] = {}
dias_p, projetos_count_p = conta("PROMULGADO")
for z in dias_p:
	relatorio['promulgado'][z] = dias_p[z]/projetos_count_p

dias_t, projetos_count_t = conta("TERMINO DE LEGISLATURA (ART. 275 REG. INT.)")
for z in dias_t:
	relatorio['termino'][z] = dias_t[z]/projetos_count_t
