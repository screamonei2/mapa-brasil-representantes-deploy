#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para normalizar nomes de estados e cidades no arquivo representantes_por_estado.json
- Remove acentuação e cedilha
- Converte para uppercase
- Faz backup antes da modificação
"""

import json
import os
import shutil
from datetime import datetime
import unicodedata

def remover_acentos(texto):
    """
    Remove acentos e cedilhas de um texto, convertendo para ASCII
    """
    if not isinstance(texto, str):
        return texto
    
    # Normaliza para forma NFD (decomposição) e remove diacríticos
    texto_sem_acentos = unicodedata.normalize('NFD', texto)
    texto_sem_acentos = ''.join(
        char for char in texto_sem_acentos 
        if unicodedata.category(char) != 'Mn'
    )
    
    # Mapeamento específico para caracteres especiais
    mapeamento = {
        'ç': 'C',
        'Ç': 'C',
        'ñ': 'N',
        'Ñ': 'N'
    }
    
    for char_original, char_substituto in mapeamento.items():
        texto_sem_acentos = texto_sem_acentos.replace(char_original, char_substituto)
    
    return texto_sem_acentos.upper()

def normalizar_estados_cidades(data):
    """
    Normaliza recursivamente os nomes de estados e cidades
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "estados":
                # Normaliza nomes dos estados
                estados_normalizados = {}
                for estado, info_estado in value.items():
                    estado_normalizado = remover_acentos(estado)
                    estados_normalizados[estado_normalizado] = info_estado
                    
                    # Normaliza cidades dentro do estado
                    if "cidades" in info_estado:
                        info_estado["cidades"] = [
                            remover_acentos(cidade) for cidade in info_estado["cidades"]
                        ]
                    
                    # Normaliza mesorregiões se existirem
                    if "mesorregioes" in info_estado:
                        info_estado["mesorregioes"] = [
                            remover_acentos(mesorregiao) for mesorregiao in info_estado["mesorregioes"]
                        ]
                
                data[key] = estados_normalizados
            elif key == "estados_atendidos":
                # Normaliza lista de estados atendidos
                data[key] = [remover_acentos(estado) for estado in value]
            else:
                # Recursão para outros campos
                normalizar_estados_cidades(value)
    
    elif isinstance(data, list):
        for item in data:
            normalizar_estados_cidades(item)

def fazer_backup(arquivo_original):
    """
    Cria um backup do arquivo original com timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"{arquivo_original}.backup_{timestamp}"
    
    try:
        shutil.copy2(arquivo_original, nome_backup)
        print(f"✅ Backup criado: {nome_backup}")
        return nome_backup
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def main():
    arquivo_json = "data/representantes_por_estado.json"
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_json):
        print(f"❌ Arquivo não encontrado: {arquivo_json}")
        return
    
    print(f"📁 Processando arquivo: {arquivo_json}")
    
    # Faz backup do arquivo original
    backup_criado = fazer_backup(arquivo_json)
    if not backup_criado:
        print("❌ Não foi possível criar backup. Abortando operação.")
        return
    
    try:
        # Carrega o JSON
        print("📖 Carregando arquivo JSON...")
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("🔧 Normalizando nomes de estados e cidades...")
        
        # Normaliza os dados
        normalizar_estados_cidades(data)
        
        # Salva o arquivo normalizado
        print("💾 Salvando arquivo normalizado...")
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ Arquivo normalizado com sucesso!")
        print(f"📋 Backup salvo em: {backup_criado}")
        
        # Estatísticas
        total_representantes = len(data.get("representantes", {}))
        print(f"📊 Total de representantes processados: {total_representantes}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        print("🔄 Restaurando arquivo original do backup...")
        try:
            shutil.copy2(backup_criado, arquivo_json)
            print("✅ Arquivo original restaurado do backup")
        except Exception as restore_error:
            print(f"❌ Erro ao restaurar backup: {restore_error}")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("🔄 Restaurando arquivo original do backup...")
        try:
            shutil.copy2(backup_criado, arquivo_json)
            print("✅ Arquivo original restaurado do backup")
        except Exception as restore_error:
            print(f"❌ Erro ao restaurar backup: {restore_error}")

if __name__ == "__main__":
    main()
