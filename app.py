from flask import Flask
from flask import render_template , request , redirect
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os


app = Flask (__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']= 'localhost'
app.config['MYSQL_DATABASE_USER']= 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB']= 'sistema2170'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route("/")
def index():

    sql = "SELECT * FROM `empleados`;";
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    #print(empleados)
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

@app.route("/create")
def create():
     return render_template('empleados/create.html')

@app.route("/destroy/<int:id>")
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route("/update", methods=['POST'])
def update():
    id      =request.form['txtId']
    _nombre =request.form['txtNombre']
    _correo =request.form['txtCorreo']
    _foto   =request.files['txtFoto']

    sql = "UPDATE empleados SET nombre=%s , correo=%s WHERE id=%s;"
    datos=(_nombre, _correo, id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect("/")

@app.route('/store', methods=['POST'])
def store():
    _nombre =request.form['txtNombre']
    _correo =request.form['txtCorreo']
    _foto   =request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    # TODO hay que hacer una foto generica en caso de que no suba 
    nuevoNombreFoto=tiempo + _foto.filename
    if _foto.filename != "" :
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);";
    datos = (_nombre, _correo, nuevoNombreFoto)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

if __name__ == '__main__':
    app.run(debug=True)