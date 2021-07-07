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
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import great_circle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gmplot


def get_sales_comps(tdata,instance,Miles,numofneighbors,features=None,):
    tdata = pd.read_csv('apps/data/Data_For_KNN_salescomps.csv')
    #features to compare inst to other houses
    if features== None:
        features=['GrLivArea',  'LotArea',  'OverallQual', 'YearBuilt',
        'TotalBsmtSF',
       'GarageArea',
       'Remodeled']

    def getlatlong(address):
            locator = Nominatim(user_agent="myGeocoder")
            address=address+', Ames, Iowa'

            location = locator.geocode(address)
            lat=location[1][0]
            long=location[1][1]
            return [lat,long]

    ## find people within x mis
    def houses_within_x_mi(tdata,instance,Miles):
        instance_coords=[instance.Lat.iloc[0],instance.Long.iloc[0]]
        tdata['Dist_from_Inst']=tdata.apply(lambda x: distance.distance([x.Lat,x.Long], instance_coords).miles,axis=1)
        return tdata[tdata.Dist_from_Inst<=Miles]

    instance['Lat'],instance['Long']=getlatlong(instance.Prop_Addr[0])
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




def neighborhood_cluster(numofgroups):
    Neighborhood_as_instance_narrowed = pd.read_csv('apps/data/data_for_clusters.csv',index_col=0)
    tdataneighborhood=pd.read_csv('apps/data/tdata_for_clusters.csv')
    def linkage_frame(data):
        row_clusters = linkage(data, method='complete', metric='euclidean')
        columns = ['row label 1', 'row label 2', 'distance', 'no. items in clust.']
        index = ['cluster %d' % (i + 1) for i in range(row_clusters.shape[0])]
        linkage_df = pd.DataFrame(row_clusters, columns=columns, index=index)
        return linkage_df

    labelList=Neighborhood_as_instance_narrowed.index
    print(tdataneighborhood)
    Z = linkage(Neighborhood_as_instance_narrowed, metric='euclidean')
    i=27-numofgroups
    Labels=(fcluster(Z, t=Z[i,2], criterion='distance'))#1.3129504372389496
    neighborhoodasnum=[list(Neighborhood_as_instance_narrowed.index).index(i) for i in tdataneighborhood.Neighborhood]
    clusterlabel=[]
    for i in range(len(neighborhoodasnum)):
        clusterlabel.append(Labels[neighborhoodasnum[i]])
    clusterdf=pd.DataFrame({'Lat':tdataneighborhood.Lat,'Long':tdataneighborhood.Long,'Label':clusterlabel})
    return clusterdf
