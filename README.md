
# 🌾 Self-Sufficiency Dashboard

**Visualització interactiva de la sobirania alimentària global**  
Un projecte de *Data Visualization* dins la pràctica final del Màster en Ciència de Dades (UOC).

[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-fuchsia)](https://streamlit.io)  
[![License: CC0-1.0](https://img.shields.io/badge/license-CC0%201.0-lightgrey)](LICENSE)

---

## 🗺️ Objectiu

Explorar, comparar i entendre la sostenibilitat i la sobirania alimentària a escala mundial amb cinc indicadors clau:

| Indicador | Descripció | Font |
|-----------|------------|------|
| **Self‑Sufficiency Ratio (SSR)** | Producció pròpia vs. disponibilitat domèstica | FAOSTAT |
| **Export/Import Balance** | Pes de les exportacions i importacions | FAOSTAT, Eurostat |
| **WomenAgriShare** | Quota femenina dins la mà d’obra agrícola | World Bank WDI |
| **Food Footprint CO₂** | Emissions agrícoles per tona produïda | FAOSTAT Emissions |
| **Producció vegetal / ramadera** | Volum i evolució de producció | FAOSTAT |

---

## 🗂️ Estructura del repositori

```
selfsuficiency_dashboard/
│
├── app.py
├── pages/                 # Pàgines Streamlit
│   ├── 1_SSR.py
│   ├── 2_Export_Import.py
│   ├── 3_Gender.py
│   ├── 4_Emissions_CO2.py
│   └── 5_Production.py
│
├── utils/                 # Càrrega, indicadors i gràfics
│   ├── loaders.py
│   ├── indicators.py
│   └── plotting.py
│
├── scripts/               # Utilitats de línia d’ordres
│   └── download_data.py   # ↩︎ baixa i descomprimeix els datasets FAO
│
├── data/                  # S’omple via download_data.py
│   ├── fao_QCL.csv
│   ├── fao_FBS.csv
│   ├── fao_ET.csv
│   ├── fao_EI.csv
│   └── wb_gender.csv
└── README.md
```

> 🔒 **Nota datasets**  
> Per mantenir el repositori lleuger, els CSV massius (> 25 MB) no es versionen.  
> Executa **`python scripts/download_data.py`** per descarregar automàticament els quatre paquets *bulk* de FAOSTAT i extreure els `*_Normalized.csv` dins `./data/`.

---

## 🚀 Instal·lació ràpida

```bash
git clone https://github.com/jalmenech27/selfsuficiency_dashboard.git
cd selfsuficiency_dashboard

python -m venv venv && source venv/bin/activate   # Windows: .env\Scriptsctivate
pip install -r requirements.txt

# 👉 Descarrega datasets (pot trigar uns minuts i ocupar ~2,5 GB)
python scripts/download_data.py
```

---

## ▶️ Execució local

```bash
streamlit run app.py
```

La siderbar et permet navegar:

1. **SSR** – Autosuficiència  
2. **Export / Import** – Comerç exterior  
3. **Gender** – Participació femenina  
4. **Emissions CO₂** – Intensitat emissiva  
5. **Production** – Tendències de producció  

---

## 📈 Metodologia

1. **Càrrega** dels *bulk* FAO/World Bank → `scripts/download_data.py`.  
2. **Almacenament** en CSV a `data/`.  
3. **Processament** i càlcul d’indicadors a `utils/indicators.py`.  
4. **Visualització** amb Streamlit + Plotly.  
5. **Cache** (`@st.cache_data`) per millorar el rendiment en temps real.

---

## ✍️ Autoria i crèdits

Projecte de **Jordi Almiñana Domènech**  
Màster de Ciència de Dades – UOC (2024‑2025)

Fonts: FAOSTAT, World Bank, Eurostat. Paleta ColorBrewer/Viridis. Icons FontAwesome.

---

## 📝 License

Publicat sota **Creative Commons CC0 1.0 Universal** – lliure d’usos amb atribució voluntària.
