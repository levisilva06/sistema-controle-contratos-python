"""Projeto Integrador UNISA — Sistema de Controle de Contratos.

Aplicação de terminal, escrita em Python e com persistência em CSV.
Utilize somente registros fictícios para os testes acadêmicos.
"""

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path


ARQUIVO_CSV = Path(__file__).with_name("contratos.csv")
CAMPOS = (
    "numero", "cliente", "objeto", "data_inicio", "data_termino",
    "situacao", "observacoes",
)
SITUACOES = ("Pendente", "Em andamento", "Concluído", "Inativo")
CAMPOS_OPCIONAIS = ("data_inicio", "data_termino", "observacoes")


def validar_data(valor):
    """Aceita uma data em DD/MM/AAAA ou um texto vazio (campo opcional)."""
    if not valor:
        return
    try:
        data = datetime.strptime(valor, "%d/%m/%Y")
    except ValueError as erro:
        raise ValueError(f"Data inválida: {valor}. Use DD/MM/AAAA.") from erro
    if data.strftime("%d/%m/%Y") != valor:
        raise ValueError(f"Data inválida: {valor}. Use DD/MM/AAAA.")


def validar_contrato(dados):
    """Padroniza e valida um registro antes de gravá-lo."""
    contrato = {campo: str(dados.get(campo, "")).strip() for campo in CAMPOS}
    for campo in ("numero", "cliente", "objeto", "situacao"):
        if not contrato[campo]:
            raise ValueError(f"O campo '{campo}' é obrigatório.")

    if contrato["situacao"] not in SITUACOES:
        raise ValueError("Situação inválida.")

    inicio, termino = contrato["data_inicio"], contrato["data_termino"]
    validar_data(inicio)
    validar_data(termino)
    if inicio and termino:
        primeira = datetime.strptime(inicio, "%d/%m/%Y")
        ultima = datetime.strptime(termino, "%d/%m/%Y")
        if ultima < primeira:
            raise ValueError("A data de término não pode ser anterior à de início.")
    return contrato


def buscar_contrato(contratos, numero):
    """Devolve a posição do contrato ou -1 quando ele não existe."""
    for indice, contrato in enumerate(contratos):
        if contrato["numero"] == numero.strip():
            return indice
    return -1


def adicionar_contrato(contratos, dados):
    """Cria uma lista nova com o contrato, evitando números duplicados."""
    contrato = validar_contrato(dados)
    if buscar_contrato(contratos, contrato["numero"]) != -1:
        raise ValueError("Já existe um contrato com esse número.")
    return contratos + [contrato]


def alterar_contrato(contratos, numero, alteracoes):
    """Atualiza os campos informados sem modificar o número do contrato."""
    indice = buscar_contrato(contratos, numero)
    if indice == -1:
        raise ValueError("Contrato não encontrado.")
    if "numero" in alteracoes:
        raise ValueError("O número do contrato não pode ser alterado.")
    if any(campo not in CAMPOS for campo in alteracoes):
        raise ValueError("Campo de atualização desconhecido.")
    novo = dict(contratos[indice])
    novo.update(alteracoes)
    novo = validar_contrato(novo)
    resultado = list(contratos)
    resultado[indice] = novo
    return resultado


def carregar_contratos(caminho=ARQUIVO_CSV):
    """Recupera os dados previamente salvos; começa vazio se não há CSV."""
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    with caminho.open("r", newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        if leitor.fieldnames != list(CAMPOS):
            raise ValueError("O arquivo CSV não possui o cabeçalho esperado.")
        registros = []
        for linha in leitor:
            registros = adicionar_contrato(registros, linha)
        return registros


def salvar_contratos(contratos, caminho=ARQUIVO_CSV):
    """Salva os contratos em CSV, com separador ; e codificação UTF-8."""
    caminho = Path(caminho)
    with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS, delimiter=";")
        escritor.writeheader()
        escritor.writerows(contratos)


def mostrar_contrato(contrato):
    nomes = {
        "numero": "Número", "cliente": "Cliente", "objeto": "Objeto",
        "data_inicio": "Data de início", "data_termino": "Data de término",
        "situacao": "Situação", "observacoes": "Observações",
    }
    print("\n--- DADOS DO CONTRATO ---")
    for campo in CAMPOS:
        print(f"{nomes[campo]}: {contrato[campo] or '(não informado)'}")


def escolher_situacao():
    print("\nSituações disponíveis:")
    for indice, situacao in enumerate(SITUACOES, start=1):
        print(f"{indice} - {situacao}")
    opcao = input("Selecione a situação: ").strip()
    if opcao not in ("1", "2", "3", "4"):
        raise ValueError("Escolha uma situação de 1 a 4.")
    return SITUACOES[int(opcao) - 1]


def cadastrar(contratos):
    print("\n--- CADASTRAR CONTRATO ---")
    dados = {
        "numero": input("Número: "),
        "cliente": input("Cliente (fictício): "),
        "objeto": input("Objeto contratual: "),
        "data_inicio": input("Data de início (DD/MM/AAAA ou vazio): "),
        "data_termino": input("Data de término (DD/MM/AAAA ou vazio): "),
        "situacao": escolher_situacao(),
        "observacoes": input("Observações (opcional): "),
    }
    atualizados = adicionar_contrato(contratos, dados)
    salvar_contratos(atualizados)
    print("Contrato cadastrado com sucesso!")
    return atualizados


def consultar(contratos):
    numero = input("\nNúmero do contrato para consulta: ").strip()
    indice = buscar_contrato(contratos, numero)
    if indice == -1:
        print("Contrato não encontrado.")
    else:
        mostrar_contrato(contratos[indice])


def atualizar(contratos):
    print("\n--- ATUALIZAR CONTRATO ---")
    numero = input("Número do contrato: ").strip()
    indice = buscar_contrato(contratos, numero)
    if indice == -1:
        print("Contrato não encontrado.")
        return contratos
    mostrar_contrato(contratos[indice])

    editaveis = ("cliente", "objeto", "data_inicio", "data_termino", "situacao", "observacoes")
    print("\nQual campo deseja alterar?")
    for posicao, campo in enumerate(editaveis, start=1):
        print(f"{posicao} - {campo.replace('_', ' ').capitalize()}")
    print("0 - Cancelar")
    escolha = input("Opção: ").strip()
    if escolha == "0":
        print("Atualização cancelada.")
        return contratos
    if escolha not in tuple(str(i) for i in range(1, len(editaveis) + 1)):
        raise ValueError("Opção de atualização inválida.")

    campo = editaveis[int(escolha) - 1]
    if campo == "situacao":
        valor = escolher_situacao()
    else:
        print("Digite o novo valor. Para limpar um campo opcional, informe '-'.")
        valor = input("Novo valor: ").strip()
        if valor == "-":
            if campo not in CAMPOS_OPCIONAIS:
                raise ValueError("Esse campo não pode ficar vazio.")
            valor = ""
    atualizados = alterar_contrato(contratos, numero, {campo: valor})
    salvar_contratos(atualizados)
    print("Contrato atualizado com sucesso!")
    return atualizados


def listar(contratos):
    print("\n--- LISTAR CONTRATOS ---")
    print("0 - Todos os contratos")
    for indice, situacao in enumerate(SITUACOES, start=1):
        print(f"{indice} - {situacao}")
    opcao = input("Filtrar por situação: ").strip()
    if opcao == "0":
        selecionados = contratos
    elif opcao in ("1", "2", "3", "4"):
        situacao = SITUACOES[int(opcao) - 1]
        selecionados = [c for c in contratos if c["situacao"] == situacao]
    else:
        raise ValueError("Filtro inválido.")

    if not selecionados:
        print("Nenhum contrato encontrado.")
        return
    print(f"\n{'NÚMERO':<16} {'CLIENTE':<30} SITUAÇÃO")
    print("-" * 66)
    for contrato in selecionados:
        numero = contrato["numero"][:15]
        cliente = contrato["cliente"][:29]
        print(f"{numero:<16} {cliente:<30} {contrato['situacao']}")
    print(f"Total na listagem: {len(selecionados)}")


def contagem_por_situacao(contratos):
    contagem = Counter(c["situacao"] for c in contratos)
    return {situacao: contagem[situacao] for situacao in SITUACOES}


def relatorio(contratos):
    print("\n--- RELATÓRIO DE CONTRATOS ---")
    print(f"Total de contratos: {len(contratos)}")
    for situacao, quantidade in contagem_por_situacao(contratos).items():
        print(f"{situacao}: {quantidade}")


def menu():
    print("\n" + "=" * 46)
    print("      SISTEMA DE CONTROLE DE CONTRATOS")
    print("=" * 46)
    print("1 - Cadastrar contrato")
    print("2 - Consultar contrato")
    print("3 - Atualizar contrato")
    print("4 - Listar contratos")
    print("5 - Gerar relatório")
    print("0 - Sair")
    return input("Escolha uma opção: ").strip()


def main():
    try:
        contratos = carregar_contratos()
    except (OSError, ValueError) as erro:
        print(f"Não foi possível abrir o arquivo de dados: {erro}")
        return

    while True:
        try:
            opcao = menu()
            if opcao == "1":
                contratos = cadastrar(contratos)
            elif opcao == "2":
                consultar(contratos)
            elif opcao == "3":
                contratos = atualizar(contratos)
            elif opcao == "4":
                listar(contratos)
            elif opcao == "5":
                relatorio(contratos)
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opção inválida. Escolha um número do menu.")
        except (OSError, ValueError) as erro:
            print(f"Operação não concluída: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nSistema encerrado.")
            break


if __name__ == "__main__":
    main()
