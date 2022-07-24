import argparse
from collections import defaultdict
from pprint import pprint
from typing import DefaultDict, Dict, Tuple

from distribute_proceeds import (
    distribute_proceeds_till_holders_recoup_amount_invested,
    distribute_remaining_proceeds_to_holders,
    merge_distributions,
)


def distribute_proceeds_for_krakatoa_ventures(
    cash_proceeds: int, cap_table: Dict[str, Dict]
) -> Tuple[DefaultDict[str, int], DefaultDict[str, int]]:
    """
    Distribute cash_proceeds to unit holders based on the cap_table structure for Krakatoa Ventures.

    The cash distribution is done in the following manner :
    1. Proceeds are distributed exclusively amongst 'Class B' unit holders in proportion to the number
    of units held, until the total amount distributed to each holder reaches their total amount invested.
    2. Further proceeds are distributed to 'Class C', 'Class B' and 'Class A' holders in proportion to their
    number of units held.

    Args:
        amount (int): The amount of cash proceeds to distribute in cents.
        cap_table (Dict[str, Dict]): The cap_table of the venture capital firm

    Returns:
        Tuple[int, DefaultDict[str, int], DefaultDict[str, int]]:
            A tuple containing the class_distribution and the member_distribution.
    """
    net_member_distribution = defaultdict(int)
    net_class_distribution = defaultdict(int)

    b_class_unit_holders = cap_table["B"]["unit_holders"]
    total_b_class_units = cap_table["B"]["total_membership_units_held"]

    (
        remaining_amount,
        class_distribution,
        member_distribution,
    ) = distribute_proceeds_till_holders_recoup_amount_invested(
        cash_proceeds, "B", b_class_unit_holders, total_b_class_units
    )

    net_class_distribution = merge_distributions(
        net_class_distribution, class_distribution
    )
    net_member_distribution = merge_distributions(
        net_member_distribution, member_distribution
    )

    if remaining_amount > 0:
        (
            class_distribution,
            member_distribution,
        ) = distribute_remaining_proceeds_to_holders(remaining_amount, cap_table)

        net_class_distribution = merge_distributions(
            net_class_distribution, class_distribution
        )
        net_member_distribution = merge_distributions(
            net_member_distribution, member_distribution
        )

    for share_class, class_details in cap_table.items():
        class_unit_holders = class_details["unit_holders"]

        if share_class not in class_distribution:
            net_class_distribution[share_class] = 0

        for unit_holder in class_unit_holders:
            holder_name = unit_holder["name"]
            if holder_name not in member_distribution:
                net_member_distribution[holder_name] = 0

    return (net_class_distribution, net_member_distribution)


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

    # Convert cash proceeds in dollars to cents
    cash_proceeds = round(args.cash_proceeds * 100)

    class_distribution, member_distribution = distribute_proceeds_for_krakatoa_ventures(
        cash_proceeds, CAP_TABLE
    )

    # Convert cents back into dollars for user output
    for share_class, amount in class_distribution.items():
        class_distribution[share_class] /= 100
    for member, amount in member_distribution.items():
        member_distribution[member] /= 100

    pprint(dict(member_distribution), indent=4)
    pprint(dict(class_distribution), indent=4)
