from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()

    print(data)
    return render_template('index.html', contacts = data)

@app.route('/addContact', methods=['POST'])
def addContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
        (fullname, phone, email))
        mysql.connection.commit()

        flash('Contacto agregado satisfactorio')
        return redirect(url_for('Index'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        #id = request.form['id']
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE contacts 
        SET fullname = %s,
         phone = %s, 
         email = %s 
         WHERE id = %s""", 
         (fullname, phone, email, id))
        mysql.connection.commit()

        flash('Contacto Actualizado')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    #mysql.connection.commit()
    data = cursor.fetchall()

    return render_template('edit.html', contact = data[0])

@app.route('/view/<id>')
def view(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    #mysql.connection.commit()
    data = cursor.fetchall()

    return render_template('view.html', contact = data[0])
    

@app.route('/delete/<string:id>')
def deleteContact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)