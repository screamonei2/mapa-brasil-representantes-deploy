#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar especificamente o representante 33 e identificar onde está o problema
"""

import json

def debug_representante_33():
    """
    Debug específico do representante 33
    """
    try:
        # Carrega o JSON
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON carregado com sucesso")
        
        # Verifica especificamente o representante 33
        rep_33 = data["representantes"]["pelinson representacoes ltda"]
        
        print(f"\n🎯 REPRESENTANTE 33 - ANÁLISE DETALHADA:")
        print(f"   - Nome: {rep_33['nome']}")
        print(f"   - Código: {rep_33['codigo']}")
        print(f"   - Total de cidades (campo): {rep_33['total_cidades']}")
        
        # Verifica o estado MT
        estado_mt = rep_33["estados"]["MT"]
        print(f"\n📍 ESTADO MT:")
        print(f"   - Total de cidades (campo): {estado_mt['total_cidades']}")
        print(f"   - Cidades reais: {len(estado_mt['cidades'])}")
        
        # Verifica se há discrepância
        if rep_33['total_cidades'] != estado_mt['total_cidades']:
            print(f"⚠️ DISCREPÂNCIA: total_cidades do representante ({rep_33['total_cidades']}) != total_cidades do estado ({estado_mt['total_cidades']})")
        
        if estado_mt['total_cidades'] != len(estado_mt['cidades']):
            print(f"⚠️ DISCREPÂNCIA: total_cidades do estado ({estado_mt['total_cidades']}) != cidades reais ({len(estado_mt['cidades'])})")
        
        # Lista todas as cidades para verificar se há alguma vazia ou com problema
        print(f"\n🏙️ VERIFICAÇÃO DAS CIDADES:")
        cidades_vazias = []
        cidades_duplicadas = []
        cidades_unicas = set()
        
        for i, cidade in enumerate(estado_mt['cidades']):
            if not cidade or cidade.strip() == "":
                cidades_vazias.append(f"Posição {i}: '{cidade}'")
            elif cidade in cidades_unicas:
                cidades_duplicadas.append(cidade)
            else:
                cidades_unicas.add(cidade)
        
        if cidades_vazias:
            print(f"❌ Cidades vazias encontradas: {len(cidades_vazias)}")
            for cidade_vazia in cidades_vazias[:5]:
                print(f"   - {cidade_vazia}")
        else:
            print("✅ Nenhuma cidade vazia encontrada")
        
        if cidades_duplicadas:
            print(f"❌ Cidades duplicadas encontradas: {len(cidades_duplicadas)}")
            for cidade_dup in cidades_duplicadas[:5]:
                print(f"   - {cidade_dup}")
        else:
            print("✅ Nenhuma cidade duplicada encontrada")
        
        print(f"✅ Total de cidades únicas: {len(cidades_unicas)}")
        
        # Verifica se há algum problema com caracteres especiais
        print(f"\n🔍 VERIFICAÇÃO DE CARACTERES:")
        cidades_com_problemas = []
        for cidade in estado_mt['cidades']:
            if any(char in cidade for char in ['\n', '\r', '\t', '\0']):
                cidades_com_problemas.append(cidade)
        
        if cidades_com_problemas:
            print(f"⚠️ Cidades com caracteres especiais: {len(cidades_com_problemas)}")
            for cidade_problema in cidades_com_problemas[:5]:
                print(f"   - '{cidade_problema}' (repr: {repr(cidade_problema)})")
        else:
            print("✅ Nenhuma cidade com caracteres especiais")
        
        # Verifica se há algum problema com o nome da empresa
        print(f"\n🏢 VERIFICAÇÃO DO NOME DA EMPRESA:")
        nome_empresa = "pelinson representacoes ltda"
        print(f"   - Nome procurado: '{nome_empresa}'")
        print(f"   - Nome encontrado: '{list(data['representantes'].keys())[-1]}'")
        
        if nome_empresa in data["representantes"]:
            print("✅ Nome da empresa encontrado corretamente")
        else:
            print("❌ Nome da empresa NÃO encontrado")
            print(f"   - Chaves disponíveis (últimas 5): {list(data['representantes'].keys())[-5:]}")
        
        # Verifica se há algum problema com a estrutura geral
        print(f"\n🏗️ VERIFICAÇÃO DA ESTRUTURA:")
        campos_obrigatorios = ["codigo", "nome", "contato", "estados", "total_cidades", "estados_atendidos"]
        for campo in campos_obrigatorios:
            if campo in rep_33:
                valor = rep_33[campo]
                tipo = type(valor).__name__
                if isinstance(valor, (list, dict)):
                    tamanho = len(valor)
                    print(f"   ✅ {campo}: {tipo} com {tamanho} itens")
                else:
                    print(f"   ✅ {campo}: {tipo} = {valor}")
            else:
                print(f"   ❌ {campo}: NÃO ENCONTRADO")
        
        # Verifica se há algum problema específico com o JavaScript
        print(f"\n🌐 VERIFICAÇÃO PARA JAVASCRIPT:")
        
        # Simula o que o JavaScript faria
        nome_empresa_js = nome_empresa
        if nome_empresa_js in data["representantes"]:
            print(f"✅ JavaScript conseguiria encontrar '{nome_empresa_js}'")
            
            # Verifica se o JavaScript conseguiria acessar os dados
            rep_js = data["representantes"][nome_empresa_js]
            estados_js = rep_js.get("estados", {})
            
            if "MT" in estados_js:
                print("✅ JavaScript conseguiria acessar o estado MT")
                cidades_js = estados_js["MT"].get("cidades", [])
                print(f"✅ JavaScript encontraria {len(cidades_js)} cidades")
            else:
                print("❌ JavaScript NÃO conseguiria acessar o estado MT")
        else:
            print(f"❌ JavaScript NÃO conseguiria encontrar '{nome_empresa_js}'")
        
        # Verifica se há algum problema de encoding ou formatação
        print(f"\n📝 VERIFICAÇÃO DE ENCODING:")
        try:
            # Tenta serializar e deserializar
            json_str = json.dumps(rep_33, ensure_ascii=False)
            rep_33_deserializado = json.loads(json_str)
            
            if rep_33 == rep_33_deserializado:
                print("✅ JSON pode ser serializado e deserializado sem perda de dados")
            else:
                print("❌ JSON perde dados ao ser serializado/deserializado")
                
        except Exception as e:
            print(f"❌ Erro ao serializar/deserializar: {e}")
        
        # Verifica se há algum problema específico com o campo total_cidades
        print(f"\n🔢 VERIFICAÇÃO DO CAMPO TOTAL_CIDADES:")
        total_rep = rep_33.get("total_cidades", 0)
        total_estado = estado_mt.get("total_cidades", 0)
        total_real = len(estado_mt.get("cidades", []))
        
        print(f"   - total_cidades do representante: {total_rep}")
        print(f"   - total_cidades do estado: {total_estado}")
        print(f"   - cidades reais: {total_real}")
        
        if total_rep == total_estado == total_real:
            print("✅ Todos os campos de contagem estão consistentes")
        else:
            print("⚠️ Inconsistência nos campos de contagem detectada")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_representante_33()
