import asyncio
from enum import Enum

import aiohttp
from bs4 import BeautifulSoup


class Domain:
    def __init__(self, name: str, host: str, expected_title: str) -> None:
        self.name = name
        self.host = host
        self.expected_title = expected_title


DOMAINS: list[Domain] = [
    Domain("vulcan.net.pl", "https://uonetplus.vulcan.net.pl/warszawa/", "Dziennik UONET+"),
    Domain("vulcan.net.pl: Uczeń", "https://uonetplus-uczen.vulcan.net.pl/warszawa", "Uczeń"),
    Domain(
        "vulcan.net.pl: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.vulcan.net.pl/warszawa",
        "Wiadomości Plus",
    ),
    Domain("vulcan.net.pl: Aplikacja mobilna", "https://lekcjaplus.vulcan.net.pl", "Eduone"),
    Domain("umt.tarnow.pl", "https://uonetplus.umt.tarnow.pl/tarnow", "Zaloguj"),
    Domain("umt.tarnow.pl: Uczeń", "https://uonetplus-uczen.umt.tarnow.pl/tarnow", "Zaloguj"),
    Domain(
        "umt.tarnow.pl: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.umt.tarnow.pl/tarnow",
        "Zaloguj",
    ),
    Domain(
        "umt.tarnow.pl: Aplikacja mobilna",
        "https://uonetplus-komunikacja.umt.tarnow.pl/tarnow",
        "UONET+ dla urządzeń mobilnych",
    ),
    Domain(
        "eszkola.opolskie.pl",
        "https://uonetplus.eszkola.opolskie.pl/opole",
        "Logowanie do systemu Opolska e-Szkola",
    ),
    Domain(
        "eszkola.opolskie.pl: Uczeń",
        "https://uonetplus-uczen.eszkola.opolskie.pl/opole",
        "Logowanie do systemu Opolska e-Szkola",
    ),
    Domain(
        "eszkola.opolskie.pl: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.eszkola.opolskie.pl/opole",
        "Logowanie do systemu Opolska e-Szkola",
    ),
    Domain(
        "eszkola.opolskie.pl: Aplikacja mobilna",
        "https://uonetplus-komunikacja.eszkola.opolskie.pl/opole",
        "UONET+ dla urządzeń mobilnych",
    ),
    Domain("Rzeszów", "https://portal.vulcan.net.pl/rzeszowprojekt", "Platforma VULCAN"),
    Domain(
        "resman.pl: Uczeń",
        "https://uonetplus-uczen.vulcan.net.pl/rzeszowprojekt",
        "Logowanie do systemu",
    ),
    Domain(
        "Rzeszów: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.vulcan.net.pl/rzeszowprojekt",
        "Logowanie do systemu",
    ),
    Domain("edu.gdansk.pl", "https://uonetplus.edu.gdansk.pl/gdansk", "Logowanie do systemu"),
    Domain(
        "edu.gdansk.pl: Uczeń",
        "https://uonetplus-uczen.edu.gdansk.pl/gdansk",
        "Logowanie do systemu",
    ),
    Domain(
        "edu.gdansk.pl: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.edu.gdansk.pl/gdansk",
        "Logowanie do systemu",
    ),
    Domain(
        "edu.gdansk.pl: Aplikacja mobilna",
        "https://uonetplus-komunikacja.edu.gdansk.pl/gdansk",
        "UONET+ dla urządzeń mobilnych",
    ),
    Domain("edu.lublin.eu", "https://uonetplus.edu.lublin.eu/lublin", "Logowanie do systemu"),
    Domain(
        "edu.lublin.eu: Uczeń",
        "https://uonetplus-uczen.edu.lublin.eu/lublin",
        "Logowanie do systemu",
    ),
    Domain(
        "edu.lublin.eu: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.edu.lublin.eu/lublin",
        "Logowanie do systemu",
    ),
    Domain(
        "edu.lublin.eu: Aplikacja mobilna",
        "https://uonetplus-komunikacja.edu.lublin.eu/lublin",
        "UONET+ dla urządzeń mobilnych",
    ),
    Domain("eduportal.koszalin.pl", "https://uonetplus.eduportal.koszalin.pl/koszalin", "Zaloguj"),
    Domain(
        "eduportal.koszalin.pl: Uczeń",
        "https://uonetplus-uczen.eduportal.koszalin.pl/koszalin",
        "Zaloguj",
    ),
    Domain(
        "eduportal.koszalin.pl: Wiadomości Plus",
        "https://uonetplus-wiadomosciplus.eduportal.koszalin.pl/koszalin",
        "Zaloguj",
    ),
    Domain(
        "eduportal.koszalin.pl: Aplikacja mobilna",
        "https://uonetplus-komunikacja.eduportal.koszalin.pl/koszalin",
        "UONET+ dla urządzeń mobilnych",
    ),
]


class Result(Enum):
    OK = 0
    DATABASE_UPDATE = 1
    BREAK = 2
    ERROR = 3
    TIMEOUT = 4
    UNKNOWN = 5


class Status:
    def __init__(self, state: Result, status_code: int | None, message: str | None) -> None:
        self.state = state
        self.status_code = status_code
        self.message = message


async def check_status(http_client: aiohttp.ClientSession, url: str, expected_title: str) -> Status:
    try:
        response = await http_client.get(url, timeout=10)
    except asyncio.TimeoutError as e:
        return Status(Result.TIMEOUT, None, "Timeout")
    except aiohttp.ClientError as e:
        return Status(Result.ERROR, None, str(e))

    soup = BeautifulSoup(await response.text(), "html.parser")

    if error_div := soup.find(id="MainPage_ErrorDiv"):
        return Status(Result.ERROR, response.status, error_div.get_text())

    title = soup.title.string if soup.title else None

    if title == expected_title:
        return Status(Result.OK, response.status, None)

    return Status(Result.UNKNOWN, response.status, title)


async def check_all(http_client: aiohttp.ClientSession) -> list[tuple[str, Status]]:
    status = await asyncio.gather(
        *(check_status(http_client, domain.host, domain.expected_title) for domain in DOMAINS)
    )

    return [(domain.name, result) for (domain, result) in zip(DOMAINS, status)]
