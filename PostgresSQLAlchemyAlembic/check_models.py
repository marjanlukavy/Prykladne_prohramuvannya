from datetime import datetime

from crud import s
from models import Admin, Student

ad1 = Admin(
        first_name='Admin',
        last_name='Admin',
        right=1,
)
ad2 = Admin(
        first_name='Admin',
        last_name='Admin',
        right=1,
)
st1 = Student(
        first_name='Marian',
        last_name='Lukavyi',
        student_rating=88,
        right=0,
        published=datetime(2016, 11, 18),
        students=ad1
)

st2 = Student(
        first_name='John',
        last_name='Hoofoff',
        student_rating=44,
        right=0,
        published=datetime(2016, 11, 18),
        students=ad1
)



st4 = Student(
        first_name='adasdasd',
        last_name='dasdasd',
        student_rating=22,
        right=0,
        published=datetime(2016, 11, 18),
        students=ad2
)


s.add(ad1)
s.add(st1)
s.add(st2)
s.add(st4)

s.commit()
s.close()