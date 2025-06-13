# 🌾 Panell Global sobre l'Autosuficiència Alimentària 🌾

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://selfsuficiency.streamlit.app/)

**🚀 [Accés Directe al Dashboard](https://selfsuficiency.streamlit.app/)**

Aquest és un dashboard interactiu que analitza l'autosuficiència alimentària global utilitzant dades de FAOSTAT i el Banc Mundial. Una visualització completa de la sobirania alimentària mundial amb més de 15 gràfics interactius.

**📚 Projecte Final** - *Visualització de Dades* | Màster en Ciència de Dades (UOC) | 2024-2025

## ⭐ Característiques Principals

- 🌐 **Dashboard Live** a [Streamlit Cloud](https://selfsuficiency.streamlit.app/)
- 📊 **7 seccions interactives** amb 15+ visualitzacions 
- 🗺️ **Mapes interactius** amb dades de 245+ països
- 📈 **Gràfics animats** per evolució temporal
- 🎛️ **Controls dinàmics** per filtrar per any i regió
- 💾 **Dades optimitzades** (18MB vs 2.5GB originals)
- ⚡ **Carregada instantània** amb cache intel·ligent
- 📱 **Responsive design** per tots els dispositius

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Live%20on%20Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

> **💡 Tip:** Utilitza els botons de navegació ràpida a la barra lateral per saltar entre seccions del dashboard!

## 📊 Seccions del Dashboard

### 1. 📊 Indicadors Principals
- **Mètriques clau** amb targetes interactives (SSR, CO₂, Participació Femenina)
- **Distribucions estadístiques** amb línies de mitjana i mediana
- **Advertències sobre cobertura** temporal de les dades

### 2. 🗺️ Distribució Global
- **Mapa mundial d'autosuficiència** alimentària per país
- **Mapa mundial de petjada CO₂** per tona produïda
- **Visualització coroplètica** interactiva amb hover details

### 3. 🌍 Anàlisi Global
- **Context mundial** de producció i comerç
- **Distribucions avançades** d'indicadors
- **Estadístiques globals** agregades

### 4. 📈 Evolució Temporal
- **Tendències regionals** al llarg del temps (1990-2020+)
- **Línies de mitjana mundial** destacades en negre
- **Canvis temporals en autosuficiència** (2000-2013) per països
- **Filtratge per blocs regionals**

### 5. 🥗 Anàlisi de Productes
- **Top productes** per producció, importació i exportació
- **Balanç comercial** amb indicadors d'importadors/exportadors nets
- **Paleta de colors consistent** entre visualitzacions
- **Anàlisi de trade flows** globals

### 6. 🔗 Anàlisi de Correlacions
- **Scatter plots** amb correlacions estadístiques
- **Gràfics animats** per evolució temporal de correlacions
- **Interpretació automàtica** de la força de correlació
- **Anàlisi per blocs regionals**

### 7. 👩‍🌾 Perspectiva de Gènere
- **Distribució de participació femenina** amb estadístiques
- **Gràfic per blocs regionals** amb colors distintius
- **Evolució temporal** amb mitjana mundial destacada

## 📊 Indicadors Analitzats

Explorar, comparar i entendre la sostenibilitat i la sobirania alimentària a escala mundial amb cinc indicadors clau:

| Indicador | Descripció | Font |
|-----------|------------|------|
| **Self‑Sufficiency Ratio (SSR)** | Producció pròpia vs. disponibilitat domèstica | FAOSTAT |
| **Export/Import Balance** | Pes de les exportacions i importacions | FAOSTAT, Eurostat |
| **WomenAgriShare** | Quota femenina dins la mà d'obra agrícola | World Bank WDI |
| **Food Footprint CO₂** | Emissions agrícoles per tona produïda | FAOSTAT Emissions |
| **Producció vegetal / ramadera** | Volum i evolució de producció | FAOSTAT |


## 📁 Estructura del Projecte

```
selfsuficiency_dashboard/
├── app.py                    # Aplicació principal integrada
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

## Pipeline de Dades

### Descàrrega Automàtica
```bash
# Descarregar totes les dades necessàries
python data_download.py
```

### Preprocessament de Dades
```bash
# Processar dades raw de FAOSTAT i World Bank
python scripts/preprocess_data.py
```

### Fonts de Dades
- **FAOSTAT** (FAO): Producció, comerç i emissions agrícoles
- **World Bank**: Dades d'ocupació femenina en agricultura
- **Periode**: 1990-2023 (segons disponibilitat)

### Optimització de Dades
- **Compressió**: Fitxers CSV.gz (reducció del 85% en mida)
- **Aggregació**: Càlculs precomputats d'indicadors
- **Filtratge**: Només dades rellevants per a l'anàlisi

## ✨ Funcionalitats Destacades

### 🎛️ Controls Interactius
- **Selecció d'any**: Slider temporal per explorar evolució històrica
- **Filtratge regional**: Checkbox per seleccionar blocs geogràfics específics
- **Navegació ràpida**: Botons sticky per saltar entre seccions

### 📊 Visualitzacions Avançades
- **Gràfics animats**: Evolució temporal amb controls de reproducció
- **Correlacions automàtiques**: Interpretació intel·ligent de coeficients
- **Mapes interactius**: Hover details amb informació contextual
- **Estadístiques en temps real**: Càlcul dinàmic de mitjanes i medianes

### 🎨 Experiència d'Usuari
- **Navegació d'una sola pàgina**: Fluïdesa sense recàrregues
- **Responsive design**: Adaptat a mòbil, tablet i escriptori
- **Carregada optimitzada**: Cache intel·ligent per velocitat màxima
- **Indicadors visuals**: Codificació per colors i icones intuïtives

## 🗺️ Blocs Regionals

- **EU27**: 27 països de la Unió Europea
- **Amèrica Llatina i Carib**: 33 països
- **Àfrica Subsahariana**: 48 països  
- **Nord d'Àfrica**: 5 països
- **Àsia Oriental i Sud-oriental**: 17 països
- **Àsia Meridional**: 9 països
- **Àsia Occidental i Àsia Central**: 22 països
- **Amèrica del Nord**: 2 països
- **Oceania**: 14 països

## 📊 Indicadors Calculats

### Autosuficiència Alimentària (SSR)
```
SSR = Producció / (Producció + Importacions - Exportacions)
```

### Petjada Alimentària CO₂
```
FF = Emissions Totals CO₂ / Producció Total
```

### Participació Femenina
Percentatge de dones en el sector agrícola per país


## 🔧 Optimitzacions Tècniques

- **Compressió eficient**: Reducció del 99.2% de la mida original (2.5GB → 18MB)
- **Format CSV.gz**: Màxima compatibilitat i compressió
- **Caching multi-nivell**: Dades, càlculs i visualitzacions en cache
- **Arquitectura modular**: Utils separats per fàcil manteniment
- **Fallbacks robustos**: Compatibilitat amb dades originals si cal

## 📊 Fonts de Dades

- **FAOSTAT**: Organització de les Nacions Unides per a l'Alimentació i l'Agricultura
- **World Bank**: Indicadors de desenvolupament mundial
- **Període temporal**: 1961-2023
- **Cobertura geogràfica**: 245+ països i territoris

## ⚙️ Instal·lació i Ús

### 🌐 Accés Online (Recomanat)
**Dashboard Live**: **[selfsuficiency.streamlit.app](https://selfsuficiency.streamlit.app/)**

No cal instal·lar res! Accedeix directament al dashboard a través del navegador.

### 💻 Execució Local 

### Opció 1: Execució Directa
```bash
# Clonar el repositori
git clone https://github.com/username/selfsuficiency_dashboard.git
cd selfsuficiency_dashboard

# Instal·lar dependències
pip install -r requirements.txt

# Executar el dashboard (utilitza dades preprocessades)
streamlit run app.py
```

### Opció 2: Regenerar Dades des de Zero
```bash
# 1. Descarregar dades raw (seguir instruccions manuals)
python scripts/data_download.py

# 2. Processar dades raw → dades optimitzades
python scripts/preprocess_data.py

# 3. Executar dashboard
streamlit run app.py
```

### Dependències Principals
```bash
streamlit>=1.30.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
geopandas>=0.14.0  
```
---

## 📈 Estadístiques del Projecte

- **🌍 Cobertura**: 245+ països i territoris
- **📅 Temporal**: Dades des de 1961 fins 2023
- **📊 Visualitzacions**: 15+ gràfics interactius
- **💾 Optimització**: 18MB vs 2.5GB originals (99.2% reducció)
- **⚡ Rendiment**: Cache multi-nivell per velocitat òptima
## 🌐 Accés Online

## ✍️ Autoria

**Jordi Almiñana Domènech** - @jalmenech27  
Màster en Ciència de Dades (UOC) - Visualització de Dades  
Curs 2024-2025

## 📝 Llicència

Creative Commons CC0 1.0 Universal - Lliure d'usos amb atribució voluntària

---

**🔗 Links Útils:**
- 📊 [Dashboard Live](https://selfsuficiency.streamlit.app/)
- 💻 [Codi Font](https://github.com/jalmenech27/selfsuficiency_dashboard)
- 📋 [FAOSTAT](https://www.fao.org/faostat/)
- 🏦 [World Bank Data](https://data.worldbank.org/)
