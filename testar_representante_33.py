#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar se o representante 33 está sendo processado corretamente
"""

import json

def testar_representante_33():
    """
    Testa se o representante 33 está sendo processado corretamente
    """
    try:
        # Carrega o JSON
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON carregado com sucesso")
        
        # Verifica se o representante 33 existe
        if "pelinson representacoes ltda" in data["representantes"]:
            rep_33 = data["representantes"]["pelinson representacoes ltda"]
            print(f"✅ Representante 33 encontrado:")
            print(f"   - Nome: {rep_33['nome']}")
            print(f"   - Código: {rep_33['codigo']}")
            print(f"   - Estados atendidos: {rep_33['estados_atendidos']}")
            
            # Verifica se o estado MT existe
            if "MT" in rep_33["estados"]:
                estado_mt = rep_33["estados"]["MT"]
                print(f"✅ Estado MT encontrado:")
                print(f"   - Total de cidades: {estado_mt['total_cidades']}")
                print(f"   - Primeiras 5 cidades: {estado_mt['cidades'][:5]}")
                print(f"   - Últimas 5 cidades: {estado_mt['cidades'][-5:]}")
                
                # Verifica se todas as cidades estão em uppercase e sem acentos
                cidades_com_problemas = []
                for cidade in estado_mt["cidades"]:
                    if any(char in cidade for char in "áàâãäéèêëíìîïóòôõöúùûüçñ"):
                        cidades_com_problemas.append(cidade)
                
                if cidades_com_problemas:
                    print(f"⚠️ Cidades com acentuação encontradas: {cidades_com_problemas[:5]}")
                else:
                    print("✅ Todas as cidades estão sem acentuação")
                
                # Verifica se há cidades duplicadas
                cidades_unicas = set(estado_mt["cidades"])
                if len(cidades_unicas) != len(estado_mt["cidades"]):
                    print(f"⚠️ Há cidades duplicadas: {len(estado_mt['cidades']) - len(cidades_unicas)} duplicatas")
                else:
                    print("✅ Não há cidades duplicadas")
                
            else:
                print("❌ Estado MT não encontrado no representante 33")
                
        else:
            print("❌ Representante 33 não encontrado")
        
        # Verifica a estrutura geral
        print(f"\n📊 Estrutura geral:")
        print(f"   - Total de representantes: {len(data['representantes'])}")
        
        # Lista todos os representantes
        print(f"\n📋 Lista de representantes:")
        for i, (nome, dados) in enumerate(data["representantes"].items(), 1):
            codigo = dados.get("codigo", "N/A")
            estados = list(dados.get("estados", {}).keys())
            print(f"   {i:2d}. {nome[:50]:<50} | Código: {codigo:<5} | Estados: {estados}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    testar_representante_33()
