# JuntosSomosMaisApi

Aplicação desenvolvida em [Python 3.12.3](https://python.org), focada em disponibilizar dados de usuários previamente integrados durante a inicialização do sistema.

# Armazenamento de Dados

Esta aplicação possui armazenamento em memória, sendo assim, não há uso de bancos de dados ou qualquer outro tipo de persistência a longo prazo, ou seja, aoapós a interrupção da aplicação, todos os dados são perdidos.

# Instalação

É necessário que o ambiente escolhido possua os recursos listados abaixo previamente instalados e configurados:

```
Make
Docker
```

Agora, basta rodar o seguinte comando para instalar a aplicação:

```
$ make install
```

O comando acima é responsável pela execução de todas as pendências da aplicação, ao final, testes automatizados serão executados.

Caso seja necessário executar rotinas individualmente, basta utilizar o comando `make <option>`.

Para exibir a lista de todas as rotinas disponníveis, basta executar o comando `make` ou `make help`.

# Variáveis de Ambiente

Caso seja necessário alterar alguma variável de ambiente, basta editar o arquivo `.env`, porém, é necessário reinicializar a aplicação para aplicação dos novos valores.

Em ambientes externos voltados a staging e production, as variáveis de ambiente são encriptadas e estão localizadas no diretório `.k8s`, que também possui outras configurações para deploy utilizando o `kubernetes`.

Para encriptar ou desencripar as variáveis de ambiente de staging e production, é necessario que a infra esteja devidadamente alinhada com esta aplicação, porém, este recurso não se faz necessário e não será devidamente documentado neste repositório, ainda assim, é funcional e está devidamente implementado.

# Recursos Disponíveis

Todas os detalhes de utilização estão disponibilizados na documentação da aplicação, ainda assim, é válido lembrar que, para todas as rotas com exceção das de documentação e monitoramento, é necessário o envio do header `Authorization`, preenchido com um Bearer token, desta forma, a aplicação validará o acesso aos recursos disponíveis.

* Para gerar um token válido, acesse o site do [JWT](https://jwt.io), altere a data de expiração utilizando a mesma chave de segurança configurada nas variáveis de ambiente sem encodar em Base64.

```
| ----------------------------------- |
| Header                              |
| ----------------------------------- |
| {                                   |
|     "alg": "HS256",                 |
|     "typ": "JWT"                    |
| }                                   |
| ----------------------------------- |
| Payload                             |
| ----------------------------------- |
| {                                   |
|     "exp": 1916239022               |
| }                                   |
| ----------------------------------- |
| Verify Signature                    |
| ----------------------------------- |
| HMACSHA256(                         |
|     base64UrlEncode(header) + "." + |
|     base64UrlEncode(payload),       |
|     [ "secret" ]                    |
| ) [ ] secret base64 encoded         |
| ----------------------------------- |
```

# Inicialização

Para inicializar o serviço, basta executar o comando abaixo.

```
$ make run
$ make run-debug
```

Ao final da inicialização, o serviço estará disponível na seguinte url `http://localhost:8000`.

* Certifique-se de atribuir valor à variável de ambiente `JWT_SECRET` para que a aplicação possa validar a assinatura do token de acesso durante o uso da aplicação. Não há formato definido para a secret, porém, recomenda-se a utilização de um hash de 32 bits ou semelhante.

* O modo debug é indicado para fase de desenvolvimento da aplicação, permitindo o uso de breakpoints a partir do uso da configuração `Api: Launch` no `VSCode`.

# Documentação

Os arquivos de documentação dsponibilizados no diretório `.docs` podem ser importados no `Postman` para uso da aplicação em ambiente local. Caso prefira, a documentação pode ser acessada também através da url abaixo:

```
https://documenter.getpostman.com/view/4274276/2sA3QtfX7a
```

Há também a documentação do swagger, que é gerada a partir do código da aplicação e pode ser acessada ao inicializá-la em modo debug (ambiente de desenvolvimento) através da seguinte url:

```
http://localhost:8000/docs
```

# Melhorias Necessárias

* Implementar o versionamento de rotas a partir de headers
* Integrar ferramentas para registro de eventos, erros e afins
* Incrementar testes e documentação levando em consideração outros cenários de uso
* Migrar armazenamento em memória para banco de dados
* Melhorar recursos do exception handler

# Pricipais Tecnologias Utilizadas

* [Poetry](https://python-poetry.org)
* [FastAPI](https://fastapi.tiangolo.com)
* [Pydantic](https://docs.pydantic.dev/latest)
* [Faker](https://faker.readthedocs.io/en/master)
* [Swagger](https://swagger.io)
* [Docker](https://docs.docker.com)
* [Kubernetes](https://kubernetes.io/pt-br)
* [Postman](https://www.postman.com)
* [VSCode](https://code.visualstudio.com)
