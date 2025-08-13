#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se há algum problema específico que possa estar impedindo 
o representante 33 de aparecer no mapa
"""

import json

def verificar_problema_mapa():
    """
    Verifica se há algum problema específico que possa estar impedindo 
    o representante 33 de aparecer no mapa
    """
    try:
        # Carrega o JSON
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON carregado com sucesso")
        
        # Verifica se o representante 33 existe
        if "pelinson representacoes ltda" not in data["representantes"]:
            print("❌ Representante 33 não encontrado")
            return
        
        rep_33 = data["representantes"]["pelinson representacoes ltda"]
        print(f"✅ Representante 33 encontrado: {rep_33['nome']}")
        
        # Verifica se o estado MT existe
        if "MT" not in rep_33["estados"]:
            print("❌ Estado MT não encontrado no representante 33")
            return
        
        estado_mt = rep_33["estados"]["MT"]
        print(f"✅ Estado MT encontrado com {estado_mt['total_cidades']} cidades")
        
        # Verifica se há algum problema com as cidades
        cidades = estado_mt["cidades"]
        if not isinstance(cidades, list):
            print(f"❌ Cidades não é uma lista: {type(cidades)}")
            return
        
        if len(cidades) == 0:
            print("❌ Lista de cidades está vazia")
            return
        
        print(f"✅ Lista de cidades é válida com {len(cidades)} cidades")
        
        # Verifica se há cidades com caracteres especiais que possam causar problemas
        cidades_problema = []
        for cidade in cidades:
            if not isinstance(cidade, str):
                cidades_problema.append(f"{cidade} (tipo: {type(cidade)})")
            elif len(cidade.strip()) == 0:
                cidades_problema.append(f"'{cidade}' (vazia)")
            elif any(char in cidade for char in ['\n', '\r', '\t']):
                cidades_problema.append(f"'{cidade}' (contém caracteres especiais)")
        
        if cidades_problema:
            print(f"⚠️ Cidades com problemas encontradas:")
            for problema in cidades_problema[:10]:  # Mostra apenas as primeiras 10
                print(f"   - {problema}")
        else:
            print("✅ Todas as cidades estão válidas")
        
        # Verifica se há algum problema com o código
        codigo = rep_33.get("codigo")
        if codigo != "33":
            print(f"⚠️ Código do representante não é '33': {codigo}")
        else:
            print("✅ Código do representante está correto: 33")
        
        # Verifica se há algum problema com estados_atendidos
        estados_atendidos = rep_33.get("estados_atendidos", [])
        if not isinstance(estados_atendidos, list):
            print(f"❌ Estados atendidos não é uma lista: {type(estados_atendidos)}")
        elif "MT" not in estados_atendidos:
            print(f"❌ MT não está em estados_atendidos: {estados_atendidos}")
        else:
            print("✅ Estados atendidos está correto")
        
        # Verifica se há algum problema com a estrutura geral
        campos_obrigatorios = ["codigo", "nome", "contato", "estados", "total_cidades"]
        campos_faltando = []
        for campo in campos_obrigatorios:
            if campo not in rep_33:
                campos_faltando.append(campo)
        
        if campos_faltando:
            print(f"❌ Campos obrigatórios faltando: {campos_faltando}")
        else:
            print("✅ Todos os campos obrigatórios estão presentes")
        
        # Verifica se há algum problema com o contato
        contato = rep_33.get("contato", {})
        if not isinstance(contato, dict):
            print(f"❌ Contato não é um objeto: {type(contato)}")
        else:
            campos_contato = ["nome_contato", "email", "celular"]
            campos_contato_faltando = []
            for campo in campos_contato:
                if campo not in contato:
                    campos_contato_faltando.append(campo)
            
            if campos_contato_faltando:
                print(f"⚠️ Campos de contato faltando: {campos_contato_faltando}")
            else:
                print("✅ Campos de contato estão completos")
        
        # Verifica se há algum problema com a estrutura dos estados
        estados = rep_33.get("estados", {})
        if not isinstance(estados, dict):
            print(f"❌ Estados não é um objeto: {type(estados)}")
        else:
            if "MT" not in estados:
                print("❌ Estado MT não encontrado em estados")
            else:
                estado_mt_dados = estados["MT"]
                campos_estado = ["cidades", "total_cidades"]
                campos_estado_faltando = []
                for campo in campos_estado:
                    if campo not in estado_mt_dados:
                        campos_estado_faltando.append(campo)
                
                if campos_estado_faltando:
                    print(f"❌ Campos do estado MT faltando: {campos_estado_faltando}")
                else:
                    print("✅ Estrutura do estado MT está correta")
        
        # Verifica se há algum problema de encoding
        try:
            json.dumps(rep_33, ensure_ascii=False)
            print("✅ JSON pode ser serializado sem problemas")
        except Exception as e:
            print(f"❌ Problema ao serializar JSON: {e}")
        
        # Verifica se há algum problema específico com o nome da empresa
        nome_empresa = "pelinson representacoes ltda"
        if nome_empresa not in data["representantes"]:
            print(f"❌ Nome da empresa '{nome_empresa}' não encontrado")
        else:
            print(f"✅ Nome da empresa '{nome_empresa}' encontrado")
        
        # Lista todas as chaves para ver se há algum problema
        print(f"\n📋 Chaves dos representantes:")
        for i, chave in enumerate(data["representantes"].keys(), 1):
            if i <= 10 or i > len(data["representantes"]) - 10:
                print(f"   {i:2d}. {chave}")
            elif i == 11:
                print(f"   ... ({len(data['representantes']) - 20} representantes omitidos) ...")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_problema_mapa()
