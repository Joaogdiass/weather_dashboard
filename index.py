import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import plotly.graph_objs as go
from meteostat import Daily, Point
import pytz

# Carrega API Key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Funções auxiliares
def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    res = requests.get(url).json()
    if res:
        return res[0]['lat'], res[0]['lon']
    return None, None

def buscar_clima(cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    return None

def buscar_previsao(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

# Configuração da página
st.set_page_config(page_title="Clima em Tempo Real", page_icon="⛅", layout="wide")
st.title("🌦️ Dashboard de Clima em Tempo Real")

# Verificação da API
if not API_KEY:
    st.error("❌ Chave da API não encontrada. Verifique o .env.")
    st.stop()

# Histórico de busca
if "historico" not in st.session_state:
    st.session_state.historico = []

# Cidade
cidade = st.text_input("Digite o nome da cidade:", "São Paulo")

# Menu de navegação
pagina = st.radio(
    "Navegue pelas seções:",
    ["🌍 Clima Atual", "📆 Previsão", "📈 Gráfico", "🕓 Histórico de Buscas"],
    horizontal=True
)

# Processamento
if cidade:
    dados = buscar_clima(cidade)
    lat, lon = get_coordinates(cidade)

    if dados and lat and lon:
        st.session_state.historico.append(cidade)

        if pagina == "🌍 Clima Atual":
            st.subheader(f"📍 {dados['name']}, {dados['sys']['country']}")
            icon_code = dados['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            st.image(icon_url, width=100)

            col1, col2, col3 = st.columns(3)
            col1.metric("🌡️ Temperatura", f"{dados['main']['temp']}°C")
            col2.metric("🥵 Sensação Térmica", f"{dados['main']['feels_like']}°C")
            col3.metric("💧 Umidade", f"{dados['main']['humidity']}%")

            col4, col5, col6 = st.columns(3)
            col4.metric("🌀 Pressão", f"{dados['main']['pressure']} hPa")
            col5.metric("☁️ Nuvens", f"{dados['clouds']['all']}%")
            col6.metric("🌬️ Vento", f"{dados['wind']['speed']} m/s")

            nascer = datetime.fromtimestamp(dados['sys']['sunrise']).strftime('%H:%M')
            por = datetime.fromtimestamp(dados['sys']['sunset']).strftime('%H:%M')
            st.write(f"🌅 Nascer do sol: {nascer} | 🌇 Pôr do sol: {por}")
            st.success(f"📖 Condição: {dados['weather'][0]['description'].capitalize()}")

        elif pagina == "📆 Previsão":
            previsao = buscar_previsao(lat, lon)
            if previsao:
                st.subheader("📅 Previsão para os próximos 5 dias")
                dias = {}
                for item in previsao["list"]:
                    dt = datetime.fromtimestamp(item["dt"])
                    dia = dt.strftime('%d/%m')
                    if dia not in dias:
                        dias[dia] = {
                            "temp_min": item["main"]["temp_min"],
                            "temp_max": item["main"]["temp_max"],
                            "desc": item["weather"][0]["description"],
                            "icon": item["weather"][0]["icon"]
                        }
                    else:
                        dias[dia]["temp_min"] = min(dias[dia]["temp_min"], item["main"]["temp_min"])
                        dias[dia]["temp_max"] = max(dias[dia]["temp_max"], item["main"]["temp_max"])

                for dia, dados_dia in list(dias.items())[:5]:
                    col1, col2 = st.columns([1, 8])
                    with col1:
                        st.image(f"http://openweathermap.org/img/wn/{dados_dia['icon']}@2x.png", width=60)
                    with col2:
                        st.markdown(f"**{dia}** — {dados_dia['desc'].capitalize()} 🌡️ {dados_dia['temp_min']}°C ~ {dados_dia['temp_max']}°C")

        elif pagina == "📈 Gráfico":
            previsao = buscar_previsao(lat, lon)
            if previsao:
                dias = {}
                for item in previsao["list"]:
                    dt = datetime.fromtimestamp(item["dt"])
                    dia = dt.strftime('%d/%m')
                    if dia not in dias:
                        dias[dia] = {
                            "temp_min": item["main"]["temp_min"],
                            "temp_max": item["main"]["temp_max"]
                        }
                    else:
                        dias[dia]["temp_min"] = min(dias[dia]["temp_min"], item["main"]["temp_min"])
                        dias[dia]["temp_max"] = max(dias[dia]["temp_max"], item["main"]["temp_max"])

                st.subheader("📊 Gráfico de Temperatura (5 dias)")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(dias.keys()),
                    y=[v["temp_max"] for v in dias.values()],
                    mode='lines+markers',
                    name='Temp Máx',
                    line=dict(color='firebrick')
                ))
                fig.add_trace(go.Scatter(
                    x=list(dias.keys()),
                    y=[v["temp_min"] for v in dias.values()],
                    mode='lines+markers',
                    name='Temp Mín',
                    line=dict(color='royalblue')
                ))
                fig.update_layout(xaxis_title='Dia', yaxis_title='Temperatura (°C)', height=400)
                st.plotly_chart(fig, use_container_width=True)

        elif pagina == "🕓 Histórico de Buscas":
            st.subheader("📍 Histórico de buscas")
            st.write(list(set(st.session_state.historico)))

    else:
        st.error("❌ Cidade não encontrada ou erro na API.")
else:
    st.info("Digite o nome de uma cidade para começar.")
