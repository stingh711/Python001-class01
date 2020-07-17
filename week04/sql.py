import pandas as pd
import numpy as np

data = pd.DataFrame()

# select * from data;
data

# select * from data limit 10;
data.head(10)

# select id from data;
data["id"]

# select count(id) from data;
data["id"].count()

# select * from data where id <1000 and age > 30;
data[(data["id"] < 1000) & (data["age"] > 30)]

# select id, count(distinct order_id) from table1 group by id;

table1 = pd.DataFrame()
table1.groupby("id").aggregate({"order_id": "count"})

# SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
table2 = pd.DataFrame()
table1.merge(table2, on="id")

# SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([table1, table2])

# DELETE FROM table1 WHERE id=10;
table1 = table1.loc[table1["id"] != 10]

# ALTER TABLE table1 DROP COLUMN column_name;
table1.drop(columns=["column_name"])
