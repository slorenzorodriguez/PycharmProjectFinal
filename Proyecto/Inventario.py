import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2
from Proyecto.generarInventario import generarInventario


class Inventario(Gtk.Window):
    """Ventana Inventario de SerWaves
            Metodos:
                 __init__ --Constructor
                 inital_show -- Metodo para trabajar con la visibilidad
                 on_btnVolver_clicked -- Volver a la ventana pincipal
                 on_btnEbgadir_clicked -- Añadir un nuevo producto
                 on_btnModificar_clicked -- Modificar un producto existente.
                 on_btnGuardar_clicked -- Guarda los cambios realizados.
                 on_btnBorrar_clicked -- Borra el producto seleccionado.
                 on_btnGenerarInventario_clicked -- Genera un informe con los productos disponibles
    """

    def __init__(self, main):
        """Constructor de la Ventana Inventario de SerWaves
             Esta ventana nos permite visualizar, añadir, modificar y eliminar los productoss.

             Parametros:
                   :param main: recibe el objeto window del main para poder volver a la ventana principal.

             Excepciones:
                -dbapi2.DatabaseError
        """
        self.Main = main
        self.añadir = False

        builder = Gtk.Builder()
        builder.add_from_file("Diseño.glade")

        self.ventana = builder.get_object("Main")

        ##AÑADIMOS LA CABECERA
        cabeceira = Gtk.HeaderBar(title="Inventario")
        cabeceira.set_subtitle("Informacion de todos los productos de la tienda")
        cabeceira.props.show_close_button = True

        self.ventana.set_titlebar(cabeceira)

        self.mainBox = builder.get_object("mainBox")

        self.modelo = Gtk.ListStore(str, str, str, int, float, str)

        self.proveedoresCMB = Gtk.ListStore(str)

        try:
            ###Conectamos con la base de datos
            baseDatos = dbapi2.connect("BaseDeDatos.dat")
            cursor = baseDatos.cursor()

            self.listaProveedores = []
            proveedores = cursor.execute("select id,nombre from proveedores")
            for proveedor in proveedores:
                self.listaProveedores.append([proveedor[0], proveedor[1]])
                self.proveedoresCMB.append([proveedor[1]])

            productos = cursor.execute("select * from productos")
            for producto in productos:
                for prov in self.listaProveedores:
                    if (prov[0] == producto[5]):
                        self.modelo.append([producto[0], producto[1], producto[2], producto[3], producto[4], prov[1]])
        except (dbapi2.DatabaseError):
            print("ERROR BD")
        finally:
            cursor.close()
            baseDatos.close()

        self.vista = Gtk.TreeView(model=self.modelo)
        self.mainBox.pack_start(self.vista, True, True, 0)

        celdaText = Gtk.CellRendererText()
        columnaNombrePro = Gtk.TreeViewColumn('Nombre Producto', celdaText, text=1)
        columnaNombrePro.set_sort_column_id(0)
        self.vista.append_column(columnaNombrePro)

        celdaText2 = Gtk.CellRendererText()
        columnaDescripcion = Gtk.TreeViewColumn('Descripcion', celdaText2, text=2)
        self.vista.append_column(columnaDescripcion)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaStock = Gtk.TreeViewColumn('Stock', celdaText3, text=3)
        columnaStock.set_sort_column_id(2)
        self.vista.append_column(columnaStock)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaPrecio = Gtk.TreeViewColumn('Precio/Unidad', celdaText4, text=4)
        columnaPrecio.set_sort_column_id(3)
        self.vista.append_column(columnaPrecio)

        celdaText5 = Gtk.CellRendererText()
        columnaProveedor = Gtk.TreeViewColumn('Proveedor', celdaText5, text=5)
        columnaProveedor.set_sort_column_id(0)
        self.vista.append_column(columnaProveedor)

        cajaControles = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btnAñadir = Gtk.Button(label="AÑADIR")
        btnAñadir.connect("clicked", self.on_btnAñadir_clicked)
        cajaControles.pack_start(btnAñadir, True, True, 0)
        btnModificar = Gtk.Button(label="MODIFICAR")
        btnModificar.connect("clicked", self.on_btnModificar_clicked)
        cajaControles.pack_start(btnModificar, True, True, 0)
        btnBorrar = Gtk.Button(label="BORRAR")
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked)
        cajaControles.pack_start(btnBorrar, True, True, 0)
        self.mainBox.add(cajaControles)

        self.cajaModificar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.txtNombre = Gtk.Entry()
        self.txtDescripcion = Gtk.Entry()
        self.txtStock = Gtk.Entry()
        self.txtPrecio = Gtk.Entry()
        ##Para los proveedores necesitamos un comboBox
        celdaCombo = Gtk.CellRendererText()
        self.cmbProveedores = Gtk.ComboBox(model=self.proveedoresCMB)
        self.cmbProveedores.pack_start(celdaCombo, True)
        self.cmbProveedores.add_attribute(celdaCombo, "text", 0)
        btnGuardar = Gtk.Button(label="Guardar")
        btnGuardar.connect("clicked", self.on_btnGuardar_clicked)
        self.cajaModificar.pack_start(self.txtNombre, True, True, 0)
        self.cajaModificar.pack_start(self.txtDescripcion, True, True, 0)
        self.cajaModificar.pack_start(self.txtStock, True, True, 0)
        self.cajaModificar.pack_start(self.txtPrecio, True, True, 0)
        self.cajaModificar.pack_start(self.cmbProveedores, True, True, 0)
        self.cajaModificar.pack_start(btnGuardar, True, True, 0)
        self.mainBox.add(self.cajaModificar)

        cajaInventario = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btnGenerarInventario = Gtk.Button(label="GENERAR STOCK")
        btnGenerarInventario.connect("clicked", self.on_btnGenerarInventario_clicked)
        cajaInventario.pack_start(btnGenerarInventario, True, True, 0)
        self.mainBox.add(cajaInventario)

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
        self.cajaModificar.hide();

    def on_btnVolver_clicked(self, boton):
        """Vuelve a la ventana principal
                Este metodo accede a la ventana principal

            :param boton: acceso al botton
            :return: None
        """
        self.Main.show_all()
        self.ventana.hide()

    def on_btnAñadir_clicked(self, boton):
        """Este metodo se usa para hacer visible el formulario para añadir un elemento
            Pone visible la caja cajaModificar y establece que la operacion que se hara sera una insercion
                 :param boton: acceso al botton
                 :return: None
        """
        self.cajaModificar.show();
        self.añadir = True

    def on_btnModificar_clicked(self, boton):
        """Este metodo se usa para para hacer visible el formulario y cargar el producto
            Pone visible la caja cajaModificar y carga los datos del producto seleccionado.
                 :param boton: acceso al botton
                 :return: None
        """
        self.cajaModificar.show();
        self.añadir = False
        seleccion = self.vista.get_selection()
        modelo, punteiro = seleccion.get_selected()
        if punteiro is not None:
            self.txtNombre.set_text(modelo[punteiro][1])
            self.txtDescripcion.set_text(modelo[punteiro][2])
            self.txtStock.set_text(str(modelo[punteiro][3]))
            self.txtPrecio.set_text(str(modelo[punteiro][4]))
            proveedores = self.cmbProveedores.get_model()
            i = 0
            for proveedor in proveedores:
                if modelo[punteiro][5] == proveedor[0]:
                    self.cmbProveedores.set_active(i)
                i = i + 1

    def on_btnGuardar_clicked(self, boton):
        """Este metodo se usa para guardar los cambios en la base de datos
                Segun la operacion que se desee hacer añade o modifica un producto.
                   :param boton: acceso al botton
                   :return: None
        """
        if (self.añadir == True):
            ##Conectamos con la base de datos
            try:
                baseDatos = dbapi2.connect("BaseDeDatos.dat")
                cursor = baseDatos.cursor()
                cursorID = cursor.execute("SELECT id FROM 'productos' ORDER BY id DESC LIMIT 1")
                lastid = cursorID.fetchone()[0].split("pro")
                idNuevo = "pro" + str(int(lastid[0]) + 1)
                nombre = self.txtNombre.get_text()
                descripcion = self.txtDescripcion.get_text()
                stock = self.txtStock.get_text()
                precio = self.txtPrecio.get_text()
                indiceProveedor = self.cmbProveedores.get_active_iter()
                proveedor = self.cmbProveedores.get_model()[indiceProveedor][0]
                if (nombre == "" or descripcion == "" or stock == "" or precio == "" or proveedor == ""):
                    print("No se han completado todos los campos")
                else:
                    for prov in self.listaProveedores:
                        if (prov[1] == proveedor):
                            idProv = prov[0]
                    cursor.execute(
                        "insert into productos values('" + idNuevo + "','" + nombre + "','" + descripcion + "','" + stock + "','" + precio + "','" + idProv + "')")
                    baseDatos.commit()
                    print("PRODUCTO AÑADIDO CON EXITO")
                    self.modelo.append([idNuevo, nombre, descripcion, int(stock), float(precio), prov[1]])
                    self.cajaModificar.hide();
            except (dbapi2.DatabaseError):
                print("ERROR BD")
            finally:
                cursor.close()
                baseDatos.close()
        else:
            seleccion = self.vista.get_selection()
            modelo, puntero = seleccion.get_selected()
            if puntero is not None:
                idPro = modelo[puntero][0]
                nombre = self.txtNombre.get_text()
                descripcion = self.txtDescripcion.get_text()
                stock = self.txtStock.get_text()
                precio = self.txtPrecio.get_text()
                indiceProveedor = self.cmbProveedores.get_active_iter()
                proveedor = self.cmbProveedores.get_model()[indiceProveedor][0]
                if (nombre == "" or descripcion == "" or stock == "" or precio == "" or proveedor == ""):
                    print("No se han completado todos los campos")
                else:
                    for prov in self.listaProveedores:
                        if (prov[1] == proveedor):
                            idProv = prov[0]
                    ##Conectamos con la base de datos
                    try:
                        baseDatos = dbapi2.connect("BaseDeDatos.dat")
                        cursor = baseDatos.cursor()
                        cursor.execute(
                            "UPDATE productos SET nombre = '" + nombre + "', descripcion = '" + descripcion + "', cantidadStock=" + stock + ", precioUnidad=" + precio + ", idProv='" + idProv + "'  WHERE id = '" + idPro + "'")
                        baseDatos.commit()
                        print("Producto actulizado con exito")
                        self.modelo.remove(puntero)
                        self.modelo.append([idPro, nombre, descripcion, int(stock), float(precio), prov[1]])
                        self.cajaModificar.hide();
                        self.txtNombre.set_text("")
                        self.txtDescripcion.set_text("")
                        self.txtStock.set_text("")
                        self.txtPrecio.set_text("")
                    except (dbapi2.DatabaseError):
                        print("ERROR EN LA BASE DE DATOS")
                    finally:
                        print("Cerramos la conexion a la BD")
                        cursor.close()
                        baseDatos.close()

    def on_btnBorrar_clicked(self, boton):
        """Este metodo se usa para borrar un producto.
            Si hay un producto selecionado, borra dicho producto de la base de datos
                 :param boton: acceso al botton
                 :return: None
        """
        seleccion = self.vista.get_selection()
        modelo, puntero = seleccion.get_selected()
        if puntero is not None:
            idPro = modelo[puntero][0]
            ##Conectamos con la base de datos
            try:
                baseDatos = dbapi2.connect("BaseDeDatos.dat")
                cursor = baseDatos.cursor()
                cursor.execute("DELETE FROM productos WHERE id = '" + idPro + "'")
                baseDatos.commit()
                print("Producto eliminado con exito")
                self.modelo.remove(puntero)
            except (dbapi2.DatabaseError):
                print("ERROR EN LA BASE DE DATOS")
            finally:
                cursor.close()
                baseDatos.close()

    def on_btnGenerarInventario_clicked(self, boton):
        """Este metodo se usa para generar un informe con los productos de la tienda.
            Se llama a la clase informeInventario que leera los datos de la base de datos y generara un PDF.
                    :param boton: acceso al botton
                    :return: None
        """
        generarInventario()


if __name__ == "__main__":
    Inventario()
    Gtk.main()
