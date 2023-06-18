import pandas as pd
import global_var as gv

class database_backend():

    def __init__(self):

        filename_josaa = 'data/josaa.csv'
        df = pd.read_csv(filename_josaa)

        filename_csab = 'data/csab.csv'
        df_csab = pd.read_csv(filename_csab)

        stud_name = gv.stud_name
        gender = gv.gender
        main_rank = int(gv.main_rank)
        adv_rank = int(gv.advance_rank)
        quota = gv.quota

        df['Closing Rank'] = df['Closing Rank'].astype(int)
        df_csab['Closing Rank'] = df_csab['Closing Rank'].astype(int)

        csab = df_csab[(df_csab['Gender'] == gender)
                & (df_csab['Seat Type'] == quota)
                & (df_csab['Closing Rank'] >= main_rank - 1000)
                & (df_csab['Closing Rank'] <= main_rank + 5000)]
        
        
        csab.to_csv(f'output/{quota}_{stud_name}_csab_{main_rank}.csv', index=False)

        nit = df[(df['Type'] == 'Mains')
                & (df['Gender'] == gender)
                & (df['Seat Type'] == quota)
                & (df['Closing Rank'] >= main_rank - 300)
                & (df['Closing Rank'] <= main_rank + 1000)]
        
        nit.drop(['Type'],axis=1)
        nit.to_csv(f'output/{quota}_{stud_name}_mains_{main_rank}.csv', index=False)
              
        if adv_rank != 0:
            iit = df[(df['Type'] == 'IIT') 
                & (df['Gender'] == gender)
                & (df['Seat Type'] == quota)
                & (df['Closing Rank'] >= adv_rank)
                & (df['Closing Rank'] <= adv_rank + 200)]
            
            iit.drop(['Type'],axis=1)
            iit.to_csv(f'output/{quota}_{stud_name}_advance_{adv_rank}.csv', index=False)


        
