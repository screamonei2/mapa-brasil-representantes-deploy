#!/usr/bin/env python3
"""
Script para corrigir as mesorregiões exclusivas da 3L
Adiciona TODAS as cidades das mesorregiões: Presidente Prudente, Marília, Assis e Bauru
"""

import json
import os
from datetime import datetime

def carregar_dados():
    """Carrega os arquivos necessários"""
    # Carregar representantes
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        representantes = json.load(f)
    
    # Carregar mesorregiões de SP
    with open('sp_mesorregioes.json', 'r', encoding='utf-8') as f:
        mesorregioes = json.load(f)
    
    return representantes, mesorregioes

def salvar_backup(dados, nome_backup):
    """Salva um backup dos dados"""
    os.makedirs('data/backups', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"data/backups/representantes_por_estado_backup_{nome_backup}_{timestamp}.json"
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Backup salvo: {nome_arquivo}")
    return nome_arquivo

def corrigir_mesorregioes_3l(representantes, mesorregioes):
    """
    Corrige as mesorregiões exclusivas da 3L
    """
    # Mesorregiões que pertencem exclusivamente à 3L
    mesorregioes_3l = [
        "Presidente Prudente",
        "Marília", 
        "Assis",
        "Bauru"
    ]
    
    # Encontrar o representante 3L
    representante_3l = None
    for key, rep in representantes['representantes'].items():
        if '3l' in key.lower() or '3L' in rep['nome']:
            representante_3l = key
            break
    
    if not representante_3l:
        print("❌ Representante 3L não encontrado!")
        return representantes
    
    print(f"✅ Representante 3L encontrado: {representante_3l}")
    
    # Verificar se o estado SP existe
    if 'SP' not in representantes['representantes'][representante_3l]['estados']:
        print("❌ Estado SP não encontrado na 3L!")
        return representantes
    
    # Obter cidades atuais da 3L
    cidades_atuais_3l = set(representantes['representantes'][representante_3l]['estados']['SP']['cidades'])
    print(f"📊 Cidades atuais da 3L: {len(cidades_atuais_3l)}")
    
    # Coletar todas as cidades das mesorregiões exclusivas
    cidades_mesorregioes = set()
    cidades_adicionadas = {}
    
    for mesorregiao in mesorregioes_3l:
        # Encontrar a mesorregião no arquivo
        for meso in mesorregioes:
            if meso['mesorregiao'] == mesorregiao:
                municipios = [m.upper() for m in meso['municipios']]
                cidades_mesorregioes.update(municipios)
                
                # Verificar quais cidades já estão na 3L
                cidades_existentes = set(municipios).intersection(cidades_atuais_3l)
                cidades_faltantes = set(municipios) - cidades_atuais_3l
                
                cidades_adicionadas[mesorregiao] = {
                    'existentes': len(cidades_existentes),
                    'faltantes': len(cidades_faltantes),
                    'total': len(municipios),
                    'lista_faltantes': list(cidades_faltantes)
                }
                
                print(f"📍 {mesorregiao}: {len(municipios)} municípios")
                print(f"   ✅ Já existem: {len(cidades_existentes)}")
                print(f"   ➕ Faltam: {len(cidades_faltantes)}")
                break
    
    # Adicionar cidades faltantes à 3L
    cidades_para_adicionar = cidades_mesorregioes - cidades_atuais_3l
    
    if cidades_para_adicionar:
        print(f"\n➕ Adicionando {len(cidades_para_adicionar)} cidades à 3L...")
        
        # Adicionar as cidades
        for cidade in sorted(cidades_para_adicionar):
            representantes['representantes'][representante_3l]['estados']['SP']['cidades'].append(cidade)
        
        # Ordenar cidades
        representantes['representantes'][representante_3l]['estados']['SP']['cidades'].sort()
        
        # Atualizar total
        representantes['representantes'][representante_3l]['estados']['SP']['total_cidades'] = len(representantes['representantes'][representante_3l]['estados']['SP']['cidades'])
        representantes['representantes'][representante_3l]['total_cidades'] = representantes['representantes'][representante_3l]['estados']['SP']['total_cidades']
        
        print(f"✅ Total de cidades da 3L após correção: {representantes['representantes'][representante_3l]['estados']['SP']['total_cidades']}")
    else:
        print("✅ Todas as cidades das mesorregiões já estão na 3L!")
    
    # Relatório detalhado
    print("\n📋 RELATÓRIO DETALHADO:")
    print("=" * 60)
    
    for mesorregiao, info in cidades_adicionadas.items():
        print(f"\n📍 {mesorregiao}:")
        print(f"   📊 Total de municípios: {info['total']}")
        print(f"   ✅ Já existiam: {info['existentes']}")
        print(f"   ➕ Adicionados: {info['faltantes']}")
        
        if info['lista_faltantes']:
            print(f"   📝 Cidades adicionadas: {', '.join(info['lista_faltantes'][:10])}")
            if len(info['lista_faltantes']) > 10:
                print(f"   ... e mais {len(info['lista_faltantes']) - 10} cidades")
    
    return representantes

def main():
    """Função principal"""
    print("🔧 CORRIGINDO MESORREGIÕES EXCLUSIVAS DA 3L")
    print("=" * 60)
    
    # Carregar dados
    print("📂 Carregando dados...")
    representantes, mesorregioes = carregar_dados()
    
    # Fazer backup
    print("💾 Fazendo backup...")
    backup_file = salvar_backup(representantes, "antes_correcao_mesorregioes_3l")
    
    # Corrigir mesorregiões
    print("🔧 Corrigindo mesorregiões...")
    representantes_corrigidos = corrigir_mesorregioes_3l(representantes, mesorregioes)
    
    # Salvar dados corrigidos
    print("💾 Salvando dados corrigidos...")
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes_corrigidos, f, ensure_ascii=False, indent=2)
    
    print("✅ Correção concluída!")
    print(f"📁 Backup salvo em: {backup_file}")

if __name__ == "__main__":
    main()
