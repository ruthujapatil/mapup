import pandas as pd
import networkx as nx
import warnings
warnings.filterwarnings("ignore")

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    graph=nx.DiGraph()

    for index,row in df.iterrows():
        graph.add_edge(row['id_start'], row['id_end'], weight=row['distance'])

    #calculate shortest path using dijkstra algorithm
    shortest_path= dict(nx.all_pairs_dijkstra_path_length(graph))

    unique_ids= sorted(set(df['id_start'].unique())|set(df['id_end'].unique()))
    distance_matrix=pd.DataFrame(index=unique_ids, columns=unique_ids)

    for start_id in unique_ids:
        for end_id in unique_ids:
            if start_id==end_id:
                distance_matrix.at[start_id,end_id] = 0
            elif end_id in shortest_path[start_id]:
                distance_matrix.at[start_id, end_id]= shortest_path[start_id][end_id]
            else:
                distance_matrix.at[start_id,end_id]=float('nan')    #if no dirent routes set distance to nan

    distance_matrix=distance_matrix.add(distance_matrix.transpose(), fill_value=0)

    return distance_matrix

df=pd.DataFrame(pd.read_csv('dataset-3.csv'))
distance_matrix = calculate_distance_matrix(df)
distance_matrix

def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unique_ids= distance_matrix.index

    unrolled_df= pd.DataFrame(columns=['id_start','id_end','distance'])

    for id_start in unique_ids:
        for id_end in unique_ids:
            if id_start !=id_end:
                distance= distance_matrix.at[id_start,id_end]
                unrolled_df=unrolled_df.append({'id_start':id_start,'id_end':id_end,'distance':distance},ignore_index=True)

    return unrolled_df

df=pd.DataFrame(pd.read_csv('dataset-3.csv'))
unroll_distance_matrix(distance_matrix)

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Filter DataFrame for the specified reference_id
    reference_df = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    average_distance = reference_df['distance'].mean()

    # Calculate the 10% threshold range
    lower_threshold = average_distance - (0.10 * average_distance)
    upper_threshold = average_distance + (0.10 * average_distance)

    # Filter the DataFrame for values within the 10% threshold
    filtered_df = df[(df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]

    # Get unique values from 'id_start' column and sort them
    result= sorted(filtered_df['id_start'].unique())
    return result

df2=unroll_distance_matrix(distance_matrix)
reference_id=int(input('Enter the reference_id '))
results=find_ids_within_ten_percentage_threshold(df2, reference_id)
results

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coefficient={'moto':0.8,'car':1.2,'rv':1.5,'bus':2.2,'truck':3.6}

    for vehicle_type, rate_coefficient in rate_coefficient.items():
        df['vehicle_type']=df['distance']*rate_coefficient

    df=df.drop(columns=['distance'])
    return df

calculate_toll_rate(df2)

def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df