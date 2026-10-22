import pytest

class Order:
    def __init__(self, id, items):
        self.id = id
        self.items = items

    def total(self):
        return sum(item['price'] * item['quantity'] for item in self.items)

    def most_expensive(self):
        return max(self.items, key=lambda x: x['price'])

    def apply_discount(self, percent):
        if not 0 <= percent <= 100:
            raise ValueError("Invalid discount")
        for item in self.items:
            item['price'] -= item['price'] * (percent / 100)

    def __repr__(self):
        return f"<Order {self.id}: {len(self.items)} items>"


@pytest.fixture
def normal_order():
    items = [
        {'name': 'laptop', 'price': 1000.0, 'quantity': 1},
        {'name': 'mouse', 'price': 50.0, 'quantity': 2},
        {'name': 'keyboard', 'price': 150.0, 'quantity': 1}
    ]
    return Order(1, items)

@pytest.fixture
def empty_order():
    return Order(2, [])


# тести total()

def test_total_calculates_sum_for_multiple_items(normal_order):
    # Act & Assert: (1000*1) + (50*2) + (150*1) = 1250.0
    assert normal_order.total() == 1250.0

def test_total_for_empty_order_is_zero(empty_order):
    assert empty_order.total() == 0


# тести most_expensive()

def test_most_expensive_returns_item_with_highest_price(normal_order):
    # шукаємо найдорожче
    expensive = normal_order.most_expensive()
    # має бути laptop
    assert expensive['name'] == 'laptop'
    assert expensive['price'] == 1000.0

def test_most_expensive_empty_order_raises_value_error(empty_order):
    with pytest.raises(ValueError):
        empty_order.most_expensive()


# тести apply_discount()

@pytest.mark.parametrize("percent, expected_prices", [
    (0, [1000.0, 50.0, 150.0]),      
    (10, [900.0, 45.0, 135.0]),      
    (100, [0.0, 0.0, 0.0])           
])
def test_apply_discount_updates_all_prices_correctly(normal_order, percent, expected_prices):
    
    normal_order.apply_discount(percent)
    
    actual_prices = [item['price'] for item in normal_order.items]
    
    assert actual_prices == pytest.approx(expected_prices)

@pytest.mark.parametrize("invalid_percent", [-1, -50, 101, 150])
def test_apply_discount_rejects_out_of_bounds_percent(normal_order, invalid_percent):
    with pytest.raises(ValueError, match="Invalid discount"):
        normal_order.apply_discount(invalid_percent)


# тест __repr__()

def test_repr_returns_correct_string_format(normal_order):
    assert repr(normal_order) == "<Order 1: 3 items>"

def test_repr_for_empty_order(empty_order):
    assert repr(empty_order) == "<Order 2: 0 items>"