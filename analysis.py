import pandas as pd

CAPACITY = 35   # per operator

def load():

    files=[
        "data/enrolment_1.csv",
        "data/enrolment_2.csv",
        "data/enrolment_3.csv"
    ]

    li=[]
    for f in files:
        print("Reading:",f)
        d=pd.read_csv(f)
        li.append(d)

    df=pd.concat(li)

    df['date']=pd.to_datetime(df['date'],dayfirst=True)

    df['total']=df['age_0_5']+df['age_5_17']+df['age_18_greater']

    return df


# ---------- TREND ------------
def trend(df,state,district,pincode=None):

    d=df[
        (df['state']==state) &
        (df['district']==district)
    ]

    if pincode:
        d=d[d['pincode']==int(pincode)]

    g=d.groupby('date')['total'].sum().reset_index()

    g['7d']=g['total'].rolling(7).mean()
    g['30d']=g['total'].rolling(30).mean()

    return g


# ---------- STAFF ------------
def staff(n):
    return max(1, round(n/CAPACITY,1))


# ---------- INDICATORS -------
def indicators(df):

    df['adult_ratio']=df['age_18_greater']/df['total']

    g=df.groupby('date').agg({
        'adult_ratio':'mean',
        'total':'sum'
    }).reset_index()

    return g
