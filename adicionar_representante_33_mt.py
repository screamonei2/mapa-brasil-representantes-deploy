#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar o representante 33 (PELINSSON REPRESENTAÇÕES LTDA) 
ao arquivo representantes_por_estado.json com todas as cidades do Mato Grosso
"""

import json
import os
import shutil
from datetime import datetime

def fazer_backup(arquivo_original):
    """
    Cria um backup do arquivo original com timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"{arquivo_original}.backup_representante_33_{timestamp}"
    
    try:
        shutil.copy2(arquivo_original, nome_backup)
        print(f"✅ Backup criado: {nome_backup}")
        return nome_backup
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def obter_cidades_mato_grosso():
    """
    Retorna a lista completa de cidades do Mato Grosso
    """
    cidades_mt = [
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
    
    return cidades_mt

def adicionar_representante_33(data):
    """
    Adiciona o representante 33 (PELINSSON) com todas as cidades do Mato Grosso
    """
    representante_33 = {
        "codigo": "33",
        "nome": "PELINSSON REPRESENTACOES LTDA",
        "contato": {
            "nome_contato": "Adair",
            "email": "adairpelinsson@gmail.com",
            "celular": "66-99984-1208"
        },
        "observacoes": "Representante exclusivo para todo o estado do Mato Grosso",
        "total_cidades": 141,
        "estados_atendidos": ["MT"],
        "resumo_atividades": "Cobertura completa do estado de Mato Grosso",
        "performance": {},
        "estados": {
            "MT": {
                "cidades": obter_cidades_mato_grosso(),
                "total_cidades": 141,
                "mesorregioes": [],
                "total_mesorregioes": 0
            }
        }
    }
    
    # Adiciona o representante ao dicionário
    data["representantes"]["pelinson representacoes ltda"] = representante_33
    
    return data

def main():
    arquivo_json = "data/representantes_por_estado.json"
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_json):
        print(f"❌ Arquivo não encontrado: {arquivo_json}")
        return
    
    print(f"📁 Processando arquivo: {arquivo_json}")
    
    # Faz backup do arquivo original
    backup_criado = fazer_backup(arquivo_json)
    if not backup_criado:
        print("❌ Não foi possível criar backup. Abortando operação.")
        return
    
    try:
        # Carrega o JSON
        print("📖 Carregando arquivo JSON...")
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("🔧 Adicionando representante 33 (PELINSSON)...")
        
        # Adiciona o representante 33
        data = adicionar_representante_33(data)
        
        # Salva o arquivo atualizado
        print("💾 Salvando arquivo atualizado...")
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ Representante 33 adicionado com sucesso!")
        print(f"📋 Backup salvo em: {backup_criado}")
        
        # Estatísticas
        total_representantes = len(data.get("representantes", {}))
        print(f"📊 Total de representantes após adição: {total_representantes}")
        
        # Verifica se o representante foi adicionado
        if "pelinson representacoes ltda" in data["representantes"]:
            rep_33 = data["representantes"]["pelinson representacoes ltda"]
            print(f"✅ Representante 33 adicionado:")
            print(f"   - Nome: {rep_33['nome']}")
            print(f"   - Código: {rep_33['codigo']}")
            print(f"   - Estado: {rep_33['estados_atendidos'][0]}")
            print(f"   - Total de cidades: {rep_33['total_cidades']}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        print("🔄 Restaurando arquivo original do backup...")
        try:
            shutil.copy2(backup_criado, arquivo_json)
            print("✅ Arquivo original restaurado do backup")
        except Exception as restore_error:
            print(f"❌ Erro ao restaurar backup: {restore_error}")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("🔄 Restaurando arquivo original do backup...")
        try:
            shutil.copy2(backup_criado, arquivo_json)
            print("✅ Arquivo original restaurado do backup")
        except Exception as restore_error:
            print(f"❌ Erro ao restaurar backup: {restore_error}")

if __name__ == "__main__":
    main()
