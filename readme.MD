# 🌦️ Dashboard de Clima em Tempo Real

Este é um projeto interativo desenvolvido com **Python + Streamlit**, que permite ao usuário consultar:

- 🌍 Clima atual de qualquer cidade
- 📆 Previsão dos próximos 5 dias
- 📈 Gráficos interativos com Plotly
- 🕓 Histórico de buscas salvas em sessão

---

## 📸 Site

![Link site](https://weatherdb.streamlit.app)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.9+
- [Streamlit](https://streamlit.io/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- Plotly (visualização gráfica)
- dotenv (gerenciar variáveis de ambiente)
- Meteostat (opcional para clima histórico)

---

## 🚀 Como executar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/dashboard-clima-streamlit.git
cd dashboard-clima-streamlit

2. Crie um ambiente virtual e ative

python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Mac/Linux
3. Instale as dependências

pip install -r requirements.txt

4. Configure sua chave da API
Crie um arquivo .env na raiz do projeto com:

env
OPENWEATHER_API_KEY=sua_chave_aqui
Obtenha sua chave em: https://openweathermap.org/appid

5. Execute o app


streamlit run index.py
📂 Estrutura do Projeto


📁 dashboard-clima/
├── .env
├── index.py
├── requirements.txt
└── README.md
✅ Funcionalidades
Pesquisa por cidade

Navegação por abas com menu horizontal

Exibição de ícones do clima, métricas e descrição

Gráficos de temperatura mínima/máxima com Plotly

Histórico de buscas salvas durante a sessão

📌 Observações
As buscas e dados são temporários e não ficam salvos após fechar o app.

O projeto é ideal para aprendizado de APIs, Streamlit e visualização de dados.

