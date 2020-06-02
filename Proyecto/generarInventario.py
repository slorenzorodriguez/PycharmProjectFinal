import os

from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, TableStyle, Table)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from sqlite3 import dbapi2


class generarInventario():
    """Clase que genera un PDF con la lista de productos disponibles en SERWAVES .
                Metodos:
                     __init__ --Constructor
        """

    def __init__(self):
        """Constructor de la clase que genera un informe.
                     Esta clase genera una lista en forma de tabla con todos los datos de los productos

                     Parametros:
                        -No tiene

                     Excepciones:
                        -dbapi2.DatabaseError
                """
        listaInventario = []

        listaInventario.append(list(['', '', 'INVENTARIO/STOCK DE SERWAVES SKATE COMPANY', '', '', '']))
        listaInventario.append(list(['Lista de Productos', '', '', '', '', '']))
        listaInventario.append(list(['CODIGO', 'NOMBRE', 'DESCRIPCION', 'STOCK', 'PRECIO', 'PROVEEDOR']))

        try:
            ###Conectamos con la base de datos
            baseDatos = dbapi2.connect("BaseDeDatos.dat")
            cursor = baseDatos.cursor()

            listaProveedores = []
            proveedores = cursor.execute("select id,nombre from proveedores")
            for proveedor in proveedores:
                listaProveedores.append([proveedor[0], proveedor[1]])

            productos = cursor.execute("select * from productos")
            for producto in productos:
                for prov in listaProveedores:
                    if (prov[0] == producto[5]):
                        listaInventario.append(
                            list([producto[0], producto[1], producto[2], str(producto[3]), str(producto[4]), prov[1]]))
        except (dbapi2.DatabaseError):
            print("ERROR BD")
        finally:
            cursor.close()
            baseDatos.close()

        doc = SimpleDocTemplate("Stock.pdf", pagesize=A4)

        guion = []

        taboa = Table(listaInventario, colWidths=90, rowHeights=30)
        taboa.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.darkgreen),

            ('TEXTCOLOR', (0, 4), (-1, -1), colors.black),

            ('BOX', (0, 2), (-1, -4), 1, colors.black),

            ('INNERGRID', (0, 2), (-1, -1), 0.5, colors.grey),

            ('FONTSIZE', (0, 0), (-1, -1), 8),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))

        guion.append(taboa)
        guion.append(PageBreak())

        doc.build(guion)


if __name__ == "__main__":
    generarInventario()
