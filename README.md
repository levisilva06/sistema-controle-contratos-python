# Sistema de Controle de Contratos — Projeto Integrador UNISA

Aplicação local de terminal desenvolvida em Python, utilizando **apenas a biblioteca padrão** e um arquivo CSV para guardar os dados. Foi criada para demonstração acadêmica com **informações fictícias**.

## Executar

É necessário ter **Python 3.9 ou superior** instalado. Extraia os arquivos para uma pasta e execute a partir dela:

- **Windows:** `py main.py` (ou `python main.py`)
- **macOS / Linux:** `python3 main.py`

O menu oferece as opções:

1. Cadastrar contrato;
2. Consultar contrato pelo número;
3. Atualizar um campo do contrato;
4. Listar todos ou filtrar por situação;
5. Gerar relatório com os totais por situação;
0. Sair.

O arquivo `contratos.csv` será criado na mesma pasta de `main.py` quando o primeiro contrato for salvo. Para testes novos, faça backup do CSV ou remova o arquivo de dados (não é necessário apagá-lo em uso normal).

## Campos do contrato

- **Obrigatórios:** número (identificador único, armazenado como texto), cliente, objeto contratual e situação.
- **Opcionais:** data de início, data de término e observações.
- **Datas:** DD/MM/AAAA; se ambas forem preenchidas, término >= início.
- **Situações:** Pendente, Em andamento, Concluído e Inativo.

Para limpar uma data ou observação ao **atualizar**, digite `-` como novo valor. O número do contrato não pode ser alterado. As situações são atribuídas manualmente.

## Exemplo de teste manual

1. Abra o menu e escolha `1`.
2. Informe `0012`, `Empresa Fictícia A`, `Prestação de serviços`, `10/03/2026`, `10/03/2027`, situação `1` e uma observação opcional.
3. Escolha `2` e consulte o contrato `0012`.
4. Escolha `3` e atualize a situação para `Concluído`.
5. Escolha `4` para listar os contratos.
6. Escolha `5` para verificar o relatório.
7. Saia com `0`, inicie novamente e consulte o contrato para confirmar que ele foi salvo.

## Testes automatizados

Execute na pasta do projeto:

- **Windows:** `py testes.py`
- **macOS / Linux:** `python3 testes.py`

Os testes cobrem validações de cadastro, datas, duplicidade, atualização, contagem e gravação/leitura do CSV.

## Arquivos

- `main.py` — código do programa, com menus, regras de negócio e CSV;
- `testes.py` — testes automatizados;
- `contratos.csv` — criado automaticamente quando o primeiro cadastro for salvo.

## Limitações

Não há login, interface gráfica, banco de dados relacional, edição simultânea nem integração externa. O arquivo CSV não é apropriado para armazenar contratos confidenciais, e esta versão não deve ser utilizada como sistema corporativo de produção.
