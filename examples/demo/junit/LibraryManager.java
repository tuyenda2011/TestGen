package demo.junit;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.*;

public class LibraryManager {

    public static class Book {
        private String id;
        private String title;
        private String author;
        private int copies;

        public Book(String id, String title, String author, int copies) {
            if (id == null || id.trim().isEmpty() || title == null || title.trim().isEmpty() || author == null || author.trim().isEmpty()) {
                throw new IllegalArgumentException("Invalid book details");
            }
            if (copies < 0) {
                throw new IllegalArgumentException("Copies cannot be negative");
            }
            this.id = id;
            this.title = title;
            this.author = author;
            this.copies = copies;
        }

        public String getId() { return id; }
        public String getTitle() { return title; }
        public String getAuthor() { return author; }
        public int getCopies() { return copies; }
        public void setCopies(int copies) { this.copies = copies; }
    }

    public static class Loan {
        private String bookId;
        private LocalDate dueDate;

        public Loan(String bookId, LocalDate dueDate) {
            this.bookId = bookId;
            this.dueDate = dueDate;
        }

        public String getBookId() { return bookId; }
        public LocalDate getDueDate() { return dueDate; }
    }

    private final Map<String, Book> books = new HashMap<>();
    private final Map<String, List<Loan>> rented = new HashMap<>();

    public void addBook(Book book) {
        if (book == null) {
            throw new IllegalArgumentException("Book cannot be null");
        }
        if (books.containsKey(book.getId())) {
            throw new IllegalStateException("Book already exists");
        }
        books.put(book.getId(), book);
    }

    public boolean borrowBook(String userId, String bookId, int daysToReturn) {
        if (userId == null || userId.trim().isEmpty() || bookId == null || bookId.trim().isEmpty()) {
            throw new IllegalArgumentException("User ID and Book ID are required");
        }
        if (daysToReturn <= 0 || daysToReturn > 30) {
            throw new IllegalArgumentException("Borrow duration must be between 1 and 30 days");
        }

        Book book = books.get(bookId);
        if (book == null) {
            throw new NoSuchElementException("Book not found in library");
        }
        if (book.getCopies() <= 0) {
            throw new IllegalStateException("Book is out of stock");
        }

        List<Loan> userLoans = rented.computeIfAbsent(userId, k -> new ArrayList<>());
        if (userLoans.size() >= 3) {
            throw new IllegalStateException("User has reached borrowing limit of 3 books");
        }

        for (Loan loan : userLoans) {
            if (loan.getBookId().equals(bookId)) {
                throw new IllegalStateException("User has already borrowed this book");
            }
        }

        book.setCopies(book.getCopies() - 1);
        LocalDate dueDate = LocalDate.now().plusDays(daysToReturn);
        userLoans.add(new Loan(bookId, dueDate));
        return true;
    }

    public double returnBook(String userId, String bookId, LocalDate actualReturnDate) {
        if (userId == null || bookId == null || actualReturnDate == null) {
            throw new IllegalArgumentException("Arguments cannot be null");
        }

        List<Loan> userLoans = rented.get(userId);
        if (userLoans == null) {
            throw new NoSuchElementException("No loans found for user");
        }

        Loan userLoan = null;
        for (Loan loan : userLoans) {
            if (loan.getBookId().equals(bookId)) {
                userLoan = loan;
                break;
            }
        }

        if (userLoan == null) {
            throw new NoSuchElementException("Book was not borrowed by this user");
        }

        Book book = books.get(bookId);
        if (book != null) {
            book.setCopies(book.getCopies() + 1);
        }

        userLoans.remove(userLoan);
        if (userLoans.isEmpty()) {
            rented.remove(userId);
        }

        double fine = 0.0;
        if (actualReturnDate.isAfter(userLoan.getDueDate())) {
            long diffDays = ChronoUnit.DAYS.between(userLoan.getDueDate(), actualReturnDate);
            fine = diffDays * 0.5;
        }
        return fine;
    }
}
