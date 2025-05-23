"""
Script para testar a API segura implementada em exercise.py

Este script demonstra como interagir com a API segura usando Python requests.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_authentication():
    """Testa o fluxo de autenticação e recuperação do token JWT"""
    print("=== Testando autenticação ===")
    
    auth_data = {
        "username": "johndoe",
        "password": "Pass@word1"
    }
    
    response = requests.post(
        f"{BASE_URL}/token",
        data=auth_data, 
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Autenticação bem-sucedida! Token obtido.")
        return token_data["access_token"]
    else:
        print(f"❌ Falha na autenticação: {response.status_code}")
        print(response.text)
        return None

def test_user_info(token):
    """Testa o endpoint de informações do usuário"""
    print("\n=== Testando endpoint de informações do usuário ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Informações do usuário recuperadas com sucesso:")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Nome completo: {user_data['full_name']}")
    else:
        print(f"❌ Falha ao recuperar informações do usuário: {response.status_code}")
        print(response.text)

def test_send_message(token):
    """Testa o endpoint de envio de mensagem (sanitização)"""
    print("\n=== Testando endpoint de envio de mensagem ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    message_data = {
        "content": "Mensagem normal com <script>alert('XSS');</script> tentativa de XSS"
    }

    response = requests.post(
        f"{BASE_URL}/messages/send", 
        headers=headers,
        json=message_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Mensagem enviada com sucesso:")
        print(f"   ID: {result['id']}")
        print(f"   Tamanho do conteúdo: {result['content_length']}")
        print(f"   Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Falha ao enviar mensagem: {response.status_code}")
        print(response.text)

def test_search_endpoint(token):
    """Testa o endpoint de pesquisa com sanitização de parâmetros"""
    print("\n=== Testando endpoint de pesquisa ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "query": "produto'; DROP TABLE users; --", 
        "category": "products"
    }
    
    response = requests.get(
        f"{BASE_URL}/search", 
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Pesquisa realizada com sucesso:")
        print(f"   Query sanitizada: {result['query']}")
        print(f"   Categoria: {result['category']}")
        print(f"   Resultados encontrados: {result['count']}")
    else:
        print(f"❌ Falha ao realizar pesquisa: {response.status_code}")
        print(response.text)

def test_unauthenticated_access():
    """Testa o acesso a um endpoint protegido sem autenticação"""
    print("\n=== Testando acesso sem autenticação ===")
    
    response = requests.get(f"{BASE_URL}/users/me")
    
    if response.status_code == 401:
        print(f"✅ Acesso negado corretamente: {response.status_code}")
        print(f"   Mensagem: {response.json()['detail']}")
    else:
        print(f"❌ Comportamento inesperado: {response.status_code}")
        print(response.text)

def main():
    """Função principal que executa todos os testes"""
    print("🔒 Testando API Segura FastAPI 🔒\n")
    
    token = test_authentication()
    
    if token:
        test_user_info(token)
        test_send_message(token)
        test_search_endpoint(token)
    
    test_unauthenticated_access()
    
    print("\n✨ Testes concluídos ✨")

if __name__ == "__main__":
    main()
