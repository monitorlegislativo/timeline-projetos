import re
from pprint import pprint
import json
import pyes
import codecs, datetime


def timefix(t):
    #very dirty!
    try:
        r = datetime.datetime.strptime(t[1:].replace("/",""), "%d%m%Y")
        r = r.strftime("%d/%m/%Y")
    except:
        if t[0] == 'i' and t[4:6] == '00':
            t = t[0:4] + '01' + t[6:11]
        if t[0] == 'f' and t[4:6] == '00':
            t = t[0:4] + '12' + t[6:11]
        if t[0] == 'i' and t[1:3] == '00':
            t = t[0] + '01' + t[3:11]
        if t[0] == 'f' and t[1:3] == '00':
            if int(t[4:6]) in [1,3,5,7,9,11]:
                t = t[0] + '31' + t[3:11]
            if int(t[4:6]) == 2:
                t = t[0] + '28' + t[3:11]
            if int(t[4:6]) in [4,6,8,10,12]:
                t = t[0] + '30' + t[3:11]
        if t[4:6] == '02' and int(t[1:3]) > 28:
            t = t[0] + '28' + t[3:11] 
        if t[0] == 'f' and t[1:] == '':
            return None
        if t[0] == 'i' and t[1:] == '':
            return None
        r = t[1:]
    return r

def clean(dicionario):
    for i in dicionario:
        if isinstance(dicionario[i], str) and dicionario[i] == u'':
            dicionario[i] = None
        if isinstance(dicionario[i], list) and dicionario[i] == ['']:
            dicionario[i] = []
    return dicionario

def preprocessa(line):
    line = line.split("%")
    lista = []
    if line and line != ['']:
        for e in line[1:]:
            dic = {}
            for x in e.split("^"):
                if x and x != '' and x[0] != '\r':
                    dic[x[0]] = x[1:]
            lista.append(dic)
    return lista

def processa_nome(nome_tmp):
    nome = nome_tmp.split("%")
    return nome

def processa_lideranca(lideranca_tmp):
    #todo
    lideranca = lideranca_tmp
    return lideranca

def processa_mesa(mesa_tmp):
    #todo
    mesa = mesa_tmp
    return mesa

def processa_legislatura(legislatura_tmp):
    legislatura = preprocessa(legislatura_tmp)
    return legislatura

def processa_cargos(cargo_tmp):
    cargo = preprocessa(cargo_tmp)
    return cargo    

def processa_vereanca(vereanca_tmp):
    vereanca = preprocessa(vereanca_tmp)
    for index, vere in enumerate(vereanca):
        if vere.has_key('f') and vere['f']:
            vereanca[index]['f'] = timefix('f'+vere['f'])
        if vere.has_key('i') and vere['i']:
            vereanca[index]['i'] = timefix('i'+vere['i'])
    return vereanca

def processa_comissoes(comissoes_tmp):
    comissoes = preprocessa(comissoes_tmp)
    for index, com in enumerate(comissoes):
        if com.has_key('f') and com['f']:
            comissoes[index]['f'] = timefix('f'+com['f'])
        if com.has_key('i'):
            comissoes[index]['i'] = timefix('i'+com['i'])
    return comissoes

def parse_vereadores():
    vereadores = []
    with codecs.open('../raw/vereador.txt', encoding='iso-8859-1') as raw:
        for line in raw.readlines()[2:-1]:
            l = line.split('#')
            vereador = {}
            vereador['registro'] = l[0]
            vereador['nome'] = l[1]
            vereador['nome_parlamentar'] = processa_nome(l[2])
            vereador['lideranca'] = processa_lideranca(l[3])
            vereador['mesa'] = processa_mesa(l[4])
            vereador['legislatura'] = processa_legislatura(l[5])
            vereador['cargos'] = processa_cargos(l[6])
            vereador['vereanca'] = processa_vereanca(l[7])
            vereador['comissoes'] = processa_comissoes(l[8])
            vereadores.append(vereador)
    return vereadores

def upa_neguim(vereadores):
    print 'Connecting to ES...'
    conn.delete_index_if_exists('vereadores')

    settings = {
    }

    print 'Creating index...'
    conn.indices.create_index("vereadores")
    
    mapping = {
        "comissoes" : {
            "type" : "nested",
            "properties" : {
                "i" : { "type" : "date", "format" : "dd/MM/YYYY" },
                "f" : { "type" : "date", "format" : "dd/MM/YYYY" }
            }
        }
        }

    print 'Mapping...'
    conn.indices.put_mapping('vereador', {'properties': mapping}, ["vereadores"])
    
    erros = 0
    print 'Indexing!'
    for p in vereadores:
        conn.index(p, 'vereadores', 'vereador')
    conn.refresh()

conn = pyes.ES('http://127.0.0.1:9200')
vereadores = parse_vereadores()
upa_neguim(vereadores)