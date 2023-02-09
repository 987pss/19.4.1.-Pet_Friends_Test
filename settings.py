import os
import pathlib
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# URL-адреса
base_url = 'https://petfriends.skillfactory.ru'
get_api_key_url = '/api/key'
get_list_of_pets_url = '/api/pets'
add_new_pet_url = '/api/pets'
update_pet_url = f'/api/pets/'  # /api/pets/{pet_id}
delete_pet_url = f'/api/pets/'  # /api/pets/{pet_id}

# Данные для авторизации
email = os.getenv('email')
password = os.getenv('password')

# Данные для добавления нового питомца
name = 'Мася'
animal_type = 'кошка'
age = '12'
pet_photo_path = str(Path('..', 'app', 'images', 'Masya.jpg'))

# Данные для обновления информации о добавленном питомце
new_name = 'Вася'
new_animal_type = 'кот'
new_age = '7'
