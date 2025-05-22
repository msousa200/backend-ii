"""
Testes para o serviço de linguagem.
"""
import pytest
from app.services.language_service import LanguageService


def test_clean_translation_output():
    """Test cleaning translation output."""

    raw_output = """
    Here is the Portuguese to English translation:
    
    Original: O novo sistema permite processamento mais rápido de dados.
    Translation: The new system allows faster data processing.
    
    I've maintained the meaning while ensuring natural English phrasing.
    """
    original_text = "O novo sistema permite processamento mais rápido de dados."
    cleaned = LanguageService.clean_translation_output(raw_output, original_text)
    assert cleaned is not None
    assert isinstance(cleaned, str)
    assert "The new system allows faster data processing" in cleaned


def test_validate_translation():
    """Test validating translation quality."""
    original_text = "O sistema de processamento de dados foi atualizado."
    good_translation = "The data processing system has been updated."
    bad_translation = "System updated."
    cleaned_good, is_valid_good = LanguageService.validate_translation(good_translation, original_text)
    assert is_valid_good is True
    
    cleaned_bad, is_valid_bad = LanguageService.validate_translation(bad_translation, original_text)
   
    
    assert cleaned_good is not None
    assert isinstance(cleaned_good, str)
    assert cleaned_bad is not None
    assert isinstance(cleaned_bad, str)


def test_detect_language():
    """Test language detection."""

    pt_text = "Este é um exemplo de texto em português."
    en_text = "This is an example of English text."
    pt_lang, pt_confidence = LanguageService.detect_language(pt_text)
    en_lang, en_confidence = LanguageService.detect_language(en_text)
    assert pt_lang in ["Portuguese", "portuguese", "pt"]
    assert en_lang in ["English", "english", "en"]
    assert 0 <= pt_confidence <= 1
    assert 0 <= en_confidence <= 1
