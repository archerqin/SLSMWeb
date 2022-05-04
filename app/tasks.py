from manage import my_celery
from app import db
from app.base.models import Case

@my_celery.task()
def test(msg):
    case = Case(type_id=1,text=msg,detail="test_detail")
    db.session.add(case)
    db.session.commit()
    return "success"
