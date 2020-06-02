import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class NuevoProveedor(Gtk.Window):
    """Ventana NuevoProveedor de SerWaves.
           Metodos:
                __init__ --Constructor
                on_btnVolver_clicked -- Volver a la ventana pincipal
                on_btnGuardar_clicked -- Guardamos el nuevo proveedor
    """

    def __init__(self, main):
        """Constructor de la Ventana NuevoProv de SerWaves.
                  Esta ventana nos permite añadir un nuevo proveedor a nuestra tienda

                   Parametros:
                   :param main: recibe el objeto window del main para poder volver a la ventana principal.

                   Excepciones:
                   -No tiene.
        """
        self.Main = main

        ##Creamos la ventana
        builder = Gtk.Builder()
        builder.add_from_file("NuevoProveedor.glade")

        self.ventana = builder.get_object("Main")

        ##AÑADIMOS LA CABECERA
        cabeceira = Gtk.HeaderBar(title="Nuevo Proveedor")
        cabeceira.set_subtitle("Formulario para añadir un nuevo proveedor")
        cabeceira.props.show_close_button = True

        self.ventana.set_titlebar(cabeceira)

        self.nombre = builder.get_object("txtNombre")
        self.CIF = builder.get_object("txtCIF")
        self.direccion = builder.get_object("txtDireccion")
        self.telefono = builder.get_object("txtTelefono")
        self.correo = builder.get_object("txtCorreo")

        # Definimos las señales de la ventana.
        señales = {
            "on_btnVolver_clicked": self.on_btnVolver_clicked,
            "on_btnSalir_clicked": Gtk.main_quit,
            "on_Main_destroy": Gtk.main_quit,
            "on_btnGuardar_clicked": self.on_btnGuardar_clicked
        }

        builder.connect_signals(señales)

        self.ventana.show_all()

    def on_btnVolver_clicked(self, boton):
        """Vuelve a la ventana principal
                Este metodo accede a la ventana principal

            :param boton: acceso al botton
            :return: None
        """
        self.Main.show_all()
        self.ventana.hide()

    def on_btnGuardar_clicked(self, boton):
        """Guarda los proveedores en la BD.
            Este metodo recoge los datos de los entry y los guarda en la BD.
            Luego se genera el id a partir de el ultimpo id de la tabla.
            :param boton: acceso al botton
            :return: None
        """
        nombre = self.nombre.get_text()
        CIF = self.CIF.get_text()
        direccion = self.direccion.get_text()
        telefono = self.telefono.get_text()
        correo = self.correo.get_text()

        if (nombre == "" or CIF == "" or direccion == "" or telefono == "" or correo == ""):
            print("NO SE HAN INTRODUCIDO TODOS LOS DATOS")
        else:
            try:
                baseDatos = dbapi2.connect("BaseDeDatos.dat")
                cursor = baseDatos.cursor()
                cursorID = cursor.execute("SELECT id FROM 'proveedores' ORDER BY id DESC LIMIT 1")
                lastid = cursorID.fetchone()[0].split("prov")
                idNuevo = "prov" + str(int(lastid[1]) + 1)
                cursor.execute(
                    "insert into proveedores values('" + idNuevo + "','" + nombre + "','" + CIF + "','" + direccion + "','" + telefono + "','" + correo + "')")
                baseDatos.commit()
                print("PROVEEDOR AÑADIDO CON EXITO")

            except (dbapi2.DatabaseError):
                print("ERROR EN LA BASE DE DATOS")
            finally:
                print("Se cierra Conexion a BD")
                cursor.close()
                baseDatos.close()


if __name__ == "__main__":
    NuevoProveedor()
    Gtk.main()
