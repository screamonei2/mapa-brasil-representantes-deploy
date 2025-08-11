#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover do representante 42 as cidades que pertencem ao Norte de Minas,
mesmo que estejam sem acentos ou pontuação.
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
    """Obtém as cidades da região Norte de Minas (com e sem acentos)."""
    cidades_norte = set()
    
    for mesorregiao in mesorregioes:
        if mesorregiao["mesorregiao"] == "Norte de Minas":
            for municipio in mesorregiao["municipios"]:
                # Adiciona a cidade original e sem acentos
                cidades_norte.add(municipio.upper())
                # Adiciona versão sem acentos para comparação
                cidades_norte.add(municipio.upper().replace('Á', 'A').replace('À', 'A').replace('Â', 'A').replace('Ã', 'A')
                                .replace('É', 'E').replace('È', 'E').replace('Ê', 'E')
                                .replace('Í', 'I').replace('Ì', 'I').replace('Î', 'I')
                                .replace('Ó', 'O').replace('Ò', 'O').replace('Ô', 'O').replace('Õ', 'O')
                                .replace('Ú', 'U').replace('Ù', 'U').replace('Û', 'U')
                                .replace('Ç', 'C'))
    
    return cidades_norte

def remover_cidades_norte_minas_42(representantes, cidades_norte_minas):
    """Remove do representante 42 as cidades que pertencem ao Norte de Minas."""
    # Encontra o representante 42
    rep_42 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "42.0":
            rep_42 = dados
            break
    
    if not rep_42:
        print("ERRO: Não foi possível encontrar o representante 42")
        return False
    
    # Cidades atuais do representante 42
    cidades_atuais = []
    if "MG" in rep_42["estados"]:
        cidades_atuais = rep_42["estados"]["MG"]["cidades"]
    
    print(f"Cidades atuais no representante 42: {len(cidades_atuais)}")
    
    # Cidades que devem ser removidas (pertencentes ao Norte de Minas)
    cidades_remover = []
    cidades_manter = []
    
    for cidade in cidades_atuais:
        if cidade in cidades_norte_minas:
            cidades_remover.append(cidade)
        else:
            cidades_manter.append(cidade)
    
    print(f"\nCidades a serem removidas (Norte de Minas): {len(cidades_remover)}")
    if cidades_remover:
        print("Cidades removidas:", cidades_remover[:10], "..." if len(cidades_remover) > 10 else "")
    
    print(f"Cidades a serem mantidas: {len(cidades_manter)}")
    
    # Atualiza o representante 42
    rep_42["estados"]["MG"]["cidades"] = cidades_manter
    rep_42["estados"]["MG"]["total_cidades"] = len(cidades_manter)
    rep_42["total_cidades"] = len(cidades_manter)
    
    return True

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_remocao_norte_minas_42.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\nBackup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== REMOÇÃO DE CIDADES DO NORTE DE MINAS DO REPRESENTANTE 42 ===")
    print("Objetivo: Remover cidades do Norte de Minas que ainda estão com o representante 42")
    print()
    
    try:
        # Carrega os arquivos
        mesorregioes, representantes = carregar_arquivos()
        print("✓ Arquivos carregados com sucesso")
        
        # Obtém as cidades da região Norte de Minas (com e sem acentos)
        cidades_norte = obter_cidades_norte_minas(mesorregioes)
        print(f"✓ Identificadas {len(cidades_norte)} variações de cidades da região Norte de Minas")
        
        # Remove as cidades do Norte de Minas do representante 42
        if remover_cidades_norte_minas_42(representantes, cidades_norte):
            # Salva o arquivo
            salvar_arquivo(representantes)
            print("\n✓ Remoção concluída com sucesso!")
            print("✓ Cidades do Norte de Minas foram removidas do representante 42")
        else:
            print("\n✗ Erro na remoção!")
            
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
