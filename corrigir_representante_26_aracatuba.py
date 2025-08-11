#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o representante 26 para cobrir TODA a região de Araçatuba.
Adiciona as cidades faltantes e corrige as mesorregiões.
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

def obter_cidades_aracatuba(mesorregioes_sp):
    """Obtém todas as cidades da mesorregião de Araçatuba."""
    for mesorregiao in mesorregioes_sp:
        if mesorregiao["mesorregiao"] == "Araçatuba":
            return [cidade.upper() for cidade in mesorregiao["municipios"]]
    return []

def corrigir_representante_26(representantes, cidades_aracatuba):
    """Corrige o representante 26 para cobrir toda a região de Araçatuba."""
    
    # Encontrar representante 26
    rep_26 = None
    nome_rep = None
    
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            rep_26 = dados
            nome_rep = nome
            break
    
    if not rep_26:
        print("❌ Representante 26 não encontrado!")
        return None
    
    print(f"✅ Representante 26 encontrado: {rep_26['nome']}")
    
    # Obter cidades atuais do representante 26
    cidades_atuais = set()
    if "estados" in rep_26 and "SP" in rep_26["estados"]:
        cidades_sp = rep_26["estados"]["SP"].get("cidades", [])
        cidades_atuais = {cidade.upper() for cidade in cidades_sp}
    
    # Verificar quais cidades de Araçatuba já estão cobertas
    cidades_aracatuba_set = set(cidades_aracatuba)
    cidades_ja_cobertas = cidades_aracatuba_set.intersection(cidades_atuais)
    cidades_faltantes = cidades_aracatuba_set - cidades_atuais
    
    print(f"\n📊 ANÁLISE ATUAL:")
    print(f"   Cidades de Araçatuba já cobertas: {len(cidades_ja_cobertas)}")
    print(f"   Cidades de Araçatuba faltantes: {len(cidades_faltantes)}")
    
    if cidades_faltantes:
        print(f"\n➕ ADICIONANDO CIDADES FALTANTES:")
        for cidade in sorted(cidades_faltantes):
            print(f"   • {cidade}")
        
        # Adicionar cidades faltantes
        if "estados" not in rep_26:
            rep_26["estados"] = {}
        if "SP" not in rep_26["estados"]:
            rep_26["estados"]["SP"] = {"cidades": []}
        
        # Adicionar apenas as cidades que não estão duplicadas
        for cidade in cidades_faltantes:
            if cidade not in rep_26["estados"]["SP"]["cidades"]:
                rep_26["estados"]["SP"]["cidades"].append(cidade)
        
        # Atualizar total de cidades
        rep_26["estados"]["SP"]["total_cidades"] = len(rep_26["estados"]["SP"]["cidades"])
        rep_26["total_cidades"] = rep_26["estados"]["SP"]["total_cidades"]
        
        # Corrigir mesorregiões
        rep_26["estados"]["SP"]["mesorregioes"] = ["Araçatuba"]
        rep_26["estados"]["SP"]["total_mesorregioes"] = 1
        
        print(f"\n✅ CIDADES ADICIONADAS COM SUCESSO!")
        print(f"   Total de cidades atualizado: {rep_26['total_cidades']}")
        print(f"   Mesorregiões corrigidas: {rep_26['estados']['SP']['mesorregioes']}")
    else:
        print(f"\n✅ Todas as cidades de Araçatuba já estão cobertas!")
    
    return representantes

def verificar_resultado(representantes, cidades_aracatuba):
    """Verifica se a correção foi bem-sucedida."""
    
    # Encontrar representante 26
    rep_26 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            rep_26 = dados
            break
    
    if not rep_26:
        return None
    
    # Obter cidades após correção
    cidades_apos_correcao = set()
    if "estados" in rep_26 and "SP" in rep_26["estados"]:
        cidades_sp = rep_26["estados"]["SP"].get("cidades", [])
        cidades_apos_correcao = {cidade.upper() for cidade in cidades_sp}
    
    # Verificar cobertura
    cidades_aracatuba_set = set(cidades_aracatuba)
    cidades_cobertas = cidades_aracatuba_set.intersection(cidades_apos_correcao)
    cidades_nao_cobertas = cidades_aracatuba_set - cidades_apos_correcao
    
    return {
        "total_aracatuba": len(cidades_aracatuba_set),
        "total_cobertas": len(cidades_cobertas),
        "total_nao_cobertas": len(cidades_nao_cobertas),
        "percentual_cobertura": (len(cidades_cobertas) / len(cidades_aracatuba_set)) * 100 if cidades_aracatuba_set else 0,
        "cidades_nao_cobertas": sorted(list(cidades_nao_cobertas))
    }

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_representante_26_aracatuba.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("✅ Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("🔧 CORRIGINDO REPRESENTANTE 26 PARA COBRIR TODA A REGIÃO DE ARAÇATUBA")
    print("=" * 80)
    
    # Carregar arquivos
    representantes, mesorregioes_sp = carregar_arquivos()
    if not representantes or not mesorregioes_sp:
        return
    
    # Obter cidades de Araçatuba
    cidades_aracatuba = obter_cidades_aracatuba(mesorregioes_sp)
    if not cidades_aracatuba:
        print("❌ Mesorregião de Araçatuba não encontrada!")
        return
    
    print(f"📍 Região de Araçatuba: {len(cidades_aracatuba)} cidades")
    
    # Corrigir representante 26
    representantes_corrigidos = corrigir_representante_26(representantes, cidades_aracatuba)
    if not representantes_corrigidos:
        return
    
    # Verificar resultado
    resultado = verificar_resultado(representantes_corrigidos, cidades_aracatuba)
    
    if resultado:
        print(f"\n📊 RESULTADO APÓS CORREÇÃO:")
        print(f"   Total de cidades em Araçatuba: {resultado['total_aracatuba']}")
        print(f"   Cidades cobertas: {resultado['total_cobertas']}")
        print(f"   Cidades NÃO cobertas: {resultado['total_nao_cobertas']}")
        print(f"   Percentual de cobertura: {resultado['percentual_cobertura']:.1f}%")
        
        if resultado['cidades_nao_cobertas']:
            print(f"\n❌ AINDA HÁ CIDADES NÃO COBERTAS:")
            for cidade in resultado['cidades_nao_cobertas']:
                print(f"   • {cidade}")
        else:
            print(f"\n🎉 SUCESSO! TODAS as cidades de Araçatuba estão cobertas!")
        
        # Salvar arquivo
        salvar_arquivo(representantes_corrigidos)
        
        print(f"\n✅ CORREÇÃO CONCLUÍDA!")
        print(f"   O representante 26 agora cobre {resultado['percentual_cobertura']:.1f}% da região de Araçatuba")

if __name__ == "__main__":
    main()
