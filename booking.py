def find_low(df,state,district,pincode,date):

    d=df[
        (df['state']==state) &
        (df['district']==district)
    ]

    if pincode:
        d=d[d['pincode']==int(pincode)]

    d=d[d['date']==date]

    g=d.groupby(['pincode'])['total'].sum().reset_index()

    g=g[g['total']<25]

    return g.to_dict('records')
