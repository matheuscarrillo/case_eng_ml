# Case Seleção

## Software Engineer Python - AWS

### Tarefas

1. Criar um repositório no Github que deve conter todos com os códigos do case;
2. Criar o código que sobe uma API usando IaC (com Terraform, por exemplo), preferencialmente usando o serviço API Gateway da Cloud AWS:
   - O contrato deve ser especificado usando o OpenAPI 3.0 (Swagger)
   - Deve expor um endpoint com um recurso */sobreviventes* que recebe um JSON com um array de características necessárias para escorar o modelo de Machine Learning treinado em cima do Dataset do Titanic. O modelo é disponibilizado neste repositório na seguinte *path*: */modelo/model.pkl*;
   - O método POST deve receber um JSON no body com um array de características e retornar um JSON com a probabilidade de sobrevivência do passageiro, junto com o ID do passageiro;
     - O processamento - escoragem - deve ser feita numa função Lambda **com código escrito em Python**, e caso seja escolhido outro serviço AWS, justificar a escolha;
     - Além disso, a probabilidade de sobrevivência pode ser armazenada em um banco de dados de baixa latência e serverless - DynamoDB;
     - O Banco de Dados e a função Lambda devem ser criados usando IaC com Terraform, por exemplo;
     - **Não provisionar o banco DynamoDB, dado o baixo volume de requisições que serão feitas;**
   - O método GET /sobreviventes deve retornar um JSON com a lista de passageiros que já foram avaliados (fica a critério do candidato implementar paginação ou não);
   - O método GET /sobreviventes/{id} deve retornar um JSON com a probabilidade de sobrevivência do passageiro com o ID informado;
   - O método DELETE deve deletar o passageiro com o ID informado;
3. Disponibilizar os arquivos de IaC (Terraform) no repositório, assim como o contrato OpenAPI e o código da função Lambda;
4. Você possui o prazo de 7 dias corridos para entrega do case, uma vez recebido o link para este repositório;


1. Configuração do ambiente usando o .toml
2. Construção do pipeline do modelo
3. Construção do código python para execução em lambda 
4. Criação de imagem docker
  - docker buildx build --platform linux/amd64 -t ml-lambda --load .
5. Teste da imagem:
  ```bash
    docker run -p 9000:8080 ml-lambda
    
    # Teste da imagem em outro terminal.
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations/sobreviventes" -d @event.json
  ```
7. OpenAPI 3.0 (Swagger)
  - OpenAPI = “documento que explica exatamente como sua API funciona”
  - Construção do yaml da API
8. Construção dos métodos de chamada das API.
9. Construção do Terraform de subida de lambda no ECR
6. Subida de imagem no ECR.
  - atualizar o aws configure
  - aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 123687089814.dkr.ecr.sa-east-1.amazonaws.com
  - cria o repositório via terraform:
    - terraform init
    - terraform apply -target=aws_ecr_repository.repo
  - docker tag ml-lambda:latest 123687089814.dkr.ecr.sa-east-1.amazonaws.com/ml-lambda:latest
  - docker push 123687089814.dkr.ecr.sa-east-1.amazonaws.com/ml-lambda:latest
X. Subida do lambda via terraform
  - terraform apply -target=aws_lambda_function.lambda

  
X. Criar ajuste do do código para escrever no dynamo cada chamada.
11. Construção do Terraform de subida de Dynamo.
10. Construção do Terraform de subida de API GetWay
