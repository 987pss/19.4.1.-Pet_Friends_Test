import pytest
import pathlib
from pathlib import Path
from app.api import PetFriends
from app.settings import email, password, name, animal_type, age, pet_photo_path, new_name, new_animal_type, new_age

pf = PetFriends()


def test_get_api_key_for_valid_user(email=email,
                                    password=password):
    """Позитивное тестирование получения ключа API:
    - код ответа HTTP
    - получен ключ API"""

    response_status_code, api_key, _ = pf.get_api_key(email, password)

    assert response_status_code == 200
    assert api_key


def test_add_new_pet_for_valid_data(name=name,
                                    animal_type=animal_type,
                                    age=age):
    """Позитивное тестирование добавления нового питомца:
    - код ответа HTTP = 200
    - получено id добавленного питомца
    - имя добавленного питомца совпадает с именем, переданным при добавлении питомца
    - тип питомца совпадает с типом, переданным при добавлении питомца
    - возраст питомца совпадает с возрастом, переданным при добавлении питомца
    - у добавленного питомца есть фото"""

    auth_key = pf.get_api_key(email, password)[1]
    response_status_code, id_new_pet, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo_path)

    assert response_status_code == 200
    assert id_new_pet
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo']


def test_update_pet_successful(new_name=new_name,
                               new_animal_type=new_animal_type,
                               new_age=new_age):
    """Позитивное тестирование обновления информации о добавленном питомце:
    - код ответа HTTP = 200
    - имя питомца было изменено и совпадает с именем, переданным при обновлении информации о добавленном питомце
    - тип питомца был изменён и совпадает с типом, переданным при обновлении информации о добавленном питомце
    - возраст питомца был изменён и совпадает с возрастом, переданным при обновлении информации о добавленном питомце"""

    auth_key = pf.get_api_key(email, password)[1]
    pet_photo_path = str(Path('..', 'app', 'images', 'Masya.jpg'))
    pet_id = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo_path)[1]
    response_status_code, result = pf.update_pet(auth_key, pet_id, new_name, new_animal_type, new_age)

    assert response_status_code == 200
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age


def test_delete_pet_successful():
    """Позитивное тестирование удаления добавленного питомца:
    - код ответа HTTP = 200
    - id удалённого питомца нет в полученном после удаления списке питомцев"""

    auth_key = pf.get_api_key(email, password)[1]
    pet_photo_path = str(Path('..', 'app', 'images', 'Masya.jpg'))
    pet_id = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo_path)[1]
    response_status_code, result = pf.delete_pet(auth_key, pet_id)
    filter = 'my_pets'
    result_text = pf.get_list_of_pets(auth_key, filter)[2]

    assert response_status_code == 200
    assert pet_id not in result_text


def test_add_update_delete_pet_scenario():
    """Сценарное позитивное тестирование: добавление нового питомца, обновление информации о добавленном питомце,
    удаление добавленного питомца"""

    """Позитивное тестирование добавления нового питомца:
    - код ответа HTTP = 200
    - получено id добавленного питомца
    - имя добавленного питомца совпадает с именем, переданным при добавлении питомца
    - тип питомца совпадает с типом, переданным при добавлении питомца
    - возраст питомца совпадает с возрастом, переданным при добавлении питомца
    - у добавленного питомца есть фото"""
    auth_key = pf.get_api_key(email, password)[1]
    response_status_code, id_new_pet, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo_path)

    assert response_status_code == 200
    assert id_new_pet
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo']

    """Позитивное тестирование обновления информации о добавленном питомце:
    - код ответа HTTP = 200
    - имя питомца было изменено и совпадает с именем, переданным при обновлении информации о добавленном питомце
    - тип питомца был изменён и совпадает с типом, переданным при обновлении информации о добавленном питомце
    - возраст питомца был изменён и совпадает с возрастом, переданным при обновлении информации о добавленном питомце"""
    response_status_code, result = pf.update_pet(auth_key, id_new_pet, new_name, new_animal_type, new_age)

    assert response_status_code == 200
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age

    """Позитивное тестирование удаления добавленного питомца:
    - код ответа HTTP = 200
    - id удалённого питомца нет в полученном после удаления списке питомцев"""
    response_status_code, result = pf.delete_pet(auth_key, id_new_pet)
    filter_ = 'my_pets'
    result_text = pf.get_list_of_pets(auth_key, filter_)[2]

    assert response_status_code == 200
    assert id_new_pet not in result_text
    