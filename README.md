
# 🌾 Self-Sufficiency Dashboard

**Visualització interactiva de la sobirania alimentària global**  
Un projecte de *Data Visualization* dins la pràctica final del Màster en Ciència de Dades (UOC).

[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-fuchsia)](https://streamlit.io)  
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

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
├── data/                   # CSV pre-processats (no versió LFS)
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
git clone https://github.com/<usuari>/selfsuficiency_dashboard.git
cd selfsuficiency_dashboard

python -m venv venv
source venv/bin/activate   # Windows: .env\Scriptsctivate

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
2. **Export / Import** – Comerç exterior  
3. **Gender** – Participació femenina  
4. **Emissions CO₂** – Intensitat emissiva  
5. **Production** – Tendències de producció  

---

## ⚙️ Configuració opcional

| Variable d’entorn | Propòsit | Exemple |
|-------------------|----------|---------|
| `MAPBOX_TOKEN`    | Tiles d’alta resolució als mapes Plotly | `pk.eyJ1IjoibWFwYm94dXNlciIsImEiOiJ...` |

Exporter: `st.download_button` et permet baixar qualsevol subset filtrat a CSV.

---

## 📈 Metodologia

1. **Càrrega** de dades bulk (FAOSTAT, Eurostat, World Bank).  
2. **Processament** i càlcul d’indicadors a `utils/indicators.py`.  
3. **Almacenament** en CSV (o Parquet) a `data/`.  
4. **Visualització** amb Streamlit + Plotly (Choropleth, Scatter, Boxplot…).  
5. **Cache** de resultats per accelerar experiència d’usuari (`@st.cache_data`).  

---

## ✍️ Autoria i crèdits

Projecte desenvolupat per **Jordi Almiñana Domènech**  
Màster de Ciència de Dades, UOC · Assignatura *Visualització de Dades* (curs 2024-2025)

Fonts principals: FAO, World Bank, Eurostat. Paleta de colors de ColorBrewer i Viridis. Icons de [Font Awesome](https://fontawesome.com/).

---

## 📝 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
