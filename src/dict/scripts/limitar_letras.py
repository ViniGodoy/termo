from __future__ import annotations

from pathlib import Path

from game.constants import WORD_SIZE


def limitar_5_letras() -> None:
    """Processa todos os arquivos de texto (.txt), mantendo apenas as palavras que possuem exatamente 5 letras.

    A função lê cada arquivo, remove espaços em branco, filtra as palavras de 5 caracteres,
    converte-as para letras minúsculas, remove duplicatas e ordena o resultado em ordem alfabética.
    O arquivo original é então sobrescrito com a lista resultante.
    """
    caminho_dir = Path(__file__).parent.parent
    # Itera sobre todos os arquivos .txt no diretório
    for arquivo in caminho_dir.glob("*.txt"):
        print(f"Processando {arquivo.name}")
        with arquivo.open(encoding="utf-8") as f:
            # splitlines() remove as quebras de linha (\n ou \r\n) facilitando a contagem
            linhas = f.read().splitlines()

        # Remove espaços em branco nas pontas, filtra por 5 letras e converte para minúsculo
        palavras_filtradas = [
            linha.strip().lower() for linha in linhas if len(linha.strip()) == WORD_SIZE
        ]

        # Sobrescreve o arquivo original
        with arquivo.open("w", encoding="utf-8") as f:
            if palavras_filtradas:
                f.write("\n".join(sorted(set(palavras_filtradas))) + "\n")
            else:
                f.write("")


if __name__ == "__main__":
    limitar_5_letras()
