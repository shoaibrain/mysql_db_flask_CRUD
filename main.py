from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'artgallery'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  artist.aID,artist.name,artist.birthDate,artist.commission,artist.city,artist.street FROM artist")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', artists=data )

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        birthDate = request.form['birthDate']
        commission = request.form['commission']
        city = request.form['city']
        street = request.form['street']
        stateAb = request.form['stateAb']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM artist")
        aID = len(cur.fetchall())+1
        cur.execute("INSERT INTO artist (aID,name, birthDate, deathDate, commission, street, city, stateAb, zipcode) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)", (aID, name, birthDate, None, commission, street, city, stateAb, '12345'))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM artist WHERE artist.aID=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        aID = request.form['aID']
        name = request.form['name']
        birthDate = request.form['birthDate']
        deathDate = request.form['deathDate']
        commission = request.form['commission']
        street = request.form['street']
        city = request.form['city']
        stateAb = request.form['stateAb']
        zipcode = request.form['zipcode']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE artist
               SET name=%s,birthDate=%s, deathDate=%s, commission=%s, street=%s, city=%s, stateAb=%s,zipcode=%s
               WHERE aID=%s
            """, (name, birthDate, deathDate, commission, street, city, stateAb, zipcode, aID))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
