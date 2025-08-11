#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar TODAS as mesorregiões de MG com seus respectivos representantes
"""

import json
import os
from datetime import datetime

def carregar_mesorregioes():
    """Carrega o arquivo de mesorregiões de MG"""
    with open('mesorregioes_mg.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_representantes():
    """Carrega o arquivo de representantes"""
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_representantes(data):
    """Salva o arquivo de representantes atualizado"""
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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

def atualizar_todas_mesorregioes():
    """Atualiza todas as mesorregiões de MG"""
    
    print("=== ATUALIZAÇÃO COMPLETA DE TODAS AS MESORREGIÕES DE MG ===\n")
    
    print("Carregando arquivos...")
    mesorregioes = carregar_mesorregioes()
    representantes = carregar_representantes()
    
    # Obter distribuição das mesorregiões
    distribuicao = obter_distribuicao_mesorregioes()
    
    print("Distribuição das mesorregiões:")
    for codigo, mesorregioes_list in distribuicao.items():
        print(f"  {codigo}: {', '.join(mesorregioes_list)}")
    print()
    
    # Processar cada representante
    for codigo, mesorregioes_nomes in distribuicao.items():
        print(f"=== PROCESSANDO REPRESENTANTE {codigo} ===")
        
        # Encontrar o representante
        representante_key = encontrar_representante_por_codigo(representantes, codigo)
        if not representante_key:
            print(f"❌ Representante {codigo} não encontrado!")
            continue
        
        print(f"Representante encontrado: {representante_key}")
        
        # Obter cidades atuais
        cidades_atuais = representantes['representantes'][representante_key]['estados']['MG']['cidades']
        print(f"Cidades atuais: {len(cidades_atuais)}")
        
        # Coletar todas as cidades das mesorregiões atribuídas
        todas_cidades = []
        for nome_mesorregiao in mesorregioes_nomes:
            for mesorregiao in mesorregioes:
                if mesorregiao['mesorregiao'] == nome_mesorregiao:
                    todas_cidades.extend(mesorregiao['municipios'])
                    print(f"  {nome_mesorregiao}: {len(mesorregiao['municipios'])} cidades")
                    break
        
        # Remover duplicatas e ordenar
        todas_cidades = sorted(list(set(todas_cidades)))
        print(f"Total de cidades únicas: {len(todas_cidades)}")
        
        # Atualizar o representante
        representantes['representantes'][representante_key]['estados']['MG']['cidades'] = todas_cidades
        representantes['representantes'][representante_key]['estados']['MG']['total_cidades'] = len(todas_cidades)
        representantes['representantes'][representante_key]['total_cidades'] = len(todas_cidades)
        
        print(f"✅ Representante {codigo} atualizado com {len(todas_cidades)} cidades\n")
    
    # Salvar arquivo atualizado
    print("Salvando arquivo atualizado...")
    salvar_representantes(representantes)
    
    print("=== ATUALIZAÇÃO CONCLUÍDA ===")
    print("Todos os representantes foram atualizados com suas respectivas mesorregiões!")

if __name__ == "__main__":
    atualizar_todas_mesorregioes()
