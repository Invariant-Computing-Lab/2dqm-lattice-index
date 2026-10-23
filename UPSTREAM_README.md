# 2DQM final manuscript and reproducibility package

## Package purpose
This archive contains a journal-ready generic manuscript, supplementary appendix, cover letter, locked external data, complete analysis code, unit tests, numerical outputs, publication figures, source material, and integrity hashes for the invariant-reduced two-dimensional worldsheet quark model (2DQM).

The package is written at a Q1-journal **methodological and reporting standard**, but no journal rank or acceptance outcome is implied. A selected journal's house style, article category, length limits, and reference format still need to be applied before upload.

## Final scientific result
The quotient/topological/algebraic invariant machinery survives the tested nuisance transformations and explicit synthetic lattice stress tests. The exact affine mass-squared spectral submodel does not survive the locked external test.

Primary PDG 2026 Upsilon(1S)-Upsilon(4S) result:
- chi-square = 70359.152 for 2 degrees of freedom; survival probability is far below machine-resolved double precision and is reported in the manuscript as p < 1e-300;
- unit-free R3 = 1.616220 vs exact-linear target 2;
- unit-free R4 = 2.044285 vs exact-linear target 3;
- adjacent Delta M^2 = 10.969379, 6.759548, 4.695608 GeV^2;
- spacing coefficient of variation = 0.4278;
- about 38.4% intrinsic fractional scatter in adjacent Delta M^2 is required for a constant-spacing description to reach chi-square/dof approximately one.

Accordingly, the normalized spectrum is retained as an invariant observable object, while the exact affine relation among its levels is rejected.

## Evidence boundary
The lattice calculation is an explicit Wilson/overlap-index stress test on smooth synthetic two-dimensional U(1) torus backgrounds. It does not establish that real quark flavor equals topological degree. The PDG test falsifies the exact affine spectral branch used here; it does not exclude every possible two-dimensional effective worldsheet model or replace QCD.

## Main deliverables
- `Manuscript_2DQM_Invariant_Reduction_Final.docx` / `.pdf`
- `Supplementary_Appendix_2DQM_Final.docx` / `.pdf`
- `Generic_Cover_Letter.docx` / `.pdf`
- `HIGHLIGHTS.txt`
- `SUBMISSION_CHECKLIST.md`
- `ANALYSIS_PROTOCOL.md`

## Reproducibility layout
- `data/` - source-locked PDG table used by the analysis
- `results/` - raw CSV/JSON numerical outputs and test logs
- `figures/` - 300-dpi publication figures
- `code/` - complete Python analysis, unit tests, requirements, environment snapshot
- `source_material/` - the supplied old mathematical appendix and invariant-framework notes
- `SHA256_MANIFEST.csv` - integrity manifest for package files

## Reproduction
Install the packages in `code/requirements.txt`, then from the package root run:

    python -m unittest discover -s code -p 'test_*.py' -v
    python code/run_all.py

`run_all.py` regenerates the core lattice-index outputs, spectral fits, Monte Carlo uncertainty table, intrinsic-spacing-scatter analysis, and figures from the locked CSV.
