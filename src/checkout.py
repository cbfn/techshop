from typing import List
from src.models import CartItem, CheckoutResult, PaymentRequest, PaymentResponse, User


class FakePaymentAPI:
    """Simula uma API de pagamentos externa."""

    def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Simula a chamada a um gateway de pagamento de forma protegida, sem dados sensiveis reais.

        Args:
            request (PaymentRequest): Os dados para processamento do pagamento.

        Returns:
            PaymentResponse: A resposta do provedor de pagamentos.
        """
        if 0 < request.total_amount < 9999:
            return PaymentResponse(status="pagamento_aprovado", transaction_id="xyz123abc")
        return PaymentResponse(status="pagamento_recusado", reason="valor_invalido")


class CheckoutService:
    """Servico responsavel por orquestrar o processo de checkout respeitando SOLID."""

    def __init__(self, payment_api: FakePaymentAPI) -> None:
        """
        Inicializa o servico de checkout.

        Args:
            payment_api (FakePaymentAPI): A API de pagamentos injetada (Inversion of Control).
        """
        self.payment_api = payment_api
        self.shipping_cost = 15.50

    def check_stock(self, items: List[CartItem]) -> bool:
        """
        Verifica a disponibilidade de estoque para todos os itens do carrinho.

        Args:
            items (List[CartItem]): Lista de itens do carrinho.

        Returns:
            bool: Verdadeiro se ha estoque para todos, falso caso contrario.
        """
        mock_stock = 10
        for item in items:
            if item.quantity > mock_stock:
                return False
        return True

    def calculate_total(self, items: List[CartItem], user: User) -> float:
        """
        Calcula o valor total do carrinho, incluindo frete e descontos.

        Args:
            items (List[CartItem]): Itens que compoem o carrinho.
            user (User): O usuario que esta realizando o pedido.

        Returns:
            float: O valor final do pedido.
        """
        subtotal = sum(item.product.price * item.quantity for item in items)
        if subtotal == 0:
            return 0.0

        total_with_shipping = subtotal + self.shipping_cost
        
        if total_with_shipping > 200:
            if user.is_vip:
                return total_with_shipping * 0.85
            return total_with_shipping * 0.95

        return total_with_shipping

    def process_checkout(self, items: List[CartItem], user: User, payment_token: str) -> CheckoutResult:
        """
        Processa o checkout validando o carrinho, calculando o valor e processando o pagamento.

        Args:
            items (List[CartItem]): Os itens presentes no carrinho do usuario.
            user (User): O usuario logado realizando a compra.
            payment_token (str): O token de pagamento (seguro) fornecido pelo gateway no frontend.

        Returns:
            CheckoutResult: Objeto indicando sucesso ou fracasso do checkout, e ID da transacao caso sucesso.
        """
        if not items:
            return CheckoutResult(success=False, error="Carrinho vazio")

        if not self.check_stock(items):
            return CheckoutResult(success=False, error="Erro de estoque")

        total = self.calculate_total(items, user)
        if total == 0:
            return CheckoutResult(success=False, error="Valor invalido")

        payment_request = PaymentRequest(
            user_id=user.id,
            total_amount=round(total, 2),
            payment_token=payment_token
        )

        response = self.payment_api.process_payment(payment_request)
        if response.status == "pagamento_aprovado":
            return CheckoutResult(success=True, transaction_id=response.transaction_id)
        
        return CheckoutResult(success=False, error="problema_na_api_de_pagamento")
