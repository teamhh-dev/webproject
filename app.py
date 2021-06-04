from flask import Flask,render_template,redirect,session
from flask.globals import request
from DBHandler import *
from werkzeug.utils import secure_filename



app=Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    db=DBHandler(app.config['DB_HOST'],app.config['DB_ID'],app.config['DB_PASSWORD'],app.config['DB_NAME'])
    print(db.getAllMedicines())
    medicines_list=db.getAllMedicines()
    return render_template("index.html",medicines=medicines_list)

@app.route('/haseeb')
def haseeb():
    return index()

@app.route('/add-medicine',methods=['POST','GET'])
def addMedicine():
    db=DBHandler(app.config['DB_HOST'],app.config['DB_ID'],app.config['DB_PASSWORD'],app.config['DB_NAME'])

    if request.method=="POST":
        if request.form['Submit']=="Save":
            imageExtensionFlag=True

            name=request.form['name']
            category=request.form['category']
            unit=request.form['unit']
            details=request.form['details']
            price=request.form['price']
            manufacturerName=request.form['manufacturername']
            manufacturerPrice=request.form['manufacturerprice']
            image=request.files['image']
            imageName=secure_filename(str(db.getImageName())+"."+image.filename.split(".")[1])

            if not imageName.split(".")[1] in app.config['ALLOWED_EXTENSIONS']:
                imageExtensionFlag=False

            print(name,category,unit,details,price,manufacturerName,manufacturerPrice,imageName,imageExtensionFlag)    
            if imageExtensionFlag:      
                if db.addMedicine(name,category,unit,details,price,manufacturerName,manufacturerPrice,imageName):
                    try:
                        image.save(app.config['UPLOAD_FOLDER']+imageName)
                    except Exception as e:
                        print(e.__str__())
                    return render_template("add-medicine.html",status="Added Medicine!")
                else:
                    return render_template("add-medicine.html",status="Error Adding Medicine!")

    return render_template("add-medicine.html")

@app.route('/medicine-list')
def medicineList():
    db=DBHandler(app.config['DB_HOST'],app.config['DB_ID'],app.config['DB_PASSWORD'],app.config['DB_NAME'])
    print(db.getAllMedicines())
    medicines_list=db.getAllMedicines()
    for medicine in medicines_list:
        medicine['image']="medicine_images/"+medicine['image']
    return render_template("medicine-list.html",medicines=medicines_list)
if __name__=="__main__":
    db=DBHandler(app.config['DB_HOST'],app.config['DB_ID'],app.config['DB_PASSWORD'],app.config['DB_NAME'])
    print(db.getAllMedicines())
    app.run(debug=True)
