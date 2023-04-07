from database import Database, db
from tkinter import *
from tkinter import ttk
from tkinter import Button


def display_data():
    return db.readProducts()


def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


class App(Database):
    def __init__(self):
        self.database = Database
        self.root = Tk()
        self.root.title("Inventory Store System")
        self.root.geometry("1250x300")
        self.my_tree = ttk.Treeview(self.root)

        # Création des labels et des champs d'entrée.
        self.entryNom = Entry(self.root, width=30)
        self.entryDescription = Entry(self.root, width=30)
        self.entryPrix = Entry(self.root, width=30)
        self.entryQuantite = Entry(self.root, width=30)
        self.entryIdCategorie = Entry(self.root, width=30)

        self.entryNom.grid(row=1, column=1, padx=20)
        self.entryDescription.grid(row=2, column=1, padx=20)
        self.entryPrix.grid(row=3, column=1, padx=20)
        self.entryQuantite.grid(row=4, column=1, padx=20)
        self.entryIdCategorie.grid(row=5, column=1, padx=20)

        self.entryNomLabel = Label(self.root, text="Nom")
        self.entryDescriptionLabel = Label(self.root, text="Description")
        self.entryPrixLabel = Label(self.root, text="Prix")
        self.entryQuantiteLabel = Label(self.root, text="Quantité")
        self.entryIdCategorieLabel = Label(self.root, text="ID catégorie")

        self.entryNomLabel.grid(row=1, column=0)
        self.entryDescriptionLabel.grid(row=2, column=0)
        self.entryPrixLabel.grid(row=3, column=0)
        self.entryQuantiteLabel.grid(row=4, column=0)
        self.entryIdCategorieLabel.grid(row=5, column=0)

        # création des boutons.
        self.insertButton = Button(self.root, text="Ajouter", padx=5, pady=5, width=5, bd=3, font=('Open Sans', 13),
                                   bg="#090764", command=self.insert_data)
        self.deleteButton = Button(self.root, text="Supprimer", padx=5, pady=5, width=5, bd=3, font=('Open Sans', 13),
                                   bg="#090764", command=self.delete_data)
        self.updateButton = Button(self.root, text="Modifier", padx=5, pady=5, width=5, bd=3, font=('Open Sans', 13),
                                   bg="#090764", command=self.update_data)
        self.displayButton = Button(self.root, text="Afficher", padx=5, pady=5, width=5, bd=3, font=('Open Sans', 13),
                                    bg="#090764", command=display_data)

        self.insertButton.grid(row=6, column=0, pady=10)
        self.deleteButton.grid(row=6, column=1)
        self.updateButton.grid(row=6, column=2)
        self.displayButton.grid(row=6, column=3)

        # création de l'arborescence pour afficher la liste des produits.
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=('Open Sans', 15))

        self.my_tree['columns'] = ("ID", "Nom", "Description", "Prix", "Quantité", "ID catégorie")
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=CENTER, width=50)
        self.my_tree.column("Nom", anchor=CENTER, width=150)
        self.my_tree.column("Description", anchor=CENTER, width=200)
        self.my_tree.column("Prix", anchor=CENTER, width=100)
        self.my_tree.column("Quantité", anchor=CENTER, width=100)
        self.my_tree.column("ID catégorie", anchor=CENTER, width=100)

        self.my_tree.heading("ID", text="ID", anchor=W)
        self.my_tree.heading("Nom", text="Nom", anchor=W)
        self.my_tree.heading("Description", text="Description", anchor=W)
        self.my_tree.heading("Prix", text="Prix", anchor=W)
        self.my_tree.heading("Quantité", text="Quantité", anchor=W)
        self.my_tree.heading("ID catégorie", text="ID catégorie", anchor=W)

        self.my_tree.tag_configure('orow', background="#DED7C1", font=('Open Sans', 15))
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

        for self.data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for self.result in reverse(db.readProducts()):
            self.my_tree.db.addProduct(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background="#DED7C1", font=('Open Sans', 15))
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    # ajouter un produit.
    def insert_data(self):
        itemNom = str(self.entryNom.get())
        itemDescription = str(self.entryDescription.get())
        itemPrix = str(self.entryPrix.get())
        itemQuantite = str(self.entryQuantite.get())
        itemIdCategorie = str(self.entryIdCategorie.get())
        if itemNom == "" or itemNom == " ":
            print("Error Inserting Name")
        if itemDescription == "" or itemDescription == " ":
            print("Error Inserting Description")
        if itemPrix == "" or itemPrix == " ":
            print("Error Inserting Price")
        if itemQuantite == "" or itemQuantite == " ":
            print("Error Inserting Quantity")
        if itemIdCategorie == "" or itemIdCategorie == " ":
            print("Error Inserting Id Categorie")
        else:
            db.addProduct(str(itemNom), str(itemDescription), str(itemPrix), str(itemQuantite),
                          str(itemIdCategorie))

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in reverse(readProducts()):
            self.my_tree.db.addProduct(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, pdx=10, pady=10)

    # supprimer un produit.
    def delete_data(self):
        selected_item = self.my_tree.selection()[0]
        deleteData = str(self.my_tree.item(selected_item)['values'][0])
        db.deleteProduct(deleteData)

        for data in self.my_tree.get_children():
            self.my_tree.db.deleteProduct(data)

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, pdx=10, pady=10)

    # modifier un produit.
    def update_data(self):
        selected_item = self.my_tree.selection()[0]
        update_nom = self.my_tree.item(selected_item)['values'][0]
        db.updateProduct(self.entryNom.get(), self.entryDescription.get(), self.entryPrix.get(),
                         self.entryQuantite.get(), self.entryIdCategorie.get(), update_nom)

        self.root.mainloop()


# lance le programme principal.
if __name__ == "__main__":
    root = Tk()
    app = App()
    root.mainloop()
