#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar quais outros representantes estão atendendo cidades de Araçatuba.
Identifica todos os representantes que têm cidades da região de Araçatuba.
"""

import json
import os

def carregar_arquivos():
    """Carrega os arquivos necessários."""
    try:
        # Carregar representantes
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            representantes = json.load(f)
        
        # Carregar mesorregiões de SP
        with open('sp_mesorregioes.json', 'r', encoding='utf-8') as f:
            mesorregioes_sp = json.load(f)
        
        return representantes, mesorregioes_sp
    except Exception as e:
        print(f"❌ Erro ao carregar arquivos: {e}")
        return None, None

def obter_cidades_aracatuba(mesorregioes_sp):
    """Obtém todas as cidades da mesorregião de Araçatuba."""
    for mesorregiao in mesorregioes_sp:
        if mesorregiao["mesorregiao"] == "Araçatuba":
            return [cidade.upper() for cidade in mesorregiao["municipios"]]
    return []

def verificar_representantes_aracatuba(representantes, cidades_aracatuba):
    """Verifica quais representantes estão atendendo cidades de Araçatuba."""
    
    cidades_aracatuba_set = set(cidades_aracatuba)
    representantes_aracatuba = {}
    
    for nome, dados in representantes["representantes"].items():
        if "estados" in dados and "SP" in dados["estados"]:
            cidades_sp = dados["estados"]["SP"].get("cidades", [])
            cidades_aracatuba_rep = []
            
            for cidade in cidades_sp:
                if cidade.upper() in cidades_aracatuba_set:
                    cidades_aracatuba_rep.append(cidade.upper())
            
            if cidades_aracatuba_rep:
                representantes_aracatuba[nome] = {
                    "codigo": dados.get("codigo", "N/A"),
                    "nome": dados.get("nome", nome),
                    "cidades_aracatuba": cidades_aracatuba_rep,
                    "total_cidades_aracatuba": len(cidades_aracatuba_rep),
                    "total_cidades_sp": len(cidades_sp)
                }
    
    return representantes_aracatuba

def gerar_relatorio(representantes_aracatuba, cidades_aracatuba):
    """Gera um relatório detalhado da verificação."""
    print("=" * 80)
    print("🔍 VERIFICAÇÃO: REPRESENTANTES ATENDENDO ARAÇATUBA")
    print("=" * 80)
    
    print(f"\n📍 REGIÃO DE ARAÇATUBA:")
    print(f"   Total de cidades: {len(cidades_aracatuba)}")
    print(f"   Cidades: {', '.join(sorted(cidades_aracatuba))}")
    
    if not representantes_aracatuba:
        print(f"\n✅ Nenhum representante está atendendo cidades de Araçatuba!")
        return
    
    print(f"\n📋 REPRESENTANTES ATENDENDO ARAÇATUBA:")
    print(f"   Total encontrados: {len(representantes_aracatuba)}")
    
    for nome, dados in representantes_aracatuba.items():
        print(f"\n   🏢 {dados['nome']}")
        print(f"      Código: {dados['codigo']}")
        print(f"      Cidades de Araçatuba: {dados['total_cidades_aracatuba']}")
        print(f"      Total de cidades em SP: {dados['total_cidades_sp']}")
        print(f"      Cidades: {', '.join(dados['cidades_aracatuba'])}")
    
    # Identificar representante 26
    rep_26 = None
    for nome, dados in representantes_aracatuba.items():
        if dados['codigo'] == '26.0':
            rep_26 = dados
            break
    
    if rep_26:
        print(f"\n🎯 REPRESENTANTE 26 (PRINCIPAL):")
        print(f"   Nome: {rep_26['nome']}")
        print(f"   Cidades de Araçatuba: {rep_26['total_cidades_aracatuba']}")
        print(f"   Status: {'✅ COBERTURA COMPLETA' if rep_26['total_cidades_aracatuba'] == len(cidades_aracatuba) else '⚠️ COBERTURA INCOMPLETA'}")
    
    # Identificar outros representantes
    outros_representantes = {nome: dados for nome, dados in representantes_aracatuba.items() 
                           if dados['codigo'] != '26.0'}
    
    if outros_representantes:
        print(f"\n⚠️ OUTROS REPRESENTANTES (DEVEM SER REMOVIDOS):")
        for nome, dados in outros_representantes.items():
            print(f"   • {dados['nome']} ({dados['codigo']}) - {dados['total_cidades_aracatuba']} cidades")
    
    print(f"\n📊 RESUMO:")
    print(f"   Representante 26: {'✅' if rep_26 else '❌'}")
    print(f"   Outros representantes: {len(outros_representantes)}")
    print(f"   Total de representantes: {len(representantes_aracatuba)}")

def main():
    """Função principal."""
    print("🔍 Verificando quais representantes estão atendendo cidades de Araçatuba...")
    
    # Carregar arquivos
    representantes, mesorregioes_sp = carregar_arquivos()
    if not representantes or not mesorregioes_sp:
        return
    
    # Obter cidades de Araçatuba
    cidades_aracatuba = obter_cidades_aracatuba(mesorregioes_sp)
    if not cidades_aracatuba:
        print("❌ Mesorregião de Araçatuba não encontrada!")
        return
    
    # Verificar representantes
    representantes_aracatuba = verificar_representantes_aracatuba(representantes, cidades_aracatuba)
    
    # Gerar relatório
    gerar_relatorio(representantes_aracatuba, cidades_aracatuba)

if __name__ == "__main__":
    main()
