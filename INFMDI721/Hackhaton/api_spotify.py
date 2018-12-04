# Import Librairies
import pandas as pd
import numpy as np
from scipy import stats as scs
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', 60)

# Import data
path = "C:/Users/Pascal/Desktop/Telecom ParisTech/Cours/INFMDI780 - Projet BigData/Data/"
file_data = "t3_all_fr_prices_posweekly_prod_without_price.csv"
file_ref = "2018.11.21_innoscape_internal_architecture.csv"
df_data = pd.read_csv(path+file_data, sep = ",")
df_ref = pd.read_csv(path+file_ref, sep = ",")

# On s'intéresse aux features product family
product_family_source = df_data["t3_all_fr_prices_posweekly_prod.productfamily_seller"]
product_family_initial_ref = df_ref["productfamily_seller"]
prodcategory1_initial_ref = df_ref["prodcategory1_seller"]
prodcategory2_initial_ref = df_ref["prodcategory2_seller"]

product_family_source = product_family_source.dropna()
product_family_initial_ref = product_family_initial_ref.dropna()
lol = product_family_initial_ref.isna()
prodcategory1_initial_ref = prodcategory1_initial_ref.dropna()
prodcategory2_initial_ref = prodcategory2_initial_ref.dropna()
product_family_initial_ref[lol]
product_family_initial_ref[100]
