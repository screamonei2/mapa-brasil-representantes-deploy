#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar um arquivo geojs básico com as coordenadas aproximadas
das mesorregiões de São Paulo para visualização no mapa.
"""

import json
import os

def gerar_geojs_sp():
    """Gera um arquivo geojs básico com coordenadas aproximadas das mesorregiões de SP."""
    
    # Coordenadas aproximadas das mesorregiões de SP (centro de cada região)
    coordenadas_mesorregioes = {
        "São José do Rio Preto": [-20.8126, -49.3763],
        "Ribeirão Preto": [-21.1765, -47.8208],
        "Araçatuba": [-21.2089, -50.4329],
        "Bauru": [-22.3145, -49.0606],
        "Araraquara": [-21.7945, -48.1750],
        "Piracicaba": [-22.7253, -47.6492],
        "Campinas": [-22.9064, -47.0616],
        "Presidente Prudente": [-22.1257, -51.3889],
        "Marília": [-22.2178, -49.9500],
        "Assis": [-22.6619, -50.4116],
        "Itapetininga": [-23.5886, -48.0483],
        "Macro Metropolitana Paulista": [-23.1861, -47.3022],
        "Vale do Paraíba Paulista": [-23.1861, -45.8847],
        "Litoral Sul Paulista": [-24.1125, -47.0011],
        "Metropolitana de São Paulo": [-23.5505, -46.6333]
    }
    
    # Estrutura do GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Carregar dados das mesorregiões
    with open('sp_mesorregioes.json', 'r', encoding='utf-8') as f:
        mesorregioes = json.load(f)
    
    # Gerar features para cada mesorregião
    for mesorregiao in mesorregioes:
        nome = mesorregiao["mesorregiao"]
        municipios = mesorregiao["municipios"]
        
        # Obter coordenadas aproximadas
        if nome in coordenadas_mesorregioes:
            lat, lon = coordenadas_mesorregioes[nome]
        else:
            # Coordenadas padrão (centro de SP)
            lat, lon = -23.5505, -46.6333
        
        # Criar polígono aproximado (círculo)
        feature = {
            "type": "Feature",
            "properties": {
                "nome": nome,
                "total_municipios": len(municipios),
                "municipios": municipios,
                "cor": "#FF6B6B"  # Cor padrão
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    # Círculo aproximado com raio de ~0.5 graus
                    [
                        [lon - 0.5, lat - 0.5],
                        [lon + 0.5, lat - 0.5],
                        [lon + 0.5, lat + 0.5],
                        [lon - 0.5, lat + 0.5],
                        [lon - 0.5, lat - 0.5]
                    ]
                ]
            }
        }
        
        geojson["features"].append(feature)
    
    # Salvar arquivo geojs
    with open('sp_mesorregioes.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Arquivo sp_mesorregioes.geojson gerado com {len(geojson['features'])} mesorregiões")
    print("✓ Coordenadas aproximadas definidas para visualização no mapa")
    print("✓ Arquivo pronto para ser usado no HTML")

def main():
    """Função principal."""
    print("=== GERADOR DE GEOJS PARA MESORREGIÕES DE SP ===")
    print("Objetivo: Criar arquivo geojs básico para visualização no mapa")
    print()
    
    try:
        # Verificar se o arquivo sp_mesorregioes.json existe
        if not os.path.exists('sp_mesorregioes.json'):
            print("✗ Erro: Arquivo sp_mesorregioes.json não encontrado!")
            print("   Certifique-se de que o arquivo está na pasta atual.")
            return
        
        # Gerar arquivo geojs
        gerar_geojs_sp()
        
        print("\n✓ Arquivo geojs gerado com sucesso!")
        print("✓ Agora você pode abrir sp_mesorregioes.html para visualizar no mapa")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
