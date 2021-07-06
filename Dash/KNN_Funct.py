import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from geopy import distance
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def get_sales_comps(tdata,instance,Miles,numofneighbors,features=None,):

    #features to compare inst to other houses
    if features== None:
        features=['GrLivArea',  'LotArea',  'OverallQual', 'YearBuilt',
        'TotalBsmtSF',
       'GarageArea',
       'Remodeled']


    ## find people within x mis
    def houses_within_x_mi(tdata,instance,Miles):
        instance_coords=[instance.Lat.iloc[0],instance.Long.iloc[0]]
        tdata['Dist_from_Inst']=tdata.apply(lambda x: distance.distance([x.Lat,x.Long], instance_coords).miles,axis=1)
        return tdata[tdata.Dist_from_Inst<=Miles]



    datasubset=houses_within_x_mi(tdata,instance,Miles)
    datasubsetSalePrices=datasubset.SalePrice
    instance=instance[features]
    datasubset=datasubset[features]
    untransformed_data=datasubset

    scaler=StandardScaler()
    scaler.fit(datasubset)
    datasubset=scaler.transform(datasubset)
    instance=scaler.transform(instance)

    neigh = NearestNeighbors(n_neighbors=numofneighbors)
    neigh.fit(datasubset)
    dist,ind=neigh.kneighbors(instance)

    Sales_Comps=untransformed_data.iloc[ind.tolist()[0]]
    Sales_Comps['SalePrice']=datasubsetSalePrices.iloc[ind.tolist()[0]]
    return Sales_Comps
