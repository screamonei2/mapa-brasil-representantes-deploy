#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para LIMPAR TODAS as cidades de TODOS os representantes de MG
Deixa todos os representantes com 0 cidades
"""

import json

def carregar_representantes():
    """Carrega o arquivo de representantes"""
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_representantes(data):
    """Salva o arquivo de representantes atualizado"""
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def limpar_todos_representantes_mg():
    """Remove TODAS as cidades de TODOS os representantes de MG"""
    
    print("=== LIMPEZA COMPLETA DE TODOS OS REPRESENTANTES DE MG ===")
    print("Objetivo: Remover TODAS as cidades, deixar tudo vazio\n")
    
    print("Carregando arquivo de representantes...")
    representantes = carregar_representantes()
    
    # Encontrar todos os representantes que atendem MG
    representantes_mg = []
    
    for key, value in representantes['representantes'].items():
        if 'MG' in value.get('estados', {}):
            representantes_mg.append({
                'key': key,
                'codigo': value.get('codigo'),
                'nome': value.get('nome'),
                'cidades_atuais': len(value['estados']['MG']['cidades'])
            })
    
    print(f"Total de representantes que atendem MG: {len(representantes_mg)}")
    
    # Mostrar representantes encontrados
    for rep in representantes_mg:
        print(f"  {rep['codigo']} - {rep['nome']}: {rep['cidades_atuais']} cidades")
    
    print(f"\n=== INICIANDO LIMPEZA ===")
    
    # Limpar TODOS os representantes de MG
    for rep in representantes_mg:
        key = rep['key']
        
        # Limpar cidades
        representantes['representantes'][key]['estados']['MG']['cidades'] = []
        representantes['representantes'][key]['estados']['MG']['total_cidades'] = 0
        representantes['representantes'][key]['total_cidades'] = 0
        
        print(f"✅ {rep['codigo']} - {rep['nome']}: {rep['cidades_atuais']} → 0 cidades")
    
    # Salvar arquivo atualizado
    print(f"\nSalvando arquivo atualizado...")
    salvar_representantes(representantes)
    
    print(f"\n=== LIMPEZA CONCLUÍDA ===")
    print("✅ TODOS os representantes de MG foram limpos!")
    print("✅ Todas as cidades foram removidas!")
    print("✅ Todos os totais foram zerados!")
    print("✅ Arquivo salvo com sucesso!")

if __name__ == "__main__":
    limpar_todos_representantes_mg()
