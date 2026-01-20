from flask import Flask,render_template,request
from analysis import load,trend,staff,indicators
from forecast import forecast
from booking import find_low
import pandas as pd

app=Flask(__name__)

df=load()

# -------- HOME --------
@app.route("/")
def home():
    states=sorted(df['state'].unique())
    return render_template("index.html",states=states)


# -------- DISTRICT --------
@app.route("/district")
def district():

    state=request.args.get("state")

    d=sorted(df[df['state']==state]['district'].unique())

    return render_template("district.html",
        state=state,
        districts=d)


# -------- PINCODE --------
@app.route("/pincode")
def pincode():

    state=request.args.get("state")
    district=request.args.get("district")

    p=df[
        (df['state']==state) &
        (df['district']==district)
    ]['pincode'].unique()

    return render_template("pincode.html",
        state=state,
        district=district,
        pincodes=p)


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():

    state=request.args.get("state")
    district=request.args.get("district")
    pincode=request.args.get("pincode")

    t=trend(df,state,district,pincode)

    f=forecast(df,state,district,pincode,14)

    t['staff']=t['total'].apply(staff)

    ind=indicators(df)

    return render_template("dashboard.html",
        trend=t.to_dict('records'),
        forecast=f,
        ind=ind.to_dict('records'),
        state=state,
        district=district,
        pincode=pincode)


# -------- BOOKING --------
@app.route("/booking",methods=['POST'])
def booking():

    state=request.form['state']
    district=request.form['district']
    pincode=request.form['pincode']

    date=pd.to_datetime(
        request.form['date'],
        dayfirst=True
    )

    r=find_low(df,state,district,pincode,date)

    return render_template("booking.html",result=r)


app.run(debug=True)
