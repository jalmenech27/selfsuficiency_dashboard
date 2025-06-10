
# 🌾 Self-Sufficiency Dashboard

**Visualització interactiva de la sobirania alimentària global**  
Un projecte de *Data Visualization* dins la pràctica final del Màster en Ciència de Dades (UOC).

[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-fuchsia)](https://streamlit.io)  
[![License: CC0-1.0](https://img.shields.io/badge/license-CC0%201.0-lightgrey)](LICENSE)


---

## 🗺️ Objectiu

El quadre de comandament permet explorar, comparar i entendre la relació entre:

| Indicador | Descripció | Font |
|-----------|------------|------|
| **Self-Sufficiency Ratio (SSR)** | Producció pròpia vs. disponibilitat domèstica d’aliments | FAOSTAT (QCL + Trade) |
| **Export/Import Balance** | Pes de les exportacions i importacions en tones | FAOSTAT, Eurostat |
| **WomenAgriShare** | Quota femenina dins de la mà d’obra agrícola | World Bank WDI |
| **Food Footprint CO₂** | Emissions agrícoles (CO₂ eq) per tona produïda | FAOSTAT Emissions |
| **Producció vegetal / ramadera** | Evolució i volum de producció per país i cultiu | FAOSTAT QCL |

---

## 🗂️ Estructura del repositori

```
selfsuficiency_dashboard/
│
├── app.py                  # Lander + barra lateral global
│
├── pages/                  # Pàgines Streamlit
│   ├── 1_SSR.py
│   ├── 2_Export_Import.py
│   ├── 3_Gender.py
│   ├── 4_Emissions_CO2.py
│   └── 5_Production.py
│
├── data/
│   ├── fao_QCL.csv
│   ├── fao_FBS.csv
│   ├── fao_ET.csv
│   ├── fao_EI.csv
│   └── wb_gender.csv
│
└── utils/
    ├── loaders.py
    ├── indicators.py
    └── plotting.py
```

> 🔒 **Nota dades**  
> Els fitxers CSV no s’inclouen al GitHub per grandària; ves a `scripts/download_data.py` o a la Wiki del repo per saber com descarregar-los amb l’API de la FAO i del Banc Mundial.

---

## 🚀 Instal·lació ràpida

```bash
git clone https://github.com/jalmenech27/selfsuficiency_dashboard.git
cd selfsuficiency_dashboard

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python scripts/download_data.py     # opcional
```

---

## ▶️ Execució local

```bash
streamlit run app.py
```

La pàgina inicial mostra els KPI globals i la navegació lateral:

1. **SSR** – Autosuficiència alimentària  
2. **Export / Import** – Dades de comerç (exportacions i importacions)  
3. **Gender** – Participació femenina a l'agricultura
4. **Emissions CO₂** – Intensitat emissions   
5. **Production** – Tendències de producció  

---

## 📈 Metodologia

1. **Càrrega** de dades bulk (FAOSTAT, Eurostat, World Bank).
2. **Emmagatzematge** en CSV al directori `data/`.  
3. **Processament** i càlcul d’indicadors a `utils/indicators.py`.  
4. **Visualització** amb Streamlit + Plotly (Choropleth, Scatter, Boxplot…).  
5. **Cache** de resultats per accelerar experiència d’usuari (`@st.cache_data`).  

---

## ✍️ Autoria i crèdits

Projecte desenvolupat per **Jordi Almiñana Domènech · @jalmenech27**  
Màster en Ciència de Dades (UOC) · Assignatura *Visualització de Dades* (curs 2024-2025)

Fonts principals: FAO, World Bank, Eurostat. Paleta de colors de ColorBrewer i Viridis. Icons de [Font Awesome](https://fontawesome.com/).

---

## 📝 License

Aquest projecte es publica sota Creative Commons CC0 1.0 Universal – vegeu l’arxiu [LICENSE](LICENSE) per a més detalls.
