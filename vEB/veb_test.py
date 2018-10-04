import unittest
from veb import Veb

class TestStringMethods(unittest.TestCase):

    def test_ctor(self):
        b = Veb(8)
        b.insert(6)
        self.assertEqual(b.pred(7), 6)
        self.assertEqual(b.succ(1), 6)
        
    def test_structure(self):
        sut = Veb(15)
        sut.insert(0)
        sut.insert(10)
        # 1010 -> 10 10
        # insert have summary entry for 2
        self.assertEqual(2, sut.summary.max_x)
        # 2 inserted in cluster 2
        self.assertTrue(2, sut.clusters[2].max_x)
        
        sut.insert(11)
        self.assertTrue(3, sut.clusters[2].max_x)
        self.assertTrue(1, sut.clusters[2].clusters[1].max_x)

    def test_1wide(self):
        sut = Veb(1)
        sut.insert(0)
        self.assertEqual(sut.succ(0), None)
        self.assertEqual(sut.succ(1), None)
        self.assertEqual(sut.pred(0), None)
        self.assertEqual(sut.pred(1), 0)    
        
        sut.insert(1)
        self.assertEqual(sut.succ(0), 1)
        self.assertEqual(sut.succ(1), None)
        self.assertEqual(sut.pred(0), None)
        self.assertEqual(sut.pred(1), 0)        
        
        
    def test_2wide(self):
        sut = Veb(3)
        sut.insert(2)
        self.assertEqual(sut.succ(0), 2)
        self.assertEqual(sut.succ(1), 2)
        self.assertEqual(sut.succ(2), None)
        self.assertEqual(sut.succ(3), None)
        
        self.assertEqual(sut.pred(0), None)
        self.assertEqual(sut.pred(1), None)
        self.assertEqual(sut.pred(2), None)
        self.assertEqual(sut.pred(3), 2)
        
        sut.insert(3)
        self.assertEqual(sut.succ(0), 2)
        self.assertEqual(sut.succ(1), 2)
        self.assertEqual(sut.succ(2), 3)
        self.assertEqual(sut.succ(3), None)
        
        self.assertEqual(sut.pred(0), None)
        self.assertEqual(sut.pred(1), None)
        self.assertEqual(sut.pred(2), None)
        self.assertEqual(sut.pred(3), 2)
        
        sut.insert(0)
        self.assertEqual(sut.succ(0), 2)
        self.assertEqual(sut.succ(1), 2)
        self.assertEqual(sut.succ(2), 3)
        self.assertEqual(sut.succ(3), None)
        
        self.assertEqual(sut.pred(0), None)
        self.assertEqual(sut.pred(1), 0)
        self.assertEqual(sut.pred(2), 0)
        self.assertEqual(sut.pred(3), 2)
        
        sut.insert(1)
        self.assertEqual(sut.succ(0), 1)
        self.assertEqual(sut.succ(1), 2)
        self.assertEqual(sut.succ(2), 3)
        self.assertEqual(sut.succ(3), None)
        
        self.assertEqual(sut.pred(0), None)
        self.assertEqual(sut.pred(1), 0)
        self.assertEqual(sut.pred(2), 1)
        self.assertEqual(sut.pred(3), 2)
        
        
    def test_big_numbers(self):
        u = 1 << 31
        a = Veb(u)
        a.insert(1)
        a.insert(12345)
        a.insert(99999999)
        a.insert(750000)
        a.insert(750001)
        a.insert((1 << 16))
        a.insert((1 << 31) - 1)
        
        self.assertEqual(a.pred(2), 1)
        self.assertEqual(a.succ(2), 12345)
        self.assertEqual(a.succ(99999998), 99999999)
        self.assertEqual(a.pred(100000000), 99999999)
        self.assertEqual(a.pred(750001), 750000)
        self.assertEqual(a.pred((1 << 17)), 1 << 16)
        self.assertEqual(a.succ((1 << 30)), (1 << 31) - 1)
        
    def test_split_bits(self):
        a = Veb(15) # 4 bits
        self.assertEqual(a.split_bits(15), (3, 3)) # 1111 -> 11 11
        self.assertEqual(a.split_bits(10), (2, 2)) # 1010 -> 10 10
        self.assertEqual(a.split_bits(12), (3, 0)) # 1100 -> 11 00
        
        b = Veb(255) # 8 bits
        self.assertEqual(b.split_bits(255), (15, 15)) # 11111111 -> 1111 1111
        self.assertEqual(b.split_bits(0), (0, 0))   # 00000000 -> 0000 0000
        self.assertEqual(b.split_bits(15), (0, 15))   # 00001111 -> 0000 1111
        
        c = Veb(3)
        self.assertEqual(c.split_bits(3), (1, 1))
        self.assertEqual(c.split_bits(2), (1, 0))
        self.assertEqual(c.split_bits(1), (0, 1))
        
    def test_halve_universe(self):
        a = Veb(15) # 4 bits
        self.assertEqual(a.halve_universe(), 3) # 1111 -> 11
        
        b = Veb(255) # 8 bits
        self.assertEqual(b.halve_universe(), 15) # 11111111 -> 1111
        
        c = Veb(3) # 2 bits
        self.assertEqual(c.halve_universe(), 1) # 11 -> 1
        
    def test_print_ones(self):
        a = Veb(15)
        self.assertEqual(a.print_ones(15), '1111')
        self.assertEqual(a.print_ones(10), '1010')
        self.assertEqual(a.print_ones(3), '0011')
        self.assertEqual(a.print_ones(0), '0000')
        
    def test_universe_width(self):
        a = Veb(15)
        self.assertEqual(a.universe_width(15), 4)
        self.assertEqual(a.universe_width(5), 4)
        self.assertEqual(a.universe_width(3), 2)
        self.assertEqual(a.universe_width(2), 2)
        self.assertEqual(a.universe_width(1), 1)
    
        
        
if __name__ == '__main__':
    unittest.main()