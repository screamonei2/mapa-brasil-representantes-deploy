#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se há cidades duplicadas na lista do representante 48.01
"""

import json

def carregar_representantes():
    """Carrega o arquivo de representantes"""
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def verificar_duplicatas():
    """Verifica se há cidades duplicadas"""
    
    print("=== VERIFICAÇÃO DE DUPLICATAS ===\n")
    
    print("Carregando arquivo de representantes...")
    representantes = carregar_representantes()
    
    # Encontrar o representante 48.01
    representante_48_01 = None
    for key, value in representantes['representantes'].items():
        if value.get('codigo') == '48.01':
            representante_48_01 = key
            break
    
    if not representante_48_01:
        print("ERRO: Representante 48.01 não encontrado!")
        return
    
    # Obter cidades do representante
    cidades = representantes['representantes'][representante_48_01]['estados']['MG']['cidades']
    
    print(f"Representante: {representante_48_01}")
    print(f"Código: 48.01")
    print(f"Total de cidades: {len(cidades)}")
    
    # Verificar duplicatas
    cidades_normalizadas = []
    duplicatas = []
    
    for cidade in cidades:
        cidade_norm = cidade.upper().strip()
        if cidade_norm in cidades_normalizadas:
            duplicatas.append(cidade)
        else:
            cidades_normalizadas.append(cidade_norm)
    
    if duplicatas:
        print(f"\n✗ ERRO: {len(duplicatas)} cidades duplicadas encontradas:")
        for cidade in sorted(set(duplicatas)):
            print(f"  - {cidade}")
    else:
        print("\n✓ Nenhuma cidade duplicada encontrada")
    
    # Verificar se há cidades com nomes muito similares
    cidades_similares = []
    for i, cidade1 in enumerate(cidades):
        for j, cidade2 in enumerate(cidades):
            if i != j:
                # Normalizar para comparação
                norm1 = cidade1.upper().replace(' ', '').replace('-', '').replace("'", '')
                norm2 = cidade2.upper().replace(' ', '').replace('-', '').replace("'", '')
                
                if norm1 == norm2 and cidade1 != cidade2:
                    par = tuple(sorted([cidade1, cidade2]))
                    if par not in cidades_similares:
                        cidades_similares.append(par)
    
    if cidades_similares:
        print(f"\n⚠️  AVISO: {len(cidades_similares)} pares de cidades com nomes muito similares:")
        for cidade1, cidade2 in cidades_similares:
            print(f"  - '{cidade1}' e '{cidade2}'")
    else:
        print("\n✓ Nenhuma cidade com nome muito similar encontrada")
    
    print(f"\n=== VERIFICAÇÃO CONCLUÍDA ===")
    print(f"Total de cidades únicas: {len(set(cidades))}")
    print(f"Total de cidades na lista: {len(cidades)}")

if __name__ == "__main__":
    verificar_duplicatas()
