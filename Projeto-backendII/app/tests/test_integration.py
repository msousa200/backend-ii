"""
Testes de integração para validar a interação entre os componentes do sistema.
"""
import pytest
import asyncio
import os
import json
import re
from app.services.crew_service import CrewAIService
from app.models.pydantic_models import ProcessingType

PORTUGUESE_TEXT = "O novo sistema permite processamento mais rápido de grandes conjuntos de dados."

@pytest.mark.asyncio
async def test_translation_integration():
    """
    Teste de integração para o fluxo de tradução.
    
    Este teste verifica se o serviço CrewAI consegue traduzir
    um texto do português para o inglês corretamente.
    """
    crew_service = CrewAIService()
    
    result = await crew_service.process_text(
        PORTUGUESE_TEXT,
        ProcessingType.TRANSLATION.value,
        "English"
    )
    
    assert result is not None
    
    if hasattr(result, 'raw'):
        result_text = result.raw
    else:
        result_text = str(result)
    
    expected_words = ["system", "processing", "data"]
    assert any(word in result_text.lower() for word in expected_words)
    
    print(f"\nResultado da tradução:\n{result_text}")
    
    return result_text

@pytest.mark.asyncio
async def test_summarization_integration():
    """
    Teste de integração para o fluxo de sumarização.
    
    Este teste verifica se o serviço CrewAI consegue sumarizar
    um texto longo corretamente.
    """
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
    
    crew_service = CrewAIService()
    
    result = await crew_service.process_text(
        long_text,
        ProcessingType.SUMMARIZATION.value
    )
    
    assert result is not None
    
    if hasattr(result, 'raw'):
        result_text = result.raw
    else:
        result_text = str(result)
    
    
    clean_result = result_text
    
   
    expected_keywords = ["ai", "artificial intelligence", "machine learning", "technology"]
    assert any(keyword in clean_result.lower() for keyword in expected_keywords)
    
    print(f"\nResultado da sumarização:\n{clean_result}")
    
    return clean_result
