from collections import defaultdict
from pprint import pprint
from typing import DefaultDict, Dict, List, Tuple

CAP_TABLE = {
    "A": {
        "total_membership_units_held": 10,
        "unit_holders": [{"name": "David", "units_held": 10, "amount_invested": None}],
    },
    "B": {
        "total_membership_units_held": 30,
        "unit_holders": [
            {"name": "Alex", "units_held": 10, "amount_invested": 250.00},
            {"name": "Becky", "units_held": 10, "amount_invested": 500.00},
            {"name": "Chad", "units_held": 10, "amount_invested": 750.00},
        ],
    },
    "C": {
        "total_membership_units_held": 5,
        "unit_holders": [{"name": "Becky", "units_held": 5, "amount_invested": None}],
    },
}


def merge_distributions(
    distribution_a: DefaultDict[str, float], distribution_b: DefaultDict[str, float]
) -> DefaultDict[str, float]:
    merged_distribution = defaultdict(float)

    for key, distribution in distribution_a.items():
        merged_distribution[key] += distribution
    for key, distribution in distribution_b.items():
        merged_distribution[key] += distribution

    return merged_distribution


def distribute_proceeds_till_holders_recoup_amount_invested(
    amount: float,
    share_class: str,
    unit_holders: List[Dict],
    total_membership_units_held: int,
) -> Tuple[int, DefaultDict[str, float], DefaultDict[str, float]]:
    """
    Distribute cash proceeds(amount) to unit holders in proportion to the number of units held,
    until the total amount distributed to each holder reaches their total amount invested.

    Args:
        amount (float): The amount of cash proceeds to distribute
        share_class (str): The share class of the unit_holders
        unit_holders (List[Dict]): List of the unit holders in this share_class with details of their holdings
        total_membership_units_held (int): The total number of units held in this share_class

    Returns:
        Tuple[int, DefaultDict[str, float], DefaultDict[str, float]]: _description_
    """
    member_distribution = defaultdict(float)
    class_distribution = defaultdict(float)
    holders_still_to_be_paid_out = []
    total_remaining_units = 0
    total_remaining_amount = amount

    for unit_holder in unit_holders:
        holder_name = unit_holder["name"]
        amount_invested = unit_holder["amount_invested"]
        units_held = unit_holder["units_held"]
        distribution_ratio = units_held / total_membership_units_held

        amount_distributed = distribution_ratio * amount
        if amount_distributed > amount_invested:
            amount_distributed = amount_invested
        amount_distributed = round(amount_distributed, 2)

        if amount_invested - amount_distributed > 0:
            holders_still_to_be_paid_out.append(
                {
                    "name": holder_name,
                    "amount_invested":  round(amount_invested - amount_distributed, 2),
                    "units_held": units_held,
                }
            )
            total_remaining_units += units_held

        total_remaining_amount -= amount_distributed
        member_distribution[holder_name] += amount_distributed
        class_distribution[share_class] += amount_distributed

    total_remaining_amount = round(total_remaining_amount, 2)
    # Distribute any money left to holders who's distribution amount is less
    # than their invested amount. Distribution is done in proportion to the
    # number of units held.
    if total_remaining_amount > 0 and len(holders_still_to_be_paid_out) > 0:
        (
            total_remaining_amount,
            class_dists,
            member_dists,
        ) = distribute_proceeds_till_holders_recoup_amount_invested(
            total_remaining_amount,
            share_class,
            holders_still_to_be_paid_out,
            total_remaining_units,
        )
        class_distribution = merge_distributions(class_distribution, class_dists)
        member_distribution = merge_distributions(member_distribution, member_dists)

    return (total_remaining_amount, class_distribution, member_distribution)


def distribute_proceeds_proportional_to_units_held(
    amount: float,
    share_class: str,
    unit_holders: List[Dict],
    total_membership_units_held: int,
) -> Tuple[DefaultDict[str, float], DefaultDict[str, float]]:
    """
    Distribute the cash proceeds (amount) to the holders in proportion to their
    number of units held in this share_class.

    Args:
        amount (float): The amount of cash proceeds to distribute
        share_class (str): The share class of the unit_holders
        unit_holders (List[Dict]): List of the unit holders in this share_class with details of their holdings.
        total_membership_units_held (int): The total number of units held in this share_class

    Returns:
        Tuple[DefaultDict[str, float], DefaultDict[str, float]]:
            A tuple containing the class_distribution and the member_distribution.
    """
    member_distribution = defaultdict(float)
    class_distribution = defaultdict(float)

    for unit_holder in unit_holders:
        holder_name = unit_holder["name"]
        units_held = unit_holder["units_held"]
        distribution_ratio = units_held / total_membership_units_held

        amount_distributed = round(distribution_ratio * amount, 2)

        member_distribution[holder_name] += amount_distributed
        class_distribution[share_class] += amount_distributed

    return (class_distribution, member_distribution)


def distribute_remaining_proceeds_to_holders(
    amount: float, cap_table: Dict[str, Dict]
) -> Tuple[DefaultDict[str, float], DefaultDict[str, float]]:
    """
    Distribute the cash proceeds (amount) to the holders in proportion to their
    number of units held based on the cap_table structure.

    Args:
        amount (float): The amount of cash proceeds to distribute
        cap_table (Dict[str, Dict]): The cap_table of the venture capital firm

    Returns:
        Tuple[DefaultDict[str, float], DefaultDict[str, float]]:
            A tuple containing the class_distribution and the member_distribution.
    """
    member_distribution = defaultdict(float)
    class_distribution = defaultdict(float)
    total_units_held_across_classes = 0

    for class_details in cap_table.values():
        total_units_held_across_classes += class_details["total_membership_units_held"]

    for share_class, class_details in cap_table.items():
        total_class_units = class_details["total_membership_units_held"]
        class_unit_holders = class_details["unit_holders"]
        distribution_ratio = total_class_units / total_units_held_across_classes
        class_distribution_amount = round(distribution_ratio * amount, 2)

        (class_dists, member_dists) = distribute_proceeds_proportional_to_units_held(
            class_distribution_amount,
            share_class,
            class_unit_holders,
            total_class_units,
        )

        class_distribution = merge_distributions(class_distribution, class_dists)
        member_distribution = merge_distributions(member_distribution, member_dists)

    return (class_distribution, member_distribution)


def distribute_proceeds(
    cash_proceeds: float, cap_table: Dict[str, Dict]
) -> Tuple[DefaultDict[str, float], DefaultDict[str, float]]:
    """
    Distribute cash_proceeds to unit holders based on the cap_table structure.

    The cash distribution is done in the following manner :
    1. Proceeds are distributed exclusively amongst 'Class B' unit holders in proportion to the number
    of units held, until the total amount distributed to each holder reaches their total amount invested.
    2. Further proceeds are distributed to 'Class C', 'Class B' and 'Class A' holders in proportion to their
    number of units held.

    Args:
        amount (float): The amount of cash proceeds to distribute
        cap_table (Dict[str, Dict]): The cap_table of the venture capital firm

    Returns:
        Tuple[int, DefaultDict[str, float], DefaultDict[str, float]]:
            A tuple containing the class_distribution and the member_distribution.
    """
    net_member_distribution = defaultdict(float)
    net_class_distribution = defaultdict(float)

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

    return (net_class_distribution, net_member_distribution)


if __name__ == "__main__":
    class_distribution, member_distribution = distribute_proceeds(1356.00, CAP_TABLE)

    for share_class, class_details in CAP_TABLE.items():
        class_unit_holders = class_details["unit_holders"]

        if share_class not in class_distribution:
            class_distribution[share_class] = 0.0

        for unit_holder in class_unit_holders:
            holder_name = unit_holder["name"]
            if holder_name not in member_distribution:
                member_distribution[holder_name] = 0.0

    pprint(dict(member_distribution), indent=4)
    pprint(dict(class_distribution), indent=4)
