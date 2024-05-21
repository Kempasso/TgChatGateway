import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
hostname_db = os.environ.get('HOSTNAME_DB')
postgres_db = os.environ.get('POSTGRES_DB')
postgres_port = os.environ.get('POSTGRES_PORT')
telegram_bot_key = os.environ.get('TELEGRAM_BOT_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')
hostname = os.environ.get('HOSTNAME')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_url = os.environ.get('REDIS_URL')
database_url = os.environ.get('DATABASE_URL')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
