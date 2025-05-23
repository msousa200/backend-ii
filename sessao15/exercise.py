"""
Sessão 15: Desenvolvimento Avançado de Agentes IA com CrewAI

Exercício: Criar um agente de IA que busca dados de clima em tempo real de uma 
API externa e responde com a temperatura atual.
"""

import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain.tools import tool
from langchain.agents import Tool


load_dotenv()


WEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'sua-chave-aqui')

class WeatherAgent:
    """Agente que busca e responde com informações de clima."""
    
    def __init__(self, name="ClimaTempo"):
        """
        Inicializa o agente de clima.
        
        Args:
            name (str): Nome do agente
        """
        self.name = name
        self.history = []
        self.setup_agent()
    
    def setup_agent(self):
        """Configura o agente com ferramentas para buscar dados de clima."""
        try:
         
            weather_tool = Tool(
                name="get_weather",
                func=self.get_weather,
                description="Obtém dados de clima para uma cidade específica"
            )
            
           
            self.agent = Agent(
                name=self.name,
                goal=f"Fornecer informações precisas sobre o clima",
                backstory=f"Você é um assistente especializado em fornecer informações meteorológicas para qualquer cidade do mundo.",
                verbose=True,
                tools=[weather_tool]
            )
            
            self.use_llm = True
        except Exception as e:
            print(f"Aviso: Não foi possível configurar o agente com LLM. Erro: {e}")
            self.use_llm = False
    
    @tool
    def get_weather(self, city_name):
        """
        Busca dados de clima para uma cidade específica.
        
        Args:
            city_name (str): Nome da cidade para a qual buscar o clima
        
        Returns:
            dict: Dados de clima formatados
        """
        try:
   
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
       
            response = requests.get(url)
            response.raise_for_status()  
       
            data = response.json()

            weather_info = {
                "cidade": data["name"],
                "pais": data["sys"]["country"],
                "temperatura": data["main"]["temp"],
                "sensacao_termica": data["main"]["feels_like"],
                "minima": data["main"]["temp_min"],
                "maxima": data["main"]["temp_max"],
                "umidade": data["main"]["humidity"],
                "descricao": data["weather"][0]["description"],
                "vento": data["wind"]["speed"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            return {
                "erro": True,
                "mensagem": f"Erro ao buscar dados de clima: {str(e)}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except (KeyError, IndexError) as e:
            return {
                "erro": True,
                "mensagem": f"Erro ao processar dados de clima: {str(e)}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def respond(self, query):
        """
        Responde a uma consulta do usuário sobre o clima.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: A resposta formatada com os dados de clima
        """

        self.history.append({
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    
        if "histórico" in query.lower() or "history" in query.lower():
            past_queries = [entry["query"] for entry in self.history[:-1]]
            if not past_queries:
                return "Você ainda não fez nenhuma consulta sobre o clima anteriormente."
            return f"Suas consultas anteriores: {', '.join(past_queries)}"
        
   
        city_name = self.extract_city(query)
        
        if not city_name:
            return "Por favor, informe uma cidade para que eu possa verificar o clima. Exemplo: 'Como está o clima em Lisboa?'"
        
     
        weather_data = self.get_weather(city_name)
        
     
        if weather_data.get("erro", False):
            return f"Desculpe, não foi possível obter os dados de clima para '{city_name}'. {weather_data.get('mensagem', '')}"
        
  
        response = self.format_weather_response(weather_data)
        return response
    
    def extract_city(self, query):
        """
        Extrai o nome da cidade da consulta do usuário.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: O nome da cidade identificada, ou None se não for encontrada
        """
   
        keywords = ["em", "para", "de", "sobre", "clima em", "tempo em", "temperatura em", "previsão para"]
        
        query_lower = query.lower()
        
      
        for keyword in keywords:
            if keyword in query_lower:
                parts = query_lower.split(keyword, 1)
                if len(parts) > 1 and parts[1].strip():
                 
                    city = parts[1].strip().split("?")[0].split(".")[0].split(",")[0].strip()
                    return city
        
       
        words = query.strip("?!.,").split()
        if words:
            return words[-1]
        
        return None
    
    def format_weather_response(self, weather_data):
        """
        Formata os dados de clima em uma resposta legível.
        
        Args:
            weather_data (dict): Dados de clima obtidos da API
            
        Returns:
            str: Resposta formatada
        """
        return f"""
Informações do clima para {weather_data['cidade']}, {weather_data['pais']}:

🌡️ Temperatura: {weather_data['temperatura']}°C
🌡️ Sensação térmica: {weather_data['sensacao_termica']}°C
🔽 Mínima: {weather_data['minima']}°C
🔼 Máxima: {weather_data['maxima']}°C
💧 Umidade: {weather_data['umidade']}%
🌤️ Condição: {weather_data['descricao']}
💨 Velocidade do vento: {weather_data['vento']} m/s
"""



if __name__ == "__main__":
    print("Inicializando o Agente de Clima...")
    agent = WeatherAgent()
    
    print(f"\nBem-vindo ao {agent.name}! Digite 'sair' para terminar.")
    print("Você pode fazer perguntas como: 'Como está o clima em Lisboa?'")
    print("Ou consultar seu histórico digitando: 'histórico'")
    

    while True:
        user_input = input("\nVocê: ")
        
        if user_input.lower() == "sair":
            print(f"{agent.name}: Até logo! Espero ter ajudado com informações sobre o clima!")
            break
            
        response = agent.respond(user_input)
        print(f"{agent.name}: {response}")
