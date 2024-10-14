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

### **RF01: Gerenciamento de Pré-Cadastro**  
- O sistema deve permitir que uma empresa realize um pré-cadastro, fornecendo informações básicas como nome e email.  
- Após o pré-cadastro, o sistema deve gerar um token JWT exclusivo para a empresa.  
- Esse token JWT será utilizado para autenticar todas as requisições realizadas pela empresa.  

### **RF02: Envio de Dataset para Treinamento**  
- O sistema deve permitir que a empresa envie um dataset contendo informações de análise de crédito/cliente via endpoint dedicado.  
- O dataset deve incluir os dados necessários para treinar um modelo de IA capaz de avaliar as condições de crédito do cliente.  
- O sistema deve validar a estrutura e integridade dos dados recebidos antes de iniciar o treinamento do modelo.  

### **RF03: Treinamento do Modelo de IA**  
- O sistema deve utilizar o dataset fornecido para treinar um modelo de IA personalizado para a empresa solicitante.  
- O modelo treinado deve ser armazenado e associado à empresa que o solicitou.  

### **RF04: Processamento de Novos Pedidos**  
- O sistema deve permitir que a empresa envie novos pedidos por meio de um endpoint, utilizando o token JWT para autenticação.  
- O modelo de IA deve processar o pedido e retornar uma decisão sobre a aprovação ou não do pedido para faturamento.  
- A resposta deve incluir uma justificativa com base nas condições analisadas pelo modelo.  

### **RF05: Retreinamento do Modelo de IA**  
- O sistema deve permitir que a empresa solicite o retreinamento do modelo de IA a qualquer momento, enviando um novo dataset.  
- O retreinamento deve gerar um novo modelo, mantendo versões anteriores disponíveis para a empresa realizar comparações ou testes.  

### **RF06: Auditoria e Log de Atividades**  
- O sistema deve registrar todas as atividades relacionadas ao envio de datasets, treinamentos de modelo e processamento de pedidos.  
- O log deve estar acessível para a empresa consultar e monitorar as atividades realizadas.  

# Requisitos não Funcionais  

### **RNF01: Segurança**  
- O sistema deve garantir a segurança dos dados através da autenticação baseada em JWT para acesso aos end-points.  

### **RNF02: Escalabilidade**  
- O sistema deve ser capaz de escalar horizontalmente para suportar um número crescente de empresas e pedidos simultâneos
- O sistema deve ser capaz de lidar com grandes volumes de dados para treinamento de modelos sem comprometer o desempenho.

### **RNF03: Performance**  
- O processamento de pedidos novos deve ocorrer em tempo real ou near real-time, com latência mínima.
- O tempo de resposta para a decisão de crédito deve ser rápido o suficiente para não prejudicar a experiência do cliente final.

### **RNF04: Manutenibilidade**  
- O sistema deve ser projetado para facilitar a manutenção e atualizações, com código modular e bem documentado.
- Deve haver suporte para logs detalhados e monitoramento, permitindo a identificação e correção rápida de problemas.


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


