import unittest
import numpy as np
from lattice_index import torus_u1_links, overlap_index

class TestInvariantCore(unittest.TestCase):
    def test_overlap_index_matches_degree_orientation(self):
        for d in range(-3,4):
            idx,_=overlap_index(*torus_u1_links(8,d))
            self.assertEqual(idx,-d)

    def test_unit_free_spectral_ratio(self):
        masses=np.array([9.46040,10.0234,10.3551,10.5794])
        y=masses**2
        R=(y-y[0])/(y[1]-y[0])
        u=123.456
        yu=u*y
        Ru=(yu-yu[0])/(yu[1]-yu[0])
        np.testing.assert_allclose(R,Ru,rtol=0,atol=1e-12)

if __name__=='__main__': unittest.main()
