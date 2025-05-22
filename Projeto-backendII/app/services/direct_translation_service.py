"""
Direct translation service that bypasses CrewAI for better results with small models.
This approach creates a more specialized and streamlined translation approach
optimized for TinyLlama and other small models.
"""

import os
import time
import re
from typing import Tuple, Dict, Optional, List
import logging
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from app.services.language_service import LanguageService
from app.utils.logging_util import crew_logger, PerformanceTimer

OLLAMA_BASE_URL = "http://localhost:11436"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

print(f"DirectTranslationService using Ollama URL: {OLLAMA_BASE_URL}")


class DirectTranslationService:
    def __init__(self):
        try:
            self.llm = ChatOllama(
                base_url=OLLAMA_BASE_URL,
                model=OLLAMA_MODEL,
                temperature=0.1
            )
            self.logger = crew_logger
            self.logger.info(f"DirectTranslationService initialized with model: {OLLAMA_MODEL}")
        except Exception as e:
            self.logger.error(f"Error initializing DirectTranslationService: {str(e)}")
            raise

    def translate(self, text: str, target_language: str = None) -> str:
        with PerformanceTimer("direct_translation") as timer:
            try:
                detected_language, confidence = LanguageService.detect_language(text)
                timer.add_info("detected_language", detected_language)
                timer.add_info("detection_confidence", confidence)
                
                if target_language is None:
                    if detected_language == 'Portuguese':
                        target_language = 'English'
                    else:
                        target_language = 'Portuguese'
                
                timer.add_info("target_language", target_language)
                self.logger.info(f"Direct translation from {detected_language} to {target_language}")
                
                start_time = time.time()
                
                translation_strategies = []
                
                if detected_language == 'Portuguese' and target_language == 'English':
                    translation_strategies.append({
                        "system_message": "You are a professional Portuguese to English translator with expertise in academic and technical translation. Translate the text accurately and fluently.",
                        "user_prompt": f"Translate the following Portuguese text to English:\n\n```\n{text}\n```\n\nProvide only the English translation without any explanations or additional comments."
                    })
                    
                    examples = (
                        "Portuguese: A inteligência artificial está revolucionando diversos setores da economia.\n"
                        "English: Artificial intelligence is revolutionizing various sectors of the economy.\n\n"
                        "Portuguese: Os pesquisadores desenvolveram um novo método para análise de dados.\n"
                        "English: Researchers have developed a new method for data analysis.\n\n"
                    )
                    translation_strategies.append({
                        "system_message": "You are a Portuguese to English translator. Translate exactly like the examples.",
                        "user_prompt": f"Examples:\n{examples}\n\nPortuguese: {text}\n\nEnglish:"
                    })
                    
                    translation_strategies.append({
                        "system_message": "Translate Portuguese to English. Output only the translation.",
                        "user_prompt": f"Text: {text}\n\nTranslation:"
                    })
                    
                else:
                    translation_strategies.append({
                        "system_message": "You are a professional Portuguese translator. Translate the English text to Portuguese accurately.",
                        "user_prompt": f"Translate this English text to Portuguese:\n\n{text}\n\nPortuguese translation:"
                    })
                    
                    translation_strategies.append({
                        "system_message": "You are a professional translator from English to Portuguese.",
                        "user_prompt": f"Translate this text from English to Portuguese:\n\nEnglish: {text}\n\nPortuguese:"
                    })
                    
                    translation_strategies.append({
                        "system_message": "Translate to Portuguese.",
                        "user_prompt": f"Text: {text}\n\nTranslation:"
                    })
                
                processed_output = None
                successful_strategy = None
                
                for i, strategy in enumerate(translation_strategies):
                    strategy_name = f"Strategy {i+1}"
                    self.logger.info(f"Trying {strategy_name} for {detected_language} to {target_language}")
                    
                    system_message = strategy["system_message"]
                    user_prompt = strategy["user_prompt"]
                    
                    try:
                        result = self.llm.invoke([
                            SystemMessage(content=system_message),
                            HumanMessage(content=user_prompt)
                        ])
                        
                        raw_output = result.content
                        self.logger.info(f"Raw result using {strategy_name}: {raw_output[:100]}...")
                        
                        current_output = self._extract_translation(raw_output)
                        
                        is_valid = (current_output and 
                                   not current_output.startswith("Translation failed") and 
                                   len(current_output.split()) >= 2)
                        
                        if is_valid:
                            self.logger.info(f"Successfully translated using {strategy_name}")
                            processed_output = current_output
                            successful_strategy = strategy_name
                            break
                        else:
                            self.logger.warning(f"{strategy_name} failed to produce valid translation")
                            
                    except Exception as e:
                        self.logger.error(f"Error in {strategy_name}: {str(e)}")
                        continue
                
                processing_time = time.time() - start_time
                
                if processed_output:
                    self.logger.info(f"Translation completed in {processing_time:.2f}s using {successful_strategy}")
                    timer.add_info("successful_strategy", successful_strategy)
                    timer.add_info("result_length", len(processed_output))
                    return processed_output
                else:
                    error_msg = f"All translation strategies failed for {detected_language} to {target_language}"
                    self.logger.error(error_msg)
                    timer.add_info("error", error_msg)
                    
                    fallback_translation = self._fallback_translation(text, detected_language, target_language)
                    if fallback_translation:
                        self.logger.info("Using rule-based fallback translation")
                        return fallback_translation
                    
                    if detected_language == "Portuguese":
                        return "Error translating to English: All translation strategies failed."
                    else:
                        return "Erro na tradução para Português: Todas as estratégias de tradução falharam."
                
            except Exception as e:
                self.logger.error(f"Translation error: {str(e)}")
                timer.add_info("error", str(e))
                
                if detected_language == "Portuguese":
                    return f"Error translating to English: {str(e)}"
                else:
                    return f"Erro na tradução para Português: {str(e)}"
    
    def _get_examples(self, source_language: str, target_language: str) -> str:
        if source_language == 'English' and target_language == 'Portuguese':
            return (
                "English: Hello, how are you today?\nPortuguese: Olá, como está você hoje?\n\n"
                "English: I want to learn Portuguese.\nPortuguese: Eu quero aprender português.\n\n"
                "English: The weather is nice today.\nPortuguese: O tempo está bom hoje.\n\n"
                "English: Can you help me find the nearest restaurant?\nPortuguese: Pode me ajudar a encontrar o restaurante mais próximo?\n\n"
            )
        elif source_language == 'Portuguese' and target_language == 'English':
            return (
                "Portuguese: Olá, como está você hoje?\nEnglish: Hello, how are you today?\n\n"
                "Portuguese: Eu quero aprender inglês.\nEnglish: I want to learn English.\n\n"
                "Portuguese: O tempo está bom hoje.\nEnglish: The weather is nice today.\n\n"
                "Portuguese: Pode me ajudar a encontrar o restaurante mais próximo?\nEnglish: Can you help me find the nearest restaurant?\n\n"
            )
        else:
            return ""
    
    def _attempt_translation(self, text: str, source_language: str, target_language: str, examples: str) -> str:
        system_message = (
            f"You are a professional translator from {source_language} to {target_language}. "
            f"Your task is to translate the exact text given to you. "
            f"Only output the translation itself, no additional comments, explanations, or descriptions. "
            f"Never say what you're doing, just do it."
        )
        
        prompt = (
            f"Here are some example translations from {source_language} to {target_language}:\n\n"
            f"{examples}\n"
            f"Now translate this text from {source_language} to {target_language}:\n"
            f"{text}"
        )
        
        try:
            start_time = time.time()
            self.logger.info("Attempt 1: Direct prompt translation")
            
            result = self.llm.invoke([
                SystemMessage(content=system_message),
                HumanMessage(content=prompt)
            ])
            
            raw_output = result.content
            processed_output = self._extract_translation(raw_output, source_language, target_language)
            
            processing_time = time.time() - start_time
            self.logger.info(f"Translation completed in {processing_time:.2f}s")
            
            is_valid = self._validate_output(processed_output, text, source_language, target_language)
            
            if is_valid:
                return processed_output
            
            self.logger.info("Attempt 2: Using more structured prompt")
            
            system_message = (
                f"Translate from {source_language} to {target_language}. Output only the translation."
            )
            
            prompt = (
                f"Text to translate: \"{text}\"\n\n"
                f"Translation: "
            )
            
            result = self.llm.invoke([
                SystemMessage(content=system_message),
                HumanMessage(content=prompt)
            ])
            
            raw_output = result.content
            processed_output = self._extract_translation(raw_output, source_language, target_language)
            
            if not self._validate_output(processed_output, text, source_language, target_language):
                self.logger.info("Attempt 3: Using minimal prompt")
                
                system_message = f"Translate to {target_language}"
                prompt = text
                
                result = self.llm.invoke([
                    SystemMessage(content=system_message),
                    HumanMessage(content=prompt)
                ])
                
                raw_output = result.content
                processed_output = self._extract_translation(raw_output, source_language, target_language)
            
            return processed_output
            
        except Exception as e:
            self.logger.error(f"Translation error: {str(e)}")
            if source_language == "Portuguese":
                return f"Error translating to English: {str(e)}"
            else:
                return f"Erro na tradução para Português: {str(e)}"
    
    def _extract_translation(self, output: str) -> str:
        if not output or not output.strip():
            return "No translation produced"
        
        self.logger.debug(f"Extracting translation from raw output: {output}")
        
        cleaned = re.sub(r'```(?:.*?)```', '', output, flags=re.DOTALL)
        
        cleaned = re.sub(r'^(Translation:|Tradução:|Portuguese translation:|Português:|Portuguese:|English:|Inglês:|Here is the translation:|The translation is:)', '', cleaned, flags=re.IGNORECASE).strip()
        
        cleaned = re.sub(r'(Tradução|Translation)(\.|:|$|\s+$)', '', cleaned, flags=re.IGNORECASE).strip()
        
        portuguese_match = re.search(r'(?:Portuguese|Português):\s*(.*?)(?=$|English:|Inglês:)', cleaned, re.IGNORECASE | re.DOTALL)
        english_match = re.search(r'(?:English|Inglês):\s*(.*?)(?=$|Portuguese:|Português:)', cleaned, re.IGNORECASE | re.DOTALL)
        
        if portuguese_match and portuguese_match.group(1).strip():
            return portuguese_match.group(1).strip()
        if english_match and english_match.group(1).strip():
            return english_match.group(1).strip()
        
        lines = cleaned.strip().split('\n')
        filtered_lines = []
        
        skip_markers = ['translate', 'translation:', 'tradução:', 'input:', 'output:', 'source:', 'target:', 
                       'original text:', 'translated text:', 'instructions:', 'note:', 'tradução',
                       'translation', 'portuguese:', 'english:']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if any(marker in line.lower() for marker in skip_markers):
                continue
            
            filtered_lines.append(line)
        
        if filtered_lines:
            return ' '.join(filtered_lines)
        
        return cleaned
    
    def _validate_output(self, output: str, original_text: str, 
                         source_language: str, target_language: str) -> bool:
        if not output or len(output.split()) < 2:
            self.logger.warning("Translation too short or empty")
            return False
        
        if "translation failed" in output.lower() or "error" in output.lower():
            self.logger.warning("Translation contains explicit failure message")
            return False
            
        if len(output.split()) > len(original_text.split()) * 3:
            self.logger.warning(f"Translation suspiciously long: {len(output.split())} words vs {len(original_text.split())} words in original")
            return False
            
        output_lang, confidence = LanguageService.detect_language(output)
        self.logger.info(f"Detected output language: {output_lang} (confidence: {confidence:.2f})")
        
        if output_lang == target_language and confidence > 0.6:
            return True
            
        if output_lang == source_language and confidence > 0.6:
            if source_language == "Portuguese" and target_language == "English":
                english_specific_words = ["the", "is", "are", "and", "of", "to", "in", "by", "with", "for", "this", "that"]
                word_count = sum(1 for word in output.lower().split() if word in english_specific_words)
                
                if word_count >= 3:
                    self.logger.info(f"Found {word_count} English-specific words, overriding language detection")
                    return True
            
            return False
        
        if output_lang == "Unknown" or confidence < 0.6:
            instruction_markers = ["translate", "translation:", "input:", "output:", 
                                  "original:", "here is", "here's", "example", "task"]
            
            if any(marker in output.lower() for marker in instruction_markers):
                self.logger.warning(f"Found instruction markers in output")
                return False
                
            original_words = set(original_text.lower().split())
            output_words = set(output.lower().split())
            overlap = len(original_words.intersection(output_words))
            
            if overlap > len(original_words) * 0.7:
                self.logger.warning(f"High word overlap with original: {overlap} of {len(original_words)} words")
                return False
        
        return True
        
    def _fallback_translation(self, text: str, source_language: str, target_language: str) -> str:
        log_prefix = "[Fallback Translation]"
        self.logger.warning(f"{log_prefix} Using rule-based fallback translation")
        
        if source_language == "Portuguese" and target_language == "English":
            self.logger.info(f"{log_prefix} Applying PT→EN pattern-based translation")
            
            sentences = re.findall(r'[^.!?]+[.!?]', text)
            short_text = ' '.join(sentences[:3]) if len(sentences) > 3 else text
            
            pt_en_dict = {
                r'\bo\b': 'the', r'\ba\b': 'the', r'\bos\b': 'the', r'\bas\b': 'the',
                r'\bum\b': 'a', r'\buma\b': 'a', r'\buns\b': 'some', r'\bumas\b': 'some',
                r'\bde\b': 'of', r'\bda\b': 'of the', r'\bdo\b': 'of the', r'\bdas\b': 'of the', r'\bdos\b': 'of the',
                r'\bem\b': 'in', r'\bna\b': 'in the', r'\bno\b': 'in the', r'\bnas\b': 'in the', r'\bnos\b': 'in the',
                r'\bpara\b': 'to', r'\bcom\b': 'with',
                r'\bé\b': 'is', r'\bsão\b': 'are', r'\bestá\b': 'is', r'\bestão\b': 'are',
                r'\btem\b': 'has', r'\btêm\b': 'have', r'\bfoi\b': 'was', r'\bforam\b': 'were',
                r'\bser\b': 'to be', r'\bestar\b': 'to be', r'\bter\b': 'to have',
                r'\bfazer\b': 'to do', r'\bfaz\b': 'does', r'\bfazem\b': 'do',
                r'\beu\b': 'I', r'\btu\b': 'you', r'\bele\b': 'he', r'\bela\b': 'she',
                r'\bnós\b': 'we', r'\bvocês\b': 'you', r'\beles\b': 'they', r'\belas\b': 'they',
                r'\binteligência artificial\b': 'artificial intelligence',
                r'\bredes neurais\b': 'neural networks',
                r'\bprocessamento\b': 'processing',
                r'\bdesenvolvimento\b': 'development',
                r'\btecnologia\b': 'technology',
                r'\btécnicos\b': 'technical',
                r'\bdados\b': 'data',
                r'\banálise\b': 'analysis',
                r'\bempresa\b': 'company',
                r'\bempresas\b': 'companies',
                r'\bsistema\b': 'system',
                r'\bsistemas\b': 'systems'
            }
            
            translated = short_text
            for pt_pattern, en_text in pt_en_dict.items():
                translated = re.sub(pt_pattern, lambda m: en_text if m.group(0).islower() else en_text.capitalize(), 
                                  translated, flags=re.IGNORECASE)
            
            adj_patterns = [
                (r'(\w+) (grande|pequeno|novo|velho|bom|mau|alto|baixo|longo|curto)', r'\2 \1'),
                (r'(\w+) (técnico|científico|importante|significativo|relevante)', r'\2 \1'),
            ]
            
            for pattern, replacement in adj_patterns:
                translated = re.sub(pattern, replacement, translated)
            
            self.logger.info(f"{log_prefix} Generated fallback translation")
            return translated
            
        elif source_language == "English" and target_language == "Portuguese":
            self.logger.info(f"{log_prefix} EN→PT fallback not yet implemented, using direct substitution")
            return None
            
        return None