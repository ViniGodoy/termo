from __future__ import annotations

from pathlib import Path

# Nomes dos arquivos
ARQUIVO_NEGATIVAS = "negativas.txt"
ARQUIVO_LEXICO = "lexico.txt"


def filtrar_negativas(caminho_alvo: str, caminho_referencia: str) -> None:
    """Filtra as palavras de um arquivo alvo, mantendo apenas aquelas que também existem em um arquivo de referência (léxico).

    Args:
        caminho_alvo (str): Nome ou caminho relativo do arquivo a ser filtrado.
        caminho_referencia (str): Nome ou caminho relativo do arquivo usado como referência (léxico).

    Raises:
        FileNotFoundError: Se o arquivo alvo ou o arquivo de referência não forem encontrados.
    """
    path_palavras = Path(__file__).parent.parent
    path_alvo = path_palavras / Path(caminho_alvo)
    path_ref = path_palavras / Path(caminho_referencia)

    if not path_alvo.exists():
        msg = f"Arquivo alvo não encontrado: {path_alvo.absolute()}"
        raise FileNotFoundError(msg)
    if not path_ref.exists():
        msg = f"Arquivo de referência não encontrado: {path_ref.absolute()}"
        raise FileNotFoundError(msg)

    # Carrega o léxico em memória usando um set para buscas otimizadas
    with path_ref.open(encoding="utf-8") as f_ref:
        lexico = {linha.strip() for linha in f_ref if linha.strip()}

    # Lê o arquivo que será filtrado
    with path_alvo.open(encoding="utf-8") as f_alvo:
        palavras_alvo = [linha.strip() for linha in f_alvo if linha.strip()]

    # Mantém apenas as palavras que estão presentes no set do léxico
    palavras_filtradas = [palavra for palavra in palavras_alvo if palavra in lexico]

    # Sobrescreve o arquivo alvo
    with path_alvo.open("w", encoding="utf-8") as f_alvo:
        if palavras_filtradas:
            f_alvo.write("\n".join(palavras_filtradas) + "\n")
        else:
            f_alvo.write("")


if __name__ == "__main__":
    filtrar_negativas(ARQUIVO_NEGATIVAS, ARQUIVO_LEXICO)
