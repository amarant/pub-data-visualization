
import pandas as pd
#
from ... import global_var
from . import entsoe, rte


def load(source             = None,
         map_code           = None,
         company            = None,
         unit_name          = None,
         production_source  = None,
         publication_dt_min = None,
         publication_dt_max = None,
         ):
    
    if source == global_var.data_source_rte:
        df, dikt_incoherences = rte.load(map_code = map_code)
        
    elif source == global_var.data_source_entsoe:
        df = entsoe.load(map_code = map_code)
    
    else: 
        raise ValueError('Incorrect source : {0}'.format(source))
        
    df = df.set_index([global_var.publication_id,
                       global_var.publication_version, 
                       global_var.publication_dt_UTC, 
                       ], 
                      drop = True, 
                      )
    
    df = df[col_order]
    
    dg = df.loc[  pd.Series(True, index = df.index)
                & ((df[global_var.company_name]     .isin([company]           if type(company)           == str else company))           if bool(company)            else True)
                & ((df[global_var.production_source].isin([production_source] if type(production_source) == str else production_source)) if bool(production_source)  else True)
                & ((df[global_var.unit_name]        .isin([unit_name]         if type(unit_name)         == str else unit_name))         if bool(unit_name)          else True)
                & ((df[global_var.publication_dt_UTC] >= publication_dt_min)                                                             if bool(publication_dt_min) else True)
                & ((df[global_var.publication_dt_UTC] <= publication_dt_max)                                                             if bool(publication_dt_max) else True)
                ]
    
    assert dg.shape[0] > 0
    
    return dg


col_order = [
global_var.outage_begin_dt_UTC,
global_var.outage_end_dt_UTC,
global_var.unit_name,
global_var.outage_remaining_power_mw,
global_var.unit_nameplate_capacity,
global_var.company_name,
global_var.geography_map_code,
global_var.production_source,
global_var.publication_creation_dt_UTC,
global_var.outage_type,
global_var.outage_cause,
global_var.outage_status,
global_var.file_name,
]   
