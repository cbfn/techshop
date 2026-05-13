from src.cart import ShoppingCart
from src.models import Product


def test_add_item_to_cart_creates_item() -> None:
    """Valida a inclusao de um item novo no carrinho."""

    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Teclado", price=100.0)

    # Act
    cart.add_item(product=product, quantity=2)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 2


def test_add_item_to_cart_updates_existing_quantity() -> None:
    """Valida o incremento de quantidade para produto ja existente."""

    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Mouse", price=50.0)
    cart.add_item(product=product, quantity=1)

    # Act
    cart.add_item(product=product, quantity=3)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 4


def test_remove_item_from_cart() -> None:
    """Valida a remocao de um item especifico pelo id do produto."""

    # Arrange
    cart = ShoppingCart()
    first_product = Product(id=1, name="Monitor", price=800.0)
    second_product = Product(id=2, name="Cabo HDMI", price=30.0)
    cart.add_item(product=first_product, quantity=1)
    cart.add_item(product=second_product, quantity=2)

    # Act
    cart.remove_item(product_id=1)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product.id == 2


def test_calculate_total_with_discount_rules() -> None:
    """Valida desconto de 10 por cento para total acima de 500."""

    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Notebook", price=600.0)
    cart.add_item(product=product, quantity=1)

    # Act
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total_with_discount == 540.0


def test_calculate_total_with_high_discount() -> None:
    """Valida desconto de 20 por cento para total acima de 1000."""

    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Computador", price=1200.0)
    cart.add_item(product=product, quantity=1)

    # Act
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total_with_discount == 960.0
