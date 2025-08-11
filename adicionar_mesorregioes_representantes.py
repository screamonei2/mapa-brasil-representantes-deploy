#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar informações de mesorregiões aos representantes.
Adiciona um campo 'mesorregioes' mostrando quais regiões cada representante atende.
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

def mapear_cidade_mesorregiao(mesorregioes):
    """Cria um mapeamento de cidade -> mesorregião."""
    mapeamento = {}
    
    for mesorregiao in mesorregioes:
        nome_mesorregiao = mesorregiao["mesorregiao"]
        for municipio in mesorregiao["municipios"]:
            # Adiciona tanto com acentos quanto sem
            mapeamento[municipio.upper()] = nome_mesorregiao
            mapeamento[municipio.upper().replace('Á', 'A').replace('À', 'A').replace('Â', 'A').replace('Ã', 'A')
                      .replace('É', 'E').replace('È', 'E').replace('Ê', 'E')
                      .replace('Í', 'I').replace('Ì', 'I').replace('Î', 'I')
                      .replace('Ó', 'O').replace('Ò', 'O').replace('Ô', 'O').replace('Õ', 'O')
                      .replace('Ú', 'U').replace('Ù', 'U').replace('Û', 'U')
                      .replace('Ç', 'C')] = nome_mesorregiao
    
    return mapeamento

def adicionar_mesorregioes_representantes(representantes, mapeamento_cidade_mesorregiao):
    """Adiciona informações de mesorregiões aos representantes."""
    for nome_rep, dados_rep in representantes["representantes"].items():
        if "estados" in dados_rep:
            for sigla_estado, dados_estado in dados_rep["estados"].items():
                if "cidades" in dados_estado:
                    # Conjunto para armazenar mesorregiões únicas
                    mesorregioes_estado = set()
                    
                    # Para cada cidade, identifica a mesorregião
                    for cidade in dados_estado["cidades"]:
                        if cidade in mapeamento_cidade_mesorregiao:
                            mesorregioes_estado.add(mapeamento_cidade_mesorregiao[cidade])
                    
                    # Adiciona o campo mesorregiões
                    dados_estado["mesorregioes"] = sorted(list(mesorregioes_estado))
                    
                    # Adiciona contador de mesorregiões
                    dados_estado["total_mesorregioes"] = len(mesorregioes_estado)
                    
                    print(f"✓ {nome_rep} ({sigla_estado}): {len(mesorregioes_estado)} mesorregiões")

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_com_mesorregioes.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\nBackup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== ADIÇÃO DE INFORMAÇÕES DE MESORREGIÕES AOS REPRESENTANTES ===")
    print("Objetivo: Adicionar campo 'mesorregioes' mostrando quais regiões cada representante atende")
    print()
    
    try:
        # Carrega os arquivos
        mesorregioes, representantes = carregar_arquivos()
        print("✓ Arquivos carregados com sucesso")
        
        # Cria mapeamento cidade -> mesorregião
        mapeamento = mapear_cidade_mesorregiao(mesorregioes)
        print(f"✓ Mapeamento criado para {len(mapeamento)} variações de cidades")
        
        # Adiciona informações de mesorregiões
        print("\nAdicionando mesorregiões aos representantes...")
        adicionar_mesorregioes_representantes(representantes, mapeamento)
        
        # Salva o arquivo
        salvar_arquivo(representantes)
        print("\n✓ Adição de mesorregiões concluída com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
