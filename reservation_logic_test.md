Test Scenarios for Book Reservation Logic:

1. User with 0 reservations:
   - Can reserve up to 3 books
   - Should show "0 / 3 books reserved"
   - Should show "You can reserve 3 more book(s)"

2. User with 1 reservation:
   - Can reserve up to 2 more books
   - Should show "1 / 3 books reserved"
   - Should show "You can reserve 2 more book(s)"

3. User with 2 reservations:
   - Can reserve up to 1 more book
   - Should show "2 / 3 books reserved"
   - Should show "You can reserve 1 more book(s)"

4. User with 3 reservations:
   - Cannot reserve any more books
   - Should show "3 / 3 books reserved"
   - Should show "You have reached the maximum reservation limit"
   - Should hide reservation form and show message

5. Attempt to reserve more than remaining slots:
   - Should show error message with remaining count
   - Should not create any reservations

This fixes the issue where users could reserve 3 books at a time regardless of existing reservations.
