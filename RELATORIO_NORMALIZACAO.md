# Relatório de Normalização - representantes_por_estado.json

## Resumo da Operação

**Data:** 13/08/2025  
**Hora:** 09:32:24  
**Arquivo processado:** `data/representantes_por_estado.json`  
**Backup criado:** `data/representantes_por_estado.json.backup_20250813_093224`

## O que foi normalizado

### ✅ Campos normalizados com sucesso:
- **Estados**: Nomes das chaves do dicionário de estados
- **Cidades**: Lista de cidades dentro de cada estado
- **Estados atendidos**: Lista de estados que cada representante atende
- **Mesorregiões**: Nomes das mesorregiões (quando existem)

### 🔍 Exemplos de normalização:
- `"BOA ESPERANÇA DO SUL"` → `"BOA ESPERANCA DO SUL"`
- `"ACAUÃ"` → `"ACAUA"`
- `"TRIÂNGULO MINEIRO"` → `"TRIANGULO MINEIRO"`
- `"ALTO PARANAÍBA"` → `"ALTO PARANAIBA"`
- `"SÃO PAULO"` → `"SAO PAULO"` (se existisse)

### ⚠️ Campos NÃO normalizados (intencionalmente):
- **"observacoes"**: Textos descritivos mantidos com acentuação original
- **"nome_contato"**: Nomes de pessoas mantidos com acentuação original
- **"nome"**: Nomes das empresas mantidos com acentuação original
- **"resumo_atividades"**: Descrições mantidas com acentuação original

## Estatísticas

- **Total de representantes processados:** 46
- **Arquivo original preservado:** ✅ Sim (backup com timestamp)
- **Estrutura JSON mantida:** ✅ Sim
- **Encoding preservado:** ✅ Sim (UTF-8)

## Função de Normalização

O script utiliza a função `remover_acentos()` que:
1. Normaliza o texto para forma NFD (decomposição Unicode)
2. Remove todos os diacríticos (acentos, cedilhas, etc.)
3. Mapeia caracteres especiais (ç → C, ñ → N)
4. Converte para UPPERCASE

## Segurança

- ✅ Backup automático antes da modificação
- ✅ Restauração automática em caso de erro
- ✅ Validação de JSON antes e depois da operação
- ✅ Preservação da estrutura original

## Arquivos Criados

1. **`normalizar_nomes_estados_cidades.py`** - Script de normalização
2. **`RELATORIO_NORMALIZACAO.md`** - Este relatório
3. **Backup do arquivo original** - Com timestamp único

## Como usar o script

```bash
cd vercel-deploy
python3 normalizar_nomes_estados_cidades.py
```

## Observações

- O script é seguro e faz backup automático
- Apenas os campos geográficos (estados, cidades) são normalizados
- Campos de texto descritivo mantêm a acentuação original
- A normalização facilita buscas e comparações sem problemas de encoding
