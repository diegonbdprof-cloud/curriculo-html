# Currículo HTML — Diego Nonato Bastos Dias

Currículo estático de Diego Nonato Bastos Dias, em Colombo, PR. A página apresenta um físico em transição de carreira que busca a primeira vaga de engenheiro de dados júnior e não está empregado nessa função.

O contato público da página é o [GitHub](https://github.com/diegonbdprof-cloud) e o [LinkedIn](https://www.linkedin.com/in/diego-nonato-bastos-dias-aa2821342/). Não há telefone, e-mail, endereço postal, foto, data de nascimento nem dado pessoal inventado.

## Adaptação

A estrutura parte do template de currículo da Digital Innovation One:

https://github.com/digitalinnovationone/cv

Esse template é uma página única (`index.html`) com cartão à esquerda, conteúdo à direita, rodapé em faixa e ícones. O HTML original aponta o artigo [How TO - Create a CV](https://www.w3schools.com/howto/howto_website_create_resume.asp), da W3Schools, e os ícones do Font Awesome 4. Os dois avisos de `@falvojr` permanecem literais no topo de `index.html`.

O que mudou, e por quê:

- Os dados do exemplo (nome, cidade, e-mail, telefone, empregos, barras de porcentagem e certificados) não entram. Eles pertenciam a outra pessoa.
- A coluna da esquerda continua com identificação, contato, competências e idiomas. A coluna da direita continua com sobre, situação profissional (no lugar da lista de empregos), formação e projetos.
- A paleta clara com destaque verde-azulado, os cartões e a faixa final seguem a composição do template. O desenho foi refeito em CSS próprio para permitir impressão, contraste e tela estreita sem depender da folha inteira do W3.CSS.
- W3.CSS, Google Fonts e o CSS do Font Awesome saíram. Abrir a página não dispara pedido para esses serviços. A fonte usa a pilha do sistema e, se o computador já tiver Roboto instalada, ela entra sem download. Os ícones são SVG locais.
- Não há barra de porcentagem. O template usava percentuais de exemplo. Aqui não existe nível numérico verificado para Python, SQL, Excel, idiomas ou qualquer outra competência.
- Não há backend, formulário, cookie, armazenamento local nem script de análise de audiência. A página não coleta dados. O único JavaScript liga o botão Imprimir a `window.print`. Sem JavaScript, a impressão do navegador continua valendo.

## Créditos e licença

O repositório de origem não publica arquivo `LICENSE`. Esta adaptação também não cria uma licença nova no lugar da que não existe lá.

Crédito obrigatório:

- Template: [digitalinnovationone/cv](https://github.com/digitalinnovationone/cv), com os avisos originais de `@falvojr` preservados em `index.html`.
- Artigo citado por esse template: [How TO - Create a CV](https://www.w3schools.com/howto/howto_website_create_resume.asp), da W3Schools.
- Font Awesome era a biblioteca de ícones indicada no template ([fontawesome.com/v4/icons](https://fontawesome.com/v4/icons/)). Esta página não embute a fonte nem o CSS dessa biblioteca. Os desenhos são SVG simples feitos para o arquivo.

Quem for reutilizar o layout deve conferir também os termos da W3Schools e do repositório da DIO. O texto biográfico, os projetos e os dados de Diego Nonato Bastos Dias descrevem esta pessoa e este conjunto de repositórios públicos.

## O que a página afirma

Só entra fato conferido. Nada de cargo, empresa, certificado, carga horária, ano de experiência ou nota de proficiência foi completado por estimativa.

| Tema | O que está escrito | De onde veio |
| --- | --- | --- |
| Nome | Diego Nonato Bastos Dias | Dado informado para o currículo |
| Local | Colombo, PR | Dado informado. Não é endereço postal |
| Objetivo | Primeira vaga de engenheiro de dados júnior, sem emprego nessa função | Dado informado |
| Formação | Licenciatura em Física na UEPA, concluída em 2020 | Dado informado. UEPA expandido como Universidade do Estado do Pará |
| Formação | Bacharelado em Administração na UNINTER, em andamento, sem datas | Dado informado. Início e formatura não foram informados |
| Estudos | DIO em andamento, sem certificado nem carga horária | Dado informado: estuda na DIO. Nenhum certificado foi fornecido |
| Competências | Python, SQL, Excel avançado, IA generativa e LLMs, engenharia de prompt | Dado informado, sem percentual |
| Inglês | Leitura avançada de documentação técnica | Dado informado. Não há afirmação de conversação fluente |
| Português | Idioma deste currículo | A página está em pt-BR. Não há nível CEFR |

Projetos, todos públicos:

- [etl-python-santander](https://github.com/diegonbdprof-cloud/etl-python-santander): pipeline CSV com mensagens educativas por modelos de texto fixos, não por inteligência artificial, execução local e sem rede, dados de exemplo fictícios. O arquivo público `tests/test_pipeline.py` tem 20 testes, contados pelos métodos `def test_`. Essa contagem foi feita lendo o fonte. A suíte não foi executada a partir deste repositório, então a página não diz que os testes passaram aqui.
- [agente-trello](https://github.com/diegonbdprof-cloud/agente-trello): agente em Python com Google ADK e Gemini para organizar tarefas em cards no Trello. O README desse projeto descreve testes automáticos que não chamam a API. A integração ao vivo depende de chaves e não foi validada. A quantidade de testes desse repositório não é citada, porque não foi contada para esta página.
- [meus-desafios-criativos](https://github.com/diegonbdprof-cloud/meus-desafios-criativos): desafio de prompt da DIO. O arquivo público `prompt_agente_atendimento.md` é um prompt de agente de atendimento ao cliente. O prompt não foi copiado para o currículo.
- [desafios-python](https://github.com/diegonbdprof-cloud/desafios-python): exercícios de lógica em Python, com enunciados e soluções, no sentido geral do README. Os exercícios não são listados um a um aqui.

## Arquivos

```text
index.html                  página do currículo
css/estilo.css              layout, tela estreita e impressão
js/curriculo.js             botão Imprimir
tests/verificar_curriculo.py
.github/workflows/verificar.yml
README.md
```

Não há `package.json`, banco, servidor de aplicação nem segredo. O workflow só roda a conferência local e tem permissão de leitura. Ele não publica o site.

## Como abrir no computador

Na pasta do repositório:

```bash
python3 -m http.server 8000
```

Abra `http://127.0.0.1:8000/`.

O `index.html` também abre direto no navegador, por `file://`, porque não há módulo JavaScript nem `fetch`. O servidor local só facilita a navegação e o teste de links internos.

Para encerrar o servidor, use Ctrl+C no terminal em que ele está rodando.

## Como personalizar

Os fatos visíveis estão em `index.html`. Os ids marcam cada bloco: `competencias`, `idiomas`, `sobre`, `situacao`, `formacao`, `projetos`.

Ao editar:

- Mantenha `lang="pt-BR"` e um único `h1` com o nome.
- Não recoloque telefone, e-mail, endereço, foto ou data de nascimento se a decisão for continuar sem esses dados. Se um contato for acrescentado de propósito, que seja um dado real e público por escolha de quem edita.
- Não invente emprego, certificado, data ou percentual para preencher um espaço. O bloco de situação profissional existe justamente porque a lista de empregos do template não tinha fato correspondente.
- Links que abrem outra aba precisam de `rel="noopener noreferrer"` e do texto oculto `(abre em nova aba)`.
- Não adicione script de audiência, iframe ou imagem remota. O verificador recusa CDN, `mailto:`, `http://` e barra de porcentagem no texto visível.
- CSS fica em `css/estilo.css`. Impressão é o bloco `@media print` no fim do arquivo. A coluna única na impressão cabe melhor em A4 do que as duas colunas da tela.
- O botão Imprimir está em `js/curriculo.js`. Ele só chama `window.print()`.

Depois da edição:

```bash
python3 tests/verificar_curriculo.py
```

Se a frase obrigatória mudar, atualize a lista correspondente no verificador. O teste existe para segurar fato e estrutura, não para impedir uma revisão honesta.

## Impressão e celular

Na tela larga, o perfil fica à esquerda e o conteúdo à direita, como no template. Abaixo de 800 pixels de largura, as duas áreas ficam uma sob a outra, com o nome primeiro. Os alvos de toque do menu, dos links de contato e do botão têm altura mínima de 44 pixels. O menu quebra a linha em vez de abrir um painel extra.

O botão Imprimir e o atalho de impressão do navegador usam a mesma folha. Em `@media print`:

- somem a barra de navegação, o atalho “Ir para o conteúdo” e o botão;
- o fundo colorido sai, o texto fica preto e os cartões ganham borda;
- cada link `https` mostra o endereço depois do texto, para a folha impressa continuar utilizável;
- artigos evitam quebra no meio.

## Acessibilidade

A página usa HTML semântico: `header`, `nav`, `main`, `section`, `article`, `footer` e cabeçalhos em ordem, do `h1` ao `h3`, sem pular nível. Há um link “Ir para o conteúdo”. O `main` recebe foco quando esse link é usado (`tabindex="-1"`).

Ícones são decorativos (`aria-hidden` e `focusable="false"`). O nome do link está no texto. Links externos avisam a abertura em nova aba para leitor de tela. A sigla PR tem `abbr` com o título Paraná. O nome do artigo da W3Schools está marcado com `lang="en"`.

O contraste do texto usa tinta escura sobre branco e branco sobre verde-azulado escuro (`#084842`). A informação não depende só de cor: datas e “Em andamento” estão escritos. Há estilo de `:focus-visible`, suporte a `prefers-reduced-motion` e borda em `forced-colors`.

Isto não é um laudo formal de WCAG. O que dá para repetir está no verificador e na inspeção descrita abaixo.

## Testes

Conferência automática, sem rede e sem dependência externa:

```bash
python3 tests/verificar_curriculo.py
```

O script confere, entre outros pontos:

- arquivos presentes e HTML com tags balanceadas;
- `lang="pt-BR"`, um `h1` e a sequência de títulos;
- frases dos fatos verificados e ausência, no texto visível, de e-mail, telefone, porcentagem, nome do exemplo e termos que indicariam fluência oral, emprego ou ferramenta não informados;
- preservação literal dos dois avisos `@falvojr`;
- nenhum `img`, iframe, CDN, `http://`, atributo `style` ou evento inline;
- uma folha e um script, ambos locais;
- cada link externo dentro da lista prevista, e cada item dessa lista presente na página;
- âncoras do menu apontando para ids existentes;
- dez links com `target="_blank"`, todos com `noopener`, `noreferrer` e o aviso de nova aba;
- CSS com `@media (max-width: 800px)`, `@media print` e `@page`, sem `url(`;
- JavaScript limitado ao `window.print`, sem `fetch`, armazenamento ou cookie;
- README com crédito, modo de abrir, personalização e a frase “GitHub Pages não foi habilitado”.

A saída termina com a contagem de falhas. Código de saída `0` significa nenhuma falha estrutural. Código `1` significa falha.

Consulta opcional de links, separada porque depende da rede e de bloqueio a robôs:

```bash
python3 tests/verificar_curriculo.py --links
```

Status 200 a 399 conta como acesso. 404 e 410 contam como falha. 401, 403, 429, 503 e 999 são aviso: vários sites recusam cliente automático e isso, sozinho, não prova link quebrado. O workflow do GitHub roda só o modo sem rede.

O que esta suíte não faz: não mede contraste com analisador visual, não executa os testes dos outros repositórios e não substitui a leitura da página impressa.

GitHub Pages não foi habilitado. Não há workflow de publicação.

## O que ficou de fora

- Telefone, e-mail, endereço, foto e aniversário.
- Empregos, estágios, certificados, cargas horárias e anos de experiência não fornecidos.
- Percentuais de competência e nível falado de inglês.
- Backend, formulário, banco, analytics, cookies e pixels.
- Publicação em GitHub Pages ou outro hospedeiro. A página pode ser publicada depois, se isso for decidido à parte. Este repositório não liga esse serviço.
