import os
import cx_Oracle
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file

service_port = port=os.environ.get('PORT', '8080')

app = Flask(__name__)
user = ''
passwd = ''
connection = cx_Oracle.connect(user + '/' + passwd + '@scsp.mst.edu')


@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('home.html')

@app.route('/publisher', methods = ['POST', 'GET'])
def publisher():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT B.BOOK_TITLE ,P.NAME , PU.PUBLISH_YEAR
        FROM  NJL44F.BOOK B, NJL44F.PUBLISHER P, NJL44F.PUBLICATION PU
        WHERE B.BOOK_ID = PU.BOOK_ID AND PU.PUBLISHER_ID = P.PUBLISHER_ID AND P.NAME LIKE '%%' """)
    Datas = cursor.fetchall()
    return render_template('publisher.html', Datas=Datas)

@app.route('/User_publisher', methods = ['POST', 'GET'])
def Upublisher():
    publisherName = request.form['pu']
    cursor = connection.cursor()
    cursor.execute("""
        SELECT B.BOOK_TITLE ,P.NAME , PU.PUBLISH_YEAR
        FROM  NJL44F.BOOK B, NJL44F.PUBLISHER P, NJL44F.PUBLICATION PU
        WHERE B.BOOK_ID = PU.BOOK_ID AND PU.PUBLISHER_ID = P.PUBLISHER_ID AND P.NAME LIKE '%""" + publisherName +'%\'')
    Datas = cursor.fetchall()
    return render_template('publisher.html', Datas=Datas)

@app.route('/author', methods = ['POST', 'GET'])
def author():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT B.BOOK_TITLE, A.AUTHOR_NAME, A.COUNTRY_ID
        FROM  NJL44F.BOOK B, NJL44F.AUTHOR A, NJL44F.WRITES W
        WHERE B.BOOK_ID = W.BOOK_ID AND W.AUTHOR_ID = A.AUTHOR_ID AND A.AUTHOR_NAME LIKE '%%' """)
    Datas = cursor.fetchall()
    return render_template('author.html', Datas=Datas)

@app.route('/User_author', methods = ['POST', 'GET'])
def Uauthor():
    authorName = request.form['au']
    cursor = connection.cursor()
    cursor.execute("""
        SELECT B.BOOK_TITLE, A.AUTHOR_NAME, A.COUNTRY_ID
        FROM  NJL44F.BOOK B, NJL44F.AUTHOR A, NJL44F.WRITES W
        WHERE B.BOOK_ID = W.BOOK_ID AND W.AUTHOR_ID = A.AUTHOR_ID AND A.AUTHOR_NAME LIKE '%""" + authorName +'%\'')
    Datas = cursor.fetchall()
    return render_template('author.html', Datas=Datas)

@app.route('/book', methods = ['POST', 'GET'])
def book():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT B.BOOK_TITLE, B.BINDING, B.BOOK_TYPE, B.EDITION, B.GRADE, B.ISBN, B.JACKET_CONDITION, B."LANGUAGE", B.NOTES, B.PAGES
        FROM  NJL44F.BOOK B
        WHERE B.BOOK_TITLE LIKE '%%'""")
    Datas = cursor.fetchall()
    return render_template('book.html', Datas=Datas)

@app.route('/User_book', methods = ['POST', 'GET'])
def Ubook():
    bookName = request.form['bu']
    cursor = connection.cursor()
    cursor.execute("""
        SELECT B.BOOK_TITLE, B.BINDING, B.BOOK_TYPE, B.EDITION, B.GRADE, B.ISBN, B.JACKET_CONDITION, B."LANGUAGE", B.NOTES, B.PAGES
        FROM  NJL44F.BOOK B
        WHERE B.BOOK_TITLE LIKE '%""" +bookName +"%'")
    Datas = cursor.fetchall()
    return render_template('book.html', Datas=Datas)

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    return render_template('upload.html')

@app.route('/uploaded', methods = ['POST', 'GET'])
def uploaded():
    cursor = connection.cursor()
    BookID1 = request.form['BID']
    BookID = int(BookID1)
    BookTitle = request.form['BTI']
    BookType = request.form['BTY']
    Binding = request.form['B']
    JacketCondtion = request.form['JC']
    Grade = request.form['G']
    ISBN = request.form['ISBN']
    Edition = request.form['E']
    Pages1 = request.form['P']
    Pages = int(Pages1)
    Language = request.form['L']
    Notes = request.form['N']
    cursor.execute("""INSERT INTO NJL44F.BOOK (BOOK_ID,BOOK_TITLE,BOOK_TYPE,BINDING,JACKET_CONDITION,GRADE,ISBN,EDITION,PAGES,"LANGUAGE",NOTES) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(BookID, BookTitle, BookType, Binding, JacketCondtion,Grade, ISBN, Edition, 1, Language, Notes))
    connection.commit()             
    return render_template('upload.html')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port= int(service_port) )