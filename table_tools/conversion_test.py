import pandas as pd
import os

table_path = os.path.join(os.getcwd(),'cfde_association.txt')
association_table = pd.read_csv(table_path,sep='\t')

print(association_table.dtypes)
print(association_table.head(11))