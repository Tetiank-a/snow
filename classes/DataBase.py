app = Flask(__name__)
app.secret_key = 'myawesomesecretkey'
app.config["MONGO_URI"] = "mongodb+srv://ronia:2021@cluster0.wdfgt.mongodb.net/snowDB?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db