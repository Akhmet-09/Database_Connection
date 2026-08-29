import random
from datetime import timedelta
from faker import Faker
from Reports.models import Member, Book, BorrowRecord, MembershipType, Genre  # Replace 'app_name' with your actual Django app name
fake = Faker()
def create_members(count=30):
    members = []
    membership_choices = [choice[0] for choice in MembershipType.choices]
    for _ in range(count):
        member = Member.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            membership_type=random.choice(membership_choices),
            is_active=fake.boolean(chance_of_getting_true=85),
            total_borrowed=random.randint(0, 15)
        )
        members.append(member)
    print(f"Inserted {count} Members.")
    return members

def create_books(count=30):
    books = []
    genre_choices = [choice[0] for choice in Genre.choices]
    
    for _ in range(count):
        total_qty = random.randint(1, 10)
        available_qty = random.randint(0, total_qty)
        
        book = Book.objects.create(
            title=fake.catch_phrase(),
            author=fake.name(),
            genre=random.choice(genre_choices),
            publication_year=random.randint(1990, 2026),
            quantity_total=total_qty,
            quantity_available=available_qty,
            rating=random.randint(1, 5),
            is_rare=fake.boolean(chance_of_getting_true=15)
        )
        books.append(book)
    print(f"Inserted {count} Books.")
    return books

def create_borrow_records(members, books, count=30):
    for _ in range(count):
        borrow_date = fake.date_between(start_date='-1y', end_date='today')
        due_date = borrow_date + timedelta(days=14)
        is_returned = fake.boolean(chance_of_getting_true=70)
        
        return_date = None
        late_fee = 0.00
        
        if is_returned:
            
            days_kept = random.randint(1, 30)
            return_date = borrow_date + timedelta(days=days_kept)
            if return_date > due_date:
                overdue_days = (return_date - due_date).days
                late_fee = round(overdue_days * 0.50, 2)

        BorrowRecord.objects.create(
            book=random.choice(books),
            member=random.choice(members),
            borrow_date=borrow_date,
            due_date=due_date,
            return_date=return_date,
            late_fee=late_fee,
            is_returned=is_returned
        )
    print(f"Inserted {count} BorrowRecords.")

def run():
    print("Populating database...")
    members = create_members(30)
    books = create_books(30)
    create_borrow_records(members, books, 30)
    print("Done! Inserted 30 records into each table.")

if __name__ == "__main__":
    run()