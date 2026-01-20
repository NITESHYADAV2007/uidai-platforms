import pandas as pd

def forecast(df,state,district,pincode=None,days=14):

    d=df[
        (df['state']==state) &
        (df['district']==district)
    ]

    if pincode:
        d=d[d['pincode']==int(pincode)]

    g=d.groupby('date')['total'].sum().reset_index()

    avg=g['total'].tail(14).mean()

    future=[]

    last=g['date'].max()

    for i in range(days):

        future.append({
            "date": last + pd.Timedelta(days=i+1),
            "predicted": round(avg,1)
        })

    return future
