import presto
import pandas as pd
import numpy as np


def presto_query(query,
                 user='test',
                 catalog='pulsar',
                 schema='public/default',
                 host='localhost',
                 port=8081):
    conn = presto.dbapi.connect(
        host=host,
        port=port,
        user=user,
        catalog=catalog,
        schema=schema)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    columns = cur.description
    df = pd.DataFrame(data)
    df.columns = [x[0] for x in columns]
    return df.replace('', np.nan)