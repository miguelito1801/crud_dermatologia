from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os
import datetime

app=Flask(__name__)

#inicio de session
app.secret_key="develoteca"


#conexicon a la base de datos
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='adrianagomez'
mysql.init_app(app)



#redireccionando las paginas sitio
@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/libros')
def libros():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()

    return render_template('sitio/libros.html', libros=libros)

@app.route('/contacto')
def contacto():
    return render_template('sitio/contacto.html')

@app.route('/tc')
def tc():
    return render_template('sitio/tc.html')

@app.route('/tfc')
def tfc():
    return render_template('sitio/tfc.html')


#redireccionando administrador
@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

@app.route('/admin/libros') #conexion a la db
def admin_libros():

    #restringir
    if not 'login' in session:
        return redirect("/admin/login")

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template("/admin/libros.html", libros=libros)



#redireccionando login
@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

#recibir informacion mediante el metodo post
@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    print(_usuario)
    print(_password)

    if _usuario=="admin" and _password=="123":
        session["login"]=True
        session["usuario"]="ADRIANA"
        return redirect("/admin")

    return render_template("admin/login.html", mensaje="Usuario o contraseña incorrecta")

#cerrar session
@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')




#recibiendo datos del crud
@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():

    if not 'login' in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _edad=request.form['txtEdad']
    _dni=request.form['txtDni']
    _correo=request.form['txtCorreo']
    _telefono=request.form['txtTelefono']
    _turno=request.form['txtFechaturno']
    _hora=request.form['txtHorario']

#base de datos
    sql="INSERT INTO `libros` (`id`, `nombre`, `apellido`, `edad`, `dni`, `correo`, `telefono`, `fecha`, `horario`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s);"
    datos=(_nombre,_apellido,_edad,_dni,_correo,_telefono,_turno,_hora)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

#recibiendo datos del crud
    print(_nombre)
    print(_apellido)
    print(_edad)
    print(_dni)
    print(_correo)
    print(_telefono)
    print(_turno)
    print(_hora)

    return redirect('/admin/libros')

#borrar contenido
@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    if not 'login' in session:
        return redirect("/admin/login")
    _id=request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros` WHERE id=%s",(_id))
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)

    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s",(_id))
    conexion.commit()


    
    return redirect('/admin/libros')


if __name__=='__main__':
    app.run(debug=True)