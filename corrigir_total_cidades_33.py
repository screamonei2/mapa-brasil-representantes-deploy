#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o campo total_cidades do representante 33
"""

import json
import shutil
from datetime import datetime

def corrigir_total_cidades_33():
    """
    Corrige o campo total_cidades do representante 33
    """
    try:
        # Carrega o JSON
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON carregado com sucesso")
        
        # Verifica se o representante 33 existe
        if "pelinson representacoes ltda" not in data["representantes"]:
            print("❌ Representante 33 não encontrado")
            return
        
        rep_33 = data["representantes"]["pelinson representacoes ltda"]
        print(f"✅ Representante 33 encontrado: {rep_33['nome']}")
        
        # Verifica o estado MT
        if "MT" not in rep_33["estados"]:
            print("❌ Estado MT não encontrado no representante 33")
            return
        
        estado_mt = rep_33["estados"]["MT"]
        cidades_reais = len(estado_mt["cidades"])
        
        print(f"📊 Situação atual:")
        print(f"   - total_cidades do representante: {rep_33['total_cidades']}")
        print(f"   - total_cidades do estado: {estado_mt['total_cidades']}")
        print(f"   - cidades reais: {cidades_reais}")
        
        # Corrige os campos total_cidades
        rep_33["total_cidades"] = cidades_reais
        estado_mt["total_cidades"] = cidades_reais
        
        print(f"\n✅ Campos corrigidos:")
        print(f"   - total_cidades do representante: {rep_33['total_cidades']}")
        print(f"   - total_cidades do estado: {estado_mt['total_cidades']}")
        
        # Faz backup antes de salvar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"data/representantes_por_estado.json.backup_correcao_total_{timestamp}"
        
        try:
            shutil.copy2("data/representantes_por_estado.json", backup_file)
            print(f"✅ Backup criado: {backup_file}")
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return
        
        # Salva o arquivo corrigido
        with open('data/representantes_por_estado.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ Arquivo salvo com sucesso")
        print(f"📋 Backup salvo em: {backup_file}")
        
        # Verifica se a correção foi aplicada
        with open('data/representantes_por_estado.json', 'r', encoding='utf-8') as f:
            data_verificacao = json.load(f)
        
        rep_33_verificacao = data_verificacao["representantes"]["pelinson representacoes ltda"]
        estado_mt_verificacao = rep_33_verificacao["estados"]["MT"]
        
        print(f"\n🔍 Verificação da correção:")
        print(f"   - total_cidades do representante: {rep_33_verificacao['total_cidades']}")
        print(f"   - total_cidades do estado: {estado_mt_verificacao['total_cidades']}")
        print(f"   - cidades reais: {len(estado_mt_verificacao['cidades'])}")
        
        if (rep_33_verificacao['total_cidades'] == estado_mt_verificacao['total_cidades'] == 
            len(estado_mt_verificacao['cidades'])):
            print("✅ Correção aplicada com sucesso!")
        else:
            print("❌ Erro na correção")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    corrigir_total_cidades_33()
