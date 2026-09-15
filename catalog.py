from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Connector:
    name: str
    target: str
    binary: str
    args: tuple[str, ...]
    description: str
    level: str = "passive"


# Every command is argument-vector based: no shell interpolation is performed.
# These integrations restrict themselves to public records / passive collection.
CONNECTORS = (
    Connector("whois", "domain", "whois", ("{domain}",), "Registro público del dominio."),
    Connector("dns", "domain", "dig", ("+noall", "+answer", "{domain}", "ANY"), "Registros DNS públicos."),
    Connector("subfinder-passive", "domain", "subfinder", ("-d", "{domain}", "-silent", "-all"), "Subdominios de fuentes pasivas."),
    Connector("amass-intel", "domain", "amass", ("intel", "-d", "{domain}"), "Intel de dominio con Amass."),
    Connector("theharvester", "domain", "theHarvester", ("-d", "{domain}", "-b", "all", "-l", "100"), "Fuentes públicas indexadas."),
    Connector("sherlock", "username", "sherlock", ("{username}", "--print-found", "--no-color"), "Perfiles públicos por nombre de usuario."),
    Connector("maigret", "username", "maigret", ("{username}", "--no-color"), "Búsqueda pública de alias."),
)


def for_target(kind: str) -> tuple[Connector, ...]:
    return tuple(c for c in CONNECTORS if c.target == kind)
