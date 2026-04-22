# CliVet Relatório Gerencial

Aplicação em `Streamlit` para leitura gerencial de duas frentes independentes:

- `Financeiro`
- `Comercial`

O app identifica os arquivos pela estrutura das colunas, não pelo nome do arquivo.

## O que o projeto entrega

- leitura de `CSV`, `XLSX` e `XLS`
- financeiro com visão de:
  - `Caixa realizado`
  - `Competência do período`
- comercial com foco em vendas `Baixadas` e `Baixa parcial`
- DRE simplificada com parametrização por categoria
- rankings, mapas, quadros executivos e reflexões
- proteção de dados sensíveis no comercial
- exportação preparada para impressão/PDF pelo navegador

## Estrutura esperada dos anexos

### Financeiro

Colunas-base esperadas:

- `Data`
- `Conta`
- `Categoria`
- `Receita`
- `Despesa`
- `Valor pago`
- `Natureza`

### Comercial

Colunas-base esperadas:

- `Data e hora`
- `Venda`
- `Status da venda`
- `Cliente`
- `Animal`
- `Espécie`
- `Raça`
- `Tipo do Item`
- `Grupo`
- `Produto/serviço`
- `Líquido`

## Regras principais do app

### Financeiro

- `Caixa realizado`: considera apenas o que tem pagamento/recebimento efetivo
- `Competência do período`: considera todos os lançamentos do período, exceto transferências
- transferências ficam fora da análise principal
- lançamentos sem data de pagamento são tratados como `em aberto`
- movimentos societários aparecem em alerta, mas ficam fora da DRE operacional

### Comercial

- entram apenas `Baixado` e `Baixa parcial`
- `Aberto` fica fora das análises principais
- `P.A.` = quantidade de itens/linhas vendidas / quantidade de vendas únicas
- dados sensíveis são removidos da visualização antes da análise

## Rodar localmente

Crie e ative um ambiente virtual, depois instale as dependências:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se quiser testar com as bases já existentes na pasta, suba os dois arquivos pela sidebar do app.

## Deploy

O projeto está pronto para deploy simples em `Streamlit Community Cloud` ou ambiente equivalente.

### Arquivos essenciais

- `app.py`
- `requirements.txt`
- `README.md`
- `.streamlit/config.toml`
- `logo-clivet.jpg` (quando a logo final estiver definida)
- `mapeamento_financeiro.json` será criado/atualizado pelo app conforme a parametrização

### Checklist antes de subir

- confirmar se a logo final da clínica está na pasta do projeto
- revisar se o rodapé institucional do Maurício continua em placeholder, se ainda não for definir
- validar uma leitura com:
  - `Financeiro`
  - `Comercial`
  - `Caixa realizado`
  - `Competência do período`
- gerar um PDF de teste para conferir quebra de página e cortes visuais

### Observações de ambiente

- `XLSX` usa `openpyxl`
- `XLS` usa `xlrd`
- o arquivo `mapeamento_financeiro.json` precisa ficar gravável para salvar novas parametrizações

## Segurança e dados

- o comercial oculta nome completo e descarta campos sensíveis de contato e documentação
- o deploy deve usar apenas as bases enviadas pelo usuário, sem persistir cópias extras fora do projeto
- a visualização foi pensada para análise gerencial, não para exibir cadastro completo de clientes

## Observações finais

- o rodapé com a logo e o nome da empresa do Maurício ficou propositalmente em aberto
- o projeto foi mantido em um único arquivo para facilitar manutenção rápida
- se quiser uma versão futura mais robusta, o próximo passo natural seria criar um modo de exportação PDF dedicado
