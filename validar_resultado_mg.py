#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar o resultado final da atualização do representante 48.01
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

def normalizar_nome_cidade(nome):
    """Normaliza o nome da cidade para comparação"""
    return nome.upper().strip()

def validar_resultado():
    """Valida o resultado final da atualização"""
    
    print("=== VALIDAÇÃO DO RESULTADO FINAL ===\n")
    
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
    total_cidades = representantes['representantes'][representante_48_01]['estados']['MG']['total_cidades']
    total_geral = representantes['representantes'][representante_48_01]['total_cidades']
    
    print(f"Representante: {representante_48_01}")
    print(f"Código: 48.01")
    print(f"Total de cidades atuais: {len(cidades_atuais)}")
    print(f"Total registrado no estado: {total_cidades}")
    print(f"Total geral registrado: {total_geral}")
    
    # Verificar consistência dos totais
    if len(cidades_atuais) == total_cidades == total_geral:
        print("✓ Totais consistentes")
    else:
        print("✗ ERRO: Totais inconsistentes!")
        return
    
    # Criar dicionário de referência para busca rápida
    ref_dict = {normalizar_nome_cidade(cidade): cidade for cidade in cidades_referencia}
    
    # Verificar se todas as cidades estão na Zona da Mata
    cidades_fora_zona = []
    cidades_na_zona = []
    
    for cidade_atual in cidades_atuais:
        cidade_normalizada = normalizar_nome_cidade(cidade_atual)
        if cidade_normalizada in ref_dict:
            cidades_na_zona.append(cidade_atual)
        else:
            cidades_fora_zona.append(cidade_atual)
    
    print(f"\nCidades na Zona da Mata: {len(cidades_na_zona)}")
    print(f"Cidades fora da Zona da Mata: {len(cidades_fora_zona)}")
    
    if cidades_fora_zona:
        print("\n✗ ERRO: Cidades fora da Zona da Mata encontradas:")
        for cidade in sorted(cidades_fora_zona):
            print(f"  - {cidade}")
        return
    else:
        print("✓ Todas as cidades estão na Zona da Mata")
    
    # Verificar se todas as cidades da Zona da Mata estão cobertas
    cidades_cobertas = set(normalizar_nome_cidade(cidade) for cidade in cidades_atuais)
    cidades_referencia_normalizadas = set(normalizar_nome_cidade(cidade) for cidade in cidades_referencia)
    
    cidades_nao_cobertas = cidades_referencia_normalizadas - cidades_cobertas
    
    if cidades_nao_cobertas:
        print(f"\n⚠️  AVISO: {len(cidades_nao_cobertas)} cidades da Zona da Mata não estão cobertas:")
        for cidade_norm in sorted(cidades_nao_cobertas):
            # Encontrar o nome original
            for cidade_orig in cidades_referencia:
                if normalizar_nome_cidade(cidade_orig) == cidade_norm:
                    print(f"  - {cidade_orig}")
                    break
    else:
        print("✓ Todas as cidades da Zona da Mata estão cobertas")
    
    # Verificar ortografias
    ortografias_incorretas = []
    for cidade_atual in cidades_atuais:
        cidade_normalizada = normalizar_nome_cidade(cidade_atual)
        if cidade_normalizada in ref_dict:
            cidade_correta = ref_dict[cidade_normalizada]
            if cidade_atual != cidade_correta:
                ortografias_incorretas.append((cidade_atual, cidade_correta))
    
    if ortografias_incorretas:
        print(f"\n✗ ERRO: {len(ortografias_incorretas)} ortografias incorretas encontradas:")
        for cidade_incorreta, cidade_correta in ortografias_incorretas:
            print(f"  - '{cidade_incorreta}' -> '{cidade_correta}'")
        return
    else:
        print("✓ Todas as ortografias estão corretas")
    
    print("\n=== VALIDAÇÃO CONCLUÍDA ===")
    print("✓ Representante 48.01 está configurado corretamente!")
    print("✓ Atende apenas cidades da Zona da Mata de MG")
    print("✓ Ortografias estão corretas")
    print("✓ Totais estão consistentes")

if __name__ == "__main__":
    validar_resultado()
