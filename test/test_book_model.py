from app.models.book import Book

print("Testing Book model methods...")
print("="*50)

stats = Book.get_library_stats()
print(f"Library Statistics:")
print(f"  Total Books: {stats['total_books']}")
print(f"  Available Books: {stats['available_books']}")
print(f"  Issued Books: {stats['issued_books']}")
print(f"  Overdue Books: {stats['overdue_books']}")
print(f"  Reservations: {stats['reservations']}")
print(f"  Availability Percentage: {stats['availability_percentage']}%")
print()

activities = Book.get_recent_activities()
print(f"Recent Activities ({len(activities)} items):")
for i, activity in enumerate(activities, 1):
    print(f"  {i}. {activity['activity']} - {activity['time_ago']}")

print("\nBook model methods working correctly!")
