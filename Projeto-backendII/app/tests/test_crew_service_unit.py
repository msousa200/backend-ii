"""
Testes unitários para o serviço CrewAI.
"""
import pytest
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from app.services.crew_service import CrewAIService
from app.models.pydantic_models import ProcessingType

@pytest.fixture
def crew_service():
    return CrewAIService()

@pytest.mark.asyncio
async def test_crew_translation(crew_service):
    english_text = "The quick brown fox jumps over the lazy dog."
    result = await crew_service.process_text(
        english_text, 
        ProcessingType.TRANSLATION.value,
        "Portuguese"
    )
    assert result is not None
    if hasattr(result, 'raw'):
        result_text = result.raw
    else:
        result_text = str(result)
    assert isinstance(result_text, str)
    assert len(result_text) > 10
    assert result_text.lower() != english_text.lower()

@pytest.mark.asyncio
async def test_crew_summarization(crew_service):
    long_text = """
    Artificial Intelligence (AI) is transforming industries across the globe. From healthcare to finance, 
    transportation to entertainment, AI technologies are being deployed to solve complex problems, 
    improve efficiency, and create new opportunities. Machine learning, a subset of AI, enables 
    systems to learn from data and improve performance over time without being explicitly programmed. 
    Deep learning, a specialized form of machine learning, uses neural networks with many layers to 
    analyze patterns in data. Natural Language Processing (NLP) allows machines to understand and 
    generate human language, powering applications like virtual assistants and language translation. 
    Computer Vision enables machines to interpret and make decisions based on visual data. 
    The rapid growth of AI raises important ethical and societal questions about privacy, bias, 
    unemployment, and decision-making authority. Responsible development of AI requires careful 
    consideration of these issues alongside technological advancement.
    """
    result = await crew_service.process_text(
        long_text, 
        ProcessingType.SUMMARIZATION.value
    )
    assert result is not None
    if hasattr(result, 'raw'):
        result_text = result.raw
    else:
        result_text = str(result)
    assert len(result_text) < len(long_text)
    assert len(result_text) > 20

@pytest.mark.asyncio
async def test_crew_language_detection(crew_service):
    portuguese_text = "Este é um exemplo de texto em português para testar a detecção de idioma."
    result = crew_service._detect_language(
        portuguese_text
    )
    assert result is not None
    assert result.lower() in ["portuguese", "português", "pt"]
    english_text = "This is an example of English text to test language detection."
    result = crew_service._detect_language(
        english_text
    )
    assert result is not None
    assert result.lower() in ["english", "inglês", "en"]

@pytest.mark.asyncio
async def test_crew_all_agents(crew_service):
    texto = (
        "A cidade de Faro sofreu danos generalizados no património eclesiástico, desde igrejas e conventos até o próprio Paço Episcopal. "
        "As muralhas, o castelo com as suas torres e baluartes, os quartéis, o corpo da guarda, armazéns, o edifício da alfândega, "
        "a cadeia e os conventos de S. Francisco e o de Santa Clara foram destruídos e arruinados."
    )
    traducao = await crew_service.process_text(texto, ProcessingType.TRANSLATION.value, "English")
    if hasattr(traducao, 'raw'):
        traducao_text = traducao.raw
    else:
        traducao_text = str(traducao)
    resumo = await crew_service.process_text(texto, ProcessingType.SUMMARIZATION.value)
    if hasattr(resumo, 'raw'):
        resumo_text = resumo.raw
    else:
        resumo_text = str(resumo)
    idioma = crew_service._detect_language(texto)
    assert isinstance(traducao_text, str) and len(traducao_text) > 10
    assert isinstance(resumo_text, str) and len(resumo_text) > 10
    assert idioma.lower() in ["portuguese", "português", "pt"]
