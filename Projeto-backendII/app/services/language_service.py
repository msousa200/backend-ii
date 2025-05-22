"""
Language detection and text processing utilities for the CrewAI service
This module provides more advanced language detection and text processing
functionality to improve translation quality and reliability.
"""
import re
from typing import Tuple, Dict, Any, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LanguageService:
    
    PORTUGUESE_INDICATORS = [
        'ção', 'ções', 'ário', 'ária', 'é', 'á', 'ã', 'ê', 'ó', 'ô',
        ' da ', ' do ', ' das ', ' dos ', ' na ', ' no ', ' nas ', ' nos ',
        ' um ', ' uma ', ' uns ', ' umas ', ' e ', ' ou ', ' que ', ' de ',
        'não', 'sim', 'muito', 'todos', 'como', 'está', 'são', 'está',
        'obrigado', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'por favor',
        'então', 'assim', 'porque', 'para', 'mais', 'menos', 'também'
    ]
    
    ENGLISH_INDICATORS = [
        ' the ', ' is ', ' are ', ' were ', ' was ', ' be ', ' been ',
        ' a ', ' an ', ' this ', ' these ', ' those ', ' and ', ' or ',
        ' of ', ' to ', ' in ', ' on ', ' at ', ' from ', ' with ',
        'not', 'yes', 'very', 'all', 'how', 'what', 'when', 'where',
        'thank', 'hello', 'good morning', 'good afternoon', 'good evening',
        'please', 'so', 'because', 'for', 'more', 'less', 'also'
    ]
    
    PORTUGUESE_CHARS = "çãõéáêóôâúíà"
    ENGLISH_SPECIFIC_CHARS = "wyx"
    
    @staticmethod
    def detect_language(text: str) -> Tuple[str, float]:
        if not text or not isinstance(text, str) or len(text) < 5:
            logger.warning(f"Invalid or too short text for language detection: {text}")
            return ('Unknown', 0.0)
        
        text_lower = ' ' + text.lower() + ' '
        pt_score = 0
        en_score = 0
        text_length = len(text_lower)
        
        for ind in LanguageService.PORTUGUESE_INDICATORS:
            pt_score += text_lower.count(ind) * len(ind)
        
        for ind in LanguageService.ENGLISH_INDICATORS:
            en_score += text_lower.count(ind) * len(ind)
        
        for char in LanguageService.PORTUGUESE_CHARS:
            pt_score += text_lower.count(char) * 4
            
        for char in LanguageService.ENGLISH_SPECIFIC_CHARS:
            en_score += text_lower.count(char) * 2
        
        pt_score_normalized = pt_score / max(1, text_length)
        en_score_normalized = en_score / max(1, text_length)
        total_score = pt_score_normalized + en_score_normalized
        
        if total_score == 0:
            logger.warning(f"Could not determine language scores for text: {text[:100]}...")
            return ('Unknown', 0.0)
        
        pt_confidence = pt_score_normalized / total_score
        en_confidence = en_score_normalized / total_score
        
        if pt_confidence > en_confidence:
            return ('Portuguese', pt_confidence)
        else:
            return ('English', en_confidence)
    
    @staticmethod
    def clean_translation_output(processed_text: str, original_text: str) -> str:
        logger.info(f"Cleaning translation output, length: {len(processed_text)}")
        
        if not processed_text:
            return "Translation error: Empty response"
            
        output_markers = [
            r'Output:\s*(.*?)(?=$|\n\n|Example|\[)',
            r'Output \(ONLY.*?\):\s*(.*?)(?=$|\n\n|Example|\[)', 
            r'Translation:\s*(.*?)(?=$|\n\n|Example|\[)',
            r'Tradução:\s*(.*?)(?=$|\n\n|Example|\[)',
            r'(?:Input:.*?\n)(?:Output:)?\s*(.*?)(?=$|\n\nInput:|\n\nExample|\[)',
        ]
        
        for marker in output_markers:
            matches = re.search(marker, processed_text, re.DOTALL | re.IGNORECASE)
            if matches and matches.group(1) and len(matches.group(1).strip().split()) >= 1:
                logger.info(f"Found translation after output marker: {marker[:30]}...")
                return matches.group(1).strip()
        
        quote_matches = re.findall(r'[""\"\'](.*?)[\"""\'\"]', processed_text, re.DOTALL)
        if quote_matches and len(quote_matches[0].split()) >= 1:
            logger.info("Found translation in quotes")
            return quote_matches[0].strip()
            
        patterns = [
            r"(?:Translation:|Translated text:|Result:|Translation result:)(.*?)(?:$|Original:|Source:)",
            r"(?:Here is the translation:|Here's the translation:)(.*?)(?:$|Original:)",
            r"(?:^|\n)((?!.*?:).*?)(?=$|\n\n)",
            r"(?:^|\n\n)(?!Example|Input|Output|Translation|###)(.*?)(?=$|\n\n)",
        ]
        
        for pattern in patterns:
            matches = re.search(pattern, processed_text, re.DOTALL | re.IGNORECASE)
            if matches and len(matches.group(1).strip().split()) >= 1:
                logger.info(f"Found translation using pattern: {pattern[:20]}...")
                return matches.group(1).strip()
        
        lines = processed_text.split('\n')
        content_lines = []
        
        instruction_patterns = [
            'instructions:', 'task:', 'translate', 'translation task', 'expected output', 
            'criteria:', 'final answer', 'user:', 'system:', 'assistant:', 'prompt:',
            'format:', 'provides:', 'given:', 'requirement:', 'language:', 'detected:',
            'step ', 'guideline', 'please', 'note:', 'original text', 'following text',
            'respond', 'input:', 'output:', 'response', 'commentary', 'explanations',
            'example', 'attempt', 'important', '###', 'translate the', 'translation:', 
            'translated:', 'source:', 'target:'
        ]
        
        for line in lines:
            line_lower = line.lower().strip()
            if not line_lower:
                continue
            if any(pattern in line_lower for pattern in instruction_patterns):
                continue
            if re.match(r'^[\s*#\-_=]{1,5}$', line_lower):
                continue
            if len(line_lower.split()) < 2 and len(line_lower) < 10:
                continue
            content_lines.append(line.strip())
        
        if content_lines:
            logger.info("Used line filtering to clean translation")
            cleaned_text = ' '.join(content_lines)
            return cleaned_text
        
        prompt_elements = ['Input:', 'Output:', 'Example', '###', 'Now translate']
        last_element_pos = -1
        
        for element in prompt_elements:
            pos = processed_text.rfind(element)
            if pos > last_element_pos:
                last_element_pos = pos
        
        if last_element_pos >= 0:
            line_end = processed_text.find('\n', last_element_pos)
            if line_end >= 0:
                remaining_text = processed_text[line_end + 1:].strip()
                if remaining_text and len(remaining_text.split()) >= 2:
                    logger.info("Extracted text after the last prompt element")
                    return remaining_text
        
        cleaned = re.sub(r'^(Here is |Translation: |Translated text: |Result: )', '', processed_text.strip())
        logger.warning("Using simplified cleaning approach - returning entire response with minimal cleaning")
        return cleaned
    
    @staticmethod
    def validate_translation(processed_text: str, original_text: str) -> Tuple[str, bool]:
        if not processed_text or len(processed_text) < 3:
            logger.warning("Translation validation failed: Translation too short or empty")
            return "Translation error: Empty or too short response", False
            
        def clean_text_for_comparison(text):
            return re.sub(r'[^\w\s]', '', text.lower())
            
        original_clean = clean_text_for_comparison(original_text)
        processed_clean = clean_text_for_comparison(processed_text)
        
        original_words = set(original_clean.split())
        processed_words = set(processed_clean.split())
        
        original_word_list = original_clean.split()
        processed_word_list = processed_clean.split()
        
        if len(original_words) < 4:
            if len(processed_words) > 0:
                logger.info("Original text very short, accepting any non-empty translation")
                return processed_text, True
        
        overlap_ratio = len(original_words.intersection(processed_words)) / max(len(original_words), 1)
        length_ratio = len(processed_words) / max(len(original_words), 1)
        
        instructional_markers = [
            'translate', 'translation', 'text', 'format', 'expected', 'criteria', 
            'final answer', 'response', 'maintain', 'original', 'input', 'output',
            'example', 'following', 'user', 'assistant', 'system', 'prompt'
        ]
        instruction_count = sum(1 for word in processed_word_list if word.lower() in instructional_markers)
        instruction_ratio = instruction_count / max(len(processed_word_list), 1)
        
        original_lang, original_confidence = LanguageService.detect_language(original_text)
        processed_lang, processed_confidence = LanguageService.detect_language(processed_text)
        
        language_detection_reliable = (original_confidence > 0.6 and processed_confidence > 0.6)
        
        logger.info(f"Translation validation: overlap={overlap_ratio:.2f}, length={length_ratio:.2f}, " +
                   f"instruction_ratio={instruction_ratio:.2f}, original={original_lang}({original_confidence:.2f}), " +
                   f"result={processed_lang}({processed_confidence:.2f})")
        
        if not language_detection_reliable and instruction_ratio < 0.3:
            logger.info("Language detection not reliable, accepting translation based on low instruction ratio")
            return processed_text, True
        
        failed = False
        failure_reason = ""
        
        if overlap_ratio > 0.8 and 0.9 < length_ratio < 1.1:
            failed = True
            failure_reason = f"High overlap with original text ({overlap_ratio:.2f})"
        
        if (original_lang == processed_lang and original_lang != "Unknown" and overlap_ratio > 0.6):
            failed = True
            failure_reason = "Same language and high overlap"
        
        if instruction_ratio > 0.3:
            failed = True
            failure_reason = f"Too much instructional content ({instruction_ratio:.2f})"
        
        if failed:
            logger.warning(f"Translation validation failed: {failure_reason}")
            return f"Translation error: {failure_reason}", False
        
        return processed_text, True
