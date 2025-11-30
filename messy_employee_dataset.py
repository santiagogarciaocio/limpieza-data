# -*- coding: utf-8 -*-
"""Messy Employee Dataset.ipynb

Objetivos:
    - limpieza de data frame .csv
"""
import pandas as pd


"""
Primer paso.

Cargar el csv. 
    Chequeo de encoding, delimitador
"""

messy_data_csv = "Messy_Employee_dataset.csv"

df = pd.read_csv(messy_data_csv) #cargo el df. 

"""
Segundo paso.

Inspeccionar data set
"""

# hago head y tail para darme una idea con que estoy trabajando
df.head()

df.tail()

#con info veo que tengo 1020 filas. En la columna 'Age' tengo 809 celdas con valores. En la columna 'Salary'
df.info()

#Veo si tengo filas duplicadas
df.duplicated().sum()

#Analizis de valores unicos por columna. ' First_Name' y 'Last_Name' tienen pocos valores únicos porque el data set es fabricado, no hay problema ahi. 
#'Department_Region' tiene 36, un valor alto que tendré que analizar.
#'Email' y 'Phone' tienen 1020 valores unicos, no hay problemas aca
df.nunique()

#Analiziz univariable para detectar posibles problemas. Encuentro que panda tomo a los valores 'phones' como numeros muy pequeños
df.describe()

#cuantifico la data faltante. 'Age' tiene 211 datos faltantes; 'Salary' tiene 24 datos faltantes.
df.isnull().sum()


#Problemas a solucionas: Valores faltantes en 'Age' y 'Salary'. Typo de 'Phone'

"""
Tercer paso.

Estandarizar nombre de columnas. 
Corregir tipo de datos.
Solucionar los valores faltantes
"""

#estandarizao el nombre de las columnas. snake_case y minuscula para todos, eliminado espacio iniciales y finales.
df.columns = df.columns.str.lower().str.replace(' ','_').str.strip()

#demarco la columna 'employee_id' como el indice
df.set_index('employee_id', inplace=True)

#arreglo el tipo de la columna 'phone'
df['phone'] = df['phone'].astype(str)

#datos faltantes
#Elimino las filas sin valores de 'salary' dado que son estadisitcamente pocos, 2.35%, No los completo con media/mediana dado que son un valor estadisticamente importante que no quiero que me sesgo futuras conclusiones
df.dropna(subset='salary', inplace=True)

#Reyeno los valores faltantes de 'age' con la mediana. Eliminar el 20% de mi data es muy costoso; la mediana es la que menos me altera cualquier trabajo futuro.
median_age = df['age'].median()

df['age'].fillna(median_age,inplace=True)

#Chequeo que este todo bien
df.info()

"""
Cuarto paso.

Estandarizacion de los valores. Hacer la data consistente
"""
#limpieza de data erronea. Modificacion del tipo de dato de 'phone'
df['phone'] = df['phone'].str.replace(r'\D', '', regex=True)
df['phone'] = df['phone'].str.slice(-10)

#separacion de 'department_region' en dos columnas diferentes.
df[['department','region']] = df['department_region'].str.split('-',expand=True)

df.drop('department_region',axis=1, inplace=True)

#modificacion del tipo de dato de 'join_date' de string a panda datetime
df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')


"""
Quinto paso.

Chequeo final de que todo este bien
"""
df.info()

df.describe()


"""
Sexto paso.

Exportar el data set limpio
"""
df.to_csv('clean_employee_dataset.csv', index=True)
