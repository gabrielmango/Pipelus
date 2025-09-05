# Regras de Git para o Projeto

Este documento descreve as convenções de **branches** e **commits** para manter o histórico limpo, organizado e rastreável.

---

## 1. Branches

O projeto segue um modelo inspirado no **Git Flow simplificado**:

### **Branches principais**
- **main**: Somente código pronto, revisado e testado.
  - Não fazer commits diretos.
- **develop**: Branch integradora de novas features.
  - Contém código funcional, mas pode ter pequenas instabilidades.
  - PRs de feature devem ir para aqui antes de ir para main.

### **Branches secundárias**
- **Feature**: Nova funcionalidade.
  - Criadas a partir de `develop`.
  - Nomenclatura: `feature/<descrição-curta>`
  - Exemplo: `feature/pipeline-etl-clientes`
  - PR vai para `develop`.
  
- **Hotfix**: Correções críticas.
  - Criadas a partir de `main`.
  - Nomenclatura: `hotfix/<descrição-curta>`
  - Exemplo: `hotfix/fix-erro-conexao-db`
  - PR vai para `main`, depois merge para `develop`.
  
- **Release** *(opcional)*: Preparação para versão.
  - Nomenclatura: `release/<versão>`
  - Exemplo: `release/1.2.0`

---

## 2. Commits

O projeto segue o padrão **Conventional Commits**:

### **Formato**
```

<tipo>\[escopo opcional]: <mensagem curta>

\[corpo opcional com mais detalhes]

\[footer opcional para issues, breaking changes, etc.]

```

### **Tipos recomendados**
| Tipo      | Uso                                           | Exemplo |
|-----------|----------------------------------------------|---------|
| feat      | Nova funcionalidade                           | feat(pipeline): adicionar transformação de clientes ativos |
| fix       | Correção de bug                               | fix(etl): corrigir erro de duplicidade no staging |
| docs      | Documentação                                 | docs(readme): atualizar instruções de setup |
| style     | Formatação, lint, espaçamento                | style(code): aplicar PEP8 com black |
| refactor  | Refatoração sem mudança de funcionalidade    | refactor(etl): extrair função de validação |
| test      | Adicionar ou corrigir testes                 | test(etl): adicionar teste para pipeline de vendas |
| chore     | Tarefas administrativas (ex: dependências)  | chore(deps): atualizar pandas para 2.1 |

### **Boas práticas**
1. Mensagem curta **imperativa** (ex: “Adicionar validação”).
2. Escopo opcional ajuda a identificar módulo ou área do código (`etl`, `db`, `pipeline`).
3. Mensagem do corpo deve explicar **porquê** da mudança, não só **o que**.
4. Footer pode referenciar tickets ou breaking changes, ex:  
   `BREAKING CHANGE: altera nome da tabela staging`

---

## 3. Regras operacionais

- Sempre faça **pull e rebase** antes de enviar commits.
- Não commitar arquivos gerados automaticamente ou sensíveis (`.pyc`, `.env`).
- Commits devem ser pequenos e coerentes, cada commit **uma unidade lógica**.
- Para merges de feature, use **Pull Request** e revise com pelo menos 1 colega.

---

Seguindo essas regras, garantimos um histórico limpo, fácil de entender e manutenção mais segura do projeto.
