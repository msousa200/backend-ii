"""
Script para testar agentes de tradução, sumarização e detecção de idioma via terminal.
Uso: python test_agents_terminal.py
"""
from app.services.language_service import LanguageService
from app.services.direct_translation_service import DirectTranslationService
from app.services.direct_summarization_service import DirectSummarizationService

import sys

if __name__ == "__main__":
    print("\n=== Teste de agentes (terminal) ===\n")

    if len(sys.argv) > 1:
        texto = sys.argv[1]
    else:
        texto = (
            "A cidade de Faro sofreu danos generalizados no património eclesiástico, desde igrejas e conventos até o próprio Paço Episcopal. "
            "As muralhas, o castelo com as suas torres e baluartes, os quartéis, o corpo da guarda, armazéns, o edifício da alfândega, "
            "a cadeia e os conventos de S. Francisco e o de Santa Clara foram destruídos e arruinados."
        )

    translator = DirectTranslationService()
    traducao = translator.translate(texto, target_language="English")
    print(f"[TRADUÇÃO PT→EN]\n{traducao}\n")

    summarizer = DirectSummarizationService()
    resumo = summarizer.summarize(texto)
    print(f"[RESUMO]\n{resumo}\n")

    lang, conf = LanguageService.detect_language(texto)
    print(f"[IDIOMA DETECTADO]\n{lang} (confiança: {conf:.2f})\n")

    print("=== Fim dos testes ===\n")
