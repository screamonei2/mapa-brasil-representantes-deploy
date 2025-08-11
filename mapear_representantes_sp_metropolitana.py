#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mapear as cidades da Região Metropolitana de São Paulo
aos representantes baseado na análise da imagem com divisão sub-regional.
"""

import json
import os

def carregar_arquivos():
    """Carrega os arquivos necessários."""
    # Carrega os representantes
    with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        representantes = json.load(f)
    
    # Carrega as mesorregiões de SP
    with open('sp_mesorregioes.json', 'r', encoding='utf-8') as f:
        mesorregioes_sp = json.load(f)
    
    return representantes, mesorregioes_sp

def mapear_subareas_representantes():
    """Mapeia as subáreas da região metropolitana aos representantes."""
    
    # Mapeamento baseado na análise da imagem
    mapeamento = {
        "09.02": {
            "representante": "schioppa",
            "nome": "SCHIOPPA",
            "subarea": "Oeste/Sudoeste",
            "cidades": [
                "PIRAPORA DO BOM JESUS",
                "SANTANA DE PARNAIBA",
                "BARUERI", 
                "JANDIRA",
                "ITAPEVI",
                "CARAPICUIBA",
                "COTIA",
                "EMBU DAS ARTES",
                "ITAQUAQUECETUBA",
                "ITAQUAQUECETUBA",
                "ITAQUAQUECETUBA",
                "ITAQUAQUECETUBA",
                "ITAQUAQUECETUBA",
                "ITAQUAQUECETUBA"
            ]
        },
        "07.01": {
            "representante": "l323 repres.de ferragens e ferram. eirei",
            "nome": "L323 REPRES.DE FERRAGENS E FERRAM. EIREI",
            "subarea": "Norte Central",
            "cidades": [
                "FRANCISCO MORATO",
                "FRANCO DA ROCHA",
                "CAIEIRAS",
                "CAJAMAR",
                "MAIRIPORA"
            ]
        },
        "4.0": {
            "representante": "gl - representacao comercial ltda",
            "nome": "GL - REPRESENTAÇÃO COMERCIAL LTDA",
            "subarea": "Central - Município de São Paulo",
            "cidades": [
                "SAO PAULO",
                "DIADEMA",
                "SAO BERNARDO DO CAMPO",
                "SANTO ANDRE",
                "SAO CAETANO DO SUL",
                "MAUA",
                "RIBEIRAO PIRES",
                "RIO GRANDE DA SERRA",
                "SUZANO",
                "POA",
                "FERRAZ DE VASCONCELOS",
                "ITAQUAQUECETUBA",
                "ARUJA",
                "GUARULHOS"
            ]
        },
        "21.01": {
            "representante": "liber marketing e representacao ltda",
            "nome": "LIBER MARKETING E REPRESENTAÇÃO LTDA",
            "subarea": "Leste/Sudeste",
            "cidades": [
                "SANTA ISABEL",
                "JACAREI",
                "GUARAREMA",
                "SANTA BRANCA",
                "SALESOPOLIS",
                "BIRITIBA MIRIM",
                "MOGI DAS CRUZES"
            ]
        },
        "06.02": {
            "representante": "v&b representacao comercial s/c ltda",
            "nome": "V&B REPRESENTAÇÃO COMERCIAL S/C LTDA",
            "subarea": "Litoral/Baixada Santista",
            "cidades": [
                "CUBATAO",
                "SANTOS",
                "SAO VICENTE",
                "PRAIA GRANDE",
                "BERTIOGA"
            ]
        }
    }
    
    return mapeamento

def verificar_cidades_representantes(representantes, mapeamento):
    """Verifica quais cidades já estão com os representantes e quais precisam ser adicionadas."""
    
    resultados = {}
    
    for codigo, info in mapeamento.items():
        representante_nome = info["representante"]
        cidades_subarea = info["cidades"]
        
        # Encontrar o representante
        rep_encontrado = None
        for nome, dados in representantes["representantes"].items():
            if dados.get("codigo") == codigo:
                rep_encontrado = dados
                break
        
        if rep_encontrado:
            # Verificar se já tem estado SP
            if "SP" not in rep_encontrado["estados"]:
                rep_encontrado["estados"]["SP"] = {
                    "cidades": [],
                    "total_cidades": 0
                }
            
            cidades_atuais = rep_encontrado["estados"]["SP"]["cidades"]
            cidades_para_adicionar = []
            cidades_ja_existem = []
            
            for cidade in cidades_subarea:
                if cidade in cidades_atuais:
                    cidades_ja_existem.append(cidade)
                else:
                    cidades_para_adicionar.append(cidade)
            
            resultados[codigo] = {
                "representante": representante_nome,
                "nome": info["nome"],
                "subarea": info["subarea"],
                "cidades_atuais": len(cidades_atuais),
                "cidades_para_adicionar": cidades_para_adicionar,
                "cidades_ja_existem": cidades_ja_existem,
                "total_novas": len(cidades_para_adicionar)
            }
        else:
            resultados[codigo] = {
                "representante": representante_nome,
                "nome": info["nome"],
                "subarea": info["subarea"],
                "erro": "Representante não encontrado",
                "cidades_para_adicionar": cidades_subarea
            }
    
    return resultados

def aplicar_mapeamento(representantes, mapeamento):
    """Aplica o mapeamento das cidades aos representantes."""
    
    alteracoes = []
    
    for codigo, info in mapeamento.items():
        representante_nome = info["representante"]
        cidades_subarea = info["cidades"]
        
        # Encontrar o representante
        rep_encontrado = None
        for nome, dados in representantes["representantes"].items():
            if dados.get("codigo") == codigo:
                rep_encontrado = dados
                break
        
        if rep_encontrado:
            # Verificar se já tem estado SP
            if "SP" not in rep_encontrado["estados"]:
                rep_encontrado["estados"]["SP"] = {
                    "cidades": [],
                    "total_cidades": 0
                }
            
            cidades_atuais = rep_encontrado["estados"]["SP"]["cidades"]
            cidades_adicionadas = []
            
            for cidade in cidades_subarea:
                if cidade not in cidades_atuais:
                    cidades_atuais.append(cidade)
                    cidades_adicionadas.append(cidade)
            
            # Atualizar contadores
            rep_encontrado["estados"]["SP"]["total_cidades"] = len(cidades_atuais)
            rep_encontrado["total_cidades"] = len(cidades_atuais)
            
            # Adicionar SP aos estados atendidos se não estiver
            if "SP   " not in rep_encontrado["estados_atendidos"]:
                rep_encontrado["estados_atendidos"].append("SP   ")
            
            alteracoes.append({
                "codigo": codigo,
                "representante": representante_nome,
                "cidades_adicionadas": cidades_adicionadas,
                "total_apos_alteracao": len(cidades_atuais)
            })
    
    return alteracoes

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_mapeamento_sp_metropolitana.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\nBackup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("=== MAPEAMENTO DE REPRESENTANTES - REGIÃO METROPOLITANA DE SP ===")
    print("Objetivo: Mapear cidades das subáreas aos representantes baseado na análise da imagem")
    print()
    
    try:
        # Carrega os arquivos
        representantes, mesorregioes_sp = carregar_arquivos()
        print("✓ Arquivos carregados com sucesso")
        
        # Mapeamento das subáreas
        mapeamento = mapear_subareas_representantes()
        print(f"✓ Mapeamento criado para {len(mapeamento)} subáreas")
        
        # Verificar situação atual
        print("\nVerificando situação atual dos representantes...")
        resultados = verificar_cidades_representantes(representantes, mapeamento)
        
        # Mostrar resultados da verificação
        total_cidades_para_adicionar = 0
        for codigo, resultado in resultados.items():
            print(f"\n--- {codigo} - {resultado['nome']} ---")
            print(f"Subárea: {resultado['subarea']}")
            
            if "erro" in resultado:
                print(f"❌ {resultado['erro']}")
                print(f"Cidades para adicionar: {len(resultado['cidades_para_adicionar'])}")
            else:
                print(f"Cidades atuais: {resultado['cidades_atuais']}")
                print(f"Cidades para adicionar: {resultado['total_novas']}")
                if resultado['total_novas'] > 0:
                    print(f"Novas cidades: {', '.join(resultado['cidades_para_adicionar'][:5])}{'...' if resultado['total_novas'] > 5 else ''}")
                total_cidades_para_adicionar += resultado['total_novas']
        
        print(f"\n📊 Total de cidades para adicionar: {total_cidades_para_adicionar}")
        
        if total_cidades_para_adicionar > 0:
            # Aplicar mapeamento
            print("\nAplicando mapeamento...")
            alteracoes = aplicar_mapeamento(representantes, mapeamento)
            
            # Mostrar alterações aplicadas
            print("\n=== ALTERAÇÕES APLICADAS ===")
            for alteracao in alteracoes:
                print(f"✓ {alteracao['codigo']}: {len(alteracao['cidades_adicionadas'])} cidades adicionadas")
                print(f"  Total após alteração: {alteracao['total_apos_alteracao']} cidades")
            
            # Salvar arquivo
            salvar_arquivo(representantes)
            print("\n✓ Mapeamento aplicado com sucesso!")
        else:
            print("\n✓ Todas as cidades já estão mapeadas corretamente!")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    main()
