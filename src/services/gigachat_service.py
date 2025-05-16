from typing import List, Dict, Any
import json
from gigachat import GigaChat
from config import settings

class GigaChatService:
    def __init__(self):
        self.client = GigaChat(credentials=settings.GIGACHAT_API_KEY, verify_ssl_certs=False)

    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """Анализирует запрос пользователя и определяет тип поиска"""
        prompt = f"""
        Проанализируй следующий запрос и определи, какую информацию ищет пользователь.
        Верни JSON с полями:
        - search_type: "events", "users", "tasks" или "all"
        - search_criteria: список ключевых слов для поиска
        - time_period: "past", "future", "all" или null
        - location: строка с местоположением или null
        
        Запрос: {query}
        """
        
        response = self.client.chat(prompt)
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {
                "search_type": "all",
                "search_criteria": query.split(),
                "time_period": None,
                "location": None
            }

    async def generate_response(self, search_results: List[Dict[str, Any]], original_query: str) -> str:
        """Генерирует естественный ответ на основе результатов поиска"""
        results_str = json.dumps(search_results, ensure_ascii=False)
        prompt = f"""
        На основе следующих результатов поиска сгенерируй естественный ответ на запрос пользователя.
        Используй только информацию из результатов поиска.
        
        Запрос пользователя: {original_query}
        
        Результаты поиска: {results_str}
        """
        
        response = self.client.chat(prompt)
        return response.choices[0].message.content 