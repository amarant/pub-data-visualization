

import pandas as pd
import os
#
import global_var
from . import paths
from . import transcode

def load(map_code = None):
    assert map_code == global_var.geography_map_code_france
    df_path         = paths.fpath_tmp.format(map_code = map_code) + '.csv'
    try:
        print('Load df - ', end = '')
        df = pd.read_csv(df_path,
                         header = [0],
                         sep = ';',
                         )
        for col in [global_var.capacity_dt_local]:
            df.loc[:,col] = pd.to_datetime(df[col])
        print('Loaded') 
    except Exception as e:
        print('fail - has to read raw data')
        print(e)
        dikt_capacity = {}
        list_files    = sorted([fname
                                for fname in os.listdir(paths.folder_raw)
                                if os.path.splitext(fname)[1] == '.xls'
                                ])
        for ii, fname in enumerate(list_files):
            print('\r{0:3}/{1:3} - {2}'.format(ii,
                                               len(list_files),
                                               fname,
                                               ),
                  end = '',
                  )
            df = pd.read_csv(os.path.join(paths.folder_raw,
                                          fname,
                                          ), 
                             sep       = '\t', 
                             encoding  = 'latin-1',
                             na_values = ["*"],
                             skipinitialspace = True,
                             low_memory       = False,
                             )
            df.columns = [global_var.capacity_mw]
            df = df.dropna(axis = 0, how = 'all')
            df[global_var.capacity_year_local]  = int(df.loc['Type'].item())
            df[global_var.geography_map_code] = map_code
            df = df.drop('Type',
                         axis = 0,
                         )
            df.index.name = global_var.production_source
            df.index      = df.index.astype(str).replace(transcode.production_source)
            dikt_capacity[fname] = df
        print()
    
        df = pd.concat([dikt_capacity[key]
                        for key in dikt_capacity.keys()
                        ],
                       axis = 0,
                       )
        df = df.reset_index()
        df[global_var.geography_map_code] = map_code

        # Save
        print('Save')
        os.makedirs(os.path.dirname(df_path),
                    exist_ok = True,
                    )
        df.to_csv(df_path,
                  sep = ';',
                  index = False,
                  )
    print('done')
    return df


    
    
