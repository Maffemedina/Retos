import this
from tkinter import ttk
from tkinter import *
from tkinter import Frame

import sqlite3
class Ventana:
    def __init__(self,window):
        self.wind = window
        self.wind.title('Reto 1')

class Producto(Ventana):
    
    db_nombre='database.db'

    def __init__(self,window):
        super().__init__(self,window)
        #crear contenedor
        frame = LabelFrame(self.wind,text = 'Registra un nuevo producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #insertar nombre
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.nombre=Entry(frame)
        self.nombre.grid(row=2, column=1)

        #insertar descripcion
        Label(frame, text='Descripcion: ').grid(row=2, column=0)
        self.descripcion=Entry(frame)
        self.descripcion.grid(row=3, column=1)

        

        #boton agregar producto
        ttk.Button(frame, text='Guardar Producto',command=self.add_product).grid(row=6, columnspan=2, sticky= W+E)

        #mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 8, column = 0, columnspan = 2, sticky = W + E)

        #Tabla
        self.tree=ttk.Treeview(height=20, columns=('#1','#2'))#Mejor metodo de agregar columnas
        self.tree.grid(row=9,column=0,columnspan=5)
        self.tree['show'] = 'headings' #Ocultar la columna que '#0' que por defecto trae ttk
        self.tree.heading('#1',text='Nombre',anchor=CENTER)
        self.tree.heading('#2',text='Descripcion',anchor=CENTER)

        # botones
        ttk.Button(text = 'ELIMINAR', command = self.delete_product).grid(row = 10, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_product).grid(row = 10, column = 1, sticky = W + E)
        
        #llenando las filas
        self.get_products()


    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_nombre)as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        #limpiando la tabla
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consultando los datos
        query='SELECT * FROM Producto ORDER BY nombre_producto ASC'
        db_rows=self.run_query(query)#filas de la base de datos
        #rellenando los datos
        for row in db_rows:
            #print (row) #<---- imprime una tupla
            self.tree.insert('',0,text=row[0],values=row[2])
    def validation(self):
        return len(self.nombre.get) !=0 and len(self.descripcion.get) !=0 and len(self.idprovider.get) !=0 and len(self.nameprovider.get) !=0 and len(self.direccion.get) !=0
    
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO Producto VALUES(?, ?, ?, ?, ?, ?)'
            parameters =  (self.codigo.get(), self.nombre.get(), self.descripcion.get(), self.idprovider.get(), self.nameprovider.get(), self.direccion.get())
            self.run_query(query, parameters)
            self.message['text'] = 'El Producto {} ha sido agregado satisfactoriamente'.format(self.nombre.get())
            self.codigo.delete(0, END)
            self.nombre.delete(0, END)
            self.descripcion.delete(0, END)
        else:
            self.message['text'] = 'Todos los campos son requeridos'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccione un registro'
            return
        self.message['text'] = ''
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Producto WHERE nombre_producto = ?'
        self.run_query(query, (nombre, ))
        self.message['text'] = 'El registro {} ha sido eliminado satisfactoriamente'.format(nombre)
        self.get_products()    

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor, Selecione el registro'
            return
        nombre = self.tree.item(self.tree.selection())['text']
        old_descripcion = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'
        # Old Name
        Label(self.edit_wind, text = 'Nombre Anterior:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'Nuevo Nombre:').grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre.grid(row = 1, column = 2)

        # Old description 
        Label(self.edit_wind, text = 'Descripcion Anterior:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_descripcion), state = 'readonly').grid(row = 2, column = 2)
        # New description
        Label(self.edit_wind, text = 'Nueva Descripcion:').grid(row = 3, column = 1)
        nueva_descripcion= Entry(self.edit_wind)
        nueva_descripcion.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(nuevo_nombre.get(), nombre, nueva_descripcion.get(), old_descripcion)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, nuevo_nombre, nombre, nueva_descripcion, old_descripcion):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (nuevo_nombre, nombre, nueva_descripcion, old_descripcion)
        self.run_query(query, parameters)
        self.edit_wind.destroy()#se cierra la ventana
        self.message['text'] = 'Record {} updated successfylly'.format(nombre)
        self.get_products()

class Proveedor(Ventana):
    
    db_nombre='database.db'

    def __init__(self,window):
        super().__init__(self,window)
        #crear contenedor
        frame = LabelFrame(self.wind,text = 'Registra un nuevo proveedor')
        frame.grid(row=1, column=2, columnspan=3, pady=20)

        #insertar id proveedor
        Label(frame, text='ID Proveedor: ').grid(row=2, column=0)
        self.idproveedor=Entry(frame)
        self.idproveedor.grid(row=3, column=2)

        #insertar nombre proveedor
        Label(frame, text='Nombre Proveedor: ').grid(row=4, column=0)
        self.nombreproveedor=Entry(frame)
        self.nombreproveedor.grid(row=5, column=2)

        #insertar direccion
        Label(frame, text='Direccion : ').grid(row=5, column=0)
        self.direccion=Entry(frame)
        self.direccion.grid(row=6, column=2)

        #boton agregar producto
        ttk.Button(frame, text='Guardar Proveedor',command=self.add_proveedor).grid(row=6, columnspan=2, sticky= W+E)

        #mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 8, column = 0, columnspan = 2, sticky = W + E)

        #Tabla
        self.tree=ttk.Treeview(height=20, columns=('#1','#2','#3'))#Mejor metodo de agregar columnas
        self.tree.grid(row=9,column=0,columnspan=5)
        self.tree['show'] = 'headings' #Ocultar la columna que '#0' que por defecto trae ttk
        self.tree.heading('#3',text='ID Provedor',anchor=CENTER)
        self.tree.heading('#4',text='Nombre Provedor',anchor=CENTER)
        self.tree.heading('#5',text='Direccion',anchor=CENTER)

        # botones
        ttk.Button(text = 'ELIMINAR', command = self.delete_proveedor).grid(row = 10, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_proveedor).grid(row = 10, column = 1, sticky = W + E)
        
        #llenando las filas
        self.get_proveedor()

    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_nombre)as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_proveedor(self):
        #limpiando la tabla
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consultando los datos
        query='SELECT * FROM Producto ORDER BY nombre_producto ASC'
        db_rows=self.run_query(query)#filas de la base de datos
        #rellenando los datos
        for row in db_rows:
            #print (row) #<---- imprime una tupla
            self.tree.insert('',0,text=row[0],values=row[2])
    def validation(self):
        return len(self.idproveedor.get) !=0 and len(self.nombreproveedor.get) !=0 and len(self.direccion.get) !=0
    
    def add_proveedor(self):
        if self.validation():
            query = 'INSERT INTO Proveedor VALUES(?, ?, ?, ?, ?, ?)'
            parameters =  (self.idproveedor.get(), self.nombreproveedor.get(), self.direccion.get())
            self.run_query(query, parameters)
            self.message['text'] = 'El Proveedor {} ha sido agregado satisfactoriamente'.format(self.nombreproveedor.get())
            self.idproveedor.delete(0, END)
            self.nombreproveedor.delete(0, END)
            self.direccion.delete(0, END)
        else:
            self.message['text'] = 'Todos los campos son requeridos'
        self.get_proveedor()

    def delete_proveedor(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccione un registro'
            return
        self.message['text'] = ''
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Proveedor WHERE nombre = ?'
        self.run_query(query, (nombre, ))
        self.message['text'] = 'El registro {} ha sido eliminado satisfactoriamente'.format(nombre)
        self.get_proveedor()    

    def edit_proveedor(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor, Selecione el registro'
            return
        nombre = self.tree.item(self.tree.selection())['text']
        old_id = self.tree.item(self.tree.selection())['values'][0]
        old_direccion=self.tree.item(self.tree.selection())['text']
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'
        # Old Name
        Label(self.edit_wind, text = 'Nombre Anterior:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'Nuevo Nombre:').grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre(row = 1, column = 2)

        # Old id 
        Label(self.edit_wind, text = 'ID Anterior:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_id), state = 'readonly').grid(row = 2, column = 2)
        # New id
        Label(self.edit_wind, text = 'Nuevo ID:').grid(row = 3, column = 1)
        nuevo_id= Entry(self.edit_wind)
        nuevo_id.grid(row = 3, column = 2)

         # Old direccion 
        Label(self.edit_wind, text = 'Direccion Anterior:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_direccion), state = 'readonly').grid(row = 2, column = 2)
        # New direccion
        Label(self.edit_wind, text = 'Nueva Direccion:').grid(row = 3, column = 1)
        nueva_direccion= Entry(self.edit_wind)
        nueva_direccion(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(nuevo_nombre.get(), nombre, nuevo_id.get(), old_id, nueva_direccion.get(), old_direccion)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_registrosprov(self, nuevo_nombre, nombre, nuevo_id, old_id, nueva_direccion, old_direccion):
        query = 'UPDATE Proveedor SET nombre = ?, id = ?, direccion = ? WHERE nombre = ? AND id = ? AND direccion = ?'
        parameters = (nuevo_nombre, nombre, nuevo_id, old_id, nueva_direccion, old_direccion)
        self.run_query(query, parameters)
        self.edit_wind.destroy()#se cierra la ventana
        self.message['text'] = 'Registro {} actualizado satisfactoriamente'.format(nombre)
        self.get_proveedores()
if __name__ == '__main__':
    window = Tk()
    application = Ventana(window)
    window.mainloop()