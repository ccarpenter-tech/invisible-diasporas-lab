# A diáspora asiática sob o olhar da mídia global

Projeto Final A2 — Programação / Comunicação Digital — FGV

## Tema

Este projeto analisa como a mídia global cobre comunidades asiáticas em países de destino, comparando a visibilidade jornalística com dados demográficos de migração.

## Pergunta de pesquisa

A mídia dos países de destino oferece visibilidade proporcional ao tamanho das comunidades asiáticas? E, quando há cobertura, qual é o tom predominante?

## Fontes de dados

- Google BigQuery: coleta de metadados jornalísticos globais.
- UN DESA International Migrant Stock 2020 — Destination.
- UN DESA International Migrant Stock 2020 — Origin.
- Python: limpeza, análise, cálculo de invisibilidade e embeddings.
- Streamlit: dashboard interativo.

## Observação metodológica

Os arquivos da ONU usados neste projeto não formam uma matriz bilateral origem × destino.
Por isso, o app usa dois níveis de análise:

1. Índice por país de destino:
   compara cobertura midiática com o total de migrantes vivendo naquele país.

2. Índice proxy por comunidade × destino:
   combina o tamanho global da diáspora de origem com o peso migratório do país de destino.

O índice proxy não representa a contagem exata de migrantes de uma origem específica vivendo em um destino específico.
Ele funciona como indicador comparativo de invisibilidade midiática.

## Funcionalidades

1. Visão geral da seleção.
2. Volume e sentimento ao longo do tempo.
3. Invisibilidade midiática.
4. Busca semântica e resumo por IA.

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py