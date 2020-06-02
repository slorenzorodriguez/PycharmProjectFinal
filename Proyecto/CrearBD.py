import os
from sqlite3 import dbapi2

"""
    Genera la base de datos y le introduce unos datos iniciales.
"""
try:
    ###Creación de la base de datos.
    baseDatos = dbapi2.connect("BaseDeDatos.dat")
    cursor = baseDatos.cursor()

    ###Creación de las tablas
    cursor.execute(
        "create table proveedores(id text, nombre text,CIF text, direccion text, telefono text, correo text)")
    cursor.execute(
        "create table productos(id text, nombre text , descripcion text, cantidadStock number, precioUnidad number,idProv text)")
    cursor.execute(
        "create table facturasClientes(idFactura number, nombreCliente text, telefono text, direccion text, correo text)")
    cursor.execute("create table facturasInfo(idFactura number,idProducto text, cantidad number)")

    ###Realizamos Inserts en las tablas
    cursor.execute(
        "insert into proveedores values('idprov1','Element','562-352-143','Rúa de Alexandre Bóveda','986453328','ElementUrban@gmail.com')")
    cursor.execute(
        "insert into proveedores values('idprov2','Blind','150-488-654','Av. Ricardo Mella Nª87','955125688','Blind@gmail.deu')")
    cursor.execute(
        "insert into proveedores values('idprov3','Powell','563-234-789','Rúa da Coruña Nº76','986097984','Powell@enterprise.com.eng')")

    cursor.execute(
        "insert into productos values('232051760','6es7540-3220-age0','Tablas completas de skate y longboard', 100, 110.00,'idprov1')")
    cursor.execute("insert into productos values('255045198','6k7mup','Rodamientos', 200, 49.99, 'idprov2')")
    cursor.execute("insert into productos values('276043207','CHO10','Lijas', 150, 15.90, 'idprov3')")

    cursor.execute(
        "insert into facturasClientes values(1,'Novalbos Wave Company','986208787','Rúa Pintor Laxeiro Nº16','NovalbosWave@gmail.com')")
    cursor.execute(
        "insert into facturasClientes values(1,'Cromoly','986502010','Rúa de Urzaiz Nº61','Cromoly@gmail.es')")

    cursor.execute("insert into facturasInfo values(1,'232051760',2)")
    cursor.execute("insert into facturasInfo values(1,'255045198',1)")

    ###Realizamos commit en la BD
    baseDatos.commit()

###Creamos una excepción para los errores y finalmente cerramos la conexión
except (dbapi2.DatabaseError):
    print("ERROR BD")
finally:
    print("Cerramos conexionBD")
    cursor.close()
    baseDatos.close()
