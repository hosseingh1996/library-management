import sys
import pymysql
from PyQt5.QtWidgets import (
    QApplication , QMainWindow , QTableWidgetItem , QMessageBox
)
from PyQt5.QtCore import QDate
from PyQt5 import uic




def connect_to_db():
    try:
        connection = pymysql.connect (
            host="localhost",
            user="root",
            password="",
            database="library_db"
        )
        return connection
    except pymysql.Error as e:
        print ( f"Error connecting to MySQL: {e}" )
        return None



class LibraryManagement ( QMainWindow ):
    def __init__( self ):
        super ().__init__ ()

        self.setWindowTitle ( "Library Management System" )
        uic.loadUi ( 'libraryy.ui' , self )

        self.connection = connect_to_db ()
        if not self.connection:
            QMessageBox.critical(self, "Failed to connect to the database.")
            sys.exit()


        self.btnAddBook.clicked.connect ( self.add_book )
        self.btnSearchBook.clicked.connect ( self.search_books )
        self.btnRefresh.clicked.connect ( self.display_books )


        self.display_books ()


    def add_book( self ):
        book_no = self.lineEditBookNo.text()
        name = self.lineEditBookName.text()
        author = self.lineEditAuthor.text()
        isbn = self.lineEditISBN.text()
        subject = self.lineEditSubject.text ()
        language = self.lineEditLanguage.text ()
        date_of_purchase = self.dateEditPurchase.date().toString("yyyy-MM-dd")

        if not (book_no and name and author and language):
            QMessageBox.warning (self, "Please fill all required fields.")
            return

        try:
            cursor = self.connection.cursor ()
            query = """INSERT INTO books 
                       (book_no, name, author, isbn, subject, language, date_of_purchase) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute ( query , (book_no , name , author , isbn , subject , language , date_of_purchase) )
            self.connection.commit ()
            QMessageBox.information (self,"Book added successfully!" )
            self.clear_form()
            self.display_books ()
        except pymysql.Error as e:
            QMessageBox.critical ( self , "Database Error" , f"Error: {e}" )


    def search_books( self ):
        search_term = self.lineEditBookName.text ()
        if not search_term:
            QMessageBox.warning(self,"Enter a book name to search")
            return

        try:
            cursor = self.connection.cursor ()
            query = "SELECT * FROM books WHERE name LIKE %s"
            cursor.execute(query ,(f"%{search_term}%"))
            result = cursor.fetchall ()
            self.populate_table(result)
        except pymysql.Error as e:
            QMessageBox.critical(self, "Database Error" , f"Error: {e}")


    def display_books( self ):
        try:
            cursor = self.connection.cursor ()
            cursor.execute ( "SELECT * FROM books" )
            result = cursor.fetchall ()
            self.populate_table ( result )
        except pymysql.Error as e:
            QMessageBox.critical ( self , "Database Error" , f"Error: {e}" )


    def populate_table( self , result ):
        self.tableWidgetBooks.setRowCount ( 0 )
        for row_idx , book in enumerate ( result):
            self.tableWidgetBooks.insertRow(row_idx)
            for col_idx , value in enumerate(book):
                self.tableWidgetBooks.setItem ( row_idx , col_idx , QTableWidgetItem ( str ( value ) ) )


    def clear_form( self ):
        self.lineEditBookNo.clear ()
        self.lineEditBookName.clear ()
        self.lineEditAuthor.clear ()
        self.lineEditISBN.clear ()
        self.lineEditSubject.clear ()
        self.lineEditLanguage.clear ()
        self.dateEditPurchase.setDate ( QDate.currentDate () )



def main():
    app = QApplication ( sys.argv )
    window = LibraryManagement ()
    window.show ()
    sys.exit ( app.exec_ () )


if __name__ == "__main__":
    main ()
