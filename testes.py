"""Testes automáticos do sistema, usando apenas a biblioteca padrão."""

import tempfile
import unittest
from pathlib import Path

from main import (
    adicionar_contrato,
    alterar_contrato,
    buscar_contrato,
    carregar_contratos,
    contagem_por_situacao,
    salvar_contratos,
    validar_contrato,
)


class TestesContratos(unittest.TestCase):
    def setUp(self):
        self.exemplo = {
            "numero": "0012", "cliente": "Empresa Fictícia A",
            "objeto": "Prestação de serviços", "data_inicio": "10/03/2026",
            "data_termino": "10/03/2027", "situacao": "Pendente",
            "observacoes": "Teste acadêmico",
        }

    def test_cadastro_e_consulta(self):
        registros = adicionar_contrato([], self.exemplo)
        self.assertEqual(buscar_contrato(registros, "0012"), 0)
        self.assertEqual(registros[0]["cliente"], "Empresa Fictícia A")

    def test_numero_duplicado(self):
        registros = adicionar_contrato([], self.exemplo)
        with self.assertRaisesRegex(ValueError, "Já existe"):
            adicionar_contrato(registros, self.exemplo)

    def test_campos_obrigatorios(self):
        with self.assertRaisesRegex(ValueError, "obrigatório"):
            validar_contrato({**self.exemplo, "cliente": " "})

    def test_formato_de_data(self):
        with self.assertRaisesRegex(ValueError, "Data inválida"):
            validar_contrato({**self.exemplo, "data_inicio": "1/3/2026"})

    def test_termino_anterior_ao_inicio(self):
        with self.assertRaisesRegex(ValueError, "anterior"):
            validar_contrato({**self.exemplo, "data_termino": "09/03/2026"})

    def test_datas_opcionais(self):
        contrato = validar_contrato({**self.exemplo, "data_inicio": "", "data_termino": ""})
        self.assertEqual(contrato["data_inicio"], "")

    def test_atualizar_situacao(self):
        registros = adicionar_contrato([], self.exemplo)
        atualizados = alterar_contrato(registros, "0012", {"situacao": "Concluído"})
        self.assertEqual(atualizados[0]["situacao"], "Concluído")
        self.assertEqual(registros[0]["situacao"], "Pendente")

    def test_bloqueio_da_alteracao_do_numero(self):
        registros = adicionar_contrato([], self.exemplo)
        with self.assertRaisesRegex(ValueError, "não pode ser alterado"):
            alterar_contrato(registros, "0012", {"numero": "0099"})

    def test_csv_persistencia_e_caracteres(self):
        registros = adicionar_contrato([], {**self.exemplo, "observacoes": "Descrição; com ç e á"})
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "contratos.csv"
            salvar_contratos(registros, arquivo)
            recuperados = carregar_contratos(arquivo)
        self.assertEqual(recuperados, registros)

    def test_csv_inexistente(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.assertEqual(carregar_contratos(Path(pasta) / "contratos.csv"), [])

    def test_csv_com_cabecalho_invalido(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "contratos.csv"
            arquivo.write_text("numero;cliente\n123;Teste\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cabeçalho"):
                carregar_contratos(arquivo)

    def test_contagem_das_situacoes(self):
        registros = adicionar_contrato([], self.exemplo)
        registros = adicionar_contrato(registros, {**self.exemplo, "numero": "0013", "situacao": "Concluído"})
        contagem = contagem_por_situacao(registros)
        self.assertEqual(contagem["Pendente"], 1)
        self.assertEqual(contagem["Concluído"], 1)
        self.assertEqual(sum(contagem.values()), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
