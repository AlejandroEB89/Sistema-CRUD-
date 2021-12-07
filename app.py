from flask import Flask
from flask import render_template , request
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask (__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']= 'localhost'
app.config['MYSQL_DATABASE_USER']= 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB']= 'sistema2170'
mysql.init_app(app)


@app.route("/")
def index():

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Alberto Mamarullo', 'mamarullo@gmail.com', 'fotoPerfil.jpg');";
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template('empleados/index.html')

@app.route("/create")
def create():
     return render_template('empleados/create.html')

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
    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(debug=True)