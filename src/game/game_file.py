import logging
from pathlib import Path
from typing import Self

log = logging.getLogger(__name__)

_INI_FILE = Path(__file__).parent.parent / "game.ini"


class GameFile:
    def __init__(self) -> None:
        self.stats = [0, 0, 0, 0, 0, 0, 0]
        self.cheat = False

    def load(self) -> Self:
        if not _INI_FILE.exists():
            self.save()
            return self

        try:
            with _INI_FILE.open(encoding="utf-8") as f:
                for item in f:
                    line = item.strip().upper()
                    if not line or line[0] == "#":
                        continue

                    prop = line.split("=")
                    if prop[0] == "STATS":
                        self.stats = [int(p) for p in prop[1].split(",")]
                    if prop[0] == "CHEAT":
                        self.cheat = prop[1] == "TRUE"
        except BaseException as error:
            log.exception("Invalid ini file. Ignoring", exc_info=error)
        return self

    def save(self) -> None:
        try:
            file = Path(__file__).parent.parent / "game.ini"
            with file.open("w", encoding="utf-8") as f:
                f.write("STATS=")
                f.write(",".join([str(s) for s in self.stats]))
                f.write("\n")
                if self.cheat:
                    f.write("CHEAT=TRUE\n")
        except BaseException as error:
            log.exception("Error saving ini file. Ignoring", exc_info=error)
