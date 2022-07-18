import argparse
from pprint import pprint

from distribute_proceeds import distribute_proceeds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Distribute cash proceeds to unit holders of Kratatoa Ventures."
    )
    parser.add_argument(
        "--proceeds",
        dest="cash_proceeds",
        type=float,
        required=True,
        help="Cash proceeds in dollars to distribute to unit holders.",
    )

    CAP_TABLE = {
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

    args = parser.parse_args()

    # Convert cash proceeds to cents
    cash_proceeds = round(args.cash_proceeds * 100)

    class_distribution, member_distribution = distribute_proceeds(
        cash_proceeds, CAP_TABLE
    )

    # Convert cents back into dollars for user output
    for share_class, amount in class_distribution.items():
        class_distribution[share_class] /= 100
    for member, amount in member_distribution.items():
        member_distribution[member] /= 100

    pprint(dict(member_distribution), indent=4)
    pprint(dict(class_distribution), indent=4)
