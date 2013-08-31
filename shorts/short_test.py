#!/usr/bin/env python

# By: Joey DeFrancesco 
# (c) smalr.io
# File: short_test.py
# Testing module for short.py (to be renamed to baseconv.py) which is in charge of converting to and from base62. 
# (see short.py docs)

import unittest

# Module we are testing
import short

# Test for success
class Base10To62Known(unittest.TestCase):
    known_values = ((1, '1'),
                    (2, '2'),
                    (10, 'A'),
                    (36, 'a'),
                    (124, '20')
                   )
    def setUp(self): pass

    def tearDown(self): pass

    def testTo62KnownValues(self):
        """
        Test that an integer for input produces the correct
        base 62 equivalent (essentially our short url string)
        """
        print 'In testTo62KnownValues...'
        for integer, val in self.known_values:
            result = short.value_encode62(integer)
            self.assertEqual(val, result)

    
class To62InvalidInput(unittest.TestCase):
    
    def setUp(self): pass

    def tearDown(self): pass

    def testNegative(self):
        """base10_to_base62 should fail with no negative input"""
        print 'In test for base10_to_base62 (testing negative input)'
        self.assertRaises(short.OutOfRangeError, short.base10_to_base62, -1)
      
    def testNoneInteger(self):
        """base10_to_base62 should fail, input must be integer (not decimal)"""
        print 'In test for base10_to_base62. Testing non-integer values'
        self.assertRaises(short.NonIntegerError, short.base10_to_base62, 0.5)
        
    
class Base62To10Known(unittest.TestCase):
    known_values = (('W', 32),
                    ('a', 36),
                    ('Qm', 1660),
                    ('fq', 2594),
                    ('mJ', 2995),
                    ('Zo', 2220),
                    ('1J', 81),
                    ('jM', 2812),
                    ('182', 4342),
                    ('CT0vN28C', 43907429847324))

    def setUp(self): pass

    def tearDown(self): pass

    def testFrom62KnownValues(self): 
        print 'In testFrom62KnownValues'
        for seq, integer in self.known_values:
            result = short.base62_to_base10(seq)
            self.assertEqual(result, integer)

    
class From62InvalidInput(unittest.TestCase):

    def setUp(self): pass

    def tearDown(self): pass

    def testNegative(self):
        pass

    def testNoneStringParamer(self):
        pass

    
if __name__ == '__main__':
    print(short.value_encode62(18446744073709551615))
    unittest.main()
