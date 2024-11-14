from flask import *
import pymysql

app = Flask(__name__)


app.secret_key = "2345678oiuytredfghjklytgjhmgfhtfc78ughvnhf"




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



    # CLOTHES QUERY
   
    sql3 = 'SELECT * FROM `products` WHERE product_category = "Clothes"'
    cursor3 = connection.cursor()
    cursor3.execute(sql3)
    Clothes = cursor3.fetchall()
    return render_template("index.html", Electronics=Electronics, Smartphones=Smartphones, Clothes=Clothes)


# Below is a route that will fetch a single product by use of the product id
@app.route("/single_page/<product_id>")
def single_page(product_id):
    # create a db connection
    connection = db_connection()

    # structure the sql query to fetch a single record of the database based on the product id
    sql = "SELECT * FROM `products` WHERE product_id = %s"

    # create a cursor that will enable you to execute the sql
    cursor = connection.cursor()

    # Use the cursor to execute the sql replacing the placeholder with an actual product id
    cursor.execute(sql, product_id)

    # create a variable that will hold the details of a single product fetched from the database
    product = cursor.fetchone()

    # Below we are going to fetch all the products that are in the category of the chosen product
    category = product[4]
    sql2 = "SELECT * FROM `products` WHERE product_category = %s"
    cursor2 = connection.cursor()
    cursor2.execute(sql2, category)
    similar = cursor2.fetchall()
    
    return render_template("single_page.html", product = product, similar = similar)


# Register Route
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        phone = request.form['phone']
        profile_picture = request.files['profile_picture']
        profile_picture.save("static/images/" + profile_picture.filename)

        if password1 != password2:
            return render_template("register.hmtl", error = 'Passwords do match')
        elif len(password1) < 6:
            return render_template('register.html', error = "Password length must be more than 6" )
        else:
            # Create a db connection
            connection = db_connection()

            # Structure sql query to enter a new user into the database
            sql = "INSERT INTO `users`(`username`, `first_name`, `last_name`, `password`, `email`, `phone_number`, `profile_picture`) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            # create a variable that will hold all the data gotten from the form
            data = (username, first_name, last_name, password1, email, phone, profile_picture.filename)

            # create a cursor
            cursor = connection.cursor()

            # use the cursor to execute the sql
            cursor.execute(sql, data)

            # finish the transaction by use of the commit function
            connection.commit()

            return render_template('register.html', success = "User Registered Successfully")


# Below is the login route
@app.route('/login', methods = ['POST' , 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']

        connection = db_connection()
        
        sql = "SELECT * FROM `users` WHERE username = %s AND password = %s "

        data = (username, password)

        cursor = connection.cursor()
        cursor.execute(sql, data)
        # Fetch the details of one person and store them in a variable
        user = cursor.fetchone()

        if cursor.rowcount == 0:
            return render_template('login.html', error = 'Invalid username or password')
        else:
            # you need to establish a session for this user. You require atleast one parameter to track all the activities done by this userwhen he or she is logged in.
            session['key'] = username
            session['profile_picture'] = user[6]
            return redirect('/')
        

        




@app.route('/logout')
def logout():
    # remobe user from the session
    session.clear()
    return redirect('/')

   
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

# the imports for the mpesa function
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/mpesapayment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href='"/"' class="btn btn-dark btn-sm">Back to Products</a>'


@app.route("/allproducts")
def product():
    
        # create a db connection
        connection = db_connection()
        # create an sql query. The %s is a placeholder, to be replaced with actual data when we execute the sql
        sql = "SELECT * FROM `products`"
        # create a cursor that will help to execute the sql
        cursor = connection.cursor()
        # execute the query
        cursor.execute(sql)

        # fetch one person
        product = cursor.fetchall()
        return render_template("productupdate.html", product=product)



@app.route("/deleteProduct/<product_id>", methods=["POST"])
def delete_product(product_id):
    connection = db_connection()
    cursor = connection.cursor()

    # SQL to delete the user by username
    sql = "DELETE FROM products WHERE product_id = %s"
    cursor.execute(sql, (product_id,))
    connection.commit()
    
    return redirect("/allproducts")  # Redirect back to the user list after deletion


@app.route("/updateProduct/<product_id>", methods=["GET", "POST"])
def update_product(product_id):
    connection = db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        # Get updated data from form
        product_name = request.form.get('product_name')
        product_description = request.form.get('product_description')
        product_price = request.form.get('product_price')
        product_category = request.form.get('product_category')
        product_picture = request.form.get('product_picture')

        # Update the user details in the database
        sql = """
        UPDATE products 
        SET product_name = %s, product_desc = %s, product_cost = %s, product_category = %s, product_image_name = %s
        WHERE product_id = %s
        """
        cursor.execute(sql, (product_name, product_description, product_price, product_category, product_picture,  product_id))
        connection.commit()

        return redirect("/allproducts")  # Redirect to the products list

    # For GET, we display the current user data to be updated
    sql = "SELECT * FROM products WHERE product_id = %s"
    cursor.execute(sql, (product_id,))
    one_product = cursor.fetchone()

    return render_template("product_update_form.html", oneProduct=one_product)





app.run(debug=True)