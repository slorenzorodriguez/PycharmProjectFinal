import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class listaProveedores(Gtk.Window):
    """Ventana listaProveedores de SerWaves.
                Metodos:
                     __init__ --Constructor
                     inital_show -- Metodo para trabajar con la visibilidad
                     on_btnVolver_clicked -- Volver a la ventana pincipal
                     on_btnModificar_clicked -- Modificar un proveedor existente.
                     on_btnGuardar_clicked -- Guarda los cambios realizados.
                     on_btnBorrar_clicked -- Borra el proveedor seleccionado.
    """

    def __init__(self, main):
        """Constructor de la Ventana listaProveedores de SerWaves.
            Esta ventana nos permite visualizar, modificar y eliminar los proveedores.

            Parametros:
                   :param main: recibe el objeto window del main para poder volver a la ventana principal.

            Excepciones:
                -dbapi2.DatabaseError
        """
        self.Main = main

        builder = Gtk.Builder()
        builder.add_from_file("Diseño.glade")

        self.ventana = builder.get_object("Main")
        ## self.set_default_size(WIDTH, HEIGHT)

        ##AÑADIMOS LA CABECERA
        cabeceira = Gtk.HeaderBar(title="Lista Proveedores")
        cabeceira.set_subtitle("Informacion de todos los proveedores de la tienda")
        cabeceira.props.show_close_button = True

        self.ventana.set_titlebar(cabeceira)

        self.mainBox = builder.get_object("mainBox")

        # Creamos el modelo del TreeView
        self.modelo = Gtk.ListStore(str, str, str, str, str, str)

        try:
            ###Conectamos con la base de datos
            baseDatos = dbapi2.connect("BaseDeDatos.dat")
            cursor = baseDatos.cursor()

            proveedores = cursor.execute("select * from proveedores")
            for proveedor in proveedores:
                self.modelo.append([proveedor[0], proveedor[1], proveedor[2], proveedor[3], proveedor[4], proveedor[5]])
        except (dbapi2.DatabaseError):
            print("ERROR EN LA BASE DE DATOS")
        finally:
            cursor.close()
            baseDatos.close()

        self.vista = Gtk.TreeView(model=self.modelo)
        self.mainBox.pack_start(self.vista, True, True, 0)

        celdaText = Gtk.CellRendererText()
        columnaNombreProv = Gtk.TreeViewColumn('Proveedor', celdaText, text=1)
        columnaNombreProv.set_sort_column_id(0)
        self.vista.append_column(columnaNombreProv)

        celdaText2 = Gtk.CellRendererText()
        columnaCIF = Gtk.TreeViewColumn('CIF', celdaText2, text=2)
        self.vista.append_column(columnaCIF)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaDireccion = Gtk.TreeViewColumn('Direccion', celdaText3, text=3)
        self.vista.append_column(columnaDireccion)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaTelefono = Gtk.TreeViewColumn('Telefono', celdaText4, text=4)
        self.vista.append_column(columnaTelefono)

        celdaText5 = Gtk.CellRendererText()
        columnaCorreo = Gtk.TreeViewColumn('Correo', celdaText5, text=5)
        self.vista.append_column(columnaCorreo)

        cajaControles = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btnModificar = Gtk.Button(label="MODIFICAR")
        btnModificar.connect("clicked", self.on_btnModificar_clicked)
        cajaControles.pack_start(btnModificar, True, True, 0)
        btnBorrar = Gtk.Button(label="BORRAR")
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked)
        cajaControles.pack_start(btnBorrar, True, True, 0)
        self.mainBox.add(cajaControles)

        self.cajaModificar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.txtNombre = Gtk.Entry()
        self.txtCIF = Gtk.Entry()
        self.txtDireccion = Gtk.Entry()
        self.txtTelefono = Gtk.Entry()
        self.txtCorreo = Gtk.Entry()
        btnGuardar = Gtk.Button(label="Guardar")
        btnGuardar.connect("clicked", self.on_btnGuardar_clicked)
        self.cajaModificar.pack_start(self.txtNombre, True, True, 0)
        self.cajaModificar.pack_start(self.txtCIF, True, True, 0)
        self.cajaModificar.pack_start(self.txtDireccion, True, True, 0)
        self.cajaModificar.pack_start(self.txtTelefono, True, True, 0)
        self.cajaModificar.pack_start(self.txtCorreo, True, True, 0)
        self.cajaModificar.pack_start(btnGuardar, True, True, 0)
        self.mainBox.add(self.cajaModificar)

        señales = {
            "on_btnVolver_clicked": self.on_btnVolver_clicked,
            "on_btnSalir_clicked": Gtk.main_quit,
            "on_Main_destroy": Gtk.main_quit
        }

        builder.connect_signals(señales)

        self.inital_show(self.ventana)

    def inital_show(self, ventana):
        """Este metodo se usa para jugar con la visibilidad de ciertos elemento.
              Pone visible todos los elementos menos la caja cajaModificar que se hara visible al
              clicar el boton de modificar o añadir.
                   :param ventana: objeto  Window
                   :return: None
        """
        ventana.show_all()
        self.cajaModificar.hide()

    def on_btnVolver_clicked(self, boton):
        """Vuelve a la ventana principal
                Este metodo accede a la ventana principal

            :param boton: acceso al botton
            :return: None
        """
        self.Main.show_all()
        self.ventana.hide()

    def on_btnModificar_clicked(self, boton):
        """Este metodo se usa para para hacer visible el formulario y cargar el proveedor
               Pone visible la caja cajaModificar y carga los datos del proveedor seleccionado.
                   :param boton: acceso al botton
                   :return: None
        """
        self.cajaModificar.show();
        seleccion = self.vista.get_selection()
        modelo, punteiro = seleccion.get_selected()
        if punteiro is not None:
            self.txtNombre.set_text(modelo[punteiro][1])
            self.txtCIF.set_text(modelo[punteiro][2])
            self.txtDireccion.set_text(str(modelo[punteiro][3]))
            self.txtTelefono.set_text(modelo[punteiro][4])
            self.txtCorreo.set_text(modelo[punteiro][5])

    def on_btnBorrar_clicked(self, boton):
        """Este metodo se usa para borrar un proveedor.
            Si hay un proveedor selecionado, borra dicho proveedor de la base de datos
                :param boton: acceso al botton
                :return: None
        """
        seleccion = self.vista.get_selection()
        modelo, puntero = seleccion.get_selected()
        if puntero is not None:
            idProv = modelo[puntero][0]
            ##Conectamos con la base de datos
            try:
                baseDatos = dbapi2.connect("BaseDeDatos.dat")
                cursor = baseDatos.cursor()
                cursor.execute("DELETE FROM proveedores WHERE id = '" + idProv + "'")
                baseDatos.commit()
                print("Proveedor eliminado con exito")
                self.modelo.remove(puntero)
            except (dbapi2.DatabaseError):
                print("ERROR EN LA BASE DE DATOS")
            finally:
                cursor.close()
                baseDatos.close()

    def on_btnGuardar_clicked(self, boton):
        """Este metodo se usa para guardar los cambios en la base de datos
                Recoge los datos del formulario y modifica el produto.
                     :param boton: acceso al botton
                     :return: None
        """
        seleccion = self.vista.get_selection()
        modelo, puntero = seleccion.get_selected()
        if puntero is not None:
            idProv = modelo[puntero][0]
            nombre = self.txtNombre.get_text()
            CIF = self.txtCIF.get_text()
            direccion = self.txtDireccion.get_text()
            telefono = self.txtTelefono.get_text()
            correo = self.txtCorreo.get_text()
            if (nombre == "" or CIF == "" or direccion == "" or telefono == "" or correo == ""):
                print("NO SE HAN INTRODUCIDO TODOS LOS DATOS")
            else:
                ##Conectamos con la base de datos
                try:
                    baseDatos = dbapi2.connect("BaseDeDatos.dat")
                    cursor = baseDatos.cursor()
                    cursor.execute(
                        "UPDATE proveedores SET nombre = '" + nombre + "', CIF = '" + CIF + "', direccion='" + direccion + "', telefono='" + telefono + "', correo='" + correo + "'  WHERE id = '" + idProv + "'")
                    print("Proveedor actulizado con exito")
                    self.cajaModificar.hide();
                    baseDatos.commit()
                    ##Actualizamos modelo.
                    self.modelo.remove(puntero)
                    self.modelo.append([idProv, nombre, CIF, direccion, telefono, correo])
                except (dbapi2.DatabaseError):
                    print("ERROR EN LA BASE DE DATOS")
                finally:

                    cursor.close()
                    baseDatos.close()


if __name__ == "__main__":
    listaProveedores()
    Gtk.main()
