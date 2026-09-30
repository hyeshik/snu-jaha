import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_weight_range import raster_weight_is_ordered


class WeightRangeAuditTests(unittest.TestCase):
    def test_equal_area_arrow_antialiasing_does_not_hide_weight_reversals(self):
        self.assertTrue(raster_weight_is_ordered(1385846, 1385806, 82923.5, 82923.5))
        self.assertFalse(raster_weight_is_ordered(1386062, 1385806, 82923.5, 82923.5))
        self.assertFalse(raster_weight_is_ordered(1385846, 1385806, 82924.0, 82923.5))
