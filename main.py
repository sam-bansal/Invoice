from flask import Flask, render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/invoice'
db = SQLAlchemy(app)

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    cname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    Addr1 = db.Column(db.String(50), nullable=False)
    Addr2 = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(6), nullable=False)
    logo = db.Column(db.String(50), nullable=False)
    bustype = db.Column(db.String(10), nullable=False)
    invoices = db.relationship('Invoices', backref='client')

class Addbus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(20), nullable=False)
    cemail = db.Column(db.String(20), nullable=False)
    cweb = db.Column(db.String(20), nullable=False)
    phno = db.Column(db.String(20), nullable=True)
    addr = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    gstin = db.Column(db.String(20), nullable=False)
    logo = db.Column(db.String(20), nullable=False)
    invoices = db.relationship('Invoices', backref='business')


class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoicedate = db.Column(db.Date,default= date.today)
    duedate = db.Column(db.Date,default= date.today)
    #clientname = db.Column(db.String(50),)
    #businessname = db.Column(db.String(50),)
    items = db.relationship('Items', backref='invoice')
    clientid = db.Column(db.Integer, db.ForeignKey('clients.id'))
    businessid = db.Column(db.Integer, db.ForeignKey('addbus.id'))

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.String(20), nullable=False)
    rate = db.Column(db.String(20), nullable=False)
    invoiceid = db.Column(db.Integer, db.ForeignKey('invoices.id'))

@app.route("/addclient", methods = [ 'GET','POST'])
def main():
    if (request.method == 'POST'):
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        cname = request.form.get('cname')
        email = request.form.get('email')
        Addr1= request.form.get('Addr1')
        Addr2 = request.form.get('Addr2')
        zip = request.form.get('zip')
        logo = request.form.get('logo')
        bustype = request.form.get('bustype')
        entry = Clients(fname=fname, lname=lname, cname=cname, email=email, Addr1=Addr1, Addr2=Addr2, zip=zip,logo=logo, bustype=bustype )
        db.session.add(entry)
        db.session.commit()

    return render_template('index.html')

@app.route("/createinvoices", methods=['GET','POST'])
def createinvoices():

    if (request.method == 'POST'):
        clientid = request.form.get('clientid')
        businessid = request.form.get('businessid')
        entry = Invoices(clientid=clientid, businessid=businessid);
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('additem',))

    else:
        client = Clients.query.filter_by().all()
        addbuss = Addbus.query.filter_by().all()
        return render_template('createinvoices.html', clients=client, addbus=addbuss)


@app.route("/additem", methods = [ 'GET','POST'])
def additem():
    invoiceid = Invoices.query.filter_by('-id').all()

    if (request.method == 'POST'):
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        rate = request.form.get('rate')
        invoicedate = request.form.get('invoicedate')
        duedate = request.form.get('duedate')
        entry1 = Items(description=description, quantity=quantity, rate=rate)
        entry = Invoices(invoicedate=invoicedate, duedate=duedate)
        db.session.add(entry)
        db.session.add(entry1)
        db.session.commit()
        return render_template('additem.html')

    else:
        return render_template('additem.html', invoices=invoiceid)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/addbuss", methods = [ 'GET','POST'])
def bussiness():
    if (request.method == 'POST'):
        cname = request.form.get('cname')
        cemail = request.form.get('cemail')
        cweb = request.form.get('cweb')
        phno = request.form.get('phno')
        addr = request.form.get('addr')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        gstin = request.form.get('gstin')
        logo = request.form.get('logo')
        entry = Addbus(cname=cname, cemail=cemail, cweb=cweb, phno=phno, addr=addr, city=city, state=state,
                        country=country, gstin=gstin,logo=logo)
        db.session.add(entry)
        db.session.commit()


    return render_template('addbuss.html')




app.run(debug=True)
