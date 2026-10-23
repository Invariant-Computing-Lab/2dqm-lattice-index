from pathlib import Path
import json
from lattice_index import run as run_lattice
from spectral_falsification import run as run_spectrum

ROOT=Path(__file__).resolve().parents[1]
summary={'seed':20260812,'lattice':run_lattice(ROOT),'spectrum':run_spectrum(ROOT)}
(ROOT/'results'/'REPRODUCED_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
