from math import log
from math import ceil

class Veb:
    def __repr__(self):
        return "Veb(min_x: {}, max_x:{}, width: {})".format(self.min_x, self.max_x, self.width)
    
    def __init__(self, U):
        self.width = self.universe_width(U)
        self.U = (1 << self.width) - 1
        self.max_x = None
        self.min_x = None
        if(self.width > 1):
            m2 = self.halve_universe()
            self.summary = Veb(m2)
            self.clusters = {}
    
    def insert(self, x):
        if (x < 0) or (x > self.U):
            raise AssertionError("{} is not between 0 and {}".format(x, self.U))
        if self.min_x == None:
            self.min_x = x
            self.max_x = x
            return
        if self.width == 1: # one bit veb is special case
            self.min_x = min(self.min_x, x)
            self.max_x = max(self.max_x, x)
            return
        if self.min_x == x or self.max_x == x: # no duplicates
            return
        to_insert = x
        if x < self.min_x:
            to_insert = self.min_x
            self.min_x = x
        if to_insert > self.max_x:
            self.max_x = to_insert
            
        c, i = self.split_bits(to_insert)
        if c not in self.clusters:
            self.clusters[c] = Veb(self.halve_universe())
            self.summary.insert(c)
        self.clusters[c].insert(i)
        
    def pred(self, x):
        if (self.min_x == None) or x <= self.min_x:
            return None
        if x > self.max_x:
            return self.max_x
            
        if self.width == 1 or self.min_x == self.max_x:
            return self.min_x
            
        c, i = self.split_bits(x)
        hi = x - i
        
        if c in self.clusters and self.clusters[c].min_x < i:
            return hi + self.clusters[c].pred(i)
        else:
            cid = self.summary.pred(c)
            if cid == None:
                return self.min_x
            hi = cid << (self.width // 2)
            return hi + self.clusters[cid].max_x
            
    def succ(self, x):
        if (self.min_x == None) or x >= self.max_x:
            return None
        if x < self.min_x:
            return self.min_x
            
        if self.width == 1 or self.min_x == self.max_x:
            return self.max_x
            
        c, i = self.split_bits(x)
        hi = x - i
        
        if c in self.clusters and self.clusters[c].max_x > i:
            return hi + self.clusters[c].succ(i)
        else:
            cid = self.summary.succ(c)
            hi = cid << (self.width // 2)
            return hi + self.clusters[cid].min_x
            
    def universe_width(self, x):
        # deal with edge cases
        if x in (0, 1):
            return 1
        if x == 2:
            return 2
        
        width = ceil(log(x, 2))
        next_pow_2_width = ceil(log(width, 2))
        return 1 << next_pow_2_width
    
    def split_bits(self, x):
        half_width = int(self.universe_width(self.U) / 2)
        mask_right =  (1 << half_width) - 1
        mask_left = mask_right << half_width
        c = (x & mask_left) >> half_width
        i = x & mask_right
        return c, i
        
    def halve_universe(self):
        h = (1 << int(self.width / 2)) - 1
        return h
        
    def print_ones(self, x):
        ones = ""
        for i in reversed(range(self.width)):
            val = (x >> i) & 1
            ones += str(val)
        return ones