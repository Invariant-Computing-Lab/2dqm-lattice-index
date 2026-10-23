# Final analysis protocol and failure gates

## Objective
Reduce the supplied 2DQM to quantities defined relative to explicit nuisance transformations, then attempt to falsify the surviving structures rather than rescue them post hoc.

## Locked transformation families
- parameter redistribution in the supplied classical coefficient;
- worldsheet coordinate/reparameterization changes;
- Lorentz-frame changes;
- local U(1) gauge transformations in the synthetic lattice sector;
- unit rescaling;
- basis/conjugacy transformations.

## Failure gates
1. **Gauge/topology:** the lattice overlap index must reproduce the oriented integer degree on the smooth synthetic backgrounds and remain unchanged under local gauge transformations.
2. **Discriminant:** a change of index along the adversarial interpolation must be accompanied by near-closure of the Hermitian Wilson-kernel gap.
3. **Unit/basis:** any claimed spectral fingerprint must survive unit and basis changes; raw dimensionful coefficients are not accepted as unit-invariant numbers.
4. **External spectrum:** the explicitly labeled PDG 2026 Upsilon(1S)-Upsilon(4S) sequence is the primary source-locked test. No relabeling or state insertion is permitted after inspecting residuals.
5. **Claim gate:** if the exact affine mass-squared law fails, it is removed from the physical model. It is not repaired by redefining units, absorbing 2pi into q, or changing the intercept.
6. **Flavor boundary:** line-bundle degree/topological index is not identified with quark flavor without an independent flavor mapping.

## Primary model
For radial label n=1,...,4,

    M_n^2 = beta_0 + kappa (n - 1).

The dimensionless shape diagnostic is

    R_n = (M_n^2 - M_1^2) / (M_2^2 - M_1^2),

for which the exact affine law predicts R_n=n-1.

## External-data lock
The primary masses are transcribed from the official 2026 Particle Data Group meson summary and stored in `data/pdg2026_bottomonium_locked.csv`. Secondary chi_b1 and chi_b2 sequences are sensitivity analyses only because the same PDG summary flags the relevant J assignments as needing confirmation.

## Interpretation rule
Synthetic/lattice tests establish only the mathematical behavior of the tested invariant constructions. The PDG test addresses only the explicit affine spectral submodel. Neither result establishes physical quark substructure or a flavor-topology correspondence.
