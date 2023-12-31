from recuperer import *
from analyse import *
'''3. Evaluer la qualité des données et la préparation nécessaires pour qu’elles soient le mieux 
exploitables (ex : valeurs manquantes, valeurs dupliquées.)'''
# Afficher les aéroports qui ont le plus de vols
def queshizhi(df):
    queshi_cols = []
    for i in df.columns:
        if df.where(F.col(i).isNull()).count() > 0:
            queshi_cols.append(i)
    return queshi_cols
#print(queshizhi(df_raw))

# Afficher les aéroports qui ont le plus de vols
def dayingqueshizhi(df):
    for i in df.columns:
        print(i, df.where(F.col(i).isNull()).count())
#dayingqueshizhi(df_raw)

# Afficher les types de données
def print_dtypes(df):
    for column, dtype in df.dtypes:
        print(f'{column}: {dtype}')
#print_dtypes(df_raw)        

#Supprimer les valeurs manquantes
df_raw=df_raw.dropna()
df_fli=df_fli.dropna()
df_air=df_air.dropna()

# Supprimer les doublons
df_raw=df_raw.dropDuplicates()
df_fli=df_fli.dropDuplicates()
df_air=df_air.dropDuplicates()

#Supprimer les valeurs aberrantes
def shanchuyichangzhi(df):
    for col in df.columns :
        if col != 'Carrier':
            Q1 = df.stat.approxQuantile(col, [0.25], 0)
            Q3 = df.stat.approxQuantile(col, [0.75], 0)
            IQR = Q3[0] - Q1[0]
            lower_bound = Q1[0] - 1.5 * IQR
            upper_bound = Q3[0] + 1.5 * IQR
            df = df.filter((F.col(col) >= lower_bound) & (F.col(col) <= upper_bound))
    return df
df_raw=shanchuyichangzhi(df_raw)
df_fli=shanchuyichangzhi(df_fli)

#Convertir le type de données
df_air = df_air.withColumn('airport_id', df_air['airport_id'].cast(IntegerType()))
for i in df_fli.columns:
    if i != 'Carrier':
        df_fli = df_fli.withColumn(i, df_fli[i].cast(IntegerType()))
for i in df_raw.columns:
    if i != 'Carrier':
        df_raw = df_raw.withColumn(i, df_raw[i].cast(IntegerType()))

