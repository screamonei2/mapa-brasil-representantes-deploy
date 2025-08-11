#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar as cidades da região Vale do Rio Doce ao representante 48,
junto com as cidades das regiões Norte, Central, Jequitinhonha e Vale do Mucuri de Minas que já estão lá.
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

def obter_cidades_regioes_48(mesorregioes):
    """Obtém as cidades das regiões que devem pertencer ao representante 48."""
    regioes_48 = ["Norte de Minas", "Central Mineira", "Jequitinhonha", "Vale do Mucuri", "Vale do Rio Doce"]
    cidades_48 = []
    
    for mesorregiao in mesorregioes:
        if mesorregiao["mesorregiao"] in regioes_48:
            for municipio in mesorregiao["municipios"]:
                cidades_48.append(municipio.upper())
    
    return cidades_48

def atualizar_representante_48(representantes, cidades_regioes_48):
    """Atualiza o representante 48 com as cidades das regiões Norte, Central, Jequitinhonha, Vale do Mucuri e Vale do Rio Doce de Minas."""
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
    
    # Cidades que devem ser adicionadas (da região Vale do Rio Doce que não estão)
    cidades_adicionar = set(cidades_regioes_48) - cidades_atuais
    
    print(f"\nCidades a serem adicionadas: {len(cidades_adicionar)}")
    if cidades_adicionar:
        print("Cidades adicionadas:", list(cidades_adicionar)[:10], "..." if len(cidades_adicionar) > 10 else "")
    
    # Atualiza o representante 48
    if "MG" not in rep_48["estados"]:
        rep_48["estados"]["MG"] = {"cidades": [], "total_cidades": 0}
    
    # Define as cidades corretas (regiões Norte, Central, Jequitinhonha, Vale do Mucuri e Vale do Rio Doce de Minas)
    rep_48["estados"]["MG"]["cidades"] = sorted(cidades_regioes_48)
    rep_48["estados"]["MG"]["total_cidades"] = len(cidades_regioes_48)
    rep_48["total_cidades"] = len(cidades_regioes_48)
    
    return True

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_vale_rio_doce_48.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\nBackup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== ADIÇÃO DA REGIÃO VALE DO RIO DOCE AO REPRESENTANTE 48 ===")
    print("Regiões que devem pertencer ao representante 48:")
    print("- Norte de Minas")
    print("- Central Mineira")
    print("- Jequitinhonha")
    print("- Vale do Mucuri")
    print("- Vale do Rio Doce")
    print()
    
    try:
        # Carrega os arquivos
        mesorregioes, representantes = carregar_arquivos()
        print("✓ Arquivos carregados com sucesso")
        
        # Obtém as cidades das regiões Norte, Central, Jequitinhonha, Vale do Mucuri e Vale do Rio Doce de Minas
        cidades_regioes_48 = obter_cidades_regioes_48(mesorregioes)
        print(f"✓ Identificadas {len(cidades_regioes_48)} cidades das regiões Norte, Central, Jequitinhonha, Vale do Mucuri e Vale do Rio Doce de Minas")
        
        # Atualiza o representante 48
        if atualizar_representante_48(representantes, cidades_regioes_48):
            # Salva o arquivo
            salvar_arquivo(representantes)
            print("\n✓ Atualização concluída com sucesso!")
            print(f"✓ Representante 48 agora tem {len(cidades_regioes_48)} cidades")
            print("✓ Regiões atendidas: Norte + Central + Jequitinhonha + Vale do Mucuri + Vale do Rio Doce")
        else:
            print("\n✗ Erro na atualização!")
            
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
