# Melhorias Shift-Left para Este PR

Este documento propõe 3 melhorias com conceito Shift-Left para reduzir defeitos nas fases iniciais do desenvolvimento, alinhadas ao PR atual e aos documentos do projeto.

## 1. Gate de Qualidade Local Antes do Push

### Por que
Hoje os checks de qualidade no CI estao fortes, mas falhas ainda podem ser descobertas apenas depois do push. Shift-Left significa antecipar essa validacao para o ambiente local.

### Melhoria
Adotar uma rotina local de pre-push com os mesmos comandos do CI:

- uv run ruff check .
- uv run mypy src
- uv run pytest --cov=src --cov-fail-under=80

### Criterios de aceite
- Todo PR deve incluir evidencia de que os checks locais passaram antes do push.
- O mesmo conjunto de comandos deve estar documentado no README e ser seguido pelo time.
- Deve haver reducao de falhas no CI por divergencia entre ambiente local e pipeline.

## 2. Testes Baseados em User Stories do Backlog (US001-US003)

### Por que
O backlog define os comportamentos centrais (adicionar item, remover item e total do carrinho). Shift-Left significa validar essas regras de negocio no momento da codificacao, e nao apenas apos integracao.

### Melhoria
Padronizar testes por user story e com padrao AAA:

- US001: adicionar item ao carrinho
- US002: visualizar total do carrinho (incluindo limites de desconto)
- US003: remover item do carrinho

Incluir testes explicitos para casos de borda nos limites de desconto (500 e 1000).

### Criterios de aceite
- Os testes devem ser nomeados ou agrupados com rastreabilidade para as user stories.
- A estrutura AAA deve ser aplicada de forma consistente nos testes unitarios.
- A cobertura das regras de negocio do carrinho deve permanecer acima de 90%.

## 3. Checagens Antecipadas de Seguranca e Risco no CI

### Por que
O PRD exige checkout seguro e protecao de dados do usuario. Shift-Left em seguranca significa detectar riscos antes do merge, e nao apenas em QA tardio ou hardening de producao.

### Melhoria
Adicionar verificacoes de seguranca no pipeline e no checklist de revisao:

- Secret scanning (deteccao de valores sensiveis hardcoded).
- Scan de vulnerabilidades de dependencias (SCA).
- Regra para isolar codigo educacional/nao produtivo dos gates de qualidade e do fluxo de producao.

### Criterios de aceite
- O CI deve falhar se segredos forem detectados em arquivos versionados.
- O CI deve reportar vulnerabilidades de dependencias acima da severidade definida pelo time.
- Arquivos marcados como educacionais devem estar explicitamente excluidos de caminhos de producao e documentados.

## Resultado Esperado

A aplicacao dessas 3 melhorias aumenta a previsibilidade de qualidade, reduz retrabalho e antecipa o cumprimento dos requisitos do produto, que e o principio central do Shift-Left.