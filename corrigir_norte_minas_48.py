#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir completamente o representante 48 com TODAS as cidades da região Norte de Minas.
Remove cidades incorretas e adiciona todas as cidades corretas da região Norte de Minas.
"""

import json
import os

def carregar_arquivos():
    """Carrega os arquivos necessários."""
    # Carrega as mesorregiões
    with open('mesorregioes_mg.json', 'r', encoding='utf-8') as f:
        mesorregioes = json.load(f)
    
    # Carrega os representantes
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        representantes = json.load(f)
    
    return mesorregioes, representantes

def obter_cidades_norte_minas(mesorregioes):
    """Obtém TODAS as cidades da região Norte de Minas."""
    cidades_norte = []
    
    for mesorregiao in mesorregioes:
        if mesorregiao["mesorregiao"] == "Norte de Minas":
            cidades_norte = [municipio.upper() for municipio in mesorregiao["municipios"]]
            break
    
    return cidades_norte

def corrigir_representante_48(representantes, cidades_norte_minas):
    """Corrige completamente o representante 48 com as cidades corretas."""
    # Encontra o representante 48
    rep_48 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "48.0":
            rep_48 = dados
            break
    
    if not rep_48:
        print("ERRO: Não foi possível encontrar o representante 48")
        return False
    
    # Cidades atuais do representante 48
    cidades_atuais = set()
    if "MG" in rep_48["estados"]:
        cidades_atuais = set(rep_48["estados"]["MG"]["cidades"])
    
    print(f"Cidades atuais no representante 48: {len(cidades_atuais)}")
    print("Cidades atuais:", list(cidades_atuais)[:10], "..." if len(cidades_atuais) > 10 else "")
    
    # Cidades que devem ser removidas (não são da região Norte de Minas)
    cidades_remover = cidades_atuais - set(cidades_norte_minas)
    
    # Cidades que devem ser adicionadas (da região Norte de Minas que não estão)
    cidades_adicionar = set(cidades_norte_minas) - cidades_atuais
    
    print(f"\nCidades a serem removidas: {len(cidades_remover)}")
    if cidades_remover:
        print("Cidades removidas:", list(cidades_remover)[:10], "..." if len(cidades_remover) > 10 else "")
    
    print(f"Cidades a serem adicionadas: {len(cidades_adicionar)}")
    if cidades_adicionar:
        print("Cidades adicionadas:", list(cidades_adicionar)[:10], "..." if len(cidades_adicionar) > 10 else "")
    
    # Atualiza o representante 48
    if "MG" not in rep_48["estados"]:
        rep_48["estados"]["MG"] = {"cidades": [], "total_cidades": 0}
    
    # Define as cidades corretas (apenas da região Norte de Minas)
    rep_48["estados"]["MG"]["cidades"] = sorted(cidades_norte_minas)
    rep_48["estados"]["MG"]["total_cidades"] = len(cidades_norte_minas)
    rep_48["total_cidades"] = len(cidades_norte_minas)
    
    return True

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_norte_minas_48.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\nBackup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== CORREÇÃO COMPLETA DO REPRESENTANTE 48 ===")
    print("Região: NORTE DE MINAS (exclusivamente)")
    print()
    
    try:
        # Carrega os arquivos
        mesorregioes, representantes = carregar_arquivos()
        print("✓ Arquivos carregados com sucesso")
        
        # Obtém TODAS as cidades da região Norte de Minas
        cidades_norte = obter_cidades_norte_minas(mesorregioes)
        print(f"✓ Identificadas {len(cidades_norte)} cidades da região Norte de Minas")
        
        # Corrige o representante 48
        if corrigir_representante_48(representantes, cidades_norte):
            # Salva o arquivo
            salvar_arquivo(representantes)
            print("\n✓ Correção concluída com sucesso!")
            print(f"✓ Representante 48 agora tem {len(cidades_norte)} cidades (apenas da região Norte de Minas)")
        else:
            print("\n✗ Erro na correção!")
            
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
