from __future__ import annotations

import csv
from pathlib import Path

ARQUIVO_COMUNS = "comuns.csv"
ARQUIVO_LEXICO = "lexico.txt"
ARQUIVO_EXCLUIDAS = "excluidas.txt"
ARQUIVO_PALAVRAS_CSV = "palavras.csv"


def filtrar_comuns_nao_no_lexico() -> None:
    """Filtra palavras do arquivo 'comuns.csv'.

    As que não existem no 'lexico.txt' são salvas no arquivo 'excluidas.txt' (uma por linha, apenas a palavra).
    As que existem são salvas integralmente no arquivo 'palavras.csv' (linhas completas com a contagem).
    O arquivo original 'comuns.csv' não é alterado.
    """
    path_dict = Path(__file__).parent.parent
    path_comuns = path_dict / ARQUIVO_COMUNS
    path_lexico = path_dict / ARQUIVO_LEXICO
    path_excluidas = path_dict / ARQUIVO_EXCLUIDAS
    path_palavras_csv = path_dict / ARQUIVO_PALAVRAS_CSV

    if not path_comuns.exists():
        msg = f"Arquivo comuns não encontrado: {path_comuns.absolute()}"
        raise FileNotFoundError(msg)
    if not path_lexico.exists():
        msg = f"Arquivo léxico não encontrado: {path_lexico.absolute()}"
        raise FileNotFoundError(msg)

    # Carrega o léxico num conjunto (set) para busca eficiente
    with path_lexico.open(encoding="utf-8") as f_lexico:
        lexico = {linha.strip() for linha in f_lexico if linha.strip()}

    excluidas = []
    palavras_manter = []
    cabecalho = None

    # Lê as palavras do CSV
    with path_comuns.open(encoding="utf-8") as f_comuns:
        leitor_csv = csv.reader(f_comuns)
        # Lê o cabeçalho se houver (vamos assumir que tem)
        cabecalho = next(leitor_csv, None)

        for linha in leitor_csv:
            if not linha:
                continue
            # A palavra é a primeira coluna
            palavra = linha[0].strip()

            if palavra:
                if palavra not in lexico:
                    # Se não estiver no léxico, vai para excluídas (apenas a palavra)
                    excluidas.append(palavra)
                else:
                    # Se estiver, mantemos a linha completa para palavras.csv
                    palavras_manter.append(linha)

    # Escreve as excluídas no novo arquivo de excluídas
    with path_excluidas.open("w", encoding="utf-8") as f_excluidas:
        if excluidas:
            f_excluidas.write("\n".join(excluidas) + "\n")
        else:
            f_excluidas.write("")

    # Escreve as mantidas no novo arquivo de CSV
    with path_palavras_csv.open("w", encoding="utf-8", newline="") as f_palavras:
        escritor_csv = csv.writer(f_palavras)
        if cabecalho:
            escritor_csv.writerow(cabecalho)
        escritor_csv.writerows(palavras_manter)


if __name__ == "__main__":
    filtrar_comuns_nao_no_lexico()
