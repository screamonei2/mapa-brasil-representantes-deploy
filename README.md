# Mapa Brasil Representantes - Deploy Vercel

Este é o projeto otimizado para deploy na Vercel.

## Arquivos Incluídos

- `index.html` - Aplicação principal
- `representantes_por_estado.json` - Dados dos representantes
- `geojs-100-mun-v2.json` - Dados geográficos dos municípios
- `uf.json` - Dados geográficos dos estados
- `vercel.json` - Configuração do Vercel

## Como Fazer o Deploy

1. **Via GitHub (Recomendado):**
   - Faça push deste diretório para um repositório GitHub
   - Conecte o repositório na Vercel
   - O deploy será automático

2. **Via Vercel CLI:**
   ```bash
   npm i -g vercel
   vercel login
   vercel
   ```

3. **Via Interface Web:**
   - Acesse [vercel.com](https://vercel.com)
   - Faça upload do diretório `vercel-deploy`

## Estrutura do Projeto

```
vercel-deploy/
├── index.html                    # Aplicação principal
├── representantes_por_estado.json # Dados dos representantes
├── geojs-100-mun-v2.json        # Dados dos municípios
├── uf.json                       # Dados dos estados
├── vercel.json                   # Configuração Vercel
└── README.md                     # Este arquivo
```

## Funcionalidades

- Mapa interativo do Brasil
- Busca por estado ou município
- Visualização de representantes por região
- Interface responsiva
- Destaque de áreas atendidas por representantes

## Tecnologias Utilizadas

- HTML5
- CSS3 (Tailwind CSS)
- JavaScript (Vanilla)
- Leaflet.js (Mapas)
- GeoJSON (Dados geográficos) 