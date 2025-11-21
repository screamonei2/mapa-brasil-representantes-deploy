#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reorganizar cidades do representante 23.01 para os representantes corretos
conforme a tabela fornecida.
"""

import json
import sys

def reorganizar_cidades():
    """Reorganiza as cidades do representante 23.01 para os representantes corretos."""
    
    # Ler o arquivo JSON
    arquivo = 'data/representantes_por_estado.json'
    with open(arquivo, 'r', encoding='utf-8') as f:
        root_data = json.load(f)
    
    # Acessar a chave 'representantes'
    data = root_data.get('representantes', {})
    
    # Mapeamento de cidades para novos representantes (conforme a tabela)
    mapeamento = {
        '38.04': [
            'SALTINHO', 'TIETE', 'JUMIRIM', 'CERQUILHO', 
            'BOITUVA', 'IPERO', 'PORTO FELIZ', 'ITU', 
            'SALTO', 'CABREUVA'
        ],
        '24': ['LOUVEIRA', 'JARINU'],
        '38': ['ITATIBA', 'MORUNGABA']
    }
    
    # Encontrar o representante 23.01 (thiago linares)
    rep_23_01 = None
    rep_23_01_key = None
    for key, value in data.items():
        if isinstance(value, dict) and value.get('codigo') == '23.01':
            rep_23_01 = value
            rep_23_01_key = key
            break
    
    if not rep_23_01:
        print("❌ Representante 23.01 não encontrado!")
        print("Representantes disponíveis:")
        for key, value in data.items():
            if isinstance(value, dict) and 'codigo' in value:
                print(f"  {key}: {value.get('codigo')}")
        return False
    
    # Encontrar os representantes de destino
    representantes_destino = {}
    for key, value in data.items():
        if isinstance(value, dict):
            codigo = value.get('codigo')
            if codigo in ['38.04', '24', '38']:
                representantes_destino[codigo] = (key, value)
    
    print(f"✓ Representante 23.01 encontrado: {rep_23_01['nome']}")
    print(f"  Cidades atuais em SP: {len(rep_23_01['estados']['SP']['cidades'])}")
    
    # Cidades atuais do 23.01
    cidades_23_01 = rep_23_01['estados']['SP']['cidades'].copy()
    
    # Processar cada destino
    cidades_movidas = []
    for codigo_destino, cidades_para_mover in mapeamento.items():
        if codigo_destino not in representantes_destino:
            print(f"❌ Representante {codigo_destino} não encontrado!")
            continue
        
        rep_key, rep_data = representantes_destino[codigo_destino]
        print(f"\n✓ Processando representante {codigo_destino}: {rep_data['nome']}")
        
        # Adicionar cidades ao representante de destino
        cidades_destino = rep_data['estados']['SP']['cidades']
        
        for cidade in cidades_para_mover:
            if cidade in cidades_23_01:
                if cidade not in cidades_destino:
                    cidades_destino.append(cidade)
                    print(f"  + Adicionando: {cidade}")
                    cidades_movidas.append(cidade)
                else:
                    print(f"  ⚠ {cidade} já existe no destino")
            else:
                print(f"  ⚠ {cidade} não encontrada no 23.01")
        
        # Ordenar as cidades
        cidades_destino.sort()
        
        # Atualizar total de cidades
        rep_data['estados']['SP']['total_cidades'] = len(cidades_destino)
        rep_data['total_cidades'] = len(cidades_destino)
    
    # Remover cidades do 23.01
    print(f"\n✓ Removendo cidades do representante 23.01:")
    cidades_restantes = []
    for cidade in cidades_23_01:
        if cidade not in cidades_movidas:
            cidades_restantes.append(cidade)
        else:
            print(f"  - Removendo: {cidade}")
    
    # Atualizar o representante 23.01
    rep_23_01['estados']['SP']['cidades'] = sorted(cidades_restantes)
    rep_23_01['estados']['SP']['total_cidades'] = len(cidades_restantes)
    rep_23_01['total_cidades'] = len(cidades_restantes)
    
    print(f"\n📊 Resumo:")
    print(f"  Cidades movidas: {len(cidades_movidas)}")
    print(f"  Cidades restantes no 23.01: {len(cidades_restantes)}")
    
    # Salvar o arquivo
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(root_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Arquivo atualizado com sucesso!")
    
    # Mostrar detalhes finais
    print(f"\n📋 Detalhes finais:")
    for codigo_destino in ['38.04', '24', '38']:
        if codigo_destino in representantes_destino:
            _, rep_data = representantes_destino[codigo_destino]
            total = rep_data['estados']['SP']['total_cidades']
            print(f"  {codigo_destino}: {total} cidades")
    print(f"  23.01: {len(cidades_restantes)} cidades")
    
    return True

if __name__ == '__main__':
    try:
        reorganizar_cidades()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
