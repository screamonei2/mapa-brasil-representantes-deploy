#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar se todas as mesorregiões de MG estão sendo atendidas corretamente
"""

import json

def carregar_mesorregioes():
    """Carrega o arquivo de mesorregiões de MG"""
    with open('mesorregioes_mg.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_representantes():
    """Carrega o arquivo de representantes"""
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def obter_distribuicao_mesorregioes():
    """Retorna a distribuição das mesorregiões por representante"""
    return {
        "48.01": ["Zona da Mata"],
        "48.0": ["Vale do Rio Doce", "Central Mineira", "Oeste de Minas", "Jequitinhonha", "Norte de Minas"],
        "42.0": ["Triângulo Mineiro/Alto Paranaíba", "Noroeste de Minas"],
        "45.0": ["Sul/Sudoeste de Minas"]
    }

def encontrar_representante_por_codigo(representantes, codigo):
    """Encontra o representante pelo código"""
    for key, value in representantes['representantes'].items():
        if value.get('codigo') == codigo:
            return key
    return None

def validar_todas_mesorregioes():
    """Valida se todas as mesorregiões estão sendo atendidas"""
    
    print("=== VALIDAÇÃO COMPLETA DE TODAS AS MESORREGIÕES DE MG ===\n")
    
    print("Carregando arquivos...")
    mesorregioes = carregar_mesorregioes()
    representantes = carregar_representantes()
    
    # Obter distribuição das mesorregiões
    distribuicao = obter_distribuicao_mesorregioes()
    
    print("Distribuição das mesorregiões:")
    for codigo, mesorregioes_list in distribuicao.items():
        print(f"  {codigo}: {', '.join(mesorregioes_list)}")
    print()
    
    # Coletar todas as mesorregiões do arquivo
    todas_mesorregioes_arquivo = [m['mesorregiao'] for m in mesorregioes]
    print(f"Total de mesorregiões no arquivo: {len(todas_mesorregioes_arquivo)}")
    
    # Verificar cobertura
    mesorregioes_cobertas = set()
    mesorregioes_nao_cobertas = []
    
    for codigo, mesorregioes_list in distribuicao.items():
        representante_key = encontrar_representante_por_codigo(representantes, codigo)
        if representante_key:
            print(f"\n=== REPRESENTANTE {codigo} ({representante_key}) ===")
            
            cidades = representantes['representantes'][representante_key]['estados']['MG']['cidades']
            total_cidades = representantes['representantes'][representante_key]['estados']['MG']['total_cidades']
            total_geral = representantes['representantes'][representante_key]['total_cidades']
            
            print(f"Cidades: {len(cidades)}")
            print(f"Total estado: {total_cidades}")
            print(f"Total geral: {total_geral}")
            
            # Verificar consistência dos totais
            if len(cidades) == total_cidades == total_geral:
                print("✅ Totais consistentes")
            else:
                print("❌ Totais inconsistentes!")
            
            # Marcar mesorregiões como cobertas
            for mesorregiao in mesorregioes_list:
                mesorregioes_cobertas.add(mesorregiao)
                print(f"  ✅ {mesorregiao}")
        else:
            print(f"❌ Representante {codigo} não encontrado!")
    
    # Verificar mesorregiões não cobertas
    for mesorregiao in todas_mesorregioes_arquivo:
        if mesorregiao not in mesorregioes_cobertas:
            mesorregioes_nao_cobertas.append(mesorregiao)
    
    print(f"\n=== RESUMO DA VALIDAÇÃO ===")
    print(f"Mesorregiões cobertas: {len(mesorregioes_cobertas)}")
    print(f"Mesorregiões não cobertas: {len(mesorregioes_nao_cobertas)}")
    
    if mesorregioes_nao_cobertas:
        print(f"\n⚠️  Mesorregiões não cobertas:")
        for mesorregiao in mesorregioes_nao_cobertas:
            print(f"  - {mesorregiao}")
    else:
        print("\n✅ Todas as mesorregiões estão cobertas!")
    
    # Verificar se há cidades duplicadas entre representantes
    print(f"\n=== VERIFICAÇÃO DE DUPLICATAS ===")
    todas_cidades = []
    for codigo in distribuicao.keys():
        representante_key = encontrar_representante_por_codigo(representantes, codigo)
        if representante_key:
            cidades = representantes['representantes'][representante_key]['estados']['MG']['cidades']
            todas_cidades.extend(cidades)
    
    cidades_unicas = set(todas_cidades)
    if len(todas_cidades) == len(cidades_unicas):
        print("✅ Nenhuma cidade duplicada entre representantes")
    else:
        print(f"❌ {len(todas_cidades) - len(cidades_unicas)} cidades duplicadas encontradas!")
    
    print(f"\n=== VALIDAÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    validar_todas_mesorregioes()
