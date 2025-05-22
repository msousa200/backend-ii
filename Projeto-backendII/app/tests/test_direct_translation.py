"""
Testes para o serviço de tradução direta.
"""
import pytest
import os
from app.services.direct_translation_service import DirectTranslationService

@pytest.fixture
def translation_service():
    return DirectTranslationService()

def test_direct_translation_pt_to_en(translation_service):
    pt_text = "O novo sistema de processamento de dados foi implementado com sucesso."
    en_text = translation_service.translate(pt_text, "English")
    assert en_text is not None
    assert isinstance(en_text, str)
    assert len(en_text) > 10
    assert en_text.lower() != pt_text.lower()
    print(f"\nResultado da tradução PT→EN:\n{en_text}")
    return en_text

def test_direct_translation_en_to_pt(translation_service):
    en_text = "The new data processing system was successfully implemented."
    pt_text = translation_service.translate(en_text, "Portuguese")
    assert pt_text is not None
    assert isinstance(pt_text, str)
    assert len(pt_text) > 10
    assert pt_text.lower() != en_text.lower()
    print(f"\nResultado da tradução EN→PT:\n{pt_text}")
    return pt_text

def test_language_detection(translation_service):
    pt_text = "Este é um exemplo de texto em português para teste."
    en_text = "This is an example of English text for testing."
    from app.services.language_service import LanguageService
    pt_lang, pt_confidence = LanguageService.detect_language(pt_text)
    en_lang, en_confidence = LanguageService.detect_language(en_text)
    assert pt_lang.lower() in ["portuguese", "pt", "português"]
    assert en_lang.lower() in ["english", "en", "inglês"]

