import mysql.connector


class Database:
    def __init__(self):
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

    def readProducts(self):
        self.cursor.execute("SELECT * FROM produit")
        return self.cursor.fetchall()

    def addProduct(self, nom, description, prix, quantite, id_categorie):
        sql = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s);"
        values = (nom, description, prix, quantite, id_categorie)
        self.cursor.execute(sql, values)
        self.connection.commit()

    def updateProduct(self, nom, description, prix, quantite, id_categorie, id_produit):
        self.cursor.execute(
            "UPDATE produit SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s WHERE id = %s;",
            (nom, description, prix, quantite, id_categorie, id_produit))
        self.connection.commit()

    def deleteProduct(self, id):
        self.cursor.execute("DELETE FROM produit WHERE id = {id};")
        self.connection.commit()

    def close(self):
        self.connection.close()


db = Database()
