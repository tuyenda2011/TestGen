class Book {
  constructor(id, title, author, copies) {
    if (!id || !title || !author) {
      throw new Error("Invalid book details");
    }
    if (copies < 0) {
      throw new Error("Copies cannot be negative");
    }
    this.id = id;
    this.title = title;
    this.author = author;
    this.copies = copies;
  }
}

class LibraryManager {
  constructor() {
    this.books = new Map();
    this.rented = new Map(); // userId -> list of {bookId, dueDate}
  }

  addBook(book) {
    if (this.books.has(book.id)) {
      throw new Error("Book already exists");
    }
    this.books.set(book.id, book);
  }

  borrowBook(userId, bookId, daysToReturn) {
    if (!userId || !bookId) {
      throw new Error("User ID and Book ID are required");
    }
    if (daysToReturn <= 0 || daysToReturn > 30) {
      throw new Error("Borrow duration must be between 1 and 30 days");
    }

    const book = this.books.get(bookId);
    if (!book) {
      throw new Error("Book not found in library");
    }
    if (book.copies <= 0) {
      throw new Error("Book is out of stock");
    }

    const userLoans = this.rented.get(userId) || [];
    if (userLoans.length >= 3) {
      throw new Error("User has reached borrowing limit of 3 books");
    }

    // Check if user already borrowed this book
    if (userLoans.some(loan => loan.bookId === bookId)) {
      throw new Error("User has already borrowed this book");
    }

    book.copies -= 1;
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + daysToReturn);

    userLoans.push({ bookId, dueDate });
    this.rented.set(userId, userLoans);
    return true;
  }

  returnBook(userId, bookId, actualReturnDate) {
    const userLoans = this.rented.get(userId);
    if (!userLoans) {
      throw new Error("No loans found for user");
    }

    const loanIndex = userLoans.findIndex(loan => loan.bookId === bookId);
    if (loanIndex === -1) {
      throw new Error("Book was not borrowed by this user");
    }

    const loan = userLoans[loanIndex];
    const book = this.books.get(bookId);
    if (book) {
      book.copies += 1;
    }

    userLoans.splice(loanIndex, 1);
    if (userLoans.length === 0) {
      this.rented.delete(userId);
    } else {
      this.rented.set(userId, userLoans);
    }

    // Calculate fine: $0.50 per day overdue
    let fine = 0;
    const returnTime = actualReturnDate ? new Date(actualReturnDate).getTime() : new Date().getTime();
    const dueTime = new Date(loan.dueDate).getTime();
    
    if (returnTime > dueTime) {
      const diffDays = Math.ceil((returnTime - dueTime) / (1000 * 60 * 60 * 24));
      fine = diffDays * 0.5;
    }
    return fine;
  }
}

module.exports = { Book, LibraryManager };
