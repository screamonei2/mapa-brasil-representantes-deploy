#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se o representante 26 está atendendo cidades que não pertencem à região de Araçatuba.
Identifica e remove cidades extras que não fazem parte da mesorregião de Araçatuba.
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

def verificar_cidades_extras_representante_26(representantes, cidades_aracatuba):
    """Verifica se o representante 26 tem cidades que não pertencem à região de Araçatuba."""
    
    # Encontrar representante 26
    rep_26 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            rep_26 = dados
            break
    
    if not rep_26:
        print("❌ Representante 26 não encontrado!")
        return None, None
    
    # Obter cidades atuais do representante 26
    cidades_atuais = []
    if "estados" in rep_26 and "SP" in rep_26["estados"]:
        cidades_sp = rep_26["estados"]["SP"].get("cidades", [])
        cidades_atuais = [cidade.upper() for cidade in cidades_sp]
    
    # Identificar cidades que não pertencem à região de Araçatuba
    cidades_aracatuba_set = set(cidades_aracatuba)
    cidades_aracatuba_rep = []
    cidades_extras = []
    
    for cidade in cidades_atuais:
        if cidade in cidades_aracatuba_set:
            cidades_aracatuba_rep.append(cidade)
        else:
            cidades_extras.append(cidade)
    
    return {
        "cidades_aracatuba": cidades_aracatuba_rep,
        "cidades_extras": cidades_extras,
        "total_aracatuba": len(cidades_aracatuba_rep),
        "total_extras": len(cidades_extras),
        "total_atual": len(cidades_atuais)
    }

def remover_cidades_extras_representante_26(representantes, cidades_extras):
    """Remove cidades extras do representante 26, mantendo apenas as de Araçatuba."""
    
    # Encontrar representante 26
    rep_26 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            rep_26 = dados
            break
    
    if not rep_26:
        return None
    
    # Obter cidades atuais
    if "estados" in rep_26 and "SP" in rep_26["estados"]:
        cidades_sp = rep_26["estados"]["SP"].get("cidades", [])
        
        # Remover cidades extras
        cidades_limpas = []
        for cidade in cidades_sp:
            if cidade.upper() not in [c.upper() for c in cidades_extras]:
                cidades_limpas.append(cidade)
        
        # Atualizar lista de cidades
        rep_26["estados"]["SP"]["cidades"] = cidades_limpas
        
        # Atualizar total de cidades
        rep_26["estados"]["SP"]["total_cidades"] = len(cidades_limpas)
        rep_26["total_cidades"] = len(cidades_limpas)
        
        print(f"✅ Cidades extras removidas do representante 26")
        print(f"   Total de cidades atualizado: {rep_26['total_cidades']}")
    
    return representantes

def gerar_relatorio_verificacao(resultado_verificacao, cidades_aracatuba):
    """Gera relatório da verificação das cidades."""
    print("=" * 80)
    print("🔍 VERIFICAÇÃO: CIDADES EXTRAS DO REPRESENTANTE 26")
    print("=" * 80)
    
    if not resultado_verificacao:
        return
    
    print(f"\n📊 ANÁLISE DO REPRESENTANTE 26:")
    print(f"   Total de cidades atuais: {resultado_verificacao['total_atual']}")
    print(f"   Cidades de Araçatuba: {resultado_verificacao['total_aracatuba']}")
    print(f"   Cidades extras: {resultado_verificacao['total_extras']}")
    
    if resultado_verificacao['cidades_extras']:
        print(f"\n⚠️ CIDADES EXTRAS (NÃO PERTENCEM A ARAÇATUBA):")
        for cidade in sorted(resultado_verificacao['cidades_extras']):
            print(f"   • {cidade}")
        
        print(f"\n🔧 AÇÃO NECESSÁRIA:")
        print(f"   Remover {len(resultado_verificacao['cidades_extras'])} cidades extras")
        print(f"   Manter apenas as {len(resultado_verificacao['cidades_aracatuba'])} cidades de Araçatuba")
    else:
        print(f"\n✅ PERFEITO!")
        print(f"   O representante 26 atende APENAS cidades da região de Araçatuba")
        print(f"   Nenhuma cidade extra encontrada")

def gerar_relatorio_limpeza(cidades_removidas, total_final):
    """Gera relatório da limpeza das cidades."""
    print("=" * 80)
    print("🧹 RELATÓRIO DE LIMPEZA - REPRESENTANTE 26")
    print("=" * 80)
    
    print(f"\n📊 RESUMO DA LIMPEZA:")
    print(f"   Cidades extras removidas: {len(cidades_removidas)}")
    print(f"   Total final de cidades: {total_final}")
    
    if cidades_removidas:
        print(f"\n🗑️ CIDADES REMOVIDAS:")
        for cidade in sorted(cidades_removidas):
            print(f"   • {cidade}")
    
    print(f"\n✅ LIMPEZA CONCLUÍDA!")
    print(f"   O representante 26 agora atende APENAS cidades da região de Araçatuba")

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_limpeza_representante_26.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("✅ Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("🔍 VERIFICANDO CIDADES EXTRAS DO REPRESENTANTE 26")
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
    
    # Verificar cidades extras
    resultado_verificacao = verificar_cidades_extras_representante_26(representantes, cidades_aracatuba)
    
    # Gerar relatório da verificação
    gerar_relatorio_verificacao(resultado_verificacao, cidades_aracatuba)
    
    if resultado_verificacao and resultado_verificacao['cidades_extras']:
        print(f"\n🧹 INICIANDO LIMPEZA...")
        
        # Remover cidades extras
        representantes_limpos = remover_cidades_extras_representante_26(representantes, resultado_verificacao['cidades_extras'])
        
        if representantes_limpos:
            # Gerar relatório da limpeza
            gerar_relatorio_limpeza(resultado_verificacao['cidades_extras'], resultado_verificacao['total_aracatuba'])
            
            # Salvar arquivo
            salvar_arquivo(representantes_limpos)
            
            print(f"\n🔍 VERIFICAÇÃO PÓS-LIMPEZA:")
            print("   Executando verificação para confirmar que apenas cidades de Araçatuba permanecem...")
            
            # Verificar resultado final
            resultado_final = verificar_cidades_extras_representante_26(representantes_limpos, cidades_aracatuba)
            
            if resultado_final:
                print(f"\n📊 RESULTADO FINAL:")
                print(f"   Total de cidades: {resultado_final['total_atual']}")
                print(f"   Cidades de Araçatuba: {resultado_final['total_aracatuba']}")
                print(f"   Cidades extras: {resultado_final['total_extras']}")
                
                if resultado_final['total_extras'] == 0:
                    print(f"\n🎉 SUCESSO! Representante 26 atende APENAS cidades de Araçatuba!")
                else:
                    print(f"\n⚠️ ATENÇÃO: Ainda há cidades extras!")
        else:
            print(f"\n❌ Erro ao limpar cidades extras!")
    else:
        print(f"\n✅ Nenhuma ação necessária!")
        print(f"   O representante 26 já atende apenas cidades da região de Araçatuba")

if __name__ == "__main__":
    main()
