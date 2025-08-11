#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para pintar o representante 3L de vermelho.
Adiciona um campo 'cor' com valor '#FF0000' ao representante 3L.
"""

import json
import os

def pintar_3l_vermelho():
    """Pinta o representante 3L de vermelho."""
    
    # Carregar arquivo de representantes
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        representantes = json.load(f)
    
    # Encontrar o representante 3L
    rep_3l = None
    for nome, dados in representantes["representantes"].items():
        if nome == "3l representacoes comerciais ltda me":
            rep_3l = dados
            break
    
    if rep_3l:
        # Adicionar cor vermelha
        rep_3l["cor"] = "#FF0000"
        print("✓ Cor vermelha (#FF0000) adicionada ao representante 3L")
        
        # Mostrar informações do representante
        print(f"\n📋 Informações do Representante 3L:")
        print(f"   Nome: {rep_3l['nome']}")
        print(f"   Código: {rep_3l['codigo']}")
        print(f"   Cor: {rep_3l['cor']}")
        print(f"   Total de cidades: {rep_3l['total_cidades']}")
        print(f"   Estados atendidos: {rep_3l['estados_atendidos']}")
        
        return representantes
    else:
        print("❌ Representante 3L não encontrado!")
        return None

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_3l_vermelho.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\nBackup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== PINTANDO REPRESENTANTE 3L DE VERMELHO ===")
    print("Objetivo: Adicionar cor vermelha (#FF0000) ao representante 3L")
    print()
    
    try:
        # Pintar 3L de vermelho
        representantes = pintar_3l_vermelho()
        
        if representantes:
            # Salvar arquivo
            salvar_arquivo(representantes)
            print("\n✅ Representante 3L pintado de vermelho com sucesso!")
            print("✅ Campo 'cor' adicionado com valor '#FF0000'")
        else:
            print("\n❌ Erro: Não foi possível pintar o representante 3L")
            
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
