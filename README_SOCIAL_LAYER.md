# Camada social — Invisible Diasporas Lab

Arquivos:

- `social_layer.py`: módulo Streamlit com login, perfis, comentários, mensagens, coleções, framing colaborativo, debates, círculos, relatórios e notificações.
- `supabase_schema_social.sql`: tabelas e políticas RLS para Supabase.
- `patch_app_social.py`: script que adiciona a integração ao final do `app.py` e acrescenta `supabase` ao `requirements.txt`.

Integração manual no app.py:

```python
from social_layer import render_social_layer

render_social_layer(
    selected_community=selected_community,
    selected_country=selected_country,
    selected_sentiment=selected_sentiment,
    start_date=start_date,
    end_date=end_date,
    filtered=filtered,
    articles=articles,
    story=story if "story" in globals() else "",
)
```
