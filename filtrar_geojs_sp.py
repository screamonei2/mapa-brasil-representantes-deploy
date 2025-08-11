#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para filtrar apenas os municípios de São Paulo do arquivo geojs
e criar um arquivo otimizado para visualização das mesorregiões.
"""

import json
import os

def filtrar_municipios_sp():
    """Filtra apenas os municípios de SP do arquivo geojs."""
    
    # Carregar dados das mesorregiões de SP
    with open('sp_mesorregioes.json', 'r', encoding='utf-8') as f:
        mesorregioes_sp = json.load(f)
    
    # Criar conjunto de todos os municípios de SP
    municipios_sp = set()
    for mesorregiao in mesorregioes_sp:
        for municipio in mesorregiao["municipios"]:
            municipios_sp.add(municipio.upper())
    
    print(f"✓ Total de municípios em SP: {len(municipios_sp)}")
    
    # Carregar arquivo geojs original
    with open('geojs-100-mun-v2.json', 'r', encoding='utf-8') as f:
        geojs_original = json.load(f)
    
    print(f"✓ Total de features no geojs original: {len(geojs_original['features'])}")
    
    # Filtrar apenas municípios de SP
    features_sp = []
    municipios_encontrados = set()
    
    for feature in geojs_original["features"]:
        nome_municipio = feature["properties"]["name"].upper()
        
        # Verificar se o município está em SP
        if nome_municipio in municipios_sp:
            # Adicionar informações da mesorregião
            mesorregiao_encontrada = None
            for mesorregiao in mesorregioes_sp:
                if nome_municipio in [m.upper() for m in mesorregiao["municipios"]]:
                    mesorregiao_encontrada = mesorregiao
                    break
            
            if mesorregiao_encontrada:
                # Criar nova feature com informações da mesorregião
                nova_feature = {
                    "type": "Feature",
                    "properties": {
                        "id": feature["properties"]["id"],
                        "name": feature["properties"]["name"],
                        "mesorregiao": mesorregiao_encontrada["mesorregiao"],
                        "total_municipios_mesorregiao": len(mesorregiao_encontrada["municipios"]),
                        "municipios_mesorregiao": mesorregiao_encontrada["municipios"]
                    },
                    "geometry": feature["geometry"]
                }
                
                features_sp.append(nova_feature)
                municipios_encontrados.add(nome_municipio)
    
    print(f"✓ Municípios de SP encontrados no geojs: {len(municipios_encontrados)}")
    
    # Verificar municípios não encontrados
    municipios_nao_encontrados = municipios_sp - municipios_encontrados
    if municipios_nao_encontrados:
        print(f"⚠️  Municípios não encontrados no geojs ({len(municipios_nao_encontrados)}):")
        for municipio in sorted(list(municipios_nao_encontrados))[:10]:  # Mostrar apenas os primeiros 10
            print(f"   - {municipio}")
        if len(municipios_nao_encontrados) > 10:
            print(f"   ... e mais {len(municipios_nao_encontrados) - 10} municípios")
    
    # Criar novo arquivo geojs filtrado
    geojs_sp = {
        "type": "FeatureCollection",
        "features": features_sp
    }
    
    # Salvar arquivo filtrado
    with open('sp_mesorregioes_filtrado.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojs_sp, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Arquivo sp_mesorregioes_filtrado.geojson criado com {len(features_sp)} features")
    
    # Criar arquivo de resumo
    resumo = {
        "total_mesorregioes": len(mesorregioes_sp),
        "total_municipios_sp": len(municipios_sp),
        "municipios_encontrados_geojs": len(municipios_encontrados),
        "municipios_nao_encontrados": len(municipios_nao_encontrados),
        "mesorregioes": []
    }
    
    for mesorregiao in mesorregioes_sp:
        municipios_encontrados_regiao = [
            m for m in mesorregiao["municipios"] 
            if m.upper() in municipios_encontrados
        ]
        
        resumo["mesorregioes"].append({
            "nome": mesorregiao["mesorregiao"],
            "total_municipios": len(mesorregiao["municipios"]),
            "municipios_encontrados": len(municipios_encontrados_regiao),
            "municipios_nao_encontrados": len(mesorregiao["municipios"]) - len(municipios_encontrados_regiao)
        })
    
    with open('resumo_filtragem_sp.json', 'w', encoding='utf-8') as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)
    
    print("✓ Arquivo resumo_filtragem_sp.json criado com estatísticas detalhadas")
    
    return resumo

def main():
    """Função principal."""
    print("=== FILTRADOR DE GEOJS PARA MUNICÍPIOS DE SP ===")
    print("Objetivo: Filtrar apenas municípios de SP do arquivo geojs original")
    print()
    
    try:
        # Verificar se os arquivos necessários existem
        if not os.path.exists('sp_mesorregioes.json'):
            print("✗ Erro: Arquivo sp_mesorregioes.json não encontrado!")
            return
        
        if not os.path.exists('geojs-100-mun-v2.json'):
            print("✗ Erro: Arquivo geojs-100-mun-v2.json não encontrado!")
            return
        
        # Filtrar municípios
        resumo = filtrar_municipios_sp()
        
        print("\n=== RESUMO DA FILTRAGEM ===")
        print(f"✓ Total de mesorregiões: {resumo['total_mesorregioes']}")
        print(f"✓ Total de municípios em SP: {resumo['total_municipios_sp']}")
        print(f"✓ Municípios encontrados no geojs: {resumo['municipios_encontrados_geojs']}")
        print(f"✓ Municípios não encontrados: {resumo['municipios_nao_encontrados']}")
        
        print("\n✓ Filtragem concluída com sucesso!")
        print("✓ Arquivo sp_mesorregioes_filtrado.geojson pronto para uso no HTML")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
