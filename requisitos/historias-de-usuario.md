# Histórias de Usuário e Critérios de Aceitação

**Produto:** Gerador de Senhas Seguras
**Baseline:** 1.0.0

Cada história segue o formato *Como … quero … para que …*, com critérios de aceitação escritos em Gherkin (Dado / Quando / Então). Os critérios foram redigidos para serem executáveis: cada um corresponde a uma verificação possível, seja por teste automatizado existente, seja por roteiro manual.

Priorização por **MoSCoW**. Rastreabilidade completa em [matriz-rastreabilidade.md](matriz-rastreabilidade.md).

---

## Épicos

| ID | Épico | Histórias | Objetivo |
|----|-------|-----------|----------|
| **EP01** | Configuração dos critérios | HU01, HU02, HU03 | Permitir que o usuário descreva a senha que precisa |
| **EP02** | Geração e apresentação | HU04, HU05, HU06 | Produzir a senha e comunicar sua qualidade |
| **EP03** | Aproveitamento da senha | HU07 | Levar a senha até o destino de uso |
| **EP04** | Operação e confiabilidade | HU08, HU09 | Sustentar o serviço em execução |
| **EP05** | Evolução (backlog) | HU10 – HU13 | Incremento candidato para a versão 1.1 |

---

## EP01 — Configuração dos critérios

### HU01 — Definir o tamanho da senha

> **Como** usuário que precisa atender à política de senha de um sistema específico,
> **quero** escolher quantos caracteres a senha terá,
> **para que** ela seja aceita por esse sistema sem tentativa e erro.

**Prioridade:** Must · **Requisitos:** RF01, RN02 · **Status:** ✅ implementado

```gherkin
Cenário: Ajustar o tamanho pelo controle deslizante
  Dado que a aplicação foi aberta
  Então o tamanho exibido é 16
  Quando eu arrasto o controle para 24
  Então o rótulo passa a exibir "24 caracteres"
  E nenhuma requisição é enviada ao servidor até que eu peça a geração

Cenário: Limites do intervalo permitido
  Dado que a aplicação foi aberta
  Então o controle não permite valor menor que 8 nem maior que 128

Esquema do Cenário: Servidor rejeita tamanho fora do intervalo
  Dado um cliente que envia "<tamanho>" diretamente à API
  Quando a requisição POST /api/gerar-senha é processada
  Então a resposta tem status 422
  E nenhuma senha é retornada

  Exemplos:
    | tamanho |
    | 4       |
    | 7       |
    | 129     |
    | 200     |
```

---

### HU02 — Escolher a composição de caracteres

> **Como** usuário,
> **quero** ligar e desligar maiúsculas, minúsculas, números e caracteres especiais,
> **para que** a senha respeite o que o sistema de destino aceita — alguns rejeitam símbolos.

**Prioridade:** Must · **Requisitos:** RF02–RF05, RN05 · **Status:** ✅ implementado

```gherkin
Cenário: Composição padrão ao abrir a aplicação
  Dado que a aplicação foi aberta
  Então "Letras maiúsculas" e "Letras minúsculas" estão marcados
  E "Números" e "Caracteres especiais" estão desmarcados

Cenário: Senha contém apenas os tipos escolhidos
  Dado que apenas "Números" está marcado
  E que o tamanho é 12
  Quando eu solicito a geração
  Então a senha retornada contém somente dígitos de 0 a 9
  E tem exatamente 12 caracteres

Cenário: Caracteres especiais respeitam o conjunto definido
  Dado que apenas "Caracteres especiais" está marcado
  Quando eu solicito a geração
  Então todo caractere da senha pertence ao conjunto !@#$%^&*()_+-=[]{}|;':",.<>?/
  E a senha não contém barra invertida nem espaço
```

---

### HU03 — Ser impedido de pedir uma senha impossível

> **Como** usuário,
> **quero** ser avisado quando desmarco todos os tipos de caractere,
> **para que** eu entenda o problema antes de acionar o botão e não receba um erro sem explicação.

**Prioridade:** Must · **Requisitos:** RF09, RN01 · **Status:** ✅ implementado

```gherkin
Cenário: Bloqueio preventivo no cliente
  Dado que a aplicação foi aberta
  Quando eu desmarco todos os quatro tipos de caractere
  Então o botão "Gerar Senha" fica desabilitado
  E a mensagem "Selecione pelo menos um tipo de caractere." é exibida
  Quando eu marco novamente qualquer um dos tipos
  Então o botão volta a ficar habilitado
  E a mensagem desaparece

Cenário: Servidor também rejeita, independentemente do cliente
  Dado um cliente que envia todos os tipos como false
  Quando a requisição POST /api/gerar-senha é processada
  Então a resposta tem status 422
```

> **Nota de elicitação:** a validação é duplicada de propósito — no cliente por usabilidade, no servidor por segurança. A API é pública e não pode confiar no cliente.

---

## EP02 — Geração e apresentação

### HU04 — Gerar a senha

> **Como** usuário,
> **quero** obter uma senha aleatória a partir dos critérios que configurei,
> **para que** eu não precise inventar uma senha por conta própria.

**Prioridade:** Must · **Requisitos:** RF06, RN03, RN07, RN08, RNF01 · **Status:** ✅ implementado

```gherkin
Cenário: Geração bem-sucedida
  Dado que ao menos um tipo de caractere está selecionado
  Quando eu aciono "Gerar Senha"
  Então uma senha do tamanho configurado é exibida na tela
  E o botão "Copiar" fica habilitado

Cenário: Cada tipo selecionado aparece ao menos uma vez
  Dado que os quatro tipos estão selecionados
  E que o tamanho é 8
  Quando eu solicito a geração
  Então a senha contém ao menos uma maiúscula, uma minúscula, um dígito e um caractere especial

Cenário: Duas gerações consecutivas não se repetem
  Dado que os critérios permanecem inalterados
  Quando eu aciono a geração duas vezes
  Então as duas senhas são diferentes entre si

Cenário: A senha é produzida no servidor
  Dado que o backend está indisponível
  Quando eu aciono "Gerar Senha"
  Então nenhuma senha é exibida
  E o cliente não produz senha alguma por conta própria
```

---

### HU05 — Entender a força da senha gerada

> **Como** usuário sem conhecimento técnico de criptografia,
> **quero** ver uma indicação visual da qualidade da senha,
> **para que** eu decida se aumento o tamanho ou incluo mais tipos antes de usá-la.

**Prioridade:** Should · **Requisitos:** RF08, RN06 · **Status:** ✅ implementado, com ressalva

```gherkin
Esquema do Cenário: Classificação por tamanho e quantidade de tipos
  Dado que "<tipos>" tipos de caractere estão selecionados
  E que o tamanho é "<tamanho>"
  Quando eu solicito a geração
  Então o indicador exibe "<forca>"
  E a barra de força é preenchida na proporção correspondente

  Exemplos:
    | tipos | tamanho | forca       |
    | 1     | 8       | Fraca       |
    | 1     | 128     | Fraca       |
    | 2     | 10      | Média       |
    | 3     | 12      | Forte       |
    | 4     | 16      | Muito Forte |
    | 4     | 12      | Forte       |

Cenário: O indicador é limpo quando a geração falha
  Dado que uma senha já foi gerada e o indicador exibe "Forte"
  Quando uma nova tentativa de geração falha
  Então a barra de força é zerada
```

> **Ressalva registrada:** a linha `| 1 | 128 | Fraca |` está correta conforme RN06, mas é contraintuitiva — 128 caracteres minúsculos têm entropia altíssima. A limitação é conhecida e aceita para a 1.0.0; ver [LA01](lacunas-ambiguidades.md#la01--força-não-mede-entropia) e HU12.

---

### HU06 — Saber o que aconteceu quando a geração falha

> **Como** usuário,
> **quero** uma mensagem clara quando a senha não puder ser gerada,
> **para que** eu saiba se o problema é meu, do servidor, ou se devo apenas tentar de novo.

**Prioridade:** Must · **Requisitos:** RF10 · **Status:** ⚠️ parcial

```gherkin
Cenário: Backend fora do ar
  Dado que o servidor backend não está em execução
  Quando eu aciono "Gerar Senha"
  Então é exibida a mensagem "Não foi possível conectar ao servidor. Verifique se o backend está em execução."
  E o indicador de força é limpo
  E o botão volta ao estado "Gerar Senha", permitindo nova tentativa

Cenário: Requisição rejeitada pelo servidor
  Dado que o servidor responde 422
  Quando eu aciono "Gerar Senha"
  Então é exibida uma mensagem de erro
  E a aplicação permanece utilizável

Cenário (não atendido na 1.0.0): Motivo específico da rejeição
  Dado que o servidor rejeitou a requisição por tamanho fora do intervalo
  Quando a mensagem é exibida ao usuário
  Então ela deveria indicar o campo e o motivo da rejeição
  Mas a 1.0.0 exibe apenas um texto genérico  # ver LA03
```

---

## EP03 — Aproveitamento da senha

### HU07 — Copiar a senha

> **Como** usuário,
> **quero** copiar a senha com um clique,
> **para que** eu não precise transcrevê-la manualmente e cometa erro de digitação.

**Prioridade:** Should · **Requisitos:** RF07 · **Status:** ✅ implementado

```gherkin
Cenário: Cópia com confirmação visual
  Dado que uma senha foi gerada
  Quando eu aciono "Copiar"
  Então o conteúdo da área de transferência é exatamente a senha exibida
  E o botão exibe "Copiado!" por 2 segundos
  E depois volta a exibir "Copiar"

Cenário: Botão indisponível antes da primeira geração
  Dado que a aplicação acabou de ser aberta
  Então o botão "Copiar" está desabilitado

Cenário: Contexto sem API de área de transferência
  Dado que a página foi aberta em contexto não seguro (file://)
  Quando eu aciono "Copiar"
  Então a cópia ocorre pelo mecanismo alternativo
  E a confirmação visual é exibida da mesma forma
```

---

## EP04 — Operação e confiabilidade

### HU08 — Monitorar a disponibilidade do serviço

> **Como** operador de infraestrutura,
> **quero** um endpoint que confirme que a API está respondendo,
> **para que** eu detecte uma queda antes que um usuário a reporte.

**Prioridade:** Could · **Requisitos:** RF11 · **Status:** ✅ implementado (endpoint) / 📋 monitoramento externo — risco [R15](../riscos/identificacao.md)

```gherkin
Cenário: Verificação de saúde
  Dado que o backend está em execução
  Quando eu consulto GET /health
  Então a resposta tem status 200
  E contém "status" igual a "ok", a versão da aplicação e um timestamp em UTC
```

---

### HU09 — Publicar a aplicação sem expor os usuários

> **Como** operador de infraestrutura,
> **quero** restringir as origens aceitas e o endereço do backend por configuração,
> **para que** eu publique a aplicação sem editar código-fonte.

**Prioridade:** Must · **Requisitos:** RNF04, RNF16 · **Status:** ✅ implementado

```gherkin
Cenário: Restrição de origem por variável de ambiente
  Dado que ALLOWED_ORIGINS está definida como "https://exemplo.com"
  Quando uma página de outra origem tenta chamar a API pelo navegador
  Então a requisição é bloqueada pela política de CORS

Cenário: Endereço do backend configurável
  Dado que o backend foi publicado em outro endereço
  Quando eu altero API_URL em frontend/config.js
  Então o frontend passa a chamar o novo endereço sem qualquer alteração em script.js
```

---

## EP05 — Backlog (incremento candidato 1.1)

Histórias elicitadas mas deliberadamente fora da baseline. Mantidas aqui para que a priorização futura parta de itens já formulados — mitigação direta do risco [R10 — escopo crescente não gerenciado](../riscos/identificacao.md).

### HU10 — Gerar várias senhas de uma vez

> **Como** usuário que precisa cadastrar credenciais para uma equipe,
> **quero** gerar de 2 a 10 senhas em uma única ação,
> **para que** eu não repita o mesmo clique dezenas de vezes.

**Prioridade:** Should (1.1) · **Requisitos:** RF12 · **Status:** 📋

```gherkin
Cenário: Lote de senhas
  Dado que a quantidade solicitada é 5
  Quando eu solicito a geração
  Então 5 senhas distintas são exibidas
  E cada uma respeita todos os critérios configurados
  E cada uma pode ser copiada individualmente
```

**Questão em aberto:** o limite máximo do lote precisa ser definido junto com o rate limiting (RNF07) — sem isso, o lote vira vetor de abuso.

---

### HU11 — Avaliar uma senha que já possuo

> **Como** usuário,
> **quero** colar uma senha existente e ver sua força,
> **para que** eu decida se preciso trocá-la.

**Prioridade:** Could (1.1) · **Requisitos:** RF13 · **Status:** 📋

**Impedimento identificado na elicitação:** esta história **conflita com RNF02**. Avaliar uma senha existente significa enviar ao servidor uma senha *em uso* — o oposto de gerar uma nova e descartável. Ver [LA06](lacunas-ambiguidades.md#la06--hu11-conflita-com-a-regra-de-não-trafegar-senha-em-uso).

---

### HU12 — Ver a força como entropia real

> **Como** usuário com alguma familiaridade técnica,
> **quero** que o indicador considere o tamanho do alfabeto e não apenas a contagem de tipos,
> **para que** a classificação não subestime senhas longas de um único tipo.

**Prioridade:** Should (1.1) · **Requisitos:** revisão de RN06 · **Status:** 📋

```gherkin
Cenário: Senha longa de tipo único deixa de ser "fraca"
  Dado que apenas "Letras minúsculas" está selecionado
  E que o tamanho é 40
  Quando eu solicito a geração
  Então a força apresentada corresponde à entropia calculada
  E não é classificada como "Fraca"
```

---

### HU13 — Excluir caracteres ambíguos

> **Como** usuário que precisa ditar ou digitar a senha manualmente,
> **quero** excluir caracteres visualmente parecidos (`0`/`O`, `1`/`l`/`I`),
> **para que** eu não erre a transcrição.

**Prioridade:** Could (1.1) · **Requisitos:** RF14 · **Status:** 📋

**Questão em aberto:** a exclusão interage com RN03 — se o usuário selecionar apenas números e excluir ambíguos, o alfabeto cai de 10 para 8 símbolos, reduzindo a entropia. É preciso decidir se a interface alerta sobre isso.

---

## Resumo da priorização

| Prioridade | Histórias | Situação |
|-----------|-----------|----------|
| **Must** | HU01, HU02, HU03, HU04, HU06, HU09 | Entregues (HU06 parcial) |
| **Should** | HU05, HU07 · HU10, HU12 (1.1) | Entregues / backlog |
| **Could** | HU08 · HU11, HU13 (1.1) | Entregue / backlog |
| **Won't (1.0)** | HU10 – HU13 | Deferidas por decisão de escopo |
