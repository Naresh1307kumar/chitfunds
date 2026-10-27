"""
Real Chit Fund Auction Calculation Engine
==========================================
Formula:
  chit_value          = monthly_amount × total_members
  discount            = chit_value - winning_bid_amount
  company_commission  = discount × commission_rate / 100
  net_discount        = discount - company_commission
  dividend_per_member = net_discount / total_members
  net_payable         = monthly_amount - dividend_per_member
  winner_receives     = winning_bid_amount
"""


def calculate_auction_draw(
    chit_value: float,
    monthly_amount: float,
    total_members: int,
    commission_rate: float,
    winning_bid_amount: float
) -> dict:
    """
    Calculate all chit fund auction values for a monthly draw.

    Args:
        chit_value:          Total pool (monthly_amount × total_members)
        monthly_amount:      Fixed monthly installment per member
        total_members:       Number of members in the plan
        commission_rate:     Company commission percentage (e.g. 5.0)
        winning_bid_amount:  The amount the auction winner agreed to accept

    Returns:
        dict with all calculated fields
    """
    if winning_bid_amount <= 0 or winning_bid_amount > chit_value:
        raise ValueError(
            f"Winning bid (₹{winning_bid_amount}) must be > 0 and ≤ Chit Value (₹{chit_value})"
        )

    discount             = chit_value - winning_bid_amount
    company_commission   = round(discount * (commission_rate / 100), 2)
    net_discount         = round(discount - company_commission, 2)
    dividend_per_member  = round(net_discount / total_members, 2)
    net_payable          = round(monthly_amount - dividend_per_member, 2)
    winner_receives      = winning_bid_amount

    return {
        "chit_value":           chit_value,
        "monthly_amount":       monthly_amount,
        "winning_bid_amount":   winning_bid_amount,
        "discount":             round(discount, 2),
        "company_commission":   company_commission,
        "net_discount":         net_discount,
        "dividend_per_member":  dividend_per_member,
        "net_payable":          net_payable,
        "winner_receives":      winner_receives,
    }


def calculate_last_month_draw(
    chit_value: float,
    monthly_amount: float,
) -> dict:
    """
    Last member gets full chit_value — no bid, no discount, no dividend.
    """
    return {
        "chit_value":           chit_value,
        "monthly_amount":       monthly_amount,
        "winning_bid_amount":   chit_value,
        "discount":             0.0,
        "company_commission":   0.0,
        "net_discount":         0.0,
        "dividend_per_member":  0.0,
        "net_payable":          monthly_amount,
        "winner_receives":      chit_value,
    }
