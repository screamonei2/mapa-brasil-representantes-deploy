#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se o representante 26 está atendendo toda a região de Araçatuba.
Compara as cidades atendidas pelo representante 26 com as cidades da mesorregião de Araçatuba.
"""

import json
import os

def carregar_arquivos():
    """Carrega os arquivos necessários."""
    try:
        # Carregar representantes
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            representantes = json.load(f)
        
        # Carregar mesorregiões de SP
        with open('sp_mesorregioes.json', 'r', encoding='utf-8') as f:
            mesorregioes_sp = json.load(f)
        
        return representantes, mesorregioes_sp
    except Exception as e:
        print(f"❌ Erro ao carregar arquivos: {e}")
        return None, None

def encontrar_representante_26(representantes):
    """Encontra o representante com código 26."""
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            return nome, dados
    return None, None

def obter_cidades_aracatuba(mesorregioes_sp):
    """Obtém todas as cidades da mesorregião de Araçatuba."""
    for mesorregiao in mesorregioes_sp:
        if mesorregiao["mesorregiao"] == "Araçatuba":
            return [cidade.upper() for cidade in mesorregiao["municipios"]]
    return []

def normalizar_nome_cidade(cidade):
    """Normaliza o nome da cidade para comparação."""
    return cidade.upper().strip()

def verificar_cobertura_aracatuba(representante_26, cidades_aracatuba):
    """Verifica se o representante 26 cobre toda a região de Araçatuba."""
    if not representante_26 or not cidades_aracatuba:
        return None
    
    # Obter cidades atendidas pelo representante 26
    cidades_representante = set()
    if "estados" in representante_26 and "SP" in representante_26["estados"]:
        cidades_sp = representante_26["estados"]["SP"].get("cidades", [])
        cidades_representante = {normalizar_nome_cidade(cidade) for cidade in cidades_sp}
    
    # Normalizar cidades de Araçatuba
    cidades_aracatuba_normalizadas = {normalizar_nome_cidade(cidade) for cidade in cidades_aracatuba}
    
    # Verificar cobertura
    cidades_cobertas = cidades_aracatuba_normalizadas.intersection(cidades_representante)
    cidades_nao_cobertas = cidades_aracatuba_normalizadas - cidades_representante
    cidades_extras = cidades_representante - cidades_aracatuba_normalizadas
    
    return {
        "total_aracatuba": len(cidades_aracatuba_normalizadas),
        "total_cobertas": len(cidades_cobertas),
        "total_nao_cobertas": len(cidades_nao_cobertas),
        "total_extras": len(cidades_extras),
        "cidades_cobertas": sorted(list(cidades_cobertas)),
        "cidades_nao_cobertas": sorted(list(cidades_nao_cobertas)),
        "cidades_extras": sorted(list(cidades_extras)),
        "percentual_cobertura": (len(cidades_cobertas) / len(cidades_aracatuba_normalizadas)) * 100 if cidades_aracatuba_normalizadas else 0
    }

def gerar_relatorio(representante_26, resultado_verificacao):
    """Gera um relatório detalhado da verificação."""
    print("=" * 80)
    print("🔍 VERIFICAÇÃO: REPRESENTANTE 26 E REGIÃO DE ARAÇATUBA")
    print("=" * 80)
    
    if representante_26:
        print(f"\n📋 REPRESENTANTE 26:")
        print(f"   Nome: {representante_26['nome']}")
        print(f"   Código: {representante_26['codigo']}")
        print(f"   Contato: {representante_26['contato']['nome_contato']}")
        print(f"   Email: {representante_26['contato']['email']}")
        print(f"   Celular: {representante_26['contato']['celular']}")
        print(f"   Total de cidades em SP: {representante_26['estados']['SP']['total_cidades']}")
        
        if 'mesorregioes' in representante_26['estados']['SP']:
            print(f"   Mesorregiões: {', '.join(representante_26['estados']['SP']['mesorregioes'])}")
    
    if resultado_verificacao:
        print(f"\n🎯 COBERTURA DA REGIÃO DE ARAÇATUBA:")
        print(f"   Total de cidades em Araçatuba: {resultado_verificacao['total_aracatuba']}")
        print(f"   Cidades cobertas: {resultado_verificacao['total_cobertas']}")
        print(f"   Cidades NÃO cobertas: {resultado_verificacao['total_nao_cobertas']}")
        print(f"   Cidades extras (não de Araçatuba): {resultado_verificacao['total_extras']}")
        print(f"   Percentual de cobertura: {resultado_verificacao['percentual_cobertura']:.1f}%")
        
        if resultado_verificacao['cidades_nao_cobertas']:
            print(f"\n❌ CIDADES DE ARAÇATUBA NÃO COBERTAS:")
            for cidade in resultado_verificacao['cidades_nao_cobertas']:
                print(f"   • {cidade}")
        
        if resultado_verificacao['cidades_cobertas']:
            print(f"\n✅ CIDADES DE ARAÇATUBA COBERTAS:")
            for cidade in resultado_verificacao['cidades_cobertas']:
                print(f"   • {cidade}")
        
        # Conclusão
        print(f"\n📊 CONCLUSÃO:")
        if resultado_verificacao['percentual_cobertura'] == 100:
            print("   🎉 O representante 26 está atendendo TODA a região de Araçatuba!")
        elif resultado_verificacao['percentual_cobertura'] >= 80:
            print("   🟡 O representante 26 está atendendo a MAIORIA da região de Araçatuba.")
        else:
            print("   🔴 O representante 26 NÃO está atendendo adequadamente a região de Araçatuba.")
        
        print(f"   Cobertura atual: {resultado_verificacao['percentual_cobertura']:.1f}%")

def main():
    """Função principal."""
    print("🔍 Iniciando verificação da cobertura do representante 26 na região de Araçatuba...")
    
    # Carregar arquivos
    representantes, mesorregioes_sp = carregar_arquivos()
    if not representantes or not mesorregioes_sp:
        return
    
    # Encontrar representante 26
    nome_rep, representante_26 = encontrar_representante_26(representantes)
    if not representante_26:
        print("❌ Representante 26 não encontrado!")
        return
    
    # Obter cidades de Araçatuba
    cidades_aracatuba = obter_cidades_aracatuba(mesorregioes_sp)
    if not cidades_aracatuba:
        print("❌ Mesorregião de Araçatuba não encontrada!")
        return
    
    # Verificar cobertura
    resultado = verificar_cobertura_aracatuba(representante_26, cidades_aracatuba)
    
    # Gerar relatório
    gerar_relatorio(representante_26, resultado)

if __name__ == "__main__":
    main()
