import unittest
from veb import Veb

class TestStringMethods(unittest.TestCase):

    def test_ctor(self):
        b = Veb(8)
        b.insert(6)
        assert b.pred(7) == 6
        assert b.succ(1) == 6
        
    def test_big_numbers(self):
        u = 1 << 31
        a = Veb(u)
        print(a.U)
        a.insert(1)
        a.insert(12345)
        a.insert(99999999)
        a.insert(750000)
        a.insert(750001)
        a.insert((1 << 16))
        a.insert((1 << 31) - 1)
        
        print("Pred of 2 is 1")
        assert a.pred(2) == 1
        print("b")
        assert a.succ(2) == 12345
        print("c")
        assert a.succ(99999998) == 99999999
        print("d")
        assert a.pred(100000000) == 99999999
        print("e")
        assert a.pred(750001) == 750000
        print("f")
        assert a.pred((1 << 17)) == 1 << 16
        print("g")
        assert a.succ((1 << 30)) == (1 << 31) - 1
        
if __name__ == '__main__':
    unittest.main()