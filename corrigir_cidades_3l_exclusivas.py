#!/usr/bin/env python3
"""
Script para corrigir cidades que pertencem exclusivamente à 3L Representações
Remove essas cidades de outros representantes que não deveriam tê-las
"""

import json
import os
from datetime import datetime

def carregar_dados():
    """Carrega o arquivo de representantes"""
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_backup(dados, nome_backup):
    """Salva um backup dos dados"""
    os.makedirs('data/backups', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"data/backups/representantes_por_estado_backup_{nome_backup}_{timestamp}.json"
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Backup salvo: {nome_arquivo}")
    return nome_arquivo

def corrigir_cidades_3l_exclusivas(dados):
    """
    Corrige as cidades que pertencem exclusivamente à 3L Representações
    """
    # Cidades que pertencem exclusivamente à 3L
    cidades_3l_exclusivas = [
        "PRESIDENTE PRUDENTE",
        "MARILIA", 
        "ASSIS",
        "BAURU"
    ]
    
    # Encontrar o representante 3L
    representante_3l = None
    for key, rep in dados['representantes'].items():
        if '3l' in key.lower() or '3L' in rep['nome']:
            representante_3l = key
            break
    
    if not representante_3l:
        print("❌ Representante 3L não encontrado!")
        return dados
    
    print(f"✅ Representante 3L encontrado: {representante_3l}")
    
    # Verificar se as cidades estão na 3L
    cidades_3l = set()
    if 'SP' in dados['representantes'][representante_3l]['estados']:
        cidades_3l = set(dados['representantes'][representante_3l]['estados']['SP']['cidades'])
    
    print(f"📊 Cidades da 3L: {len(cidades_3l)}")
    
    # Verificar quais cidades exclusivas estão realmente na 3L
    cidades_encontradas = []
    for cidade in cidades_3l_exclusivas:
        if cidade in cidades_3l:
            cidades_encontradas.append(cidade)
            print(f"✅ {cidade} encontrada na 3L")
        else:
            print(f"⚠️ {cidade} NÃO encontrada na 3L")
    
    if not cidades_encontradas:
        print("❌ Nenhuma das cidades exclusivas foi encontrada na 3L!")
        return dados
    
    # Remover essas cidades de outros representantes
    cidades_removidas = {}
    
    for key, rep in dados['representantes'].items():
        if key == representante_3l:
            continue  # Pular a 3L
        
        if 'estados' in rep:
            for uf, estado_data in rep['estados'].items():
                if 'cidades' in estado_data:
                    cidades_originais = set(estado_data['cidades'])
                    cidades_para_remover = cidades_originais.intersection(set(cidades_encontradas))
                    
                    if cidades_para_remover:
                        # Remover as cidades
                        for cidade in cidades_para_remover:
                            estado_data['cidades'].remove(cidade)
                        
                        # Atualizar total
                        estado_data['total_cidades'] = len(estado_data['cidades'])
                        
                        # Atualizar total geral
                        rep['total_cidades'] = sum(est['total_cidades'] for est in rep['estados'].values())
                        
                        cidades_removidas[key] = cidades_removidas.get(key, []) + list(cidades_para_remover)
                        
                        print(f"🗑️ Removidas de {rep['nome']}: {list(cidades_para_remover)}")
    
    # Relatório
    print("\n📋 RELATÓRIO DE CORREÇÃO:")
    print("=" * 50)
    print(f"Cidades exclusivas da 3L: {cidades_encontradas}")
    print(f"Total de representantes afetados: {len(cidades_removidas)}")
    
    for rep_key, cidades in cidades_removidas.items():
        rep_nome = dados['representantes'][rep_key]['nome']
        print(f"  - {rep_nome}: {len(cidades)} cidades removidas")
    
    return dados

def main():
    """Função principal"""
    print("🔧 CORRIGINDO CIDADES EXCLUSIVAS DA 3L")
    print("=" * 50)
    
    # Carregar dados
    print("📂 Carregando dados...")
    dados = carregar_dados()
    
    # Fazer backup
    print("💾 Fazendo backup...")
    backup_file = salvar_backup(dados, "antes_correcao_3l_exclusivas")
    
    # Corrigir cidades
    print("🔧 Corrigindo cidades...")
    dados_corrigidos = corrigir_cidades_3l_exclusivas(dados)
    
    # Salvar dados corrigidos
    print("💾 Salvando dados corrigidos...")
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)
    
    print("✅ Correção concluída!")
    print(f"📁 Backup salvo em: {backup_file}")

if __name__ == "__main__":
    main()
