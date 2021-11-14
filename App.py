from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'donate_v1'
	# mysql = MySQL(app)

try:
	mysql = MySQL(app)
	print("Conexión correcta")
except (MySQL.err.OperationalError, MySQL.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)
print(mysql)


# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        apellido = request.form['apellido']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        fecha_creacion =datetime.now()
        fecha_creacion=fecha_creacion.date()
        cur = mysql.connection.cursor()
        sql = "INSERT INTO usuarios (user_name,password,apellido,nombre,email,telefono,fecha_creacion) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        val = (user_name, password, apellido, nombre, email, telefono, fecha_creacion)
        cur.execute(sql, val)
        
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print("aca", data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        apellido = request.form['apellido']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET user_name = %s,
            password = %s,
            apellido = %s,
            nombre = %s,
            email = %s,
            telefono = %s
            WHERE id = %s
        """, [user_name,password,apellido,nombre,email,telefono, id])
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3306, debug=True)