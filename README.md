# JuntosSomosMaisApi

Aplicação desenvolvida em [Python 3.12.3](https://python.org), focada na disponibilização dos dados de usuários previamente integrados e inseridos em memória durante a inicialização do sistema.

# Armazenamento de Dados

Esta aplicação possui armazenamento em memória, sendo assim, não há uso de bancos de dados ou qualquer outro tipo de persistência a longo prazo, ou seja, após a interrupção da aplicação todos os dados são perdidos.

# Instalação

Esta aplicação foi desenvolvida sob linux utilizando algumas ferramentas excenciais, sendo assim, é necessário instalar as dependências do projeto listadas abaixo para que seja possível subir todos os serviços para sua execução.

Dependências para execução dockerizada:

```
Make
Docker
```

Dependências para execução diretamente em máquina local (opcional):

```
Pip v24.0
Python v3.12.3
```

Após certificar-se de que as dependências estejam instaladas na máquina que irá executar esta aplicação, pode-se facilmente subir os serviços utilizando os comandos listados no arquivo `Makefile`.

Para aqueles que desejarem rodar a aplicão completamente dockerizada, não se faz necessária a instalação das dependências para exeução em máquina local.

# Makefile

O arquivo `Makefile` possui comandos pré-configurados que auxiliam algumas rotinas em ambiente dockerizado, tais como: Inicializar a aplicação, rodar os testes, convenção de código e etc, assim como também manipular arquivos contendo variáveis de ambiente encriptadas e tags no github.

Para exibir a relação de comandos disponíveis e seus respectivos modos de uso, basta aplicar um dos dois comandos abaixo:

```
$ make
$ make help
```

* Caso ocorra algum problema durante a execução dos comandos, talvez seja necessária a deleção do diretório `.venv` e a re-aplicação do comando desejado.

# Inicialização da Aplicação

A abordagem a partir deste ponto será voltada à disponibilização dos serviços e a iniciaização da aplicação de forma dockerizada. Para isso, é necessário que inicialmente as imagens a serem utilizadas no Docker sejam construídas.

Para a construção das imagens, aplique o comando abaixo:

```
$ make build
```

A partir deste ponto tudo o que é necessário encontra-se devidamente instalado e disponível. Caso seja necessário executar testes e análise de código, utilize os comandos abaixo:

```
$ make tests verbose=true|false
$ make code-convention fix-imports=true|false
```

Por fim, para inicializar a aplicação basta aplicar um dos seguintes comandos:

```
$ make run target=api
$ make run-debug target=api
```

Também é possível ter acesso ao terminal da aplicação de acordo com o ambiente desejado, basta aplicar um dos comandos abaixo:

```
$ make run target=terminal
$ make run-debug target=terminal
```

Caso corra tudo conforme o esperado a aplicação estará disponível na seguinte url http://localhost:8000.

# Variáveis de Ambiente

As variáveis de ambiente são configuradas no arquivo `.env` e estão organizadas por tipo de uso e setadas para desenvolvimento local. Toda configuração é aplicada automaticamente tanto para inicialização em ambiente Docker quanto em máquina local.

Caso seja necessário alterar alguma variável, basta editá-las. As alterações serão aplicadas em todos os modos de inicialização, desde que, reinicializados ou reconstruídos.

Em ambientes externos voltados a staging e production, as variáveis de ambiente são encriptadas e estão localizadas no diretório `.k8s`, que também possui outras configurações para deploy utilizando o [kubernetes](https://kubernetes.io/pt-br).

Para encriptar e/ou desencripar as variáveis de ambiente de staging e production é necessario que o ambiente de infra esteja devidadamente alinhado com esta aplicação, porém, de acordo com o objetivo desta aplicação, este recurso não se faz necessário e não será devidamente documentado neste repositório, ainda assim, caso seja de interesse das partes, notifique-me para a demonstração de uso.

# Autorização

A aplicação está configurada para ser acessível apenas por `clientes` (interfaces, aplicações integradas e afins) que possuam chave de api válida.

Certifique-se de atribuir valor à variável de ambiente `JWT_SECRET` para que a aplicação possa validar a assinatura do token de acesso durante o uso da aplicação. Não há formato definido relacionado ao formato da secret, porém, recomenda-se a utilização de hashes de 32 bits ou semelhantes.

Com exceção das requests feitas para as urls de documentação e monitoramento, todas as demais requests feitas para esta aplicação necessitam do header `Authorization`.

# Workflows

Foram implementadas actions que são executadas em diferentes cenários com o objetivo de aplicar testes e análise de código, assim como também o deploy da aplicação.

Para que as actions relacionadas aos testes e análise de código sejam executadas, basta a realização do push para a branch na qual está recebendo modificações, caso as actions identifiquem problemas, o merge da branch não será permitido.

Quanto ao deploy, esta action utiliza workflows compartihados e assim como as variáveis de ambiente encriptadas e demais recursos de deploy, é necessário estar alinhado com o ambiente de infra, porém, a nível de explicação, para execução da action basta criar tags em formato preestabelecido e o processo inicializará automaticamente.

# Documentação

Esta aplicação possui todas as rotas e os detalhes mais importantes exemplificados em documentação gerada pelo postman. Os arquivos da documentação estão no diretório `.docs`, assim como também, é navegável acessando a url abaixo:

```
https://documenter.getpostman.com/view/4274276/2s93sc6DX5#intro
```

Há também a documentação  gerada pelo swagger que está acessível em ambiente de desenvolvimento através da url abaixo:

```
http://localhost:8000/docs
```

# Melhorias Necessárias

* Integrar aplicação com ferramentas de log, tais como: Sentry ou Datadog
* Migrar armazenamento em memória para banco de dados
* Implementar testes e documentação de forma mais elaborada levando em consideração outros cenários
* Implementar o versionamento de rotas a partir de headers

# Pricipais Tecnologias Utilizadas

* [FastAPI](https://fastapi.tiangolo.com)
* [Pydantic](https://docs.pydantic.dev/latest)
* [Swagger](https://swagger.io)
* [Postman](https://www.postman.com)
* [Faker](https://faker.readthedocs.io/en/master)
* [Docker](https://docs.docker.com)
* [Kubernetes](https://kubernetes.io/pt-br)
