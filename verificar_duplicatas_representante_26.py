#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e corrigir cidades duplicadas no representante 26.
Identifica cidades que aparecem mais de uma vez e remove as duplicatas.
"""

import json
import os
from collections import Counter

def carregar_arquivos():
    """Carrega os arquivos necessários."""
    try:
        # Carregar representantes
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            representantes = json.load(f)
        
        return representantes
    except Exception as e:
        print(f"❌ Erro ao carregar arquivos: {e}")
        return None

def encontrar_representante_26(representantes):
    """Encontra o representante 26."""
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            return nome, dados
    return None, None

def verificar_duplicatas_representante_26(representante_26):
    """Verifica se existem cidades duplicadas no representante 26."""
    
    if not representante_26 or "estados" not in representante_26 or "SP" not in representante_26["estados"]:
        return None
    
    cidades_sp = representante_26["estados"]["SP"].get("cidades", [])
    
    # Contar ocorrências de cada cidade
    contador_cidades = Counter(cidades_sp)
    
    # Identificar cidades duplicadas
    cidades_duplicadas = {cidade: count for cidade, count in contador_cidades.items() if count > 1}
    cidades_unicas = list(contador_cidades.keys())
    
    return {
        "cidades_originais": cidades_sp,
        "cidades_unicas": cidades_unicas,
        "cidades_duplicadas": cidades_duplicadas,
        "total_original": len(cidades_sp),
        "total_unicas": len(cidades_unicas),
        "total_duplicatas": sum(cidades_duplicadas.values()) - len(cidades_duplicadas)
    }

def corrigir_duplicatas_representante_26(representantes, resultado_verificacao):
    """Corrige as cidades duplicadas do representante 26."""
    
    # Encontrar representante 26
    rep_26 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            rep_26 = dados
            break
    
    if not rep_26:
        return None
    
    # Substituir lista de cidades pela versão sem duplicatas
    if "estados" in rep_26 and "SP" in rep_26["estados"]:
        rep_26["estados"]["SP"]["cidades"] = resultado_verificacao["cidades_unicas"]
        
        # Atualizar total de cidades
        rep_26["estados"]["SP"]["total_cidades"] = len(resultado_verificacao["cidades_unicas"])
        rep_26["total_cidades"] = len(resultado_verificacao["cidades_unicas"])
        
        print(f"✅ Cidades duplicadas corrigidas no representante 26")
        print(f"   Total de cidades atualizado: {rep_26['total_cidades']}")
    
    return representantes

def gerar_relatorio_verificacao(resultado_verificacao):
    """Gera relatório da verificação de duplicatas."""
    print("=" * 80)
    print("🔍 VERIFICAÇÃO: CIDADES DUPLICADAS NO REPRESENTANTE 26")
    print("=" * 80)
    
    if not resultado_verificacao:
        return
    
    print(f"\n📊 ANÁLISE DE DUPLICATAS:")
    print(f"   Total de cidades originais: {resultado_verificacao['total_original']}")
    print(f"   Total de cidades únicas: {resultado_verificacao['total_unicas']}")
    print(f"   Total de duplicatas: {resultado_verificacao['total_duplicatas']}")
    
    if resultado_verificacao['cidades_duplicadas']:
        print(f"\n⚠️ CIDADES DUPLICADAS ENCONTRADAS:")
        for cidade, count in sorted(resultado_verificacao['cidades_duplicadas'].items()):
            print(f"   • {cidade} (aparece {count} vezes)")
        
        print(f"\n🔧 AÇÃO NECESSÁRIA:")
        print(f"   Remover {resultado_verificacao['total_duplicatas']} duplicatas")
        print(f"   Manter {resultado_verificacao['total_unicas']} cidades únicas")
    else:
        print(f"\n✅ PERFEITO!")
        print(f"   Não foram encontradas cidades duplicadas no representante 26")

def gerar_relatorio_correcao(cidades_removidas, total_final):
    """Gera relatório da correção das duplicatas."""
    print("=" * 80)
    print("🔧 RELATÓRIO DE CORREÇÃO - DUPLICATAS REMOVIDAS")
    print("=" * 80)
    
    print(f"\n📊 RESUMO DA CORREÇÃO:")
    print(f"   Duplicatas removidas: {cidades_removidas}")
    print(f"   Total final de cidades: {total_final}")
    
    print(f"\n✅ CORREÇÃO CONCLUÍDA!")
    print(f"   Todas as cidades duplicadas foram removidas do representante 26")
    print(f"   O representante 26 agora tem apenas cidades únicas")

def verificar_resultado_final(representantes):
    """Verifica se a correção foi bem-sucedida."""
    
    # Encontrar representante 26
    rep_26 = None
    for nome, dados in representantes["representantes"].items():
        if dados.get("codigo") == "26.0":
            rep_26 = dados
            break
    
    if not rep_26:
        return None
    
    # Verificar se ainda há duplicatas
    cidades_sp = rep_26["estados"]["SP"].get("cidades", [])
    contador_cidades = Counter(cidades_sp)
    cidades_duplicadas = {cidade: count for cidade, count in contador_cidades.items() if count > 1}
    
    return {
        "total_cidades": len(cidades_sp),
        "cidades_duplicadas": len(cidades_duplicadas),
        "status": "✅ SEM DUPLICATAS" if len(cidades_duplicadas) == 0 else "⚠️ AINDA HÁ DUPLICATAS"
    }

def salvar_arquivo(representantes):
    """Salva o arquivo corrigido."""
    # Cria backup
    backup_path = 'data/representantes_por_estado_backup_correcao_duplicatas_26.json'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup criado: {backup_path}")
    
    # Salva o arquivo corrigido
    with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
        json.dump(representantes, f, ensure_ascii=False, indent=2)
    print("✅ Arquivo corrigido salvo!")

def main():
    """Função principal."""
    print("🔍 VERIFICANDO CIDADES DUPLICADAS NO REPRESENTANTE 26")
    print("=" * 80)
    
    # Carregar arquivos
    representantes = carregar_arquivos()
    if not representantes:
        return
    
    # Encontrar representante 26
    nome_rep, representante_26 = encontrar_representante_26(representantes)
    if not representante_26:
        print("❌ Representante 26 não encontrado!")
        return
    
    print(f"✅ Representante 26 encontrado: {representante_26['nome']}")
    
    # Verificar duplicatas
    resultado_verificacao = verificar_duplicatas_representante_26(representante_26)
    
    # Gerar relatório da verificação
    gerar_relatorio_verificacao(resultado_verificacao)
    
    if resultado_verificacao and resultado_verificacao['total_duplicatas'] > 0:
        print(f"\n🔧 INICIANDO CORREÇÃO...")
        
        # Corrigir duplicatas
        representantes_corrigidos = corrigir_duplicatas_representante_26(representantes, resultado_verificacao)
        
        if representantes_corrigidos:
            # Gerar relatório da correção
            gerar_relatorio_correcao(resultado_verificacao['total_duplicatas'], resultado_verificacao['total_unicas'])
            
            # Salvar arquivo
            salvar_arquivo(representantes_corrigidos)
            
            print(f"\n🔍 VERIFICAÇÃO PÓS-CORREÇÃO:")
            print("   Executando verificação para confirmar que as duplicatas foram removidas...")
            
            # Verificar resultado final
            resultado_final = verificar_resultado_final(representantes_corrigidos)
            
            if resultado_final:
                print(f"\n📊 RESULTADO FINAL:")
                print(f"   Total de cidades: {resultado_final['total_cidades']}")
                print(f"   Cidades duplicadas: {resultado_final['cidades_duplicadas']}")
                print(f"   Status: {resultado_final['status']}")
                
                if resultado_final['cidades_duplicadas'] == 0:
                    print(f"\n🎉 SUCESSO! Todas as duplicatas foram removidas!")
                else:
                    print(f"\n⚠️ ATENÇÃO: Ainda há duplicatas!")
        else:
            print(f"\n❌ Erro ao corrigir duplicatas!")
    else:
        print(f"\n✅ Nenhuma ação necessária!")
        print(f"   O representante 26 não tem cidades duplicadas")

if __name__ == "__main__":
    main()
