#!/usr/bin/env python3
"""
Script para remover cidades das mesorregiões da 3L de outros representantes
Remove cidades das mesorregiões: Presidente Prudente, Marília, Assis e Bauru
de todos os outros representantes, mantendo-as apenas na 3L
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

def obter_cidades_mesorregioes_3l(mesorregioes):
    """
    Obtém todas as cidades das mesorregiões exclusivas da 3L
    """
    # Mesorregiões que pertencem exclusivamente à 3L
    mesorregioes_3l = [
        "Presidente Prudente",
        "Marília", 
        "Assis",
        "Bauru"
    ]
    
    cidades_mesorregioes_3l = set()
    
    for mesorregiao in mesorregioes_3l:
        # Encontrar a mesorregião no arquivo
        for meso in mesorregioes:
            if meso['mesorregiao'] == mesorregiao:
                municipios = [m.upper() for m in meso['municipios']]
                cidades_mesorregioes_3l.update(municipios)
                print(f"📍 {mesorregiao}: {len(municipios)} municípios")
                break
    
    print(f"📊 Total de cidades das mesorregiões da 3L: {len(cidades_mesorregioes_3l)}")
    return cidades_mesorregioes_3l

def remover_cidades_3l_de_outros_representantes(representantes, cidades_mesorregioes_3l):
    """
    Remove cidades das mesorregiões da 3L de outros representantes
    """
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
    
    # Relatório de remoções
    cidades_removidas = {}
    total_removidas = 0
    
    for key, rep in representantes['representantes'].items():
        if key == representante_3l:
            continue  # Pular a 3L
        
        if 'estados' in rep:
            for uf, estado_data in rep['estados'].items():
                if 'cidades' in estado_data:
                    cidades_originais = set(estado_data['cidades'])
                    cidades_para_remover = cidades_originais.intersection(cidades_mesorregioes_3l)
                    
                    if cidades_para_remover:
                        # Remover as cidades
                        for cidade in cidades_para_remover:
                            estado_data['cidades'].remove(cidade)
                        
                        # Atualizar total do estado
                        estado_data['total_cidades'] = len(estado_data['cidades'])
                        
                        # Atualizar total geral do representante
                        rep['total_cidades'] = sum(est['total_cidades'] for est in rep['estados'].values())
                        
                        # Registrar remoções
                        if key not in cidades_removidas:
                            cidades_removidas[key] = {}
                        if uf not in cidades_removidas[key]:
                            cidades_removidas[key][uf] = []
                        
                        cidades_removidas[key][uf].extend(list(cidades_para_remover))
                        total_removidas += len(cidades_para_remover)
                        
                        print(f"🗑️ Removidas de {rep['nome']} ({uf}): {len(cidades_para_remover)} cidades")
    
    # Relatório detalhado
    print(f"\n📋 RELATÓRIO DE REMOÇÃO:")
    print("=" * 60)
    print(f"Total de cidades removidas: {total_removidas}")
    print(f"Total de representantes afetados: {len(cidades_removidas)}")
    
    for rep_key, estados in cidades_removidas.items():
        rep_nome = representantes['representantes'][rep_key]['nome']
        total_rep = sum(len(cidades) for cidades in estados.values())
        print(f"\n  📍 {rep_nome}: {total_rep} cidades removidas")
        
        for uf, cidades in estados.items():
            print(f"    - {uf}: {len(cidades)} cidades")
            if len(cidades) <= 10:
                print(f"      {', '.join(cidades)}")
            else:
                print(f"      {', '.join(cidades[:10])}... e mais {len(cidades) - 10}")
    
    return representantes

def main():
    """Função principal"""
    print("🗑️ REMOVENDO CIDADES DA 3L DE OUTROS REPRESENTANTES")
    print("=" * 70)
    
    # Carregar dados
    print("📂 Carregando dados...")
    representantes, mesorregioes = carregar_dados()
    
    # Fazer backup
    print("💾 Fazendo backup...")
    backup_file = salvar_backup(representantes, "antes_remocao_cidades_3l")
    
    # Obter cidades das mesorregiões da 3L
    print("📍 Identificando cidades das mesorregiões da 3L...")
    cidades_mesorregioes_3l = obter_cidades_mesorregioes_3l(mesorregioes)
    
    # Remover cidades de outros representantes
    print("🗑️ Removendo cidades de outros representantes...")
    representantes_corrigidos = remover_cidades_3l_de_outros_representantes(representantes, cidades_mesorregioes_3l)
    
    # Salvar dados corrigidos
    print("💾 Salvando dados corrigidos...")
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes_corrigidos, f, ensure_ascii=False, indent=2)
    
    print("✅ Remoção concluída!")
    print(f"📁 Backup salvo em: {backup_file}")

if __name__ == "__main__":
    main()
