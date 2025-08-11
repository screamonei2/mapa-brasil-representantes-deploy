#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir a distribuição das cidades das regiões Norte, Central e Centro-Oeste de Minas Gerais.
Remove essas cidades do representante 42 e deixa apenas com o representante 48.
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
    """Obtém as cidades das regiões que devem pertencer apenas ao representante 48."""
    regioes_48 = ["Norte de Minas", "Central Mineira", "Noroeste de Minas"]
    cidades_48 = set()
    
    for mesorregiao in mesorregioes:
        if mesorregiao["mesorregiao"] in regioes_48:
            for municipio in mesorregiao["municipios"]:
                cidades_48.add(municipio.upper())
    
    return cidades_48

def corrigir_distribuicao(representantes, cidades_48):
    """Corrige a distribuição das cidades."""
    # Representante 42 (RG REPRESENTAÇÕES LTDA)
    rep_42 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "42.0":
            rep_42 = dados
            break
    
    # Representante 48 (GTR REPRESENTAÇÕES LTDA)
    rep_48 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "48.0":
            rep_48 = dados
            break
    
    if not rep_42 or not rep_48:
        print("ERRO: Não foi possível encontrar os representantes 42 ou 48")
        return False
    
    # Cidades do representante 42 que devem ser removidas
    cidades_remover_42 = []
    cidades_adicionar_48 = []
    
    if "MG" in rep_42["estados"]:
        for cidade in rep_42["estados"]["MG"]["cidades"]:
            if cidade in cidades_48:
                cidades_remover_42.append(cidade)
                cidades_adicionar_48.append(cidade)
    
    # Remove as cidades do representante 42
    if cidades_remover_42:
        rep_42["estados"]["MG"]["cidades"] = [
            cidade for cidade in rep_42["estados"]["MG"]["cidades"] 
            if cidade not in cidades_48
        ]
        rep_42["estados"]["MG"]["total_cidades"] = len(rep_42["estados"]["MG"]["cidades"])
        rep_42["total_cidades"] = rep_42["estados"]["MG"]["total_cidades"]
        
        print(f"Removidas {len(cidades_remover_42)} cidades do representante 42")
        print("Cidades removidas:", cidades_remover_42[:10], "..." if len(cidades_remover_42) > 10 else "")
    
    # Adiciona as cidades ao representante 48
    if cidades_adicionar_48:
        if "MG" not in rep_48["estados"]:
            rep_48["estados"]["MG"] = {"cidades": [], "total_cidades": 0}
        
        # Adiciona apenas cidades que não estão já na lista
        cidades_existentes = set(rep_48["estados"]["MG"]["cidades"])
        for cidade in cidades_adicionar_48:
            if cidade not in cidades_existentes:
                rep_48["estados"]["MG"]["cidades"].append(cidade)
        
        rep_48["estados"]["MG"]["total_cidades"] = len(rep_48["estados"]["MG"]["cidades"])
        rep_48["total_cidades"] = rep_48["estados"]["MG"]["total_cidades"]
        
        print(f"Adicionadas {len(cidades_adicionar_48)} cidades ao representante 48")
        print("Cidades adicionadas:", cidades_adicionar_48[:10], "..." if len(cidades_adicionar_48) > 10 else "")
    
    return True

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_correcao_mg_48.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"Backup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== CORREÇÃO DA DISTRIBUIÇÃO DE CIDADES MG ===")
    print("Regiões que devem pertencer apenas ao representante 48:")
    print("- Norte de Minas")
    print("- Central Mineira") 
    print("- Noroeste de Minas")
    print()
    
    try:
        # Carrega os arquivos
        mesorregioes, representantes = carregar_arquivos()
        print("✓ Arquivos carregados com sucesso")
        
        # Obtém as cidades das regiões do representante 48
        cidades_48 = obter_cidades_regioes_48(mesorregioes)
        print(f"✓ Identificadas {len(cidades_48)} cidades das regiões do representante 48")
        
        # Corrige a distribuição
        if corrigir_distribuicao(representantes, cidades_48):
            # Salva o arquivo
            salvar_arquivo(representantes)
            print("\n✓ Correção concluída com sucesso!")
        else:
            print("\n✗ Erro na correção!")
            
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
