import mysql.connector
import traceback


class Conexion:
    
    def __init__(self):
        self.__hostBD = "localhost"
        self.__usuarioBD = "user"
        self.__contrasenaBD = '1234' #type: ignore
        self.__dataBase = "dblce"
        self.__portBD = "3306"
        
        try:
            self.conexion = mysql.connector.connect(user=self.__usuarioBD, password=self.__contrasenaBD, host=self.__hostBD, database=self.__dataBase, port=self.__portBD)
            self.cur = self.conexion.cursor()
            print("conexion exitosa")  
        except :
            
            print("Error de conexion, No se pudo conectar a la base de datos")
            traceback.print_exc()          
            

    def __del__(self):
        self.cur.close()
        self.conexion.close()
        print("conexion cerrada")


