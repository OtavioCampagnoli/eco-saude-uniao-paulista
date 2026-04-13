# eco-saude-uniao-paulista

## EcoSaúde UP — Checklist & Dashboard (ODS 6)

App em **Streamlit** (pt-BR) para registrar **inspeções** (checklist) e gerar um **dashboard** de
Meio Ambiente & Saúde (foco em **ODS 6: Água potável e saneamento**).

## Funcionalidades (MVP)
- Criar inspeção por setor (banheiros, bebedouros, etc.)
- Salvar localmente em CSV (`data/inspections.csv`)
- Dashboard com score e gráficos
- Recomendações automáticas (regras simples)

## Como rodar (local)
### 1) Criar venv e instalar dependências
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Rodar o app
```bash
streamlit run app/main.py
```

### 3) Rodar testes
```bash
pytest -q
```

## Estrutura
- `app/main.py`: entrypoint Streamlit
- `app/ui`: páginas e componentes
- `app/domain`: modelos e regras (score, recomendações)
- `app/services`: casos de uso
- `app/infra`: persistência CSV (repository)

---

Projeto desenvolvido por **Otávio Campagnoli**.