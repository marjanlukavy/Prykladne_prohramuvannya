from crud import Session
from models import Student

s = Session()

books = s.query(Student).all()

for book in books:
    student_rating = input(f"Rating for '{book.first_name}': +")
    book.student_rating = student_rating
    s.add(book)

s.commit()
s.close()