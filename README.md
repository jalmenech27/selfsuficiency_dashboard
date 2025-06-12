# Dashboard d'Autosuficiència Alimentària Global - Versió Integrada 🌾

Aquest és un dashboard interactiu d'una sola pàgina que analitza l'autosuficiència alimentària global utilitzant dades preprocessades de FAOSTAT i el Banc Mundial.

**Visualització interactiva de la sobirania alimentària global**  
Un projecte de *Data Visualization* dins la pràctica final de l'assignatura *Visualització de Dades* del Màster en Ciència de Dades (UOC).

- **Dashboard d'una sola pàgina** amb navegació fluida entre seccions
- **Dades preprocessades** (18MB total vs 2.5GB originals) 
- **Compatible amb Streamlit Cloud** (tots els fitxers <25MB)
- **6 seccions interactives** amb més de 15 visualitzacions
- **Navegació ràpida** amb botons de salts directes
- **Filtratge dinàmic** per any i blocs regionals

---

### 2. 🗺️ Distribució Global  
- Mapa mundial d'autosuficiència alimentària
- Mapa mundial de petjada de carboni
- Visualització coroplètica interactiva

Explorar, comparar i entendre la sostenibilitat i la sobirania alimentària a escala mundial amb cinc indicadors clau:

| Indicador | Descripció | Font |
|-----------|------------|------|
| **Self‑Sufficiency Ratio (SSR)** | Producció pròpia vs. disponibilitat domèstica | FAOSTAT |
| **Export/Import Balance** | Pes de les exportacions i importacions | FAOSTAT, Eurostat |
| **WomenAgriShare** | Quota femenina dins la mà d’obra agrícola | World Bank WDI |
| **Food Footprint CO₂** | Emissions agrícoles per tona produïda | FAOSTAT Emissions |
| **Producció vegetal / ramadera** | Volum i evolució de producció | FAOSTAT |

### 5. 🔗 Anàlisi de Correlacions
- Correlació autosuficiència vs petjada de carboni
- Correlació participació femenina vs autosuficiència  
- Scatter plots amb línies de tendència

### 6. 👩‍🌾 Perspectiva de Gènere
- Distribució de participació femenina per regions
- Evolució temporal de la participació femenina
- Anàlisi de l'impacte del gènere en l'agricultura

```
selfsuficiency_dashboard/
│
├── app.py
├── pages/                 
│   ├── 1_SSR.py
│   ├── 2_Export_Import.py
│   ├── 3_Gender.py
│   ├── 4_Emissions_CO2.py
│   └── 5_Production.py
│
├── utils/                 
│   ├── loaders.py
│   ├── indicators.py
│   └── plotting.py
│
├── scripts/               
│   └── download_data.py   # baixa i descomprimeix els datasets FAO
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

### Instal·lació
```bash
git clone https://github.com/jalmenech27/selfsuficiency_dashboard.git
cd selfsuficiency_dashboard

python -m venv venv && source venv/bin/activate   
pip install -r requirements.txt

# 👉 Descarrega datasets (pot trigar uns minuts i ocupar ~2,5 GB)
python scripts/download_data.py
```

### Execució Local
```bash
streamlit run app.py
```

La siderbar et permet navegar:

1. **SSR** – Autosuficiència  
2. **Export / Import** – Comerç exterior  
3. **Gender** – Participació femenina  
4. **Emissions CO₂** – Intensitat emissiva  
5. **Production** – Tendències de producció  

```
integrated_dashboard/
├── app.py                    # Aplicació principal
├── utils/
│   ├── loaders.py           # Funcions de càrrega de dades
│   ├── indicators.py        # Càlculs d'indicadors
│   └── plotting.py          # Funcions de visualització
├── data/                    # Dades preprocessades (CSV.gz)
│   ├── ssr_women.csv.gz     # Autosuficiència + gènere
│   ├── food_footprint.csv.gz
│   ├── production.csv.gz
│   ├── imports.csv.gz
│   ├── exports.csv.gz
│   └── *.csv.gz
├── requirements.txt
└── README.md
```

## 🗺️ Blocs Regionals

1. **Càrrega** dels *bulk* FAO/World Bank → `scripts/download_data.py`.  
2. **Emmagatzement** en CSV a `data/`.  
3. **Processament** i càlcul d’indicadors a `utils/indicators.py`.  
4. **Visualització** amb Streamlit + Plotly.  
5. **Cache** (`@st.cache_data`) per millorar el rendiment en temps real.

## 📊 Indicadors Calculats

### Autosuficiència Alimentària (SSR)
```
SSR = Producció / (Producció + Importacions - Exportacions)
```

Projecte desenvolupat per **Jordi Almiñana Domènech - @jalmenech27**  
Màster de Ciència de Dades, UOC · Assignatura *Visualització de Dades* (curs 2024-2025)

Fonts: FAOSTAT, World Bank, Eurostat. Paleta ColorBrewer/Viridis. Icons FontAwesome.

## 🎨 Funcionalitats Avançades

- **Navegació ràpida**: Botons sticky per saltar entre seccions
- **Filtratge intel·ligent**: Selecció d'any i regions amb actualització automàtica
- **Visualitzacions responsives**: Adapten a qualsevol mida de pantalla
- **Correlacions automàtiques**: Càlcul i interpretació de correlacions
- **Estil personalitzat**: CSS customitzat per una UX premium
- **Caching optimitzat**: Càrrega instantània de dades amb `@st.cache_data`

Publicat sota **Creative Commons CC0 1.0 Universal** – lliure d’usos amb atribució voluntària.
