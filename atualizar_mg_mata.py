#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar o representante 48.01 (RINCO REPRESENTAÇÕES)
para atender apenas as cidades da Zona da Mata de Minas Gerais
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

def obter_cidades_zona_mata(mesorregioes):
    """Extrai as cidades da Zona da Mata"""
    for mesorregiao in mesorregioes:
        if mesorregiao['mesorregiao'] == 'Zona da Mata':
            return mesorregiao['municipios']
    return []

def normalizar_nome_cidade(nome):
    """Normaliza o nome da cidade para comparação"""
    return nome.upper().strip()

def atualizar_representante_48_01():
    """Atualiza o representante 48.01 com apenas cidades da Zona da Mata"""
    
    print("Carregando arquivos...")
    mesorregioes = carregar_mesorregioes()
    representantes = carregar_representantes()
    
    # Obter cidades da Zona da Mata
    cidades_zona_mata = obter_cidades_zona_mata(mesorregioes)
    print(f"Total de cidades na Zona da Mata: {len(cidades_zona_mata)}")
    
    # Normalizar nomes das cidades da Zona da Mata
    cidades_zona_mata_normalizadas = [normalizar_nome_cidade(cidade) for cidade in cidades_zona_mata]
    
    # Encontrar o representante 48.01
    representante_48_01 = None
    for key, value in representantes['representantes'].items():
        if value.get('codigo') == '48.01':
            representante_48_01 = key
            break
    
    if not representante_48_01:
        print("ERRO: Representante 48.01 não encontrado!")
        return
    
    print(f"Representante encontrado: {representante_48_01}")
    
    # Obter cidades atuais do representante
    cidades_atuais = representantes['representantes'][representante_48_01]['estados']['MG']['cidades']
    print(f"Total de cidades atuais: {len(cidades_atuais)}")
    
    # Filtrar apenas cidades da Zona da Mata
    cidades_filtradas = []
    cidades_removidas = []
    
    for cidade_atual in cidades_atuais:
        cidade_normalizada = normalizar_nome_cidade(cidade_atual)
        if cidade_normalizada in cidades_zona_mata_normalizadas:
            cidades_filtradas.append(cidade_atual)
        else:
            cidades_removidas.append(cidade_atual)
    
    print(f"Cidades mantidas: {len(cidades_filtradas)}")
    print(f"Cidades removidas: {len(cidades_removidas)}")
    
    # Atualizar o representante
    representantes['representantes'][representante_48_01]['estados']['MG']['cidades'] = cidades_filtradas
    representantes['representantes'][representante_48_01]['estados']['MG']['total_cidades'] = len(cidades_filtradas)
    representantes['representantes'][representante_48_01]['total_cidades'] = len(cidades_filtradas)
    
    # Salvar arquivo atualizado
    print("Salvando arquivo atualizado...")
    salvar_representantes(representantes)
    
    print("\n=== RESUMO DAS ALTERAÇÕES ===")
    print(f"Representante: {representante_48_01}")
    print(f"Código: 48.01")
    print(f"Cidades mantidas: {len(cidades_filtradas)}")
    print(f"Cidades removidas: {len(cidades_removidas)}")
    
    if cidades_removidas:
        print("\nCidades removidas:")
        for cidade in sorted(cidades_removidas):
            print(f"  - {cidade}")
    
    print("\nAtualização concluída com sucesso!")

if __name__ == "__main__":
    atualizar_representante_48_01()
