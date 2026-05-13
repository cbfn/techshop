from typing import List, Optional
from pydantic import BaseModel


class Product(BaseModel):
    """Representa um produto disponivel para venda."""

    id: int
    name: str
    price: float


class CartItem(BaseModel):
    """Representa um item do carrinho com produto e quantidade."""

    product: Product
    quantity: int


class User(BaseModel):
    """Representa o usuario que esta realizando a compra."""

    id: int
    name: str
    is_vip: bool


class PaymentRequest(BaseModel):
    """Detalhes da requisicao de pagamento."""
    
    user_id: int
    total_amount: float
    payment_token: str  # Token em vez de numero de cartao para seguranca


class PaymentResponse(BaseModel):
    """Resposta simulada do servico de pagamento."""
    
    status: str
    transaction_id: Optional[str] = None
    reason: Optional[str] = None


class CheckoutResult(BaseModel):
    """Resultado do processo de checkout."""
    
    success: bool
    transaction_id: Optional[str] = None
    error: Optional[str] = None
