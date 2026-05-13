from src.checkout import CheckoutService, FakePaymentAPI
from src.models import CartItem, Product, User


def test_process_checkout_success() -> None:
    """Valida o fluxo de checkout com sucesso para um pedido valido."""

    # Arrange
    api = FakePaymentAPI()
    service = CheckoutService(payment_api=api)
    user = User(id=1, name="John Doe", is_vip=False)
    product = Product(id=1, name="Mouse Pad", price=100.0)
    items = [CartItem(product=product, quantity=1)]
    payment_token = "secure_token_123"

    # Act
    result = service.process_checkout(items=items, user=user, payment_token=payment_token)

    # Assert
    assert result.success is True
    assert result.transaction_id == "xyz123abc"
    assert result.error is None


def test_process_checkout_empty_cart() -> None:
    """Valida o erro retornado quando o carrinho esta vazio."""

    # Arrange
    api = FakePaymentAPI()
    service = CheckoutService(payment_api=api)
    user = User(id=1, name="John Doe", is_vip=False)
    items: list[CartItem] = []
    payment_token = "secure_token_123"

    # Act
    result = service.process_checkout(items=items, user=user, payment_token=payment_token)

    # Assert
    assert result.success is False
    assert result.error == "Carrinho vazio"


def test_process_checkout_stock_error() -> None:
    """Valida o erro ao tentar comprar uma quantidade acima do estoque."""

    # Arrange
    api = FakePaymentAPI()
    service = CheckoutService(payment_api=api)
    user = User(id=1, name="John Doe", is_vip=False)
    product = Product(id=1, name="Mouse Pad", price=100.0)
    # mock_stock in the code is 10, so 11 will trigger the error
    items = [CartItem(product=product, quantity=11)]
    payment_token = "secure_token_123"

    # Act
    result = service.process_checkout(items=items, user=user, payment_token=payment_token)

    # Assert
    assert result.success is False
    assert result.error == "Erro de estoque"


def test_calculate_total_vip_discount() -> None:
    """Valida se o desconto VIP de 15 por cento eh aplicado acima de R$ 200."""

    # Arrange
    api = FakePaymentAPI()
    service = CheckoutService(payment_api=api)
    user = User(id=1, name="John VIP", is_vip=True)
    product = Product(id=1, name="Monitor", price=300.0)
    items = [CartItem(product=product, quantity=1)]

    # Act
    total = service.calculate_total(items=items, user=user)

    # Assert
    # subtotal=300, frete=15.50 -> 315.50, VIP * 0.85 = 268.175
    expected_total = (300.0 + 15.50) * 0.85
    assert total == expected_total


def test_calculate_total_standard_discount() -> None:
    """Valida se o desconto padrao de 5 por cento eh aplicado acima de R$ 200."""

    # Arrange
    api = FakePaymentAPI()
    service = CheckoutService(payment_api=api)
    user = User(id=1, name="John Doe", is_vip=False)
    product = Product(id=1, name="Monitor", price=300.0)
    items = [CartItem(product=product, quantity=1)]

    # Act
    total = service.calculate_total(items=items, user=user)

    # Assert
    # subtotal=300, frete=15.50 -> 315.50, Default * 0.95 = 299.725
    expected_total = (300.0 + 15.50) * 0.95
    assert total == expected_total
