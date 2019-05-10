from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="template")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:money@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(200))
    blog_body = db.Column(db.String(2000))

    def __init__(self, blog_title, blog_body):
        self.blog_title = blog_title
        self.blog_body = blog_body


@app.route("/", methods = ["GET"])
def blog():
    blogz = Blog.query.all()
    return render_template("index.html", title="Build-A-Blog", blogz=blogz)


@app.route("/newpost", methods = ["GET", "POST"])
def newpost():

    title_error=""
    body_error=""

    if request.method =='POST':
        blog_title = request.form["blog_title"]
        blog_body = request.form["blog_body"]

        #Title Validation
        if blog_title == "":
            title_error = "Please Fill In The Title"
        
        #Body Validation
        if blog_body == "":
            body_error = "Please Fill In The Body"


        if title_error == "" and body_error =="":
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template("postpage.html", blog=new_blog)
        else:
            return render_template("newpost.html", title_error=title_error, body_error=body_error)
    return render_template("newpost.html", title="Build-A-Blog")

       



@app.route("/postpage")
def postpage():
    identity = int(request.args.get("id"))
    bl = Blog.query.get(identity)
    return render_template("postpage.html", blog=bl)

if __name__ == "__main__":
    app.run()