#import mysql.connector
import traceback
import sqlite3
import os

class Conexion:
    
    def __init__(self):
        
        #self.__hostBD = "\src\db\dbLce.sqlite"
        #self.__usuarioBD = "user"
        
        #self.__contrasenaBD = '1234' #type: ignore
        self.__dataBase = os.getenv("DB_PATH")
        #self.__portBD = "3306"
        
        try:
            self.conexion: sqlite3.connect = sqlite3.connect(self.__dataBase)
            self.cur: sqlite3.Cursor = self.conexion.cursor()
            print("conexion exitosa")  
        except :
            
            print("Error de conexion, No se pudo conectar a la base de datos")
            print(traceback.format_exc())
            

    def __del__(self):
        self.cur.close()
        self.conexion.close()
        print("conexion cerrada")


#cl = Conexion()
#cl.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#print("XDDD", cl.cur.fetchall())