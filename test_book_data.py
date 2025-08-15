from app.models.book import Book

print("Testing Book.get_all_books()...")
books = Book.get_all_books()

print(f"Total books returned: {len(books)}")
print("\nBook statuses found:")

statuses = {}
for book in books:
    status = book.get('status', 'Unknown')
    if status in statuses:
        statuses[status] += 1
    else:
        statuses[status] = 1
    print(f"- {book.get('title', 'Unknown')}: {status}")

print(f"\nStatus summary: {statuses}")
