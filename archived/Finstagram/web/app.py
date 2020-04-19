from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.utils import secure_filename
from bcrypt import hashpw, gensalt
import pymysql.cursors
import os

#Initialize the app from Flask
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads/')

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='IntroDB',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    try:
        user = session['username']
    except:
        return render_template('index.html')
    return render_template("home.html", username=user)

#Define route for login
@app.route('/login')
def login():
    try:
        user = session['username']
    except:
        return render_template("login.html")
    return render_template('home.html', username=user)

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    salt = b'$2b$12$KlB/cYzDF02ncvH3Z3ZU5e'
    password = hashpw(password.encode(), salt).decode('utf-8') #decode hash from bytes to string

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    salt = b'$2b$12$KlB/cYzDF02ncvH3Z3ZU5e'
    password = hashpw(password.encode(), salt).decode('utf-8') #decode hash from bytes to string

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:


        ins = 'INSERT INTO Person (username, password, isPrivate) VALUES(%s, %s, 1)'
        cursor.execute(ins, (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/postpage')
def post_page():
    try:
        user = session['username']
    except:
        return render_template("login.html")
    return render_template('postpage.html')


@app.route('/accountpage')
def account_page():
    try:
        user = session['username']
    except:
        return render_template("login.html")
    cursor = conn.cursor();
    query = 'SELECT * FROM Person WHERE username=%s'
    cursor.execute(query, (user))
    data = cursor.fetchone()
    if data['isPrivate'] == 0:
        data['isPrivate'] = 'public'
    else:
        data['isPrivate'] = 'private'
    return render_template('accountpage.html', username=data['username'], f=data['fname'], l=data['lname'], bio=data['bio'], avatar=data['avatar'], priv=data['isPrivate'])

@app.route('/followers')
def followers():
    try:
        user = session['username']
    except:
        return render_template("login.html")
    return render_template('followers.html')

@app.route('/account')
def account():
    try:
        user = session['username']
    except:
        return render_template("login.html")
    return render_template('account.html', username=user)

@app.route('/updateAccount', methods=['POST', 'GET'])
def updateAccount():
    try:
        user = session['username']
    except:
        return render_template("login.html")
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    avatar = request.files['avatar']
    bio = request.form['bio']
    isPrivate = request.form['isPrivate']

    salt = b'$2b$12$KlB/cYzDF02ncvH3Z3ZU5e'
    password = hashpw(password.encode(), salt).decode('utf-8') #decode hash from bytes to string

    cursor = conn.cursor()

    if not os.path.isdir(app.config['UPLOAD_FOLDER'] + user):
        os.mkdir(app.config['UPLOAD_FOLDER'] + user)
    if check_file_extension(avatar.filename, ['jpg', 'png', 'jpeg', 'gif']):
        file_name = secure_filename(avatar.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user, file_name)
        avatar.save(file_path)
    else:
        return render_template("file_upload_error.html")

    ins = 'UPDATE Person SET password=%s, fname=%s, lname=%s, avatar=%s, bio=%s, isPrivate=%s WHERE username=%s'
    cursor.execute(ins, (password, fname, lname, file_path, bio, isPrivate, user))
    conn.commit()
    cursor.close()
    return render_template('home.html', username=user)

@app.route('/home')
def home():
    try:
        user = session['username']
    except:
        return render_template("index.html")
    return render_template('home.html', username=user)


def check_file_extension(file_name, extensions):
    """
    file_name: file name
    extensions: list of valid file extensions
    """
    extension = file_name.rsplit('.', 1)[1].lower()
    if extension in extensions:
        return True
    return False

@app.route('/post', methods=['GET', 'POST'])
def post():
    try:
        username = session['username']
    except:
        return render_template("login.html")


    image = request.files['image']
    caption = request.form['caption']
    all_followers = request.form['allFollowers']

    if check_file_extension(image.filename, ['jpg', 'png', 'jpeg', 'gif']):
        file_name = secure_filename(image.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], username, file_name)
        image.save(file_path)
    else:
        return render_template("file_upload_error.html")

    cursor = conn.cursor();
    query = 'INSERT INTO Photo (photoOwner, filePath, caption, allFollowers)  VALUES(%s, %s, %s, %s)'
    cursor.execute(query, (username, file_path, caption, all_followers))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/follow', methods=['POST', 'GET'])
def follow():
    try:
        username = session['username']
    except:
        return render_template("login.html")
    to_follow = request.form['follow']
    if username == to_follow:
        return render_template('error.html', error="you can't follow yourself!")

    cursor = conn.cursor()
    query = 'SELECT * FROM Follow WHERE followerUsername = %s and followeeUsername=%s'
    cursor.execute(query, (username, to_follow))
    data = cursor.fetchone()
    if(data):
        query = 'SELECT acceptedfollow FROM Follow WHERE followerUsername = %s and followeeUsername=%s'
        cursor.execute(query, (username, to_follow))
        data = cursor.fetchone()
        data = data['acceptedfollow']
        if data:
            error = 'already following ' + to_follow
            return render_template('error.html', error=error)
        else:
            error = to_follow + " hasn't accepted your follow request or has declined"
            return render_template('error.html', error = error)
    else:
        query = 'SELECT * FROM Person WHERE username=%s'
        cursor.execute(query, (to_follow))
        data = cursor.fetchone()
        if data:
            query = 'INSERT INTO Follow (followerUsername, followeeUsername, acceptedfollow) VALUES (%s, %s, 0)'
            cursor.execute(query, (username, to_follow))
            conn.commit()
            return render_template('success.html', msg='follow request sent to ' + to_follow)
        else:
            error = to_follow + ' is not a valid username'
            return render_template('error.html', error=error)
    return render_template("home.html", username=username)

@app.route('/followreqs', methods=['POST', 'GET'])
def follow_reqs():
    try:
        user = session['username']
    except:
        return render_template('login.html')
    cursor = conn.cursor()
    query = 'SELECT * FROM Follow WHERE followeeUsername=%s AND acceptedfollow=0'
    cursor.execute(query, (user))
    reqs = cursor.fetchall()
    return render_template('followreqs.html', followreqs=reqs)



@app.route('/accept_follow/<username>', methods=['GET', 'POST'])
def accept_follow(username):
    try:
        user = session['username']
    except:
        return render_template('login.html')
    ans = request.form['Accept']
    cursor = conn.cursor()
    if ans == 1:
        query = 'UPDATE Follow SET acceptedfollow=1 WHERE followeeUsername=%s AND followerUsername=%s'
        msg = 'Accpeted ' + username + '\'s follow request.'
    else:
        query = 'DELETE FROM Follow WHERE followeeUsername=%s AND followerUsername=%s'
        msg = 'Rejected ' + username + '\'s follow request.'
    cursor.execute(query, (user, username))
    conn.commit()
    cursor.close()
    return render_template('success.html', msg=msg)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    try:
        user = session['username']
    except:
        return render_template('login.html')
    return render_template('groups.html')

@app.route('/create_group', methods = ['GET', 'POST'])
def create_group():
    try:
        user = session['username']
    except:
        return render_template('login.html')
    group_name = request.form['group_name']
    cursor = conn.cursor()
    query = 'INSERT INTO CloseFriendGroup (groupName, groupOwner) VALUES(%s, %s)'
    cursor.execute(query, (group_name, user))
    conn.commit()
    cursor.close()
    msg = group_name + " made."
    return render_template('success.html', msg=msg)

@app.route('/view_groups', methods=['GET', 'POST'])
def view_groups():
    try:
        user = session['username']
    except:
        return render_template('login.html')
    cursor = conn.cursor()
    query = 'SELECT groupName FROM CloseFriendGroup WHERE groupOwner=%s'
    cursor.execute(query, (user))
    groups = cursor.fetchall()
    return render_template('view_groups.html', groups=groups)

@app.route('/group/<group_name>', methods=['GET', 'POST'])
def view_group(group_name):
    try:
        user = session['username']
    except:
        return render_template('login.html')
    cursor = conn.cursor()
    query = 'SELECT username FROM Belong WHERE groupOwner=%s and groupName=%s'
    cursor.execute(query, (user, group_name))
    users = cursor.fetchall()
    return render_template('group.html', group_name=group_name, users=users)

@app.route('/remove_from_group/<group_name>', methods = ['GET', 'POST'])
def remove_from_group(group_name):
    try:
        user = session['username']
    except:
        return render_template('login.html')
    username = request.form['username']
    cursor = conn.cursor()
    query = ''
    cursor.execute(query, ())
    conn.commit()
    cursor.close()
    msg = username + " deleted from " + group_name
    return render_template('success.html', msg=msg)



@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'you will never guess me!'
if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug = True)
