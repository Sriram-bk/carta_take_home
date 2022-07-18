import unittest

from distribute_proceeds import distribute_proceeds

class TestDistributeProceedsForKrakatoaVentures(unittest.TestCase):
    def setUp(self):
        self.cap_table = {
            "A": {
                "total_membership_units_held": 10,
                "unit_holders": [{"name": "David", "units_held": 10, "amount_invested": 0}],
            },
            "B": {
                "total_membership_units_held": 20,
                "unit_holders": [
                    {"name": "Alex", "units_held": 10, "amount_invested": 25000},
                    {"name": "Becky", "units_held": 10, "amount_invested": 25000},
                ],
            },
            "C": {
                "total_membership_units_held": 5,
                "unit_holders": [{"name": "Becky", "units_held": 5, "amount_invested": 0}],
            },
        }
    
    def test_distribute_0_dollars(self):
        cash_proceeds = 0
        class_distribution, member_distribution = distribute_proceeds(
            cash_proceeds, self.cap_table
        )

        class_distribution_total = sum(class_distribution.values())
        member_distribution_total = sum(member_distribution.values())

        self.assertDictEqual(dict(class_distribution), {'A': 0, 'B': 0, 'C': 0})
        self.assertAlmostEqual(class_distribution_total, cash_proceeds, delta=1)
        self.assertDictEqual(dict(member_distribution), {'Alex': 0, 'Becky': 0, 'David': 0})
        self.assertAlmostEqual(member_distribution_total, cash_proceeds, delta=1)
    
    def test_distribute_100_dollars(self):
        cash_proceeds = 10000
        class_distribution, member_distribution = distribute_proceeds(
           cash_proceeds, self.cap_table
        )

        class_distribution_total = sum(class_distribution.values())
        member_distribution_total = sum(member_distribution.values())

        self.assertDictEqual(dict(class_distribution), {'A': 0, 'B': 10000, 'C': 0})
        self.assertAlmostEqual(class_distribution_total, cash_proceeds, delta=1)
        self.assertDictEqual(dict(member_distribution), {'Alex': 5000, 'Becky': 5000, 'David': 0})
        self.assertAlmostEqual(member_distribution_total, cash_proceeds, delta=1)
    
    def test_distribute_250_dollars_and_50_cents(self):
        cash_proceeds = 25050
        class_distribution, member_distribution = distribute_proceeds(
           cash_proceeds, self.cap_table
        )

        class_distribution_total = sum(class_distribution.values())
        member_distribution_total = sum(member_distribution.values())

        self.assertDictEqual(dict(class_distribution), {'A': 0, 'B': 25050, 'C': 0})
        self.assertAlmostEqual(class_distribution_total, cash_proceeds, delta=1)
        self.assertDictEqual(dict(member_distribution), {'Alex': 12525, 'Becky': 12525, 'David': 0})
        self.assertAlmostEqual(member_distribution_total, cash_proceeds, delta=1)
    
    def test_distribute_500_dollars(self):
        cash_proceeds = 50000
        class_distribution, member_distribution = distribute_proceeds(
           cash_proceeds, self.cap_table
        )

        class_distribution_total = sum(class_distribution.values())
        member_distribution_total = sum(member_distribution.values())
        
        self.assertDictEqual(dict(class_distribution), {'A': 0, 'B': 50000, 'C': 0})
        self.assertAlmostEqual(class_distribution_total, cash_proceeds, delta=1)
        self.assertDictEqual(dict(member_distribution), {'Alex': 25000, 'Becky': 25000, 'David': 0})
        self.assertAlmostEqual(member_distribution_total, cash_proceeds, delta=1)
    
    def test_distribute_1000_dollars(self):
        cash_proceeds = 100000
        class_distribution, member_distribution = distribute_proceeds(
           cash_proceeds, self.cap_table
        )

        class_distribution_total = sum(class_distribution.values())
        member_distribution_total = sum(member_distribution.values())
        
        self.assertDictEqual(dict(class_distribution), {'A': 14286, 'B': 78572, 'C': 7143})
        self.assertAlmostEqual(class_distribution_total, cash_proceeds, delta=1)
        self.assertDictEqual(dict(member_distribution), {'Alex': 39286, 'Becky': 46429, 'David': 14286})
        self.assertAlmostEqual(member_distribution_total, cash_proceeds, delta=1)
        


if __name__ == '__main__':
  unittest.main()