#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar se o representante 33 está sendo processado corretamente
"""

import json

def testar_mapa_representante_33():
    """
    Testa se o representante 33 está sendo processado corretamente para o mapa
    """
    try:
        # Carrega o JSON
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON carregado com sucesso")
        
        # Simula exatamente o que o JavaScript faria
        print("\n🔄 Simulando processamento do JavaScript...")
        
        # Verifica se existe a propriedade 'representantes'
        dadosRepresentantes = data.get('representantes', data)
        
        # Mapeamento de estados (igual ao JavaScript)
        stateToAbbrev = {
            'SAO PAULO': 'SP', 'RIO DE JANEIRO': 'RJ', 'MINAS GERAIS': 'MG', 'BAHIA': 'BA',
            'PARANA': 'PR', 'RIO GRANDE DO SUL': 'RS', 'PERNAMBUCO': 'PE', 'CEARA': 'CE',
            'PARA': 'PA', 'SANTA CATARINA': 'SC', 'GOIAS': 'GO', 'MARANHAO': 'MA',
            'PARAIBA': 'PB', 'AMAZONAS': 'AM', 'ESPIRITO SANTO': 'ES', 'MATO GROSSO': 'MT',
            'ALAGOAS': 'AL', 'PIAUI': 'PI', 'DISTRITO FEDERAL': 'DF', 'MATO GROSSO DO SUL': 'MS',
            'SERGIPE': 'SE', 'RIO GRANDE DO NORTE': 'RN', 'RONDONIA': 'RO', 'ACRE': 'AC',
            'AMAPA': 'AP', 'RORAIMA': 'RR', 'TOCANTINS': 'TO'
        }
        
        representativesMap = {}
        locationMap = {}
        municipioRepresentativeMap = {}
        
        for nomeEmpresa, dadosEmpresa in dadosRepresentantes.items():
            codigo = dadosEmpresa.get('codigo', 'N/A')
            nome = dadosEmpresa.get('nome', nomeEmpresa)
            
            # Estados é um objeto, não um array
            estados = dadosEmpresa.get('estados', {})
            
            # Coletar todas as cidades de todos os estados
            todasCidades = []
            todosEstados = []
            
            for estado, dadosEstado in estados.items():
                todosEstados.append(estado)
                if dadosEstado.get('cidades') and isinstance(dadosEstado['cidades'], list):
                    todasCidades.extend(dadosEstado['cidades'])
            
            # Determinar estado principal
            estadoPrincipal = todosEstados[0].strip() if todosEstados else 'DESCONHECIDO'
            siglaEstado = stateToAbbrev.get(estadoPrincipal, estadoPrincipal[:2])
            
            representante = {
                'id': f"{nomeEmpresa}_{codigo}",
                'NomeRepresentante': nome,
                'SiglaEstado': siglaEstado,
                'Estado': estadoPrincipal,
                'CidadesAtendidas': todasCidades,
                'CodigoRepresentante': codigo,
                'EstadosDetalhados': estados
            }
            
            representativesMap[representante['id']] = representante
            
            # Indexar por estado
            for estado in todosEstados:
                sigla = stateToAbbrev.get(estado, estado[:2])
                for key in [estado, sigla]:
                    if key not in locationMap:
                        locationMap[key] = set()
                    locationMap[key].add(representante['id'])
            
            # Indexar por cada cidade
            for estado, dadosEstado in estados.items():
                if dadosEstado.get('cidades') and isinstance(dadosEstado['cidades'], list):
                    for cidade in dadosEstado['cidades']:
                        if cidade not in locationMap:
                            locationMap[cidade] = set()
                        locationMap[cidade].add(representante['id'])
                        
                        # Mapear município+estado para representante
                        cidadeEstadoKey = f"{cidade}-{estado}"
                        if cidadeEstadoKey not in municipioRepresentativeMap:
                            municipioRepresentativeMap[cidadeEstadoKey] = []
                        municipioRepresentativeMap[cidadeEstadoKey].append(representante)
                        
                        # Também manter o mapeamento apenas por cidade
                        if cidade not in municipioRepresentativeMap:
                            municipioRepresentativeMap[cidade] = []
                        municipioRepresentativeMap[cidade].append(representante)
            
            # Verificar especificamente o representante 33
            if codigo == "33":
                print(f"\n🎯 REPRESENTANTE 33 PROCESSADO:")
                print(f"   - ID: {representante['id']}")
                print(f"   - Nome: {representante['NomeRepresentante']}")
                print(f"   - Estado: {representante['Estado']}")
                print(f"   - Sigla: {representante['SiglaEstado']}")
                print(f"   - Total de cidades: {len(representante['CidadesAtendidas'])}")
                
                # Verifica se está indexado por estado
                if 'MT' in locationMap:
                    print(f"✅ Estado MT indexado com {len(locationMap['MT'])} representantes")
                    if representante['id'] in locationMap['MT']:
                        print(f"✅ Representante 33 está indexado por estado MT")
                    else:
                        print(f"❌ Representante 33 NÃO está indexado por estado MT")
                else:
                    print(f"❌ Estado MT não encontrado no locationMap")
                
                # Verifica algumas cidades específicas
                cidades_teste = ['CUIABA', 'VARZEA GRANDE', 'RONDONOPOLIS']
                for cidade_teste in cidades_teste:
                    if cidade_teste in locationMap:
                        print(f"✅ Cidade {cidade_teste} indexada com {len(locationMap[cidade_teste])} representantes")
                        if representante['id'] in locationMap[cidade_teste]:
                            print(f"✅ Representante 33 está indexado por cidade {cidade_teste}")
                        else:
                            print(f"❌ Representante 33 NÃO está indexado por cidade {cidade_teste}")
                    else:
                        print(f"❌ Cidade {cidade_teste} não encontrada no locationMap")
        
        print(f"\n✅ Processamento concluído:")
        print(f"📊 Total de representantes: {len(representativesMap)}")
        print(f"📊 Total de localizações: {len(locationMap)}")
        print(f"📊 Total de mapeamentos município-representante: {len(municipioRepresentativeMap)}")
        
        # Verifica se o representante 33 está em representativesMap
        rep_33_encontrado = False
        for rep_id, rep in representativesMap.items():
            if rep['CodigoRepresentante'] == "33":
                rep_33_encontrado = True
                print(f"✅ Representante 33 encontrado em representativesMap com ID: {rep_id}")
                break
        
        if not rep_33_encontrado:
            print(f"❌ Representante 33 NÃO encontrado em representativesMap")
        
        # Verifica se há algum problema específico com o estado MT
        if 'MT' in locationMap:
            print(f"\n📍 Estado MT no locationMap:")
            print(f"   - Total de representantes: {len(locationMap['MT'])}")
            print(f"   - IDs dos representantes: {list(locationMap['MT'])}")
        else:
            print(f"\n❌ Estado MT NÃO encontrado no locationMap")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_mapa_representante_33()
