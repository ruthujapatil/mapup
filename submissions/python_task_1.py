import pandas as pd

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    #Pivot the dataframe to create a matrix
    car_df=df.pivot(index='id_1',columns='id_2',values='car')

    #Set diagonals to 0
    for index in car_df.index:
        car_df.at[index,index] =0

    return car_df

df=pd.DataFrame(pd.read_csv('dataset-1.csv'))
result_df=generate_car_matrix(df)
result_df

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type']=pd.cut(df['car'], bins=[float('-inf'),15,25,float('inf')],labels=['low','medium','high'],right=False)
    counts=df['car_type'].value_counts().to_dict()

    return dict(sorted(counts.items()))

df=pd.DataFrame(pd.read_csv('dataset-1.csv'))
get_type_count(df)

def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    means=df['bus'].mean()

    indexes=df[df['bus']>2*means].index

    return list(sorted(indexes))

df=pd.DataFrame(pd.read_csv('dataset-1.csv'))
get_bus_indexes(df)

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    truck_average=df.groupby('route')['truck'].mean()

    filter_routes=truck_average[truck_average>7].index

    return list(sorted(filter_routes))

df=pd.DataFrame(pd.read_csv('dataset-1.csv'))
filter_routes(df)

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modify_df=matrix.copy()
    modify_df=modify_df.applymap(lambda x:x *0.75 if x>20 else x*1.25)

    modify_df=modify_df.rount(1)

    return modify_df

multiply_matrix(result_df)

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """

    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    result_df1 = pd.DataFrame(index=df.set_index(['id', 'id_2']).index.unique())

    result_df1['is_complete'] = (
        (df.groupby(['id', 'id_2'])['start_datetime'].min().dt.time == pd.to_datetime('00:00:00').time()) &
        (df.groupby(['id', 'id_2'])['end_datetime'].max().dt.time == pd.to_datetime('23:59:59').time()) &
        (df.groupby(['id', 'id_2'])['start_datetime'].apply(lambda x: set(x.dt.dayofweek.unique()) == set(range(7))))
    )

    return pd.Series(result_df1['is_complete'])

df = pd.read_csv('dataset-2.csv')
verify_time_completeness(df)

