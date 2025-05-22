import os
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_ollama import ChatOllama

from app.services.language_service import LanguageService
from app.services.direct_translation_service import DirectTranslationService
from app.services.direct_summarization_service import DirectSummarizationService
from app.utils.logging_util import crew_logger, PerformanceTimer

load_dotenv()

OLLAMA_BASE_URL = "http://localhost:11436"  
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

print(f"CrewAIService using Ollama URL: {OLLAMA_BASE_URL}")

FORMATTED_MODEL = f"ollama/{OLLAMA_MODEL}"

thread_pool = ThreadPoolExecutor(max_workers=5)


class CrewAIService:
    """Service for handling text processing with CrewAI agents"""
    
    def __init__(self):
        self.llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=FORMATTED_MODEL,
            temperature=0.2
        )
        
        self.direct_translator = DirectTranslationService()
        
        self.direct_summarizer = DirectSummarizationService()
    
    def create_summarizer_agent(self) -> Agent:
        return Agent(
            role="Text Summarizer",
            goal="Create concise and accurate summaries of text. Only output the summary itself, never instructions or explanations.",
            backstory="You are an expert at distilling complex information into clear, concise summaries. You always respond with only the summary, never with instructions or meta-commentary.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            system_message="You are a professional summarizer. When given text to summarize, you must ONLY output the summary itself - no explanations, no instructions, no headers or formatting, no disclaimers. NEVER mention criteria, process, or formatting. NEVER use phrases like 'here's the summary', 'final answer', or similar. Just provide the pure summary. Do not include any system information or meta-commentary. The summary should be 1-2 concise sentences."
        )

    @staticmethod
    def clean_agent_output(output: str, mode: str = None) -> str:
        import re
        lines = output.splitlines()
        cleaned = []
        for line in lines:
            l = line.strip()
            if not l:
                continue
            if re.search(r'(your answer|must be|begin!|expected criteria|steps:|follow these steps|output only|respond only|explanation|criteria|final answer|task:|use the tools|provide|process|format|structure|meta-commentary|extracted|extraction process|explain|describe|instructions|how to|methodology|criteria|expected|tools available|job depends|responda apenas|apenas com|apenas a lista|apenas o resumo|apenas com o resumo|apenas com a análise|apenas com o sentimento|responda somente|só o resumo|só a lista|só o sentimento|só a análise|somente o resumo|somente a lista|somente o sentimento|somente a análise)', l, re.IGNORECASE):
                continue
            if re.match(r'^(#|\*\*|\-|=|\d+\.|agent:|task:|role:|goal:|backstory:)', l, re.IGNORECASE):
                continue
            if re.match(r'^(resuma|analise|liste|qual o sentimento|tarefa:|task:|final answer:|resposta completa:|resposta:|summary:|summarize|analyze|extract|sentiment)', l, re.IGNORECASE):
                continue
            cleaned.append(l)
        cleaned_text = '\n'.join(cleaned).strip()
        
        if mode == "summarization":
            cleaned_text = re.sub(r'^(Resumo\s*em\s*\d+\s*frases?[:\s]*|Resumo[:\s]*)', '', cleaned_text, flags=re.IGNORECASE).strip()
            
            match = re.search(r'(Resumo|Summary)\s*[:\-]\s*(.*)', cleaned_text, re.IGNORECASE)
            if match:
                return match.group(2).strip()
                
            sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
            if sentences and len(sentences) >= 2:
                return ' '.join(sentences[:3]).strip()
                
            return cleaned_text
            
        return cleaned_text

    def _clean_summary_output(self, text: str) -> str:
        """
        Thoroughly clean a summary output to remove any meta-text or instructions
        
        Args:
            text: The text to clean
            
        Returns:
            Cleaned summary text
        """
        import re
        
        if not text or not text.strip():
            return ""
            
        cleaned = re.sub(r'^(?:summary:|resumo:|final answer:|resposta:|output:|result:)', 
                        '', text, flags=re.IGNORECASE).strip()
        
        lines = cleaned.split('\n')
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if re.search(r'(your personal goal|responsive design|your job|criteria|expected|must be|final answer|task:|use the tools|provide|process|format|bullet points|numbered lists)', 
                        line, flags=re.IGNORECASE):
                continue
                
            content_lines.append(line)
            
        if content_lines:
            return ' '.join(content_lines)
            
        sentences = re.split(r'(?<=[.!?])\s+', cleaned)
        content_sentences = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            if re.search(r'(your personal goal|responsive design|your job|criteria|expected|must be|final answer|task:|use the tools|provide|process|format|bullet points|numbered lists)', 
                        sentence, flags=re.IGNORECASE):
                continue
                
            content_sentences.append(sentence.strip())
            
        if content_sentences:
            return ' '.join(content_sentences)
            
        return cleaned.strip()

    async def _summarize_text(self, text: str) -> str:
        """
        Summarize text using DirectSummarizationService for better results
        Falls back to extracting the first 1-2 sentences if needed
        """
        with PerformanceTimer("summarization") as timer:
            try:
                loop = asyncio.get_event_loop()
                start_time = time.time()
                
                result = await loop.run_in_executor(
                    thread_pool, 
                    lambda: self.direct_summarizer.summarize(text, sentences=2)
                )
                
                processing_time = time.time() - start_time
                timer.add_info("processing_time", processing_time)
                
                crew_logger.info(f"Summarization completed in {processing_time:.2f}s, length={len(result)}")
                return result
                
            except Exception as e:
                crew_logger.error(f"Summarization error: {str(e)}", exc_info=True)
                timer.add_info("error", str(e))
                
                import re
                fallback_sentences = re.findall(r'[A-Z][^.!?]*[.!?]', text)
                fallback_summary = ' '.join(fallback_sentences[:2]).strip() if fallback_sentences else text.strip()
                
                return fallback_summary

    def _detect_language(self, text: str) -> str:
        """
        Detect if text is in Portuguese or English
        Returns 'Portuguese' or 'English'
        """
        detected_language, confidence = LanguageService.detect_language(text)
        crew_logger.info(f"Language detection: {detected_language} with {confidence:.2f} confidence")
        
        if detected_language == 'Unknown':
            crew_logger.warning("Could not detect language, defaulting to English")
            return 'English'
            
        return detected_language
    
    async def _translate_text(self, text: str, target_language: str = None) -> str:
        """
        Translate text using the specialized direct translation service
        which is optimized for small models like TinyLlama
        """
        with PerformanceTimer("translation") as timer:
            detected_language = self._detect_language(text)
            timer.add_info("detected_language", detected_language)
            
            if target_language is None:
                if detected_language == 'Portuguese':
                    target_language = 'English'
                else:
                    target_language = 'Portuguese'
            
            timer.add_info("target_language", target_language)
            crew_logger.info(f"Translating text to {target_language} using direct translation service")
            
            try:
                loop = asyncio.get_event_loop()
                start_time = time.time()
                
                result = await loop.run_in_executor(
                    thread_pool, 
                    lambda: self.direct_translator.translate(text, target_language)
                )
                
                import re
                result = re.sub(r'(^|\s+)(Tradução|Translation|Tradução para o português|Tradução para o inglês|Portuguese translation|English translation)[:\s]*', 
                              '', result, flags=re.IGNORECASE).strip()
                
                result = re.sub(r'(Tradução|Translation)(\.|:|$|\s+$)', 
                              '', result, flags=re.IGNORECASE).strip()
                
                processing_time = time.time() - start_time
                timer.add_info("processing_time", processing_time)
                timer.add_info("result_length", len(result))
                
                crew_logger.info(f"Translation completed in {processing_time:.2f}s, length={len(result)}")
                return result
                
            except Exception as e:
                crew_logger.error(f"Translation error: {str(e)}", exc_info=True)
                timer.add_info("error", str(e))
                
                if detected_language == "Portuguese":
                    return f"Error translating to English: {str(e)}"
                else:
                    return f"Erro na tradução para Português: {str(e)}"

    async def process_text(self, text: str, processing_type: str, target_language: str = None) -> str:
        """
        Process text using AI agents based on the specified processing type
        
        Args:
            text: The text to process
            processing_type: Type of processing to perform (summarization, translation, detection)
            target_language: Target language for translation (optional)
            
        Returns:
            Processed text result
        """
        if processing_type == "summarization":
            return await self._summarize_text(text)
        elif processing_type == "translation":
            return await self._translate_text(text, target_language)
        elif processing_type == "detection":
            return self._detect_language(text)
        else:
            raise ValueError(f"Unsupported processing type: {processing_type}")