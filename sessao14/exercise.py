"""
Sessão 14: Introdução aos Agentes de IA em Python com CrewAI

Exercício: Construir um agente de IA simples que retorne uma mensagem predefinida 
quando recebe uma entrada específica.
"""

import os
from crewai import Agent
from langchain.llms import OpenAI




class SimpleAgent:
    """Agente simples que responde a consultas específicas com mensagens predefinidas."""
    
    def __init__(self, name="Assistente"):
        """
        Inicializa o agente com um nome.
        
        Args:
            name (str): Nome do agente
        """
  
        try:
            llm = OpenAI(temperature=0.7)
            self.agent = Agent(
                name=name,
                goal=f"Ajudar o usuário respondendo às perguntas com dados conhecidos",
                backstory=f"Você é um assistente virtual chamado {name} que ajuda pessoas respondendo perguntas.",
                llm=llm,
                verbose=True
            )
            self.use_llm = True
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar o LLM. Usando respostas predefinidas. Erro: {e}")
            self.agent = None
            self.use_llm = False
        
  
        self.predefined_responses = {
            "olá": f"Olá! Sou o {name}, como posso ajudar?",
            "quem é você": f"Sou o {name}, um agente de IA simples criado para demonstrar o uso do CrewAI.",
            "ajuda": "Posso responder a perguntas simples como 'olá', 'quem é você', e fornecer 'ajuda'.",
        }
    
    def respond(self, query):
        """
        Responde a uma consulta do usuário.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: A resposta do agente
        """
   
        normalized_query = query.lower().strip()
        
  
        if normalized_query in self.predefined_responses:
            return self.predefined_responses[normalized_query]
        

        if self.use_llm and self.agent:
            try:
          
                response = self.agent.execute_task(f"Responda à seguinte pergunta: {query}")
                return response
            except Exception as e:
                return f"Desculpe, não consegui processar sua consulta com o LLM. Erro: {e}"
        
      
        return "Desculpe, não entendi sua consulta. Por favor, tente 'olá', 'quem é você', ou 'ajuda'."



if __name__ == "__main__":

    agent = SimpleAgent(name="EticBot")
    
    print("Bem-vindo ao EticBot! Digite 'sair' para terminar.")
    

    while True:
        user_input = input("\nVocê: ")
        
        if user_input.lower() == "sair":
            print("EticBot: Até logo!")
            break
            
        response = agent.respond(user_input)
        print(f"EticBot: {response}")

