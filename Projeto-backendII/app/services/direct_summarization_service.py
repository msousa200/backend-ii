"""
Direct Summarization Service for text summarization optimized for small models.
Uses Ollama models locally for efficient text summarization without CrewAI framework.
"""

import os
import re
import time
import logging
from typing import Tuple, Dict, Optional, List
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from app.utils.logging_util import crew_logger, PerformanceTimer

OLLAMA_BASE_URL = "http://localhost:11436"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

print(f"DirectSummarizationService using Ollama URL: {OLLAMA_BASE_URL}")


class DirectSummarizationService:
    def __init__(self):
        try:
            self.llm = ChatOllama(
                base_url=OLLAMA_BASE_URL,
                model=OLLAMA_MODEL,
                temperature=0.1
            )
            self.logger = crew_logger
            self.logger.info(f"DirectSummarizationService initialized with model: {OLLAMA_MODEL}")
        except Exception as e:
            self.logger.error(f"Error initializing DirectSummarizationService: {str(e)}")
            raise

    def summarize(self, text: str, sentences: int = 2) -> str:
        with PerformanceTimer("direct_summarization") as timer:
            try:
                fallback_sentences = re.findall(r'[A-Z][^.!?]*[.!?]', text)
                fallback_summary = ' '.join(fallback_sentences[:2]).strip() if fallback_sentences else text.strip()
                
                summarization_strategies = []
                
                summarization_strategies.append({
                    "system_message": "Você é um resumidor de texto profissional. Produza apenas o resumo em texto simples, sem numeração ou formatação. Use a mesma língua do texto de entrada.",
                    "user_prompt": f"Texto para resumir: {text}\n\nResumo (exatamente 2 frases simples, sem numeração):"
                })
                
                summarization_strategies.append({
                    "system_message": "You are a text summarizer. When given text to summarize, you must ONLY output the summary itself with no numbers, bullet points, or extra formatting. Just provide the pure summary in 2 concise sentences without numbers or prefixes. Always summarize in the same language as the original text.",
                    "user_prompt": f"Summarize this text in exactly 2 sentences with no numbering or formatting: {text}"
                })
                
                summarization_strategies.append({
                    "system_message": "You are a professional text summarizer. You always maintain the original language of the text.",
                    "user_prompt": f"Summarize the following text in 2 plain sentences only. No numbering. No formatting. Just two sentences in the original language:\n\n{text}"
                })
                
                processed_output = None
                successful_strategy = None
                start_time = time.time()
                
                for i, strategy in enumerate(summarization_strategies):
                    strategy_name = f"Strategy {i+1}"
                    self.logger.info(f"Trying summarization {strategy_name}")
                    
                    system_message = strategy["system_message"]
                    user_prompt = strategy["user_prompt"]
                    
                    try:
                        result = self.llm.invoke([
                            SystemMessage(content=system_message),
                            HumanMessage(content=user_prompt)
                        ])
                        
                        raw_output = result.content
                        self.logger.info(f"Raw result using {strategy_name}: {raw_output[:100]}...")
                        
                        current_output = self._extract_summary(raw_output)
                        
                        meta_indicators = [
                            "your job", "use the tools", "ensure that", "criteria", "expected", 
                            "i am", "my goal", "my response", "i must", "i will", "responsive design",
                            "your personal goal", "final answer", "must be", "should be", "remember to",
                            "meu trabalho", "minha tarefa", "vou resumir", "resumirei", "resposta final",
                            "frases concisas", "formato solicitado", "preciso", "devo", "aqui está",
                            "industrie", "înseamnă", "transformează", "sistemele", "încadreze",
                            "nouă oportunitate", "întreaga lume"
                        ]
                        
                        is_valid = (current_output and 
                                  len(current_output.split()) >= 5 and
                                  not any(indicator in current_output.lower() for indicator in meta_indicators))
                        
                        if is_valid:
                            self.logger.info(f"Successfully summarized using {strategy_name}")
                            processed_output = current_output
                            successful_strategy = strategy_name
                            break
                        else:
                            self.logger.warning(f"{strategy_name} produced invalid summary with meta-text")
                            
                    except Exception as e:
                        self.logger.error(f"Error in {strategy_name}: {str(e)}")
                        continue
                
                processing_time = time.time() - start_time
                timer.add_info("processing_time", processing_time)
                
                if processed_output:
                    self.logger.info(f"Summarization completed in {processing_time:.2f}s using {successful_strategy}")
                    timer.add_info("successful_strategy", successful_strategy)
                    return processed_output
                else:
                    self.logger.warning("All summarization strategies failed, using fallback")
                    timer.add_info("fallback", "used")
                    return fallback_summary
                    
            except Exception as e:
                self.logger.error(f"Summarization error: {str(e)}")
                timer.add_info("error", str(e))
                return fallback_summary
    
    def _extract_summary(self, output: str) -> str:
        if not output or not output.strip():
            return ""
        
        self.logger.debug(f"Extracting summary from raw output: {output}")
        
        cleaned = re.sub(r'```(?:.*?)```', '', output, flags=re.DOTALL)
        
        cleaned = re.sub(r'^(?:Summary:|Resumo:|Sumário:|Result:|Output:|Final summary:|Final answer:|Resposta:|Resultado:|Texto para resumir:)[:\s]*', 
                        '', cleaned, flags=re.IGNORECASE).strip()
        
        cleaned = re.sub(r'(?:^|\s+)(?:\d+\.)(?:\s+)', ' ', cleaned)
        
        cleaned = re.sub(r'\b(?:sentence|paragraph|item|point)\s*\d+\b', '', cleaned, flags=re.IGNORECASE)
        
        lines = cleaned.strip().split('\n')
        filtered_lines = []
        
        skip_markers = ['summarize', 'summary:', 'input:', 'output:', 'source:', 'target:', 
                       'original text:', 'instructions:', 'note:', 'criteria', 'expected',
                       'your goal', 'my goal', 'i must', 'i will', 
                       'resumo:', 'resumir', 'texto original:', 'instruções:', 'nota:', 
                       'critérios', 'esperado', 'seu objetivo', 'meu objetivo', 
                       'devo', 'vou', 'aqui está']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if any(marker in line.lower() for marker in skip_markers):
                continue
            
            filtered_lines.append(line)
        
        if filtered_lines:
            combined = ' '.join(filtered_lines)
            combined = re.sub(r'\(\d+\)|\d+\)', '', combined)
            combined = re.sub(r'\s+', ' ', combined).strip()
            return combined
        
        return cleaned.strip()
