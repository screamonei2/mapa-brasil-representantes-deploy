#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se as cidades das mesorregiões Noroeste, Alto Parnaíba e Triângulo
estão sendo atendidas APENAS pelo representante 48.0
"""

import json

def carregar_mesorregioes():
    """Carrega o arquivo de mesorregiões de MG"""
    with open('mesorregioes_mg.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_representantes():
    """Carrega o arquivo de representantes"""
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_representantes(data):
    """Salva o arquivo de representantes atualizado"""
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def obter_cidades_mesorregioes_alvo():
    """Retorna as cidades das mesorregiões que devem pertencer APENAS ao 48.0"""
    mesorregioes = carregar_mesorregioes()
    
    cidades_alvo = []
    mesorregioes_alvo = ["Noroeste de Minas", "Triângulo Mineiro/Alto Paranaíba"]
    
    for mesorregiao in mesorregioes:
        if mesorregiao['mesorregiao'] in mesorregioes_alvo:
            cidades_alvo.extend(mesorregiao['municipios'])
            print(f"  {mesorregiao['mesorregiao']}: {len(mesorregiao['municipios'])} cidades")
    
    return cidades_alvo

def verificar_e_corrigir_cidades():
    """Verifica e corrige as cidades das mesorregiões alvo"""
    
    print("=== VERIFICAÇÃO E CORREÇÃO DE CIDADES ===")
    print("Objetivo: Garantir que cidades de Noroeste, Alto Parnaíba e Triângulo")
    print("pertençam APENAS ao representante 48.0\n")
    
    print("Carregando arquivos...")
    representantes = carregar_representantes()
    
    # Obter cidades das mesorregiões alvo
    print("Cidades das mesorregiões alvo:")
    cidades_alvo = obter_cidades_mesorregioes_alvo()
    cidades_alvo_normalizadas = [cidade.upper().strip() for cidade in cidades_alvo]
    
    print(f"\nTotal de cidades alvo: {len(cidades_alvo)}")
    
    # Encontrar representante 48.0
    representante_48_0 = None
    for key, value in representantes['representantes'].items():
        if value.get('codigo') == '48.0':
            representante_48_0 = key
            break
    
    if not representante_48_0:
        print("❌ Representante 48.0 não encontrado!")
        return
    
    print(f"\nRepresentante 48.0 encontrado: {representante_48_0}")
    
    # Verificar se o representante 48.0 tem todas as cidades alvo
    cidades_48_0 = representantes['representantes'][representante_48_0]['estados']['MG']['cidades']
    cidades_48_0_normalizadas = [cidade.upper().strip() for cidade in cidades_48_0]
    
    cidades_faltando_48_0 = []
    for cidade_alvo in cidades_alvo:
        if cidade_alvo.upper().strip() not in cidades_48_0_normalizadas:
            cidades_faltando_48_0.append(cidade_alvo)
    
    if cidades_faltando_48_0:
        print(f"\n⚠️  {len(cidades_faltando_48_0)} cidades alvo não estão no representante 48.0:")
        for cidade in cidades_faltando_48_0:
            print(f"  - {cidade}")
        
        # Adicionar cidades faltantes ao 48.0
        print(f"\nAdicionando cidades faltantes ao representante 48.0...")
        cidades_48_0.extend(cidades_faltando_48_0)
        cidades_48_0 = sorted(list(set(cidades_48_0)))  # Remover duplicatas e ordenar
        
        representantes['representantes'][representante_48_0]['estados']['MG']['cidades'] = cidades_48_0
        representantes['representantes'][representante_48_0]['estados']['MG']['total_cidades'] = len(cidades_48_0)
        representantes['representantes'][representante_48_0]['total_cidades'] = len(cidades_48_0)
        
        print(f"✅ Representante 48.0 atualizado com {len(cidades_48_0)} cidades")
    else:
        print("✅ Representante 48.0 já tem todas as cidades alvo")
    
    # Verificar outros representantes que possam ter essas cidades
    print(f"\n=== VERIFICANDO OUTROS REPRESENTANTES ===")
    representantes_com_cidades_alvo = []
    
    for key, value in representantes['representantes'].items():
        if key == representante_48_0:
            continue  # Pular o próprio 48.0
        
        if 'MG' in value.get('estados', {}):
            cidades_rep = value['estados']['MG']['cidades']
            cidades_rep_normalizadas = [cidade.upper().strip() for cidade in cidades_rep]
            
            cidades_em_comum = []
            for cidade_alvo in cidades_alvo:
                if cidade_alvo.upper().strip() in cidades_rep_normalizadas:
                    cidades_em_comum.append(cidade_alvo)
            
            if cidades_em_comum:
                representantes_com_cidades_alvo.append({
                    'key': key,
                    'codigo': value.get('codigo'),
                    'nome': value.get('nome'),
                    'cidades_em_comum': cidades_em_comum
                })
    
    if representantes_com_cidades_alvo:
        print(f"\n⚠️  {len(representantes_com_cidades_alvo)} representantes têm cidades alvo:")
        for rep in representantes_com_cidades_alvo:
            print(f"\n  {rep['codigo']} - {rep['nome']}")
            print(f"  Cidades em comum: {len(rep['cidades_em_comum'])}")
            for cidade in rep['cidades_em_comum']:
                print(f"    - {cidade}")
        
        # Remover cidades alvo dos outros representantes
        print(f"\nRemovendo cidades alvo dos outros representantes...")
        for rep_info in representantes_com_cidades_alvo:
            key = rep_info['key']
            cidades_atuais = representantes['representantes'][key]['estados']['MG']['cidades']
            cidades_atuais_normalizadas = [cidade.upper().strip() for cidade in cidades_atuais]
            
            # Remover cidades alvo
            cidades_filtradas = []
            for cidade in cidades_atuais:
                if cidade.upper().strip() not in cidades_alvo_normalizadas:
                    cidades_filtradas.append(cidade)
            
            representantes['representantes'][key]['estados']['MG']['cidades'] = cidades_filtradas
            representantes['representantes'][key]['estados']['MG']['total_cidades'] = len(cidades_filtradas)
            representantes['representantes'][key]['total_cidades'] = len(cidades_filtradas)
            
            print(f"✅ {rep_info['codigo']} - {len(cidades_atuais)} → {len(cidades_filtradas)} cidades")
    else:
        print("✅ Nenhum outro representante tem cidades alvo")
    
    # Salvar arquivo atualizado
    print(f"\nSalvando arquivo atualizado...")
    salvar_representantes(representantes)
    
    print(f"\n=== VERIFICAÇÃO CONCLUÍDA ===")
    print("✅ Todas as cidades de Noroeste, Alto Parnaíba e Triângulo")
    print("   agora pertencem APENAS ao representante 48.0!")

if __name__ == "__main__":
    verificar_e_corrigir_cidades()
