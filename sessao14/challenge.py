"""
Sessão 14: Introdução aos Agentes de IA em Python com CrewAI

Desafio: Aprimorar o agente para lidar com múltiplas consultas com respostas 
diferentes baseadas em palavras-chave.
"""

import os
import re
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tasks import TaskOutput
from langchain.llms import OpenAI
from dotenv import load_dotenv


load_dotenv()


class AdvancedAgent:
    """Agente avançado que processa consultas usando palavras-chave e contexto."""
    
    def __init__(self, name="EticAssistant"):
        """
        Inicializa o agente avançado.
        
        Args:
            name (str): Nome do agente
        """
        self.name = name
        self.setup_llm()
        self.setup_agents()
        self.setup_response_patterns()
        self.conversation_history = []
    
    def setup_llm(self):
        """Configura o modelo de linguagem para os agentes."""
        try:
            self.llm = OpenAI(temperature=0.7)
            self.use_llm = True
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar o LLM. Erro: {e}")
            self.llm = None
            self.use_llm = False
    
    def setup_agents(self):
        """Configura agentes especializados para diferentes tipos de consultas."""
        if self.use_llm:

            self.info_agent = Agent(
                name="InfoAgent",
                goal="Fornecer informações precisas e úteis aos usuários",
                backstory="Um especialista em responder a perguntas gerais com clareza e precisão.",
                llm=self.llm,
                verbose=True
            )
            
  
            self.tech_agent = Agent(
                name="TechAgent",
                goal="Resolver problemas técnicos dos usuários",
                backstory="Um especialista técnico com amplo conhecimento em tecnologia e solução de problemas.",
                llm=self.llm,
                verbose=True
            )
            
        
            self.chat_agent = Agent(
                name="ChatAgent",
                goal="Manter conversas agradáveis e engajantes com os usuários",
                backstory="Um especialista em comunicação que mantém conversas leves e amigáveis.",
                llm=self.llm,
                verbose=True
            )
    
    def setup_response_patterns(self):
        """Configura padrões de resposta baseados em palavras-chave."""
   
        self.keyword_responses = {
      
            r'\b(oi|olá|hey|e aí)\b': lambda: f"Olá! Sou o {self.name}, como posso ajudar você hoje?",
            
  
            r'\b(quem é você|seu nome|o que você é)\b': lambda: f"Sou o {self.name}, um assistente virtual desenvolvido como exemplo para a Sessão 14 do curso de Backend II da ETIC.",
            

            r'\b(hora|horas|horário)\b': lambda: f"Agora são {datetime.now().strftime('%H:%M:%S')}.",
            
      
            r'\b(data|dia|hoje)\b': lambda: f"Hoje é {datetime.now().strftime('%d/%m/%Y')}.",
            
   
            r'\b(ajuda|help|socorro|comandos)\b': lambda: "Posso ajudar com:\n" +
                                                          "- Informações gerais (pergunte algo)\n" +
                                                          "- Hora e data atual\n" +
                                                          "- Suporte técnico (mencione 'problema', 'erro', 'não funciona')\n" +
                                                          "- Conversa casual\n" +
                                                          "Digite 'sair' para encerrar.",
                                              
    
            r'\b(obrigado|obrigada|valeu|agradeço)\b': lambda: "De nada! Estou sempre à disposição para ajudar.",
            
   
            r'\b(tchau|adeus|até logo|até mais)\b': lambda: "Até logo! Foi um prazer ajudar.",
      
            r'\b(problema|erro|bug|não funciona|falha|travou)\b': lambda: "Parece um problema técnico. Posso sugerir algumas etapas básicas de solução:\n" +
                                                                         "1. Reinicie o aplicativo ou dispositivo\n" +
                                                                         "2. Verifique sua conexão com a internet\n" +
                                                                         "3. Atualize para a versão mais recente\n" +
                                                                         "4. Limpe o cache do aplicativo\n" +
                                                                         "Se o problema persistir, forneça mais detalhes sobre o erro."
        }
    
    def identify_query_type(self, query):
        """
        Identifica o tipo de consulta com base em palavras-chave.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: O tipo de consulta identificado
        """
        query_lower = query.lower()
        
   
        for pattern in self.keyword_responses:
            if re.search(pattern, query_lower):
                return "predefined"
    
        if any(word in query_lower for word in ["problema", "erro", "bug", "não funciona", "falha"]):
            return "tech"
        elif any(word in query_lower for word in ["o que", "como", "quando", "onde", "por que", "explique", "define"]):
            return "info"
        else:
            return "chat"
    
    def create_task(self, agent, query):
        """
        Cria uma tarefa para um agente específico.
        
        Args:
            agent: O agente que executará a tarefa
            query (str): A consulta do usuário
            
        Returns:
            Task: A tarefa criada
        """
        return Task(
            description=f"Responda à seguinte consulta do usuário: {query}",
            agent=agent,
            expected_output="Uma resposta útil, clara e concisa à consulta do usuário."
        )
    
    def get_predefined_response(self, query):
        """
        Obtém uma resposta predefinida com base em padrões de palavras-chave.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: A resposta predefinida, se encontrada
        """
        query_lower = query.lower()
        
        for pattern, response_func in self.keyword_responses.items():
            if re.search(pattern, query_lower):
                return response_func()
        
        return None
    
    def get_agent_response(self, query, query_type):
        """
        Obtém uma resposta de um agente especializado.
        
        Args:
            query (str): A consulta do usuário
            query_type (str): O tipo de consulta
            
        Returns:
            str: A resposta do agente
        """
        if not self.use_llm:
            return "Desculpe, não consigo processar esta consulta sem um modelo de linguagem configurado."
        
        try:
            if query_type == "tech":
                task = self.create_task(self.tech_agent, query)
            elif query_type == "info":
                task = self.create_task(self.info_agent, query)
            else:  
                task = self.create_task(self.chat_agent, query)
            
         
            crew = Crew(
                agents=[task.agent],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            return result
        
        except Exception as e:
            return f"Desculpe, encontrei um erro ao processar sua consulta: {str(e)}"
    
    def respond(self, query):
        """
        Responde a uma consulta do usuário.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: A resposta do agente
        """
      
        self.conversation_history.append({"role": "user", "content": query})
        
      
        query_type = self.identify_query_type(query)
        

        if query_type == "predefined":
            response = self.get_predefined_response(query)
        else:
            response = self.get_agent_response(query, query_type)
        
      
        if not response:
            response = "Desculpe, não consegui entender completamente sua consulta. Pode reformular ou tentar outra pergunta?"
        
  
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response



if __name__ == "__main__":
    print("Inicializando o Agente Avançado...")
    agent = AdvancedAgent(name="EticAdvancedBot")
    
    print(f"\nBem-vindo ao {agent.name}! Digite 'ajuda' para ver o que posso fazer ou 'sair' para terminar.")
    
    while True:
        user_input = input("\nVocê: ")
        
        if user_input.lower() == "sair":
            print(f"{agent.name}: Até logo! Foi um prazer ajudar.")
            break
            
        response = agent.respond(user_input)
        print(f"{agent.name}: {response}")

