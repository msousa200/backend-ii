"""
Sessão 15: Desenvolvimento Avançado de Agentes IA com CrewAI

Desafio: Desenvolver um agente de IA que pode lidar com consultas complexas e responder
com informações relevantes, possivelmente usando APIs externas para enriquecimento de dados.
"""

import os
import re
import json
import requests
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tasks import TaskOutput
from langchain.tools import tool
from langchain.agents import Tool
from langchain.llms import OpenAI


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("agent.log"), logging.StreamHandler()]
)
logger = logging.getLogger("SmartAgent")


load_dotenv()


WEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'sua-chave-aqui')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'sua-chave-aqui')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class SmartAgent:
    """Agente inteligente avançado com integração de múltiplas APIs e gerenciamento de estado."""
    
    def __init__(self, name="EticSmart"):
        """
        Inicializa o agente inteligente.
        
        Args:
            name (str): Nome do agente
        """
        self.name = name
    
        self.state = {
            "conversation_history": [],
            "user_preferences": {},
            "last_queries": [],
            "cached_data": {}
        }
        self.setup_llm()
        self.setup_tools()
        self.setup_agents()
    
    def setup_llm(self):
        """Configura o modelo de linguagem para os agentes."""
        try:
            self.llm = OpenAI(temperature=0.7)
            self.use_llm = True
        except Exception as e:
            logger.warning(f"Não foi possível inicializar o LLM. Erro: {e}")
            self.llm = None
            self.use_llm = False
    
    def setup_tools(self):
        """Configura ferramentas para os agentes."""
        self.tools = [
            Tool(
                name="get_weather",
                func=self.get_weather,
                description="Obtém dados de clima para uma localização específica"
            ),
            Tool(
                name="get_news",
                func=self.get_news,
                description="Obtém notícias recentes sobre um tópico específico"
            ),
            Tool(
                name="get_user_preferences",
                func=self.get_user_preferences,
                description="Obtém preferências do usuário para personalização"
            )
        ]
    
    def setup_agents(self):
        """Configura agentes especializados para diferentes tipos de tarefas."""
        if self.use_llm:
           
            self.info_agent = Agent(
                name="InfoAgent",
                goal="Fornecer informações precisas e relevantes aos usuários",
                backstory="Especialista em buscar e sintetizar informações de várias fontes.",
                llm=self.llm,
                tools=self.tools,
                verbose=True
            )
            
       
            self.recommendation_agent = Agent(
                name="RecommendationAgent",
                goal="Fornecer recomendações personalizadas com base nas preferências do usuário",
                backstory="Especialista em análise de preferências e fornecimento de recomendações personalizadas.",
                llm=self.llm,
                tools=self.tools,
                verbose=True
            )
            
      
            self.conversation_agent = Agent(
                name="ConversationAgent",
                goal="Manter uma conversa natural e engajante com o usuário",
                backstory="Especialista em comunicação com habilidades avançadas de conversação.",
                llm=self.llm,
                tools=self.tools,
                verbose=True
            )
    
    @tool
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Obtém dados meteorológicos atuais para uma localização específica.
        
        Args:
            location (str): Nome da cidade ou localização
        
        Returns:
            dict: Dados meteorológicos
        """
    
        cache_key = f"weather_{location}_{datetime.now().strftime('%Y-%m-%d_%H')}"
        if cache_key in self.state["cached_data"]:
            logger.info(f"Usando dados de clima em cache para {location}")
            return self.state["cached_data"][cache_key]
        
        try:
        
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
            
   
            response = requests.get(url)
            response.raise_for_status()
            
  
            data = response.json()
            weather_data = {
                "location": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "timestamp": datetime.now().isoformat()
            }
            
      
            self.state["cached_data"][cache_key] = weather_data
            logger.info(f"Obtidos dados de clima para {location}")
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Erro ao obter dados de clima para {location}: {str(e)}")
            return {"error": f"Não foi possível obter dados de clima para {location}: {str(e)}"}
    
    @tool
    def get_news(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Obtém notícias recentes sobre um tópico específico.
        
        Args:
            query (str): Termo de pesquisa
            max_results (int): Número máximo de resultados
        
        Returns:
            list: Lista de artigos de notícias
        """
 
        cache_key = f"news_{query}_{datetime.now().strftime('%Y-%m-%d')}"
        if cache_key in self.state["cached_data"]:
            logger.info(f"Usando dados de notícias em cache para '{query}'")
            return self.state["cached_data"][cache_key]
        
        try:
    
            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=pt"
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("articles", [])[:max_results]

            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    "title": article.get("title", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "published": article.get("publishedAt", ""),
                    "url": article.get("url", ""),
                    "description": article.get("description", "")
                })
            
      
            self.state["cached_data"][cache_key] = formatted_articles
            logger.info(f"Obtidas {len(formatted_articles)} notícias para '{query}'")
            
            return formatted_articles
            
        except Exception as e:
            logger.error(f"Erro ao obter notícias para '{query}': {str(e)}")
            return [{"error": f"Não foi possível obter notícias: {str(e)}"}]
    
    @tool
    def get_user_preferences(self, user_id: str = "default") -> Dict[str, Any]:
        """
        Obtém as preferências do usuário armazenadas.
        
        Args:
            user_id (str): ID do usuário
        
        Returns:
            dict: Preferências do usuário
        """
        return self.state.get("user_preferences", {})
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """
        Atualiza as preferências do usuário com base em suas interações.
        
        Args:
            preferences (dict): Novas preferências a serem adicionadas/atualizadas
        """
        self.state["user_preferences"].update(preferences)
        logger.info(f"Preferências de usuário atualizadas: {preferences}")
    
    def extract_preferences(self, query: str) -> Dict[str, Any]:
        """
        Extrai preferências implícitas da consulta do usuário.
        
        Args:
            query (str): A consulta do usuário
        
        Returns:
            dict: Preferências extraídas
        """
        preferences = {}
        

        location_patterns = [
            r'em\s+([A-Za-z\s]+)(?=[\s\.,;:]|$)',
            r'para\s+([A-Za-z\s]+)(?=[\s\.,;:]|$)',
            r'sobre\s+([A-Za-z\s]+)(?=[\s\.,;:]|$)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, query)
            if match:
                preferences["location"] = match.group(1).strip()
                break
        
  
        interest_keywords = ["notícias", "clima", "esporte", "tecnologia", "cinema", "música", "política", "economia"]
        for keyword in interest_keywords:
            if keyword in query.lower():
                if "interests" not in preferences:
                    preferences["interests"] = []
                preferences["interests"].append(keyword)
        
        return preferences
    
    def identify_query_type(self, query: str) -> str:
        """
        Identifica o tipo de consulta com base em seu conteúdo.
        
        Args:
            query (str): A consulta do usuário
        
        Returns:
            str: O tipo de consulta identificado
        """
        query_lower = query.lower()
        

        if any(word in query_lower for word in ["clima", "tempo", "temperatura", "chover", "chuva", "sol"]):
            return "weather"
     
        if any(word in query_lower for word in ["notícia", "notícias", "jornal", "acontecimento", "manchete", "reportagem"]):
            return "news"
        
 
        if any(word in query_lower for word in ["preferência", "preferências", "gosto", "gostos", "interesse"]):
            return "preferences"
        
   
        if any(word in query_lower for word in ["histórico", "história", "conversas", "perguntas anteriores"]):
            return "history"
        
        
        return "general"
    
    def create_task_for_query(self, query: str, query_type: str) -> Task:
        """
        Cria uma tarefa apropriada com base no tipo de consulta.
        
        Args:
            query (str): A consulta do usuário
            query_type (str): O tipo de consulta
            
        Returns:
            Task: A tarefa criada
        """
        if query_type == "weather":
            return Task(
                description=f"Obtenha e forneça informações sobre o clima para a localização mencionada na consulta: '{query}'",
                agent=self.info_agent
            )
        
        elif query_type == "news":
            return Task(
                description=f"Obtenha e apresente notícias relevantes relacionadas à consulta: '{query}'",
                agent=self.info_agent
            )
            
        elif query_type == "preferences":
            return Task(
                description=f"Analise as preferências do usuário com base na consulta: '{query}' e no histórico de interações",
                agent=self.recommendation_agent
            )
            
        else:
            return Task(
                description=f"Responda à consulta do usuário de maneira informativa e engajante: '{query}'",
                agent=self.conversation_agent
            )
    
    def update_conversation_history(self, role: str, content: str):
        """
        Atualiza o histórico de conversas.
        
        Args:
            role (str): O papel ('user' ou 'assistant')
            content (str): O conteúdo da mensagem
        """
        self.state["conversation_history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
  
        if len(self.state["conversation_history"]) > 20:
            self.state["conversation_history"] = self.state["conversation_history"][-20:]
    
    def get_conversation_history(self, max_entries: int = 5) -> str:
        """
        Obtém um resumo do histórico de conversas.
        
        Args:
            max_entries (int): Número máximo de entradas a retornar
            
        Returns:
            str: Resumo formatado do histórico
        """
        history = self.state["conversation_history"][-max_entries:]
        if not history:
            return "Não há histórico de conversas disponível."
        
        formatted_history = []
        for entry in history:
            role = "Você" if entry["role"] == "user" else self.name
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M:%S")
            formatted_history.append(f"[{timestamp}] {role}: {entry['content']}")
        
        return "\n".join(formatted_history)
    
    def handle_special_queries(self, query: str) -> Optional[str]:
        """
        Trata consultas especiais como histórico, ajuda, etc.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: Resposta para consulta especial, ou None se não for especial
        """
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["histórico", "history", "conversas anteriores"]):
            return f"Aqui está o histórico recente das nossas conversas:\n\n{self.get_conversation_history()}"
        
        elif any(word in query_lower for word in ["ajuda", "help", "o que você pode fazer"]):
            return (
                f"Olá! Sou o {self.name}, seu assistente virtual avançado. Posso ajudar com:\n\n"
                f"🌤️ **Clima**: Pergunte sobre o clima em qualquer cidade\n"
                f"📰 **Notícias**: Solicite notícias sobre qualquer assunto\n"
                f"🔍 **Informações**: Faça perguntas sobre diversos temas\n"
                f"📝 **Histórico**: Digite 'histórico' para ver conversas anteriores\n\n"
                f"Quanto mais conversamos, mais aprendo sobre suas preferências para personalizar minhas respostas!"
            )
        
        elif any(word in query_lower for word in ["preferências", "preferences"]):
            prefs = self.get_user_preferences()
            if not prefs:
                return "Ainda não tenho preferências armazenadas para você. Conforme interagirmos, irei aprender suas preferências."
            
            response = "Aqui estão as preferências que aprendi com base em nossas interações:\n\n"
            for key, value in prefs.items():
                response += f"- {key}: {value}\n"
            return response
        
        return None
    
    def respond(self, query: str) -> str:
        """
        Processa a consulta do usuário e gera uma resposta.
        
        Args:
            query (str): A consulta do usuário
            
        Returns:
            str: A resposta do agente
        """
  
        self.update_conversation_history("user", query)
 
        self.state["last_queries"].append(query)
        if len(self.state["last_queries"]) > 10:
            self.state["last_queries"] = self.state["last_queries"][-10:]
        

        special_response = self.handle_special_queries(query)
        if special_response:
            self.update_conversation_history("assistant", special_response)
            return special_response
       
        preferences = self.extract_preferences(query)
        if preferences:
            self.update_user_preferences(preferences)
        
     
        query_type = self.identify_query_type(query)
        logger.info(f"Tipo de consulta identificado: {query_type}")
        
   
        if query_type == "weather":
         
            location = preferences.get("location")
            if not location:
                location = self.state["user_preferences"].get("location", "Lisboa")
            
            weather_data = self.get_weather(location)
            
            if "error" in weather_data:
                response = f"Desculpe, não consegui obter os dados do clima: {weather_data['error']}"
            else:
                response = (
                    f"🌤️ **Clima em {weather_data['location']}**\n\n"
                    f"Temperatura atual: {weather_data['temperature']}°C\n"
                    f"Sensação térmica: {weather_data['feels_like']}°C\n"
                    f"Umidade: {weather_data['humidity']}%\n"
                    f"Condição: {weather_data['description']}\n"
                    f"Vento: {weather_data['wind_speed']} m/s"
                )
        
        elif query_type == "news":

            topic = None
            for interest in preferences.get("interests", []):
                topic = interest
                break
            
            if not topic:
           
                words = query.lower().split()
                for word in words:
                    if word not in ["notícias", "notícia", "sobre", "recente", "últimas", "me", "dê", "fale"]:
                        topic = word
                        break
            
            if not topic:
                topic = "geral"
            
            news_data = self.get_news(topic)
            
            if news_data and "error" in news_data[0]:
                response = f"Desculpe, não consegui obter as notícias: {news_data[0]['error']}"
            else:
                response = f"📰 **Notícias recentes sobre {topic}**\n\n"
                for i, article in enumerate(news_data[:3], 1):
                    response += f"{i}. **{article['title']}**\n"
                    response += f"   Fonte: {article['source']} | {article['published'][:10]}\n"
                    response += f"   {article['description']}\n\n"
        
        elif self.use_llm:
      
            try:
                task = self.create_task_for_query(query, query_type)
                crew = Crew(
                    agents=[task.agent],
                    tasks=[task],
                    verbose=True
                )
                response = crew.kickoff()
            except Exception as e:
                logger.error(f"Erro ao processar com CrewAI: {str(e)}")
                response = f"Desculpe, encontrei um erro ao processar sua consulta: {str(e)}"
        
        else:
     
            response = (
                "Desculpe, não consigo processar completamente sua consulta sem um modelo de linguagem configurado. "
                "Posso ajudar com consultas sobre clima e notícias. Tente perguntar sobre o clima em alguma cidade "
                "ou solicitar notícias sobre um assunto específico."
            )
        
   
        self.update_conversation_history("assistant", response)
        
        return response



if __name__ == "__main__":
    print("Inicializando o Agente Inteligente Avançado...")
    agent = SmartAgent()
    
    print(f"\nBem-vindo ao {agent.name}! Digite 'ajuda' para ver o que posso fazer ou 'sair' para terminar.")
    

    while True:
        user_input = input("\nVocê: ")
        
        if user_input.lower() == "sair":
            print(f"{agent.name}: Foi um prazer ajudar! Até a próxima!")
            break
            
        response = agent.respond(user_input)
        print(f"{agent.name}: {response}")
