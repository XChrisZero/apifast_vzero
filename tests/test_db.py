from apifast_vzero.mnodels import User
from sqlalchemy import select


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='testuser', email='testuser@example.com', password='testpassword'
        )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert user == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'created_at': time,
    }
