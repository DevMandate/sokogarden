from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def db_connection():
    return pymysql.connect(host='localhost', user='root', password='', database='sokogarden')

@app.route("/")
def home():
    # create a db_connection
    connection = db_connection()

    # structure a query that will show the products in a category Electronics
    sql = 'SELECT * FROM `products` WHERE product_category = "Electronics";'

    # Createc cursor
    cursor = connection.cursor()

    # Execute the query by use of the cursor:
    cursor.execute(sql)

    # create a variable that will store / hold all the records fetched from the database in the category Electronics
    Electronics = cursor.fetchall()

    # SMARTPHONES QUERY

    sql2 = 'SELECT * FROM `products` WHERE product_category = "Smartphones"'

    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    Smartphones = cursor2.fetchall()
    render_template("index.html", Electronics = Electronics ,  Smartphones = Smartphones )


    # CLOTHES QUERY
   
    sql3 = 'SELECT * FROM `products` WHERE product_category = "Clothes"'
    cursor3 = connection.cursor()
    cursor3.execute(sql3)
    Clothes = cursor3.fetchall()
    return render_template("index.html", Electronics=Electronics, Smartphones=Smartphones, Clothes=Clothes)


   
@app.route("/upload", methods = ["GET" , "POST" ])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        product_name = request.form["prodName"]
        product_desc = request.form["prodDesc"]
        product_price = request.form["prodCost"]
        product_category = request.form["prodCategory"]
        product_image = request.files["prodImgName"]
        product_image.save("static/images/" + product_image.filename)

        #Below we create a db connection
        connection = db_connection()

        # Structure the query to insert the different clumns
        sql = "insert into products(product_name, product_desc, product_cost, product_category, product_image_name) values(%s, %s, %s, %s, %s)"

        # create a variable that will hold the data gotten from the form
        data = (product_name, product_desc, product_price, product_category, product_image.filename)

        # create a cursor that will help us execute the sql query
        cursor = connection.cursor()

        # execute the query with the data gotten from the form by use of the cursor
        cursor.execute(sql, data)

        # finish the transaction by use of the commit function
        connection.commit()
        return render_template("upload.html", success = "Product uploaded successfully")







app.run(debug=True)