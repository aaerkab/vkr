"""Загрузка первичных данных (пример).

Запуск:
    python -m backend.seed_data

Использует create_app() и конфиг из environment.
"""

from backend.database import db
from backend.models import Criteria
from backend.app import create_app

def seed_criteria():
    app = create_app()
    with app.app_context():
        if Criteria.query.first() is not None:
            print("Критерии уже существуют")
            return
        
        criteria_list = [
            Criteria(criteria_id=1, criteria_name='Физическая безопасность', 
                    criteria_category='Физическая защита', max_score=100.0, weight=1.0,
                    description='Оценка физической защиты объекта'),
            Criteria(criteria_id=2, criteria_name='Техническая безопасность',
                    criteria_category='Техническая защита', max_score=100.0, weight=1.0,
                    description='Оценка технических средств защиты'),
            Criteria(criteria_id=3, criteria_name='Организационная безопасность',
                    criteria_category='Организационные меры', max_score=100.0, weight=1.0,
                    description='Оценка организационных мер безопасности'),
        ]
        
        db.session.add_all(criteria_list)
        db.session.commit()
        print(f"Добавлено {len(criteria_list)} критериев")

if __name__ == '__main__':
    seed_criteria()
