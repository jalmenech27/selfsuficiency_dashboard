# Build a ready-to-use download_data.py script
script = """
\"\"\"download_data.py
Descarrega automàticament els *bulk downloads* de FAOSTAT,
extreu el fitxer *_Normalized.csv* i el desa a ./data/ amb nom curt.

Ús:
    python download_data.py          # baixa tots els datasets
    python download_data.py QCL FBS  # baixa només aquests codis

Requeriments:
    pip install requests tqdm pandas
\"\"\"

import sys, zipfile, io, os, requests, pathlib
from tqdm import tqdm
import pandas as pd

# ---------------- Configuració ---------------- #
DATA_DIR = pathlib.Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Enllaços FAOSTAT bulk (.zip) -> nom curt per al CSV resultant
DATASETS = {
    "QCL": (
        "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip",
        "fao_QCL.csv",
    ),
    "FBS": (
        "https://bulks-faostat.fao.org/production/FoodBalanceSheetsHistoric_E_All_Data_(Normalized).zip",
        "fao_FBS.csv",
    ),
    "ET": (
        "https://bulks-faostat.fao.org/production/Emissions_Totals_E_All_Data_(Normalized).zip",
        "fao_ET.csv",
    ),
    "EI": (
        "https://bulks-faostat.fao.org/production/Environment_Emissions_intensities_E_All_Data_(Normalized).zip",
        "fao_EI.csv",
    ),
}

CHUNK = 2**20  # 1 MiB


def download_and_extract(code: str):
    url, out_csv = DATASETS[code]
    out_path = DATA_DIR / out_csv
    if out_path.exists():
        print(f"[{code}] {out_csv} ja existeix — ometo.")
        return

    print(f"[{code}] Descarregant {url}")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0)) // CHUNK
        buf = io.BytesIO()
        for chunk in tqdm(r.iter_content(CHUNK), total=total, unit="MB", unit_scale=True):
            buf.write(chunk)

    buf.seek(0)
    with zipfile.ZipFile(buf) as z:
        # busquem el .csv normalitzat
        fname = next(n for n in z.namelist() if n.lower().endswith("_normalized.csv"))
        print(f"[{code}] Extraient {fname}")
        with z.open(fname) as f_in:
            df = pd.read_csv(f_in, low_memory=False)
            df.to_csv(out_path, index=False)
    print(f"[{code}] Guardat a {out_path.relative_to(DATA_DIR.parent)}")


def main(argv):
    codes = argv[1:] or DATASETS.keys()
    for code in codes:
        if code not in DATASETS:
            print(f"⚠️  Codi {code} no reconegut — disponibles: {', '.join(DATASETS)}")
            continue
        download_and_extract(code)


if __name__ == "__main__":
    main(sys.argv)
"""

file_path = "/mnt/data/download_data.py"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(script)

file_path
