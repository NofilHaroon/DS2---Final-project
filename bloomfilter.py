import math
import mmh3  # will be used to generate  the hashing function
from bitarray import bitarray


class BloomFilter(object):
    def __init__(self, total_items, fp_prob):
        """ 
        total_items : int 
                The total number of items to be stored in our bloom filter 
        fp_prob : float 
                False Positive probability in decimal 
        """
        self.fp_prob = fp_prob
        self.array_size = self.get_size(total_items, fp_prob)
        # Number of hash functions to use depending on our expected total_items count
        # and the size of bits array created
        self.hash_count = self.get_hash_count(self.array_size, total_items)
        # Bit array of given size and set all values to 0 initially
        self.bit_array = bitarray(self.array_size)
        self.bit_array.setall(0)

    # To add items to the bloom filter
    def add(self, item):
        elements = []
        for i in range(self.hash_count):
            # create element for given item.
            # use the hash function to create a different seed
            element = mmh3.hash(item, i) % self.array_size
            elements.append(element)
            # update value of bit array from 0 to 1
            self.bit_array[element] = 1

    # Check for existence of an item in filter
    def check(self, item):
        for i in range(self.hash_count):
            element = mmh3.hash(item, i) % self.array_size
            if self.bit_array[element] == False:
                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        ''' 
        Return the size of bit array(m) to used using 
        following formula 
        m = -(n * lg(p)) / (lg(2)^2) 
        n : int 
                number of items expected to be stored in filter 
        p : float 
                False Positive probability in decimal 
        '''
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        ''' 
        Return the hash function(k) to be used using 
        following formula 
        k = (m/n) * lg(2) 

        m : int 
                size of bit array 
        n : int 
                number of items expected to be stored in filter 
        '''
        k = (m/n) * math.log(2)
        return int(k)
