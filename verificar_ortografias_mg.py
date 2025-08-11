#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e corrigir ortografias das cidades da Zona da Mata
comparando com o arquivo de mesorregiões
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

def normalizar_nome_cidade(nome):
    """Normaliza o nome da cidade para comparação"""
    return nome.upper().strip()

def verificar_ortografias():
    """Verifica e corrige ortografias das cidades da Zona da Mata"""
    
    print("Carregando arquivos...")
    mesorregioes = carregar_mesorregioes()
    representantes = carregar_representantes()
    
    # Obter cidades da Zona da Mata (referência)
    cidades_referencia = []
    for mesorregiao in mesorregioes:
        if mesorregiao['mesorregiao'] == 'Zona da Mata':
            cidades_referencia = mesorregiao['municipios']
            break
    
    print(f"Total de cidades de referência na Zona da Mata: {len(cidades_referencia)}")
    
    # Encontrar o representante 48.01
    representante_48_01 = None
    for key, value in representantes['representantes'].items():
        if value.get('codigo') == '48.01':
            representante_48_01 = key
            break
    
    if not representante_48_01:
        print("ERRO: Representante 48.01 não encontrado!")
        return
    
    # Obter cidades atuais do representante
    cidades_atuais = representantes['representantes'][representante_48_01]['estados']['MG']['cidades']
    print(f"Total de cidades atuais: {len(cidades_atuais)}")
    
    # Criar dicionário de referência para busca rápida
    ref_dict = {normalizar_nome_cidade(cidade): cidade for cidade in cidades_referencia}
    
    # Verificar e corrigir ortografias
    cidades_corrigidas = []
    ortografias_incorretas = []
    
    for cidade_atual in cidades_atuais:
        cidade_normalizada = normalizar_nome_cidade(cidade_atual)
        
        if cidade_normalizada in ref_dict:
            cidade_correta = ref_dict[cidade_normalizada]
            if cidade_atual != cidade_correta:
                print(f"Ortografia corrigida: '{cidade_atual}' -> '{cidade_correta}'")
                cidades_corrigidas.append(cidade_correta)
                ortografias_incorretas.append(cidade_atual)
            else:
                cidades_corrigidas.append(cidade_atual)
        else:
            print(f"AVISO: Cidade não encontrada na referência: {cidade_atual}")
            cidades_corrigidas.append(cidade_atual)
    
    # Atualizar o representante se houver correções
    if ortografias_incorretas:
        print(f"\nCorrigindo {len(ortografias_incorretas)} ortografias...")
        representantes['representantes'][representante_48_01]['estados']['MG']['cidades'] = cidades_corrigidas
        salvar_representantes(representantes)
        
        print("\n=== RESUMO DAS CORREÇÕES ===")
        print(f"Representante: {representante_48_01}")
        print(f"Código: 48.01")
        print(f"Ortografias corrigidas: {len(ortografias_incorretas)}")
        
        print("\nOrtografias corrigidas:")
        for i, cidade_incorreta in enumerate(ortografias_incorretas):
            cidade_correta = cidades_corrigidas[cidades_atuais.index(cidade_incorreta)]
            print(f"  - '{cidade_incorreta}' -> '{cidade_correta}'")
        
        print("\nCorreções concluídas com sucesso!")
    else:
        print("\nNenhuma ortografia incorreta encontrada. Todas as cidades estão corretas!")

if __name__ == "__main__":
    verificar_ortografias()
