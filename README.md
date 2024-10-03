## Objetivo
  O objetivo deste projeto é fornecer um serviço onde o usuário tem autonomia para enviar informações sobre pedidos, clientes, limites de crédito e históricos de consultas ao Serasa. Esses dados são utilizados para criar modelos de inteligência artificial capazes de prever se um pedido deve ou não ser faturado, com base nas informações fornecidas.

## Contexto
  Este projeto é aplicável a qualquer negócio que envolva a emissão de pedidos por clientes e que exija uma análise de crédito robusta. O nível de assertividade da IA dependerá diretamente da qualidade e da origem dos dados fornecidos pela empresa solicitante. Para avaliar a eficiência do projeto, utilizamos uma base de dados real e aplicamos o modelo dentro de uma empresa.
  
# Escopo
### **1. Cadastro Usuario**  
Um endpoint é disponibilizado para realizar o cadastro do usuário no serviço. No momento do cadastro, é gerado um token de acesso JWT, que será utilizado para controlar o acesso aos demais endpoints.

### **2. Envio de informações**  
Este endpoint é responsável por receber informações de pedidos, clientes, limites de crédito e históricos de consultas ao Serasa, em lotes de 500 itens, e gravá-las no banco de dados. O endpoint possui uma camada de segurança que valida o JWT Bearer Token e verifica se o usuário associado ao token é válido.

### **3. Treinamento do Modelo**  
Não é um endpoint, é um processo disparado quando o envio de todas as informações são concluidas (os tratamentos normalização dos dados, redução de dimensionalidade) devem ser feitos pelo usuario pois o serviço so é responsavel por obter as informações validar e gerar um modelo treinado.

### **4. Teste com o Modelo**  


### **5. Utilização do modelo para predição de pedidos**  

### **6. Tecnologias**  
Para o desenvolvimento do projeto, foram utilizadas as seguintes tecnologias:
  * **Linguagem:** Python 3.11+
  * **Banco de Dados:** SqlServer
  * **Mensageria:** Kafka
    
Bibliotecas e FrameWorks
  * Flask
  * JWT
  * SqlAlchemy
  * Json
  * ConfigParser
  * Kafka

# Requisitos

# Arquitetura
