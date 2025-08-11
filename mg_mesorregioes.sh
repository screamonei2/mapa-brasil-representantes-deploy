#!/bin/bash

# IDs das mesorregiões de MG
meso_ids=(3101 3102 3103 3104 3105 3106 3107 3108 3109 3110 3111 3112)

echo "["

for i in "${!meso_ids[@]}"; do
  id=${meso_ids[$i]}

  # Nome da mesorregião
  nome_meso=$(curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes/$id" | jq -r '.nome')

  # Lista de municípios
  municipios=$(curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes/$id/municipios" | jq -c '[.[].nome]')

  # Se for o último elemento, não coloca vírgula
  if [ $i -lt $((${#meso_ids[@]} - 1)) ]; then
    echo "  {\"mesorregiao\": \"$nome_meso\", \"municipios\": $municipios},"
  else
    echo "  {\"mesorregiao\": \"$nome_meso\", \"municipios\": $municipios}"
  fi
done

echo "]"
