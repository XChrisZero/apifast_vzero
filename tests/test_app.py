from http import HTTPStatus


def test_read_root_deve_retornar_Hello_world(client):

    response = client.get('/')

    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user_deve_criar_usuario(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example.com',
    }


def test_read_users_deve_retornar_lista_de_usuarios(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'testuser', 'email': 'testuser@example.com'}]
    }


def test_update_user_deve_atualizar_usuario(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'password': 'updatedpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'updateduser',
        'email': 'updateduser@example.com',
    }


def test_delete_user_deve_deletar_usuario(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.json() == {
        'id': 1,
        'username': 'updateduser',
        'email': 'updateduser@example.com',
    }


def test_update_user_nao_encontrado(client):
    # Tenta atualizar o usuário na posição 999 (que não existe no seu database)
    response = client.put(
        '/users/999',
        json={'username': 'testuser', 'email': 'test@test.com', 'password': '123'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'não achei'}


def test_update_user_id_invalido(client):
    # Tenta usar ID 0
    response = client.put(
        '/users/0',
        json={'username': 'a', 'email': 'a@a.com', 'password': '1'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_nao_encontrado(client):
    # Tenta deletar um usuário que está além do tamanho da lista
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Não achei'}


def test_delete_user_id_negativo(client):
    # Tenta deletar um ID negativo
    response = client.delete('/users/-1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_OK(client):
    # 1. Preparação: Insere um usuário para ele ocupar o ID 1
    client.post(
        '/users/',
        json={'username': 'chris', 'email': 'chris@test.com', 'password': '123'},
    )

    # 2. Ação: Busca o usuário de ID 1
    response = client.get('/users/1')

    # 3. Verificação
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'chris'
    assert response.json()['id'] == 1


def test_get_user_not_found(client):
    # O banco está vazio (o client.clear() da fixture garantiu isso)
    # Então qualquer ID deve retornar 404
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_user_invalid_id(client):
    # Testando ID zero ou negativo
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
