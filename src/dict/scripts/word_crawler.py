import asyncio
from collections import Counter
import logging
import re

import aiohttp
import pandas as pd

from game.constants import WORD_SIZE

log = logging.getLogger(__name__)


async def get_featured_articles(session: aiohttp.ClientSession) -> list[str]:
    api_url: str = "https://pt.wikipedia.org/w/api.php"

    params = {
        "action": "parse",
        "page": "Wikipédia:Artigos_destacados",
        "prop": "links",
        "format": "json",
    }

    async with session.get(api_url, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    article_titles: list[str] = []

    if "parse" in data and "links" in data["parse"]:
        for link in data["parse"]["links"]:
            if link.get("ns") == 0 and "exists" in link:
                title: str = link["*"]
                if title != "Página principal":
                    article_titles.append(title)

    return article_titles


async def process_article(
    session: aiohttp.ClientSession, title: str
) -> tuple[Counter[str], int, int]:
    api_url: str = "https://pt.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "prop": "extracts",
        "titles": title,
        "explaintext": "1",
        "format": "json",
    }

    async with session.get(api_url, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    pages = data.get("query", {}).get("pages", {})
    text: str = ""

    for page_data in pages.values():
        text = page_data.get("extract", "")
        break

    all_words: list[str] = re.findall(r"\b[^\W\d_]+\b", text.lower())
    five_letter_words: list[str] = [w for w in all_words if len(w) == WORD_SIZE]

    words_count: int = len(all_words)
    five_letter_count: int = len(five_letter_words)

    print(
        f"Processado: {title} | Total de palavras: {words_count} | 5 letras: {five_letter_count}"
    )

    return Counter(five_letter_words), words_count, five_letter_count


async def main() -> None:
    total_words_processed: int = 0
    total_five_letter_indexed: int = 0
    total_counts: Counter[str] = Counter()
    chunk_size: int = 30

    headers: dict[str, str] = {
        "User-Agent": "CrawlerArtigosWikipedia/1.0 (student@pucpr.br) aiohttp/3.x"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            all_titles: list[str] = await get_featured_articles(session)
        except aiohttp.ClientError as e:
            print(f"Erro ao buscar a lista de artigos: {e}")
            return

        total_articles: int = len(all_titles)
        if total_articles == 0:
            print("Nenhum artigo encontrado.")
            return

        print(
            f"Indexando todos os {total_articles} artigos encontrados em lotes de {chunk_size}...\n"
        )

        # Processamento em lotes
        for i in range(0, total_articles, chunk_size):
            chunk = all_titles[i : i + chunk_size]
            print(
                f"--- Iniciando lote {i // chunk_size + 1} (Artigos {i + 1} a {min(i + chunk_size, total_articles)}) ---"
            )

            tasks: list[tuple[str, asyncio.Task[tuple[Counter[str], int, int]]]] = []

            async with asyncio.TaskGroup() as tg:
                for title in chunk:
                    task = tg.create_task(process_article(session, title))
                    tasks.append((title, task))

            for title, task in tasks:
                try:
                    article_counts, words_processed, five_letter_indexed = task.result()
                    total_counts.update(article_counts)
                    total_words_processed += words_processed
                    total_five_letter_indexed += five_letter_indexed
                except aiohttp.ClientError as e:
                    print(f"Erro de rede ao processar o artigo '{title}': {e}")
                except Exception as e:
                    log.exception(
                        msg="Erro inesperado no artigo.",
                        extra={"title": title},
                        exc_info=e,
                    )

            # Aguarda 1 segundo antes do próximo lote, exceto no último
            if i + chunk_size < total_articles:
                await asyncio.sleep(10)

    output_file: str = "comuns.csv"

    df: pd.DataFrame = pd.DataFrame(
        total_counts.items(), columns=["palavra", "quantidade"]
    )
    df = df.sort_values(by="quantidade", ascending=False)
    df.to_csv(output_file, index=False, encoding="utf-8")

    print("\nProcessamento concluído.")
    print(f"Quantidade de palavras processadas: {total_words_processed}")
    print(f"Quantidade de palavras de 5 letras indexadas: {total_five_letter_indexed}")
    print(f"Total de palavras de 5 letras únicas salvas no CSV: {len(df)}")


if __name__ == "__main__":
    asyncio.run(main())
