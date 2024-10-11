## Objetivo
  O objetivo deste projeto é fornecer um serviço onde o usuário tem autonomia para enviar informações sobre pedidos, clientes, limites de crédito e históricos de consultas ao Serasa.
  Esses dados são utilizados para criar modelos de inteligência artificial capazes de prever se um pedido deve ou não ser faturado, com base nas informações fornecidas.

## Contexto
  Este projeto é aplicável a qualquer negócio que envolva a emissão de pedidos por clientes e que exija uma análise de crédito robusta. O nível de assertividade da IA dependerá diretamente 
  da qualidade e da origem dos dados fornecidos pela empresa solicitante. Para avaliar a eficiência do projeto, utilizamos uma base de dados real e aplicamos o modelo dentro de uma empresa.
  
## Escopo
#### **1. Cadastro Usuario**  
Um endpoint é disponibilizado para realizar o cadastro do usuário no serviço. No momento do cadastro, é gerado um token de acesso JWT, que será utilizado para controlar o acesso aos demais endpoints.

#### **2. Envio de informações**  
Este endpoint é responsável por receber informações de pedidos, clientes, limites de crédito e históricos de consultas ao Serasa, em lotes de 500 itens, e gravá-las no banco de dados. 
O endpoint possui uma camada de segurança que valida o JWT Bearer Token e verifica se o usuário associado ao token é válido.

#### **3. Treinamento do Modelo**  
Não é um endpoint, é um processo disparado quando o envio de todas as informações são concluidas (os tratamentos normalização dos dados, redução de dimensionalidade) devem ser feitos pelo usuario pois 
o serviço so é responsavel por obter as informações validar e gerar um modelo treinado.

#### **4. Teste com o Modelo**  


#### **5. Utilização do modelo para predição de pedidos**  

## **Tecnologias**  
Para o desenvolvimento do projeto, foram utilizadas as seguintes tecnologias:
  * **Linguagem:** Python 3.11+
  * **Banco de Dados:** SqlServer
  * **Mensageria:** Kafka
  * **Containerização:** Docker
    
Bibliotecas e FrameWorks
  * Flask
  * JWT
  * SqlAlchemy
  * Json
  * ConfigParser
  * Kafka

# Requisitos Funcionais
  **Rf1: Gerenciamento de pré-cadastro**
    a) O sistema deve permitir que uma empresa crie um pré-cadastro, fornecendo informações básicas como nome, email;
    b) Após o pré-cadastro, o sistema deve gerar um token JWT único para a empresa;
    c) O token JWT deve ser utilizado para autenticar todas as requisições feitas pela empresa;
  **Rf2: Envio de Dataset para Treinamento**
    a) O sistema deve permitir que a empresa envie um dataset com as informações de análise de crédito/cliente via end-point;
    b) O dataset deve conter informações necessários para treinar um modelo de IA que avalie as condições de crédito do cliente;
    c) O sistema deve validar a estrutura e a integridade dos dados enviados antes de iniciar o treinamento do modelo;
  **Rf3: Treinamento do Modelo de IA**
    a) O sistema deve usar o dataset fornecido para treinar um modelo de IA para a empresa solicitante;
    b) O sistema deve armazenar o modelo treinado associado a empresa que o solicitou;
  **Rf4: Processamento de Pedidos Novos**
    a) O sistema deve permitir que a empresa envie pedidos novos via um end-point, utilizando o token JWT para autenticação;
    b) O modelo de IA deve processar o pedido e retornar uma decisão sobre a liberação ou não do pedido para o faturamento;
    c) A decisão deve ser acompanhada por uma explicação do motivo, com base nas condições analisadas pelo modelo;
  **Rf5: Retreinamento do Modelo**
    a) O sistema deve permitir que a empresa solicite o retreinamento do modelo de IA a qualquer momento, enviando um novo dataset;
    b) O retreinamento gera um novo registro assim mantendo mais de um modelo disponivel pela empresa, caso ela queira realizar novos testes;
  **Rf6: Auditoria e Log de Atividades**
    a) O sistema deve registrar todas as atividades relacionadas a envios de datasets, treinamentos de modelo e processamento de pedidos.
    b) O log deve ser acessivel para a empresa consultar as atividades realizadas;
# Requisitos não Funcionais

# Arquitetura

```mermaid
flowchart TD
    Start --> Producer
    Producer --> Camada_Seguranca
    Camada_Seguranca --> Send_Messages
    
    Send_Messages --> Topic_Processamento
    Send_Messages --> Topic_Cadastros
    
    Topic_Processamento --> Microservice_Processamento
    Microservice_Processamento --> Processamento_Data
    Processamento_Data --> End_Processamento
    End_Processamento --> End
    
    Topic_Cadastros --> Microservice_Cadastros
    Microservice_Cadastros --> Process_Cadastros
    Process_Cadastros --> End_Cadastros_Process
    End_Cadastros_Process --> End


