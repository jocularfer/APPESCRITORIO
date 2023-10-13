from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:
    db = 'database/productos.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=5, pady=20)
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        self.etiqueta_categoria = Label(frame, text="Categoria: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=2, column=0)
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.focus()
        self.categoria.grid(row=2, column=1)
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=4, column=0)
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=4, column=1)
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Calibri', 13))
        self.etiqueta_stock.grid(row=3, column=0)
        self.stock = Entry(frame, font=('Calibri', 13))
        self.stock.grid(row=3, column=1)
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'), background='black', foreground='blue')
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        self.tabla = ttk.Treeview(height=20, columns=("#1", "#2","#3"), style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=5)
        self.tabla.heading('#0', text='Categoria', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.heading('#2', text='Precio', anchor=CENTER)
        self.tabla.heading('#3', text='Stock', anchor=CENTER)
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W+E)
        self.get_productos()
        boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        boton_eliminar.grid(row=5,column=0, columnspan=2, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        boton_editar.grid(row=5, column=3, columnspan=3, sticky=W + E)

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)
        for fila in registros_db:
            print(fila)
            self.tabla.insert('', 0, text=fila[3],values=(fila[1], fila[2],fila[4]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        nombre_introducido_por_usuario = self.categoria.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_stock(self):
        precio_introducido_por_usuario = self.stock.get()
        return len(precio_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() \
                and self.validacion_stock():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadido con exito'.format(self.nombre.get())
            self.categoria.delete(0, END)
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.stock.delete(0, END)
        elif self.validacion_nombre() and self.validacion_categoria() == False and self.validacion_precio() \
                and self.validacion_stock():
            print("La categoria es obligatoria")
            self.mensaje['text'] = 'La categoria es obligatoria'
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() \
                 and self.validacion_stock():
            print("El precio es obligatoria")
            self.mensaje['text'] = 'El precio es obligatorio'
        elif self.validacion_precio() and self.validacion_nombre() == False and self.validacion_categoria() \
                 and self.validacion_stock():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio'
        elif self.validacion_nombre() and self.validacion_stock() == False and self.validacion_categoria() \
                and self.validacion_precio():
            print("El stock es obligatorio")
            self.mensaje['text'] = 'El stock es obligatorio'
        else:
            print("Llenar todos los campos es obligatorio")
            self.mensaje['text'] = 'Llenar todos los campos es obligatorio'
        self.get_productos()

    def del_producto(self):
        self.mensaje['text'] = ''
        try:
            nombre = self.tabla.item(self.tabla.selection())['values'][0]
            print(nombre)
            query = 'DELETE FROM producto WHERE nombre = ?'
            self.db_consulta(query, (nombre,))
            self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
            self.get_productos()
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
        return

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        categoria = self.tabla.item(self.tabla.selection())['text']
        nombre = self.tabla.item(self.tabla.selection())['values'][0]
        old_precio = self.tabla.item(self.tabla.selection())['values'][1]
        old_stock = self.tabla.item(self.tabla.selection())['values'][2]
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')
        titulo = Label(self.ventana_editar, text='Edición del Producto', font=('Calibri', 20, 'bold'))
        titulo.grid(column=0, row=0)
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)
        self.etiqueta_categoria_antiguo = Label(frame_ep, text="Categoria antiguo: ", font=('Calibri', 13))
        self.etiqueta_categoria_antiguo.grid(row=2, column=0)
        self.input_categoria_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=categoria), state='readonly', font=('Calibri', 13))
        self.input_categoria_antiguo.grid(row=2, column=1)
        self.etiqueta_categoria_nuevo = Label(frame_ep, text="Categoria nuevo: ", font=('Calibri', 13))
        self.etiqueta_categoria_nuevo.grid(row=3, column=0)
        self.input_categoria_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nuevo.grid(row=3, column=1)
        self.input_categoria_nuevo.focus()
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13))
        self.etiqueta_nombre_antiguo.grid(row=4, column=0)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state='readonly', font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=4, column=1)
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=5, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=5, column=1)
        self.input_nombre_nuevo.focus()
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13))
        self.etiqueta_precio_antiguo.grid(row=6, column=0)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly', font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=6, column=1)
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=7, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=7, column=1)
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 13))
        self.etiqueta_stock_antiguo.grid(row=8, column=0)
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                          state='readonly', font=('Calibri', 13))
        self.input_stock_antiguo.grid(row=8, column=1)
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=lambda:
        self.actualizar_productos(self.input_categoria_nuevo.get(), self.input_categoria_antiguo.get(),
                                  self.input_nombre_nuevo.get(), self.input_nombre_antiguo.get(),
                                  self.input_precio_nuevo.get(), self.input_precio_antiguo.get(),
                                  self.input_stock_nuevo.get(), self.input_stock_antiguo.get()))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self,nuevo_categoria, antiguo_categoria, nuevo_nombre, antiguo_nombre,
                             nuevo_precio, antiguo_precio, nuevo_stock, antiguo_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria= ?, stock=? WHERE nombre = ? ' \
                'AND precio = ? AND categoria= ? AND stock= ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nuevo_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, nuevo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, nuevo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, antiguo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, nuevo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, antiguo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_categoria == '' and nuevo_stock == '':
            parametros = (antiguo_nombre, nuevo_precio, antiguo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, nuevo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, antiguo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, antiguo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_categoria != '' and nuevo_stock == '':
            parametros = (antiguo_nombre, nuevo_precio, nuevo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
            antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, antiguo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, nuevo_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, antiguo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_categoria != '' and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, nuevo_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antiguo_categoria, antiguo_stock)
            producto_modificado = True
        if producto_modificado:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            self.get_productos()
        else:
            self.ventana_editar.destroy()
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)

if __name__ == '__main__':
    root = Tk()
    app = Producto(root)
    root.mainloop()
