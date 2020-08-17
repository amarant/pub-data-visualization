
import pandas as pd
#
import global_var


def assemble(df):
    
    print('\nExtract')
    # Only keep the last publications        
    df = df.groupby([global_var.publication_id,
                     global_var.publication_version,
                     global_var.publication_dt_UTC,
                     ],
                    axis = 0,
                    ).tail(1)
    
    ### Sort rows
    print('Sort rows')
    df = df.sort_values(by = [
                              global_var.publication_creation_dt_UTC,
                              global_var.publication_id,
                              global_var.publication_version,
                              global_var.publication_dt_UTC,
                              global_var.outage_status,
                              global_var.outage_begin_dt_UTC,
                              ], 
                        ascending = [True,
                                     True,
                                     True,
                                     True,
                                     False,
                                     True,
                                     ]
                        )
                        
    ### Checks
    print('Checks')
    assert not pd.isnull(df.index.values).any()        
    assert df[df[global_var.outage_status] == global_var.outage_status_finished].index.is_unique
    
    return df
        