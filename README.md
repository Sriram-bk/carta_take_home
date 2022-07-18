# Prerequisites

- Python v3.10 or higher

# Running the CLI tool

```bash
python distribute_proceeds_for_krakatoa_ventures.py --proceeds <CASH_PROCEEDS>
```

Example :
```bash
python distribute_proceeds_for_krakatoa_ventures.py --proceeds 525.25
```

# Running the tests

```bash
python test_distribute_proceeds_for_krakatoa_ventures.py
```

# Assumptions

* The data in the cap_table is validated and correct. 
    * The `total_membership_units_held` in each share class equal to the sum of the `units_held` by each individual `unit_holder` in the class.
    * All of the `amount_invested` values are in cents and represented as an integer.
* The cash proceeds input to the program is given in dollars and is represented as a float(50.25).


# Design decisions

* I chose to convert all dollar values to cents in order to avoid weirdness with floating point arithmetic.
* I chose to display all unit holders and share classes in the final outputs even if they didn't have any proceeds distributed to them.