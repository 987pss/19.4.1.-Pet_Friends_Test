import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from app.settings import base_url, get_api_key_url, get_list_of_pets_url, add_new_pet_url, update_pet_url, \
    delete_pet_url


class PetFriends:
    """Коллекция API-запросов к вэб-приложению PetFriends"""

    def get_api_key(self,
                    email: str,
                    password: str) -> json:
        """Метод отправляет GET-запрос для получения ключа API и возвращает:
        - код ответа HTTP
        - ключ API
        - результат ответа в формате JSON или TEXT"""

        headers_get_api_key = {
            'email': email,
            'password': password,
        }

        r = requests.get(base_url + get_api_key_url, headers=headers_get_api_key)
        response_status_code = r.status_code
        try:
            result = r.json()
            api_key = result['key']
        except json.decoder.JSONDecodeError:
            result = r.text
            api_key = result.split(':')[1].split('"')[1]
        finally:
            return response_status_code, api_key, result

    def get_list_of_pets(self, auth_key: str,
                         filter_: str = '') -> json:
        """Метод отправляет GET-запрос для получения списка питомцев и возвращает:
        - код ответа HTTP
        - результат ответа в формате JSON или TEXT
        - результат ответа в формате TEXT"""

        headers_get_list_of_pets = {'auth_key': auth_key}
        params_get_list_of_pets = {'filter': filter_}

        r = requests.get(base_url + get_list_of_pets_url, headers=headers_get_list_of_pets,
                         params=params_get_list_of_pets)
        response_status_code = r.status_code
        result_text = r.text
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        finally:
            return response_status_code, result, result_text

    def add_new_pet(self,
                    auth_key: str,
                    name: str,
                    animal_type: str,
                    age: str,
                    pet_photo_path: str) -> json:
        """Метод отправляет GET-запрос для добавления нового питомца и возвращает:
        - код ответа HTTP
        - id добавленного питомца
        - результат ответа в формате JSON или TEXT"""

        data_new_pet = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo_path, open(pet_photo_path, 'rb'), 'image/jpeg'),
            }
        )
        headers_add_new_pet = {
            'auth_key': auth_key,
            'Content-Type': data_new_pet.content_type,
        }

        r = requests.post(base_url + add_new_pet_url, headers=headers_add_new_pet, data=data_new_pet)
        response_status_code = r.status_code
        try:
            result = r.json()
            id_new_pet = result['id']
        except json.decoder.JSONDecodeError:
            result = r.text
            id_new_pet = result.split(',')[4].split(':')[1].split('"')[1]
        finally:
            return response_status_code, id_new_pet, result

    def update_pet(self,
                   auth_key: str,
                   pet_id: str,
                   new_name: str,
                   new_animal_type: str,
                   new_age: str) -> json:
        """Метод отправляет GET-запрос для обновление информации о добавленном питомце и возвращает:
        - код ответа HTTP
        - результат ответа в формате JSON или TEXT"""

        headers_update_pet = {'auth_key': auth_key}
        params_update_pet = {'pet_id': pet_id}
        data_update_pet = {
            'name': new_name,
            'animal_type': new_animal_type,
            'age': new_age,
        }

        r = requests.put(base_url + update_pet_url + pet_id, headers=headers_update_pet, params=params_update_pet,
                         data=data_update_pet)
        response_status_code = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        finally:
            return response_status_code, result

    def delete_pet(self,
                   auth_key: str,
                   pet_id: str) -> json:
        """Метод отправляет GET-запрос для удаления добавленного питомца и возвращает:
        - код ответа HTTP
        - результат ответа в формате JSON или TEXT"""

        headers_update_pet = {'auth_key': auth_key}
        params_update_pet = {'pet_id': pet_id}

        r = requests.delete(base_url + delete_pet_url + pet_id, headers=headers_update_pet, params=params_update_pet)
        response_status_code = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        finally:
            return response_status_code, result
