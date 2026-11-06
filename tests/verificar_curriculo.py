#!/usr/bin/env python3
"""Conferências locais do currículo estático.

Sem rede por padrão. Com --links, consulta o status HTTP dos hrefs https
e separa bloqueio de robô (403, 429, 999 e semelhantes) de página ausente.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
HTML_PATH = RAIZ / "index.html"
CSS_PATH = RAIZ / "css" / "estilo.css"
JS_PATH = RAIZ / "js" / "curriculo.js"
README_PATH = RAIZ / "README.md"

VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}

URLS_EXTERNAS = {
    "https://github.com/diegonbdprof-cloud",
    "https://github.com/diegonbdprof-cloud/etl-python-santander",
    "https://github.com/diegonbdprof-cloud/agente-trello",
    "https://github.com/diegonbdprof-cloud/meus-desafios-criativos",
    "https://github.com/diegonbdprof-cloud/desafios-python",
    "https://www.linkedin.com/in/diego-nonato-bastos-dias-aa2821342/",
    "https://github.com/digitalinnovationone/cv",
    "https://www.w3schools.com/howto/howto_website_create_resume.asp",
}

FRAGMENTOS = {"conteudo", "sobre", "situacao", "formacao", "projetos", "competencias"}

LOCAIS = {"css/estilo.css", "js/curriculo.js", "favicon.ico"}

TITULOS = [
    ("h1", "Diego Nonato Bastos Dias"),
    ("h2", "Competências"),
    ("h2", "Idiomas"),
    ("h2", "Sobre"),
    ("h2", "Situação profissional"),
    ("h2", "Formação"),
    ("h3", "Licenciatura em Física"),
    ("h3", "Bacharelado em Administração"),
    ("h3", "Estudos na Digital Innovation One"),
    ("h2", "Projetos"),
    ("h3", "Pipeline ETL em Python"),
    ("h3", "Agente organizador de tarefas no Trello"),
    ("h3", "Desafio de prompt da DIO"),
    ("h3", "Exercícios de lógica em Python"),
]

FRASES = [
    "Colombo, PR",
    "Busca a primeira vaga como engenheiro de dados júnior e não está empregado nessa função.",
    "Universidade do Estado do Pará (UEPA)",
    "Concluída em 2020",
    "Bacharelado em Administração",
    "UNINTER",
    "Datas de início e de conclusão não informadas.",
    "Certificados e carga horária não constam deste currículo.",
    "Excel avançado",
    "Engenharia de prompt",
    "IA generativa e LLMs",
    "leitura avançada de documentação técnica",
    "registros fictícios",
    "modelos de texto",
    "não é inteligência artificial",
    "sem rede",
    "20 testes de unittest",
    "Google ADK",
    "Gemini",
    "não foi validada",
    "prompt_agente_atendimento.md",
    "lógica em Python",
    "Não coleta dados e não usa rastreamento.",
    "Font Awesome",
    "W3Schools",
]

PROIBIDO_VISIVEL = [
    r"\bjorge\b",
    r"petrobras",
    r"kempetro",
    r"santo amaro",
    r"\btodo\b",
    r"link_github",
    r"usuario_",
    r"gmail",
    r"hotmail",
    r"@",
    r"%",
    r"\bfluente\b",
    r"\bnativo\b",
    r"conversação",
    r"conversacao",
    r"\btoefl\b",
    r"\bielts\b",
    r"\bpandas\b",
    r"\bspark\b",
    r"\baws\b",
    r"\bazure\b",
    r"estágio",
    r"estagio",
    r"freelancer",
    r"anos de experiência",
    r"anos de experiencia",
    r"\bnunca\b",
    r"98718",
    r"\(\d{2}\)\s*\d",
    r"\b\d{4,5}-\d{4}\b",
    r"\b\d{2}/\d{2}/\d{4}\b",
    r"nascid",
    r"aniversário",
    r"aniversario",
    r"mailto:",
    r"\btel:",
]

PROIBIDO_BRUTO = [
    "cdnjs",
    "w3.css",
    "fonts.googleapis",
    "font-awesome.min.css",
    'class="fa',
    'class="w3-',
    "googletagmanager",
    "google-analytics",
    "gtag(",
    "facebook",
    "hotjar",
    "<img",
    "<iframe",
    "<video",
    "<audio",
    "mailto:",
    "tel:",
    "http://",
    "gravatar",
    "ui-avatars",
]

JS_PROIBIDO = [
    "fetch(",
    "XMLHttpRequest",
    "localStorage",
    "sessionStorage",
    "document.cookie",
    "sendBeacon",
    "WebSocket",
    "geolocation",
    "indexedDB",
    "document.write",
]

AVISOS_ORIGINAIS = [
    "@falvojr: Reference article https://www.w3schools.com/howto/howto_website_create_resume.asp",
    "@falvojr: Useful link to use fontawesome (fa) icons: https://fontawesome.com/v4/icons/",
]

README_FRASES = [
    "https://github.com/digitalinnovationone/cv",
    "Como abrir no computador",
    "Como personalizar",
    "## Testes",
    "python3 tests/verificar_curriculo.py",
    "GitHub Pages não foi habilitado",
    "Font Awesome",
    "W3Schools",
    "20 testes",
    "não coleta",
]


class Arvore(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pilha: list[str | tuple[str, str]] = []
        self.erros: list[str] = []
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.ancoras: list[dict[str, str]] = []
        self.titulos: list[tuple[str, str]] = []
        self.visivel: list[str] = []
        self._ignorar = 0
        self._oculto = 0
        self._titulo: str | None = None
        self._texto_titulo: list[str] = []
        self.tem_style_attr = False
        self.tem_handler = False
        self.tabindex: list[str] = []
        self.scripts: list[str | None] = []
        self.stylesheets: list[str] = []
        self.lang = ""
        self.buttons = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._abrir(tag, attrs, fechar=tag in VOID)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._abrir(tag, attrs, fechar=True)

    def _abrir(self, tag: str, attrs: list[tuple[str, str | None]], fechar: bool) -> None:
        mapa = {chave: valor or "" for chave, valor in attrs}
        if tag == "html":
            self.lang = mapa.get("lang", "")
        if "id" in mapa:
            self.ids.append(mapa["id"])
        if "style" in mapa:
            self.tem_style_attr = True
        if any(chave.startswith("on") for chave in mapa):
            self.tem_handler = True
        if "tabindex" in mapa:
            self.tabindex.append(mapa["tabindex"])
        if tag == "a":
            href = mapa.get("href", "")
            self.hrefs.append(href)
            self.ancoras.append(mapa)
        if tag in {"img", "script", "iframe", "audio", "video", "source"} and "src" in mapa:
            self.srcs.append(mapa["src"])
        if tag == "script":
            self.scripts.append(mapa.get("src"))
        if tag == "link" and mapa.get("rel") == "stylesheet":
            self.stylesheets.append(mapa.get("href", ""))
        if tag == "button":
            self.buttons += 1
            if mapa.get("type") != "button":
                self.erros.append("botão sem type=button")
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self._ignorar == 0:
            self._titulo = tag
            self._texto_titulo = []
        if tag in {"script", "style"}:
            self._ignorar += 1
        if "sr-only" in mapa.get("class", "").split():
            self._oculto += 1
            if not fechar:
                self.pilha.append(("sr-only", tag))
                return
        if not fechar:
            self.pilha.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignorar:
            self._ignorar -= 1
        if tag in VOID:
            return
        if self.pilha and self.pilha[-1] == ("sr-only", tag):
            self.pilha.pop()
            self._oculto = max(0, self._oculto - 1)
            if self._titulo == tag:
                texto = re.sub(r"\s+", " ", "".join(self._texto_titulo)).strip()
                self.titulos.append((tag, texto))
                self._titulo = None
            return
        if self._titulo == tag:
            texto = re.sub(r"\s+", " ", "".join(self._texto_titulo)).strip()
            self.titulos.append((tag, texto))
            self._titulo = None
        if not self.pilha:
            self.erros.append(f"fechamento extra </{tag}>")
            return
        if self.pilha[-1] != tag:
            self.erros.append(
                f"fechou </{tag}> com <{self.pilha[-1]}> ainda aberto"
            )
            if tag in self.pilha:
                while self.pilha and self.pilha[-1] != tag:
                    self.pilha.pop()
                if self.pilha:
                    self.pilha.pop()
            return
        self.pilha.pop()

    def handle_data(self, data: str) -> None:
        if self._ignorar:
            return
        if self._titulo and self._oculto == 0:
            self._texto_titulo.append(data)
        if data.strip():
            self.visivel.append(data)

    def fechar(self) -> None:
        if self.pilha:
            abertas = ", ".join(str(item) for item in self.pilha)
            self.erros.append("tags ainda abertas: " + abertas)


def norm(texto: str) -> str:
    return re.sub(r"\s+", " ", texto).strip()


def registrar(falhas: list[str], nome: str, condicao: bool, detalhe: str = "") -> None:
    if condicao:
        print(f"OK  {nome}")
        return
    mensagem = nome if not detalhe else f"{nome}: {detalhe}"
    print(f"FALHA  {mensagem}")
    falhas.append(mensagem)


def estrutura(falhas: list[str]) -> Arvore | None:
    for caminho in (HTML_PATH, CSS_PATH, JS_PATH, README_PATH, RAIZ / "favicon.ico"):
        registrar(falhas, f"arquivo {caminho.relative_to(RAIZ)}", caminho.is_file())
    if not HTML_PATH.is_file():
        return None

    html = HTML_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.is_file() else ""
    js = JS_PATH.read_text(encoding="utf-8") if JS_PATH.is_file() else ""
    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.is_file() else ""

    arvore = Arvore()
    arvore.feed(html)
    arvore.fechar()
    registrar(falhas, "HTML balanceado", not arvore.erros, "; ".join(arvore.erros))
    registrar(falhas, "lang pt-BR", arvore.lang == "pt-BR", arvore.lang)
    registrar(falhas, "um só h1 e outline previsto", arvore.titulos == TITULOS, repr(arvore.titulos))

    visivel = norm(" ".join(arvore.visivel))
    for frase in FRASES:
        registrar(falhas, f"frase presente: {frase}", frase in visivel)
    registrar(
        falhas,
        "Em andamento duas vezes",
        visivel.count("Em andamento") >= 2,
        str(visivel.count("Em andamento")),
    )
    for padrao in PROIBIDO_VISIVEL:
        achou = re.search(padrao, visivel, flags=re.IGNORECASE)
        registrar(falhas, f"texto visível sem {padrao}", achou is None, achou.group(0) if achou else "")

    bruto = html.lower()
    for trecho in PROIBIDO_BRUTO:
        registrar(falhas, f"HTML sem {trecho}", trecho.lower() not in bruto)
    for aviso in AVISOS_ORIGINAIS:
        registrar(falhas, "aviso original preservado", aviso in html, aviso)

    registrar(falhas, "sem atributo style", not arvore.tem_style_attr)
    registrar(falhas, "sem handler inline", not arvore.tem_handler)
    registrar(
        falhas,
        "tabindex só -1",
        arvore.tabindex == ["-1"],
        repr(arvore.tabindex),
    )
    registrar(falhas, "ids únicos", len(arvore.ids) == len(set(arvore.ids)), repr(arvore.ids))
    registrar(falhas, "folha local única", arvore.stylesheets == ["css/estilo.css"], repr(arvore.stylesheets))
    registrar(falhas, "script local único", arvore.scripts == ["js/curriculo.js"], repr(arvore.scripts))
    registrar(falhas, "botão de imprimir", arvore.buttons == 1)

    externos = []
    fragmentos = []
    for href in arvore.hrefs:
        if href.startswith("https://"):
            externos.append(href)
        elif href.startswith("#"):
            fragmentos.append(href[1:])
        else:
            registrar(falhas, f"href local conhecido {href}", href in LOCAIS)
    registrar(
        falhas,
        "nenhum href externo fora da lista",
        set(externos) <= URLS_EXTERNAS,
        repr(sorted(set(externos) - URLS_EXTERNAS)),
    )
    faltando = URLS_EXTERNAS - set(externos)
    registrar(falhas, "todos os links previstos", not faltando, repr(sorted(faltando)))
    ids = set(arvore.ids)
    registrar(
        falhas,
        "fragmentos apontam para ids",
        set(fragmentos) <= ids,
        repr(sorted(set(fragmentos) - ids)),
    )
    registrar(
        falhas,
        "atalhos do menu",
        FRAGMENTOS <= set(fragmentos),
        repr(sorted(FRAGMENTOS - set(fragmentos))),
    )
    for ancora in arvore.ancoras:
        if ancora.get("target") == "_blank":
            rel = ancora.get("rel", "")
            registrar(
                falhas,
                f"noopener em {ancora.get('href', '')}",
                "noopener" in rel and "noreferrer" in rel,
                rel,
            )
    abas = sum(1 for ancora in arvore.ancoras if ancora.get("target") == "_blank")
    avisos_aba = visivel.count("(abre em nova aba)")
    registrar(falhas, "nova aba anunciada", abas == avisos_aba and abas == 10, f"{abas} links, {avisos_aba} avisos")

    registrar(falhas, "CSS com tela estreita", "@media (max-width: 800px)" in css)
    registrar(falhas, "CSS de impressão", "@media print" in css and "@page" in css)
    registrar(falhas, "CSS sem url(", "url(" not in css.lower())
    registrar(falhas, "CSS sem http://", "http://" not in css)
    registrar(
        falhas,
        "CSS cita https só no seletor de impressão",
        css.count("https://") == 1 and 'a[href^="https://"]' in css,
        str(css.count("https://")),
    )
    for trecho in JS_PROIBIDO:
        registrar(falhas, f"JS sem {trecho}", trecho not in js)
    registrar(falhas, "JS chama window.print", "window.print" in js)
    for frase in README_FRASES:
        registrar(falhas, f"README contém {frase}", frase in readme)
    return arvore


def consultar(url: str) -> tuple[str, str]:
    pedido = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(pedido, timeout=25) as resposta:
            return str(resposta.status), resposta.geturl()
    except urllib.error.HTTPError as erro:
        return str(erro.code), url
    except Exception as erro:  # noqa: BLE001 — o relatório precisa do erro real
        return f"ERRO {type(erro).__name__}: {erro}", url


def links(falhas: list[str]) -> None:
    print("-- links --")
    bloqueio = {"401", "403", "429", "503", "999"}
    for url in sorted(URLS_EXTERNAS):
        status, final = consultar(url)
        print(f"HTTP {status}  {url}  ->  {final}")
        if status in bloqueio or status.startswith("ERRO"):
            print(f"AVISO  resposta automática inconclusiva para {url}")
            continue
        if not status.isdigit() or int(status) >= 400:
            registrar(falhas, f"link acessível {url}", False, status)


def main() -> int:
    falhas: list[str] = []
    estrutura(falhas)
    if "--links" in sys.argv:
        links(falhas)
    print(f"\n{len(falhas)} falha(s).")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
