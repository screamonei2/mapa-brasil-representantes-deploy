#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover todas as cidades de Araçatuba dos outros representantes.
Deixa apenas o representante 26 atendendo toda a região de Araçatuba.
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

def remover_cidades_aracatuba_outros_representantes(representantes, cidades_aracatuba):
    """Remove cidades de Araçatuba de todos os representantes exceto o 26."""
    
    cidades_aracatuba_set = set(cidades_aracatuba)
    representantes_afetados = {}
    total_cidades_removidas = 0
    
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            # Pular o representante 26
            continue
            
        if "estados" in dados and "SP" in dados["estados"]:
            cidades_sp = dados["estados"]["SP"].get("cidades", [])
            cidades_para_remover = []
            
            # Identificar cidades de Araçatuba para remover
            for cidade in cidades_sp:
                if cidade.upper() in cidades_aracatuba_set:
                    cidades_para_remover.append(cidade)
            
            if cidades_para_remover:
                # Remover cidades de Araçatuba
                for cidade in cidades_para_remover:
                    if cidade in dados["estados"]["SP"]["cidades"]:
                        dados["estados"]["SP"]["cidades"].remove(cidade)
                        total_cidades_removidas += 1
                
                # Atualizar total de cidades
                dados["estados"]["SP"]["total_cidades"] = len(dados["estados"]["SP"]["cidades"])
                dados["total_cidades"] = dados["estados"]["SP"]["total_cidades"]
                
                representantes_afetados[nome] = {
                    "codigo": dados.get("codigo", "N/A"),
                    "nome": dados.get("nome", nome),
                    "cidades_removidas": cidades_para_remover,
                    "total_removidas": len(cidades_para_remover),
                    "novo_total_sp": dados["estados"]["SP"]["total_cidades"]
                }
    
    return representantes, representantes_afetados, total_cidades_removidas

def verificar_resultado_final(representantes, cidades_aracatuba):
    """Verifica se apenas o representante 26 está atendendo Araçatuba."""
    
    cidades_aracatuba_set = set(cidades_aracatuba)
    representantes_aracatuba = {}
    
    for nome, dados in representantes["representantes"].items():
        if "estados" in dados and "SP" in dados["estados"]:
            cidades_sp = dados["estados"]["SP"].get("cidades", [])
            cidades_aracatuba_rep = []
            
            for cidade in cidades_sp:
                if cidade.upper() in cidades_aracatuba_set:
                    cidades_aracatuba_rep.append(cidade.upper())
            
            if cidades_aracatuba_rep:
                representantes_aracatuba[nome] = {
                    "codigo": dados.get("codigo", "N/A"),
                    "nome": dados.get("nome", nome),
                    "cidades_aracatuba": cidades_aracatuba_rep,
                    "total_cidades_aracatuba": len(cidades_aracatuba_rep)
                }
    
    return representantes_aracatuba

def gerar_relatorio_remocao(representantes_afetados, total_cidades_removidas):
    """Gera relatório da remoção das cidades."""
    print("=" * 80)
    print("🗑️ RELATÓRIO DE REMOÇÃO DE CIDADES DE ARAÇATUBA")
    print("=" * 80)
    
    print(f"\n📊 RESUMO DA OPERAÇÃO:")
    print(f"   Total de representantes afetados: {len(representantes_afetados)}")
    print(f"   Total de cidades removidas: {total_cidades_removidas}")
    
    if representantes_afetados:
        print(f"\n🏢 REPRESENTANTES AFETADOS:")
        for nome, dados in representantes_afetados.items():
            print(f"\n   📋 {dados['nome']}")
            print(f"      Código: {dados['codigo']}")
            print(f"      Cidades removidas: {dados['total_removidas']}")
            print(f"      Novo total em SP: {dados['novo_total_sp']}")
            print(f"      Cidades: {', '.join(dados['cidades_removidas'])}")
    
    print(f"\n✅ OPERAÇÃO CONCLUÍDA!")
    print(f"   Todas as cidades de Araçatuba foram removidas dos outros representantes")
    print(f"   Apenas o representante 26 atende toda a região de Araçatuba")

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_remocao_aracatuba_outros.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("✅ Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("🗑️ REMOVENDO CIDADES DE ARAÇATUBA DOS OUTROS REPRESENTANTES")
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
    
    # Remover cidades de Araçatuba dos outros representantes
    representantes_corrigidos, representantes_afetados, total_cidades_removidas = remover_cidades_aracatuba_outros_representantes(representantes, cidades_aracatuba)
    
    # Gerar relatório da remoção
    gerar_relatorio_remocao(representantes_afetados, total_cidades_removidas)
    
    # Salvar arquivo
    salvar_arquivo(representantes_corrigidos)
    
    print(f"\n🔍 VERIFICAÇÃO FINAL:")
    print("   Executando verificação para confirmar que apenas o representante 26 atende Araçatuba...")
    
    # Verificar resultado final
    resultado_final = verificar_resultado_final(representantes_corrigidos, cidades_aracatuba)
    
    if resultado_final:
        print(f"\n📋 REPRESENTANTES ATENDENDO ARAÇATUBA APÓS REMOÇÃO:")
        for nome, dados in resultado_final.items():
            print(f"   • {dados['nome']} ({dados['codigo']}) - {dados['total_cidades_aracatuba']} cidades")
        
        # Verificar se apenas o representante 26 está atendendo
        if len(resultado_final) == 1 and list(resultado_final.keys())[0] == "roberto da fonseca reis&reis rep.ltda":
            print(f"\n🎉 SUCESSO! Apenas o representante 26 atende Araçatuba!")
        else:
            print(f"\n⚠️ ATENÇÃO: Ainda há outros representantes atendendo Araçatuba!")

if __name__ == "__main__":
    main()
