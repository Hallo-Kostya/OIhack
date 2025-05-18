from pydantic_settings import BaseSettings, SettingsConfigDict
import requests
import urllib3
import certifi
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

class Settings(BaseSettings):
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_NAME: str
    SECRET_JWT_KEY: str
    GIGACHAT_AUTH_KEY: str

    # Bitrix24 настройки
    BITRIX24_WEBHOOK_URL: str = ""
    BITRIX24_LEAD_PIPELINE_ID: str = "1"
    BITRIX24_DEAL_PIPELINE_ID: str = "1"
    BITRIX24_RESPONSIBLE_USER_ID: str = "1"

    @property
    def DATABASE_URL_PSYCOPG(self):
        return f"postgresql+psycopg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"
    
    @property
    def DATABASE_URL_ASYNCPG(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"

    @property
    def AI_API_TOKEN_JSON(self):
        if hasattr(self, '_access_token') and hasattr(self, '_expires_at'):
            if datetime.now() < self._expires_at:
                return {'access_token': self._access_token, 'expires_at': self._expires_at}

        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = 'scope=GIGACHAT_API_PERS'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': 'd9f21628-28b2-48a7-9fb4-e77ffe2eaae4',
            'Authorization': f'Basic {self.GIGACHAT_AUTH_KEY}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        token_data = response.json()
        
        # Проверяем наличие токена в ответе
        if 'access_token' not in token_data:
            print("Response data:", token_data)  # Для отладки
            raise ValueError("No access_token in response")
            
        self._access_token = token_data['access_token']
        
        # Конвертируем Unix timestamp в миллисекундах в datetime
        try:
            expires_at_timestamp = int(token_data['expires_at']) / 1000  # Конвертируем в секунды
            self._expires_at = datetime.fromtimestamp(expires_at_timestamp)
        except (ValueError, TypeError, KeyError) as e:
            print(f"Error processing expires_at: {e}")
            self._expires_at = datetime.now() + timedelta(hours=1)  # Fallback на 1 час
        
        return token_data
    
    @property
    def AI_API_TOKEN(self):
        token_data = self.AI_API_TOKEN_JSON
        return token_data['access_token']

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()