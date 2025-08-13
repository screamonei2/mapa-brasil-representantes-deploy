#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar quais cidades estão faltando no representante 33
"""

def verificar_cidades_faltando():
    """
    Verifica quais cidades estão faltando no representante 33
    """
    
    # Lista completa de cidades do Mato Grosso (extraída do geojs-100)
    cidades_completas = [
        "ACORIZAL",
        "AGUA BOA",
        "ALTA FLORESTA",
        "ALTO ARAGUAIA",
        "ALTO BOA VISTA",
        "ALTO GARCAS",
        "ALTO PARAGUAI",
        "ALTO TAQUARI",
        "APIACAS",
        "ARAGUAIANA",
        "ARAGUAINHA",
        "ARAPUTANGA",
        "ARENAPOLIS",
        "ARIPUANA",
        "BARAO DE MELGACO",
        "BARRA DO BUGRES",
        "BARRA DO GARCAS",
        "BOM JESUS DO ARAGUAIA",
        "BRASNORTE",
        "CACERES",
        "CAMPINAPOLIS",
        "CAMPO NOVO DO PARECIS",
        "CAMPO VERDE",
        "CAMPOS DE JULIO",
        "CANABRAVA DO NORTE",
        "CANARANA",
        "CARLINDA",
        "CASTANHEIRA",
        "CHAPADA DOS GUIMARAES",
        "CLAUDIA",
        "COCALINHO",
        "COLIDER",
        "COLNIZA",
        "COMODORO",
        "CONFRESA",
        "CONQUISTA DOESTE",
        "COTRIGUACU",
        "CUIABA",
        "CURVELANDIA",
        "DENISE",
        "DIAMANTINO",
        "DOM AQUINO",
        "FELIZ NATAL",
        "FIGUEIROPOLIS DOESTE",
        "GAUCHA DO NORTE",
        "GENERAL CARNEIRO",
        "GLORIA DOESTE",
        "GUARANTA DO NORTE",
        "GUIRATINGA",
        "INDIAVAI",
        "IPIRANGA DO NORTE",
        "ITANHANGA",
        "ITAUBA",
        "ITIQUIRA",
        "JACIARA",
        "JANGADA",
        "JAURU",
        "JUARA",
        "JUINA",
        "JURUENA",
        "JUSCIMEIRA",
        "LAMBARI DOESTE",
        "LUCAS DO RIO VERDE",
        "LUCIARA",
        "VILA BELA DA SANTISSIMA TRINDADE",
        "MARCELANDIA",
        "MATUPA",
        "MIRASSOL DOESTE",
        "NOBRES",
        "NORTELANDIA",
        "NOSSA SENHORA DO LIVRAMENTO",
        "NOVA BANDEIRANTES",
        "NOVA NAZARE",
        "NOVA LACERDA",
        "NOVA SANTA HELENA",
        "NOVA BRASILANDIA",
        "NOVA CANAA DO NORTE",
        "NOVA MUTUM",
        "NOVA OLIMPIA",
        "NOVA UBIRATA",
        "NOVA XAVANTINA",
        "NOVO MUNDO",
        "NOVO HORIZONTE DO NORTE",
        "NOVO SAO JOAQUIM",
        "PARANAITA",
        "PARANATINGA",
        "NOVO SANTO ANTONIO",
        "PEDRA PRETA",
        "PEIXOTO DE AZEVEDO",
        "PLANALTO DA SERRA",
        "POCONE",
        "PONTAL DO ARAGUAIA",
        "PONTE BRANCA",
        "PONTES E LACERDA",
        "PORTO ALEGRE DO NORTE",
        "PORTO DOS GAUCHOS",
        "PORTO ESPERIDIAO",
        "PORTO ESTRELA",
        "POXOREO",
        "PRIMAVERA DO LESTE",
        "QUERENCIA",
        "RESERVA DO CABACAL",
        "RIBEIRAO CASCALHEIRA",
        "RIBEIRAOZINHO",
        "RIO BRANCO",
        "RONDOLANDIA",
        "RONDONOPOLIS",
        "ROSARIO OESTE",
        "SAO JOSE DOS QUATRO MARCOS",
        "SANTA CARMEM",
        "SANTO AFONSO",
        "SAO JOSE DO POVO",
        "SAO JOSE DO RIO CLARO",
        "SAO JOSE DO XINGU",
        "SAO PEDRO DA CIPA",
        "SANTA CRUZ DO XINGU",
        "SALTO DO CEU",
        "SANTA RITA DO TRIVELATO",
        "SANTA TEREZINHA",
        "SANTO ANTONIO DO LESTE",
        "SANTO ANTONIO DO LEVERGER",
        "SAO FELIX DO ARAGUAIA",
        "SAPEZAL",
        "SERRA NOVA DOURADA",
        "SINOP",
        "SORRISO",
        "TABAPORA",
        "TANGARA DA SERRA",
        "TAPURAH",
        "TERRA NOVA DO NORTE",
        "TESOURO",
        "TORIXOREU",
        "VALE DE SAO DOMINGOS",
        "VARZEA GRANDE",
        "VERA",
        "VILA RICA"
    ]
    
    print(f"📊 Lista completa de cidades do Mato Grosso: {len(cidades_completas)} cidades")
    
    # Carrega o JSON atual
    import json
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rep_33 = data["representantes"]["pelinson representacoes ltda"]
    estado_mt = rep_33["estados"]["MT"]
    cidades_atual = estado_mt["cidades"]
    
    print(f"📊 Cidades no representante 33: {len(cidades_atual)} cidades")
    
    # Encontra cidades faltando
    cidades_faltando = []
    for cidade in cidades_completas:
        if cidade not in cidades_atual:
            cidades_faltando.append(cidade)
    
    if cidades_faltando:
        print(f"\n❌ CIDADES FALTANDO ({len(cidades_faltando)}):")
        for cidade in cidades_faltando:
            print(f"   - {cidade}")
    else:
        print("\n✅ Todas as cidades estão presentes")
    
    # Encontra cidades extras (que não deveriam estar lá)
    cidades_extras = []
    for cidade in cidades_atual:
        if cidade not in cidades_completas:
            cidades_extras.append(cidade)
    
    if cidades_extras:
        print(f"\n⚠️ CIDADES EXTRAS ({len(cidades_extras)}):")
        for cidade in cidades_extras:
            print(f"   - {cidade}")
    else:
        print("\n✅ Nenhuma cidade extra encontrada")
    
    # Verifica se há cidades duplicadas na lista atual
    cidades_duplicadas = []
    cidades_vistas = set()
    for cidade in cidades_atual:
        if cidade in cidades_vistas:
            cidades_duplicadas.append(cidade)
        else:
            cidades_vistas.add(cidade)
    
    if cidades_duplicadas:
        print(f"\n⚠️ CIDADES DUPLICADAS ({len(cidades_duplicadas)}):")
        for cidade in cidades_duplicadas:
            print(f"   - {cidade}")
    else:
        print("\n✅ Nenhuma cidade duplicada encontrada")
    
    # Resumo
    print(f"\n📋 RESUMO:")
    print(f"   - Cidades completas: {len(cidades_completas)}")
    print(f"   - Cidades no representante: {len(cidades_atual)}")
    print(f"   - Cidades faltando: {len(cidades_faltando)}")
    print(f"   - Cidades extras: {len(cidades_extras)}")
    print(f"   - Cidades duplicadas: {len(cidades_duplicadas)}")
    
    # Calcula o total correto
    total_correto = len(cidades_completas)
    print(f"   - Total correto deveria ser: {total_correto}")
    
    if len(cidades_atual) != total_correto:
        print(f"⚠️ PROBLEMA: O representante tem {len(cidades_atual)} cidades, mas deveria ter {total_correto}")
        print(f"   - Diferença: {total_correto - len(cidades_atual)} cidades")

if __name__ == "__main__":
    verificar_cidades_faltando()
