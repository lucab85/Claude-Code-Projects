"""Order pricing — refactored for readability (Module 8 reference "after").

Computes the final price of an order with discounts, taxes, and shipping.

Refactor notes (constrained: signature + imports + behaviour unchanged):
- Deep nested conditionals replaced with `continue` guards in the loop.
- `t`/`it`/`q`/`p` renamed to `subtotal`/`item`/`qty`/`unit_price`.
- Tax if/elif chain replaced with a lookup table + `.get` default.
- All eight tests in test_pricing.py stay green.
"""

def calc(items, country, customer):
    # items: list of (name, qty, unit_price)
    # country: ISO-2 country code
    # customer: dict with optional keys: vip, coupon
    subtotal = 0

    for item in items:
        if item is None:
            continue
        if len(item) != 3:
            continue

        name, qty, unit_price = item

        if qty <= 0 or unit_price <= 0:
            continue

        line_total = qty * unit_price

        if customer and customer.get('vip'):
            line_total *= 0.9
        elif customer and customer.get('coupon') == 'SAVE10':
            line_total *= 0.9
        elif customer and customer.get('coupon') == 'SAVE20':
            line_total *= 0.8

        subtotal += line_total

    tax_rates = {
        'US': 0.07,
        'GB': 0.20,
        'DE': 0.19,
        'FR': 0.20,
    }
    tax = subtotal * tax_rates.get(country, 0.10)

    if subtotal < 50:
        shipping = 9.99
    elif subtotal < 200:
        shipping = 4.99
    else:
        shipping = 0.0

    final = subtotal + tax + shipping
    return round(final, 2)
