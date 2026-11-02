"""Order pricing: discounts, taxes and shipping for one order."""

TAX_RATES = {'US': 0.07, 'GB': 0.20, 'DE': 0.19, 'FR': 0.20}
DEFAULT_TAX_RATE = 0.10


def _discount(customer):
    """Return the price multiplier for this customer."""
    if customer is None:
        return 1.0
    # '== True' on purpose: values such as "no" or 2 must not count as VIP.
    if customer.get('vip') == True:  # noqa: E712
        return 0.9
    if customer.get('coupon') == 'SAVE10':
        return 0.9
    if customer.get('coupon') == 'SAVE20':
        return 0.8
    return 1.0


def _shipping(subtotal):
    """Return the shipping cost for a discounted subtotal."""
    if subtotal < 50:
        return 9.99
    if subtotal < 200:
        return 4.99
    return 0.0


def calc(items, country, customer):
    # items: list of (name, qty, unit_price)
    # country: ISO-2 country code
    # customer: dict with optional keys: vip, coupon
    subtotal = 0
    for item in items:
        if item is None or len(item) != 3:
            continue
        _name, qty, unit_price = item
        # 'not (> 0)' rather than '<= 0', so a NaN price is still skipped.
        if not (qty > 0 and unit_price > 0):
            continue
        subtotal += qty * unit_price * _discount(customer)
    tax = subtotal * TAX_RATES.get(country, DEFAULT_TAX_RATE)
    return round(subtotal + tax + _shipping(subtotal), 2)
