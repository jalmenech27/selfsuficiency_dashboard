# Dashboard d'Autosuficiència Alimentària Global - Versió Integrada 🌾

Aquest és un dashboard interactiu d'una sola pàgina que analitza l'autosuficiència alimentària global utilitzant dades preprocessades de FAOSTAT i el Banc Mundial.

## 🎯 Característiques Principals

- **Dashboard d'una sola pàgina** amb navegació fluida entre seccions
- **Dades preprocessades** (18MB total vs 2.5GB originals) 
- **Compatible amb Streamlit Cloud** (tots els fitxers <25MB)
- **6 seccions interactives** amb més de 15 visualitzacions
- **Navegació ràpida** amb botons de salts directes
- **Filtratge dinàmic** per any i blocs regionals

## 📊 Seccions del Dashboard

### 1. 📊 Indicadors Principals
- Mètriques clau d'autosuficiència, petjada CO₂ i participació femenina
- Distribucions dels indicadors principals
- Targetes de mètriques amb estil personalitzat

### 2. 🗺️ Distribució Global  
- Mapa mundial d'autosuficiència alimentària
- Mapa mundial de petjada de carboni
- Visualització coroplètica interactiva

### 3. 📈 Evolució Temporal
- Tendències per blocs regionals al llarg del temps
- Evolució de l'autosuficiència i petjada CO₂
- Gràfics de línies multi-sèrie

### 4. 🥗 Anàlisi de Productes
- Top 10 productes per producció i importació
- Balanç comercial per producte
- Comparatives import-export

### 5. 🔗 Anàlisi de Correlacions
- Correlació autosuficiència vs petjada de carboni
- Correlació participació femenina vs autosuficiència  
- Scatter plots amb línies de tendència

### 6. 👩‍🌾 Perspectiva de Gènere
- Distribució de participació femenina per regions
- Evolució temporal de la participació femenina
- Anàlisi de l'impacte del gènere en l'agricultura

## 🚀 Execució

### Instal·lació
```bash
pip install -r requirements.txt
```

### Execució Local
```bash
streamlit run app.py
```

### Desplegament a Streamlit Cloud
1. Puja el repositori a GitHub
2. Connecta amb Streamlit Cloud
3. L'aplicació es desplegarà automàticament

## 📁 Estructura

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

## 🎨 Funcionalitats Avançades

- **Navegació ràpida**: Botons sticky per saltar entre seccions
- **Filtratge intel·ligent**: Selecció d'any i regions amb actualització automàtica
- **Visualitzacions responsives**: Adapten a qualsevol mida de pantalla
- **Correlacions automàtiques**: Càlcul i interpretació de correlacions
- **Estil personalitzat**: CSS customitzat per una UX premium
- **Caching optimitzat**: Càrrega instantània de dades amb `@st.cache_data`

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

## ✍️ Autoria

**Jordi Almiñana Domènech** - @jalmenech27  
Màster en Ciència de Dades (UOC) - Visualització de Dades  
Curs 2024-2025

## 📝 Llicència

Creative Commons CC0 1.0 Universal - Lliure d'usos amb atribució voluntària
