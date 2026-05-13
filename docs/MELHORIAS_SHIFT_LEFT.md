# Melhorias Shift-Left no Processo de Checkout

O conceito de **Shift-Left** envolve mover atividades de teste, qualidade e segurança para o estágio mais inicial possível no ciclo de desenvolvimento, permitindo que problemas sejam descobertos e resolvidos por desenvolvedores antes que o código chegue ao ambiente de produção.

Com base na nossa refatoração, foram identificadas as 3 seguintes melhorias seguindo este conceito:

## 1. Implementação de Testes Unitários com Cobertura Miníma (Quality Gate)
**Problema anterior:** A validação e a lógica de pagamento dependiam de validações manuais via `prints` espalhados e cenários não testados.
**Melhoria Shift-Left:** Foram criados testes unitários utilizando o padrão **AAA (Arrange, Act, Assert)** para todas as regras de negócio em `test_checkout.py`. O uso do `pytest` integrado ao limiar obrigatório de cobertura (`--cov-fail-under=80`) garante que nenhum código sem teste básico seja transferido (merge) ou construído. Isso captura falhas de lógica imediatamente na máquina do desenvolvedor.

## 2. Tipagem Estática e Validação com Mypy/Pydantic
**Problema anterior:** `processar_tudo` usava dicionários genéricos e não possuía Type Hints, facilitando a ocorrência de erros de acesso e tipos não esperados durante o tempo de execução.
**Melhoria Shift-Left:** A utilização do `Mypy` em conjunto com a forte tipagem das classes do modelo (`BaseModel` do Pydantic no `models.py`) valida as estruturas de dados e os contratos da API em tempo de edição/compilação. Bugs relacionados a tipos são identificados pelo linter da IDE em segundos, antes mesmo dos testes rodarem.

## 3. Segurança desde o Design (DevSecOps)
**Problema anterior:** Dados sensíveis de cartão de crédito ("XXXX-XXXX...") estavam transitando como texto puro em lógicas hardcoded sob fluxos complexos, representando um altíssimo risco de vazamento de dados (Data Breach).
**Melhoria Shift-Left:** Refatorou-se a modelagem de pagamento (`PaymentRequest`) para trafegar de forma segura utilizando *tokens* gerados pelo Gateway no frontend em vez de manipular o PAN (Primary Account Number) do cartão de crédito no backend. Aplicar segurança já na modelagem arquitetural do código é a essência do "Security Shift-Left".
