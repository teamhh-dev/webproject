import pymysql
from pymysql.cursors import DictCursor
from werkzeug.datastructures import cache_property
from werkzeug.utils import ArgumentValidationError

class DBHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        try:
            self.connect()
        except Exception as e:
            raise Exception("<h1>No Db Connection</h1>")
    def connect(self):
        try:
            self.db=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            self.cursor=self.db.cursor(DictCursor)
            self.cursor.execute("CREATE TABLE if not exists `medicine_list` ( `id` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(100) NOT NULL , `category` VARCHAR(20) NOT NULL , `unit` VARCHAR(20) NOT NULL , `details` VARCHAR(1000) NOT NULL , `price` FLOAT(10,2) NOT NULL , `manufacturer_name` VARCHAR(50) NOT NULL , `manufacturer_price` FLOAT(10,2) NOT NULL , `image` VARCHAR(200) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
            self.db.commit()
        except Exception as e:
            raise Exception("<h1>No Db Connection</h1>")
    def getImageName(self):
        query="SELECT `AUTO_INCREMENT` as imagename FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'pharma' AND TABLE_NAME = 'medicine_list'"
        self.cursor.execute(query)
        name=self.cursor.fetchone()
        return name['imagename']

    def addMedicine(self,name,category,unit,details,price,manufacturerName,manufacturerPrice,imageName):
        query="INSERT INTO `medicine_list` (`id`, `name`, `category`, `unit`, `details`, `price`, `manufacturer_name`, `manufacturer_price`, `image`) VALUES (NULL, %s, %s, %s,%s, %s,%s,%s,%s)"
        args=(name,category,unit,details,price,manufacturerName,manufacturerPrice,imageName)
        try:
            self.cursor.execute(query,args)
            self.db.commit()
        except Exception as e:
            print(e.__str__())
            return False
        return True
    def getAllMedicines(self):

        medicine_list=[]
        self.cursor.execute("Select * from medicine_list")

        for medicine in self.cursor:
            medicine_list.append(medicine)

        return medicine_list