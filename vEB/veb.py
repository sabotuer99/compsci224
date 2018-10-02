import math

class Veb:
    def __init__(self, U):
        self.U = 1 << (self.universe_size(U) - 1)
        print(self.U)
        self.max_x = None
        self.min_x = None
        raise AssertionError()
        if(self.U > 1):
            m2 = 1 << int(self.universe_size(U)/ 2)
            self.summary = Veb(m2)
            self.clusters = {}
            
    
    def insert(self, x):
        if x < 0 or x > self.U:
            raise AssertionError("Out of bounds: " + str(x))
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
            self.clusters[c] = Veb(self.universe_size(self.U)/2)
            self.summary.insert(c)
        self.clusters[c].insert(i)
        
        
        
    def pred(self, x):
        if (self.min_x == None) or x <= self.min_x:
            return None
        if x > self.max_x:
            return self.max_x
        c, i = self.split_bits(x)
        if c in self.clusters and self.clusters[c].min_x < x:
            return c + self.clusters[c].pred(i)
        else:
            cid = self.summary.pred(c)
            return c + self.clusters[cid].max_x

            
    def succ(self, x):
        if (self.min_x == None) or x >= self.max_x:
            return None
        if x < self.min_x:
            return self.min_x
        c, i = self.split_bits(x)
        if c in self.clusters and self.clusters[c].max_x > x:
            return c + self.clusters[c].succ(i)
        else:
            cid = self.summary.succ(c)
            return c + self.clusters[cid].min_x
            
    def universe_size(self, x):
        msb = int(math.log(x, 2))
        return 1 << math.ceil(math.log(msb, 2))
        
    
    def split_bits(self, x):
        m2 = int(self.universe_size(self.U) / 2)
        mask_right =  (1 << m2) - 1
        mask_left = mask_right << m2
        c = x & mask_left
        i = x & mask_right
        return c, i