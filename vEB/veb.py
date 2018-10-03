from math import log
from math import ceil

class Veb:
    def __init__(self, U):
        self.U = (1 << self.universe_width(U)) - 1
        print(self.U)
        self.max_x = None
        self.min_x = None
        m2 = self.halve_universe(self.U)
        if(m2 > 1):
            self.summary = Veb(m2)
            self.clusters = {}
    
    def insert(self, x):
        if (x < 0) or (x > self.U):
            raise AssertionError("{} is not between 0 and {}".format(x, self.U))
        if self.min_x == None:
            self.min_x = x
            self.max_x = x
            return
        to_insert = x
        if x < self.min_x:
            to_insert = self.min_x
            self.min_x = x
        if to_insert > self.max_x:
            self.max_x = to_insert
        c, i = self.split_bits(to_insert)
        if c not in self.clusters:
            self.clusters[c] = Veb(self.halve_universe(self.U))
            self.summary.insert(c)
        self.clusters[c].insert(i)
        
    def pred(self, x):
        if (self.min_x == None) or x <= self.min_x:
            return None
        if x > self.max_x:
            return self.max_x
        c, i = self.split_bits(x)
        hi = x - i
        half_width = int(self.universe_width(self.U) / 2)
        print("c: " + str(c))
        print("i: " + str(i))
        print("hi: " + str(hi))
        print(self.summary.clusters)
        print("min: " + str(self.min_x))
        print("max: " + str(self.max_x))
        print(c in self.clusters)
        print(self.clusters[c].min_x)
        if c in self.clusters and self.clusters[c].min_x < x:
            return hi + self.clusters[c].pred(i)
        else:
            cid = self.summary.pred(c)
            return hi + self.clusters[cid].max_x
            
    def succ(self, x):
        if (self.min_x == None) or x >= self.max_x:
            return None
        if x < self.min_x:
            return self.min_x
        c, i = self.split_bits(x)
        hi = x - i
        half_width = int(self.universe_width(self.U) / 2)
        print("c: " + str(c))
        print("i: " + str(i))
        print("hi: " + str(hi))
        print(self.summary.clusters)
        print("min: " + str(self.min_x))
        print("max: " + str(self.max_x))
        print(c in self.clusters)
        if c in self.clusters and self.clusters[c].max_x > x:
            return hi + self.clusters[c].succ(i)
        else:
            cid = self.summary.succ(c)
            return hi + self.clusters[cid].min_x
            
    def universe_width(self, x):
        width = ceil(log(x, 2))
        next_pow_2_width = ceil(log(width, 2))
        return 1 << next_pow_2_width
    
    def split_bits(self, x):
        half_width = int(self.universe_width(self.U) / 2)
        mask_right =  (1 << half_width) - 1
        mask_left = mask_right << half_width
        
        print(mask_left)
        print(mask_right)
        
        c = (x & mask_left) >> half_width
        i = x & mask_right
        return c, i
        
    def halve_universe(self, U):
        return (1 << int(self.universe_width(U) / 2)) - 1