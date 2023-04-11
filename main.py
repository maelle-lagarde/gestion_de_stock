import tkinter as tk, mysql.connector
import tkinter.ttk as ttk
import csv


class Stock:
    def __init__(self, host, user, password, database):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "boutique"
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def display_products(self, table):
        self.cursor.execute("SELECT *FROM " + str(table))
        self.results = self.cursor.fetchall()
        return self.results

    def close_connection(self):
        self.connection.close()

    def add_product(self, nom, description, prix, quantite, categorie):
        sql = "INSERT produit (id, nom, description, prix, quantite, id_categorie) VALUES(NULL, %s, %s, %s, %s, %s);"
        self.cursor.execute(sql, (nom, description, prix, quantite, categorie))
        self.connection.commit()

    def delete_product(self, id):
        sql = "DELETE FROM produit WHERE id = %s"
        self.cursor.execute(sql, (id,))
        self.connection.commit()

    def update_product(self, id, nom, description, prix, quantite, categorie):
        sql = "UPDATE produit SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s WHERE id = %s;"
        self.cursor.execute(sql, (nom, description, prix, quantite, categorie, id,))
        self.connection.commit()


class Main:
    def __init__(self):
        self.stock = Stock("localhost", "root", "root", "boutique")
        self.window = tk.Tk()
        self.window.title("Inventory Store System")
        self.window.geometry("1300x350")
        self.current_screen = []
        self.state = 0

        # state 0 = display products / main window
        # state 1 = add product window
        # state 2 = delete product window
        # state 3 = update product window
        # state 4 = export csv window

        self.add_product = tk.Button(self.window, text="Ajouter produit", font=('Open Sans', 13))
        self.delete_product = tk.Button(self.window, text="Supprimer produit", font=('Open Sans', 13))
        self.update_product = tk.Button(self.window, text="Modifier produit", font=('Open Sans', 13))
        self.import_csv = tk.Button(self.window, text="Exporter en CSV", font=('Open Sans', 13))
        self.state0 = [self.add_product, self.delete_product, self.update_product, self.import_csv]
        self.tree_product = ttk.Treeview(self.window, columns=("col1", "col2", "col3", "col4", "col5", "col6"),
                                         show="headings")
        self.tree_product.heading("col1", text="ID")
        self.tree_product.heading("col2", text="Nom")
        self.tree_product.heading("col3", text="Description")
        self.tree_product.heading("col4", text="Prix")
        self.tree_product.heading("col5", text="Quantité")
        self.tree_product.heading("col6", text="Id Catégorie")
        self.render_tree()
        self.add_product.config(command=self.add_product_command)
        self.delete_product.config(command=self.delete_product_command)
        self.update_product.config(command=self.update_product_command)

    def render_tree(self):
        self.tree_product.delete(*self.tree_product.get_children())
        for element in self.stock.display_products("produit"):
            self.tree_product.insert("", "end", values=element)

    # State 1 : add product.
    def add_product_command(self):
        self.add_product_window = tk.Toplevel(self.window)
        self.add_product_window.title("Ajouter un produit")
        self.add_product_window.geometry("300x300")

        self.title_name = tk.Label(self.add_product_window, text="Nom :")
        self.input_name = tk.Entry(self.add_product_window)
        self.title_description = tk.Label(self.add_product_window, text="Description :")
        self.input_description = tk.Entry(self.add_product_window)
        self.title_prix = tk.Label(self.add_product_window, text="Prix :")
        self.input_prix = tk.Entry(self.add_product_window)
        self.title_quantite = tk.Label(self.add_product_window, text="Quantité :")
        self.input_quantite = tk.Entry(self.add_product_window)
        self.title_categorie = tk.Label(self.add_product_window, text="Id Categorie")
        self.input_categorie = tk.Entry(self.add_product_window)
        self.valid_state1 = tk.Button(self.add_product_window, text="OK")
        self.valid_state1.config(command=self.add_product_sql)
        self.state1 = [self.title_name, self.input_name, self.title_description, self.input_description,
                       self.title_prix, self.input_prix, self.title_quantite, self.input_quantite, self.title_categorie,
                       self.input_categorie, self.valid_state1]
        for element in self.state1:
            element.pack()

    def add_product_sql(self):
        self.stock.add_product(self.input_name.get(), self.input_description.get(), self.input_prix.get(),
                               self.input_quantite.get(), self.input_categorie.get())
        self.render_tree()
        self.add_product_window.destroy()

    # State 2 : delete product.
    def delete_product_command(self):
        self.delete_product_window = tk.Toplevel(self.window)
        self.delete_product_window.title("Supprimer un produit")
        self.delete_product_window.geometry("300x100")
        self.aff_id = tk.Label(self.delete_product_window, text="ID")
        self.input_id = tk.Entry(self.delete_product_window)
        self.valid_state2 = tk.Button(self.delete_product_window, text="OK")
        self.valid_state2.config(command=self.delete_product_sql)
        self.state2 = [self.aff_id, self.input_id, self.valid_state2]
        for element in self.state2:
            element.pack()

    def delete_product_sql(self):
        self.stock.delete_product(self.input_id.get())
        self.render_tree()
        self.delete_product_window.destroy()

    # State 3 : update product.
    def update_product_command(self):
        self.update_product_window = tk.Toplevel(self.window)
        self.update_product_window.title("Modifier un produit")
        self.update_product_window.geometry("300x350")
        self.aff_id_s3 = tk.Label(self.update_product_window, text="ID")
        self.input_id_s3 = tk.Entry(self.update_product_window)
        self.title_name_s3 = tk.Label(self.update_product_window, text="Nom :")
        self.input_name_s3 = tk.Entry(self.update_product_window)
        self.title_description_s3 = tk.Label(self.update_product_window, text="Description :")
        self.input_description_s3 = tk.Entry(self.update_product_window)
        self.title_prix_s3 = tk.Label(self.update_product_window, text="Prix :")
        self.input_prix_s3 = tk.Entry(self.update_product_window)
        self.title_quantite_s3 = tk.Label(self.update_product_window, text="Quantité :")
        self.input_quantite_s3 = tk.Entry(self.update_product_window)
        self.title_categorie_s3 = tk.Label(self.update_product_window, text="Id Categorie")
        self.input_categorie_s3 = tk.Entry(self.update_product_window)
        self.valid_state_s3 = tk.Button(self.update_product_window, text="OK")
        self.valid_state_s3.config(command=self.update_product_sql)
        self.state3 = [self.aff_id_s3, self.input_id_s3, self.title_name_s3, self.input_name_s3,
                       self.title_description_s3, self.input_description_s3, self.title_prix_s3, self.input_prix_s3,
                       self.title_quantite_s3, self.input_quantite_s3, self.title_categorie_s3, self.input_categorie_s3,
                       self.valid_state_s3]
        for element in self.state3:
            element.pack()

    def update_product_sql(self):
        self.stock.update_product(self.input_id_s3.get(), self.input_name_s3.get(), self.input_description_s3.get(),
                               self.input_prix_s3.get(), self.input_quantite_s3.get(), self.input_categorie_s3.get())
        self.render_tree()
        self.update_product_window.destroy()

    # State 4 : export csv.



    # State 0 : display products / main window.
    def render(self):
        self.current_screen = []
        self.tree_product.pack()
        self.current_screen.append(self.tree_product)
        for element in self.state0:
            element.pack()
            self.current_screen.append(element)
        self.window.mainloop()


main = Main()
main.render()