'''
License:

All data is licensed under CC BY 3.0 DE (Creative Commons Namensnennung 3.0 Deutschland Lizenz).

By: Berliner Landesamt für Bürger- und Ordnungsangelegenheiten (LABO) / BerlinOnline Stadtportal GmbH & Co. KG

Repository: https://github.com/berlinonline/haeufige-vornamen-berlin
'''

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def remove_df20_position(df):
    '''
    INPUT:
    df: dataframe df20

    OUTPUT:
    dataframe

    Purpose:
    Remove position information from datatable; collapse rows; align format with df12 and df16
    '''
    df = df.groupby(['vorname', 'geschlecht']).agg(sum).reset_index()
    df = df[['vorname', 'anzahl', 'geschlecht']]
    df = df.sort_values(by=['anzahl'], ascending=False)
    return df

def rename_columns(df):
    df = df.rename(columns={'vorname': 'first name',
                   'anzahl': 'frequency', 'geschlecht': 'gender'})
    return df

def top_names_in_position_1(df, gender):
    '''
    INPUT:
    df: dataframe, as read in at beginnign of notebook
    gender: string, 'w' or 'm'
    number_of_names: integer, how many of the top names should be retrieved

    OUTPUT:
    dataframe

    Purpose:
    Create dataframe with top names only
    '''
    df = df.loc[(df['gender'] == gender)].sort_values(by='frequency',
                                                      ascending=False)
    df = df.iloc[:5, [0, 1]]
    return df

def return_figures():
    
    """
    INPUT:
    None - files are accessed within this function
    
    OUTPUT:
    list: list containing the plotly visualizations

    Purpose:
    Data wrangling and plotting
    """
    
    # Read in data
    url20 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2020/charlottenburg-wilmersdorf.csv'
    url19 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2019/charlottenburg-wilmersdorf.csv'
    url18 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2018/charlottenburg-wilmersdorf.csv'
    url17 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2017/charlottenburg-wilmersdorf.csv'
    url16 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2016/charlottenburg-wilmersdorf.csv'
    url15 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2015/charlottenburg-wilmersdorf.csv'
    url14 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2014/charlottenburg-wilmersdorf.csv'
    url13 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2013/charlottenburg-wilmersdorf.csv'
    url12 = 'https://raw.githubusercontent.com/berlinonline/haeufige-vornamen-berlin/master/data/cleaned/2012/charlottenburg-wilmersdorf.csv'

    df20 = pd.read_csv(url20, error_bad_lines=False)
    df19 = pd.read_csv(url19, error_bad_lines=False)
    df18 = pd.read_csv(url18, error_bad_lines=False)
    df17 = pd.read_csv(url17, error_bad_lines=False)
    df16 = pd.read_csv(url16, error_bad_lines=False)
    df15 = pd.read_csv(url15, error_bad_lines=False)
    df14 = pd.read_csv(url14, error_bad_lines=False)
    df13 = pd.read_csv(url13, error_bad_lines=False)
    df12 = pd.read_csv(url12, error_bad_lines=False)
    
    # Clean data
    df20 = remove_df20_position(df20)
    df12 = rename_columns(df12)
    df13 = rename_columns(df13)
    df14 = rename_columns(df14)
    df15 = rename_columns(df15)
    df16 = rename_columns(df16)
    df17 = rename_columns(df17)
    df18 = rename_columns(df18)
    df19 = rename_columns(df19)
    df20 = rename_columns(df20)
    
    # Store dataframes in dictionary
    frame_dict = {2020: df20, 2016: df16, 2012: df12}
    
    # ------------------------------------------------------------------#
    # ------------------------- TOPIC 1 --------------------------------#
    # ------------number of newly registered children--------------------#
    
    # WRANGLE DATA
    df_total_registrations = pd.DataFrame([[2012, df12.frequency.sum()],
                                           [2013, df13.frequency.sum()],
                                           [2014, df14.frequency.sum()],
                                           [2015, df15.frequency.sum()],
                                           [2016, df16.frequency.sum()],
                                           [2017, df17.frequency.sum()],
                                           [2018, df18.frequency.sum()],
                                           [2019, df19.frequency.sum()],
                                           [2020, df20.frequency.sum()]],
                                           columns=['year', 'number of children'])
    # PLOT
    fig1 = px.bar(df_total_registrations, x="year", y="number of children",
               title="Number of children registered per year")
    
    # ------------------------------------------------------------------#
    # ------------------------- TOPIC 2 --------------------------------#
    # -------------------------top names--------------------------------#
    
    # WRANGLE DATA
    
    # Create 2 dataframes per year with top 5 female and top 5 male names
    # Store in dictionary where keys are the years
    top_names_frame_dict = {}
    for year, frame in frame_dict.items():
        frame_w = str(frame) + 'w'
        frame_m = str(frame) + 'm'
        frame_w = top_names_in_position_1(frame, 'w').reset_index(drop=True)
        frame_m = top_names_in_position_1(frame, 'm').reset_index(drop=True)
        top_names_frame_dict[year] = [frame_w, frame_m]

    # Create 1 dataframe per year that combines top 5 female and top 5 male names
    # Store in dictionary where keys are the years
    top_names_combined_frame_dict = {}
    for year, frames in top_names_frame_dict.items():
        frame_top = top_names_frame_dict[year][0].merge(top_names_frame_dict[year][1],
                                                    suffixes=(
                                                        ' female', ' male'),
                                                    left_index=True,
                                                    right_index=True)
        top_names_combined_frame_dict[year] = frame_top
        
    # PLOT 
    figt1 = go.Figure(data=[go.Table(header=dict(values=top_names_combined_frame_dict[2012].columns),
                               cells=dict(values=[top_names_combined_frame_dict[2012]['first name female'],
                                                  top_names_combined_frame_dict[2012]['frequency female'],
                                                  top_names_combined_frame_dict[2012]['first name male'],
                                                  top_names_combined_frame_dict[2012]['frequency male'], ]))
                      ])
    figt1.update_layout(title={'text': "Top names in 2012"}, 
                               height=230,
                               margin=dict(l=5, r=5, t=40, b=0))
    
    figt2 = go.Figure(data=[go.Table(header=dict(values=top_names_combined_frame_dict[2016].columns),
                               cells=dict(values=[top_names_combined_frame_dict[2016]['first name female'],
                                                  top_names_combined_frame_dict[2016]['frequency female'],
                                                  top_names_combined_frame_dict[2016]['first name male'],
                                                  top_names_combined_frame_dict[2016]['frequency male'], ]))
                      ])
    figt2.update_layout(title={'text': "Top names in 2016"},
                               height=230,
                               margin=dict(l=5, r=5, t=40, b=0))
    
    figt3 = go.Figure(data=[go.Table(header=dict(values=top_names_combined_frame_dict[2020].columns),
                               cells=dict(values=[top_names_combined_frame_dict[2020]['first name female'],
                                                  top_names_combined_frame_dict[2020]['frequency female'],
                                                  top_names_combined_frame_dict[2020]['first name male'],
                                                  top_names_combined_frame_dict[2020]['frequency male'], ]))
                      ])
    figt3.update_layout(title={'text': "Top names in 2020"},
                               height=230,
                               margin=dict(l=5, r=5, t=40, b=0))
    # WRANGLE DATA
    # Retrieve top names

    # First, combine all male dataframes and all female dataframes with each other
    top_names_across_years_dict = {}
    male_frames = []
    female_frames = []
    for year, frames in top_names_frame_dict.items():
        male_frames.append(top_names_frame_dict[year][1])
        female_frames.append(top_names_frame_dict[year][0])

    # Then, use these comined dataframes to create sets with the top names
    male_set = set()
    for frame in male_frames:
        for name in frame['first name']:
            male_set.add(name)

    female_set = set()
    for frame in female_frames:
        for name in frame['first name']:
            female_set.add(name)
            
    # Get number of names in all years by merging three original dataframes
    df1216 = df12.merge(df16, how='outer', left_on=['first name', 'gender'], right_on=[
                        'first name', 'gender'], suffixes=('_12', '_16'))
    df_allyears = df1216.merge(df20, how='outer', left_on=[
                               'first name', 'gender'], right_on=['first name', 'gender'])
    # Rename 2020 frequency column
    df_allyears = df_allyears.rename(
        columns={'frequency_12': '2012', 'frequency_16': '2016', 'frequency': '2020'})
    df_allyears = df_allyears[['first name', 'gender', '2012', '2016', '2020']]
    
    # Calculate % for each name out of all names
    for year in ['2012', '2016', '2020']:
        df_allyears[year] = df_allyears[year]/df_allyears[year].count()
        
    # Create copy of this dataframe for Topic 3
    df_newcomers = df_allyears
    
    # Filter dataframe on relevant names
    df_allyears = df_allyears.loc[
        (
            (df_allyears['first name'].isin(list(male_set))) & (
                df_allyears['gender'] == 'm')
        )
        |
        (
            (df_allyears['first name'].isin(list(female_set))) & (
                df_allyears['gender'] == 'w')
        )
    ]
    
    # Stack dataframe
    df_allyears_melt = df_allyears.melt(
        id_vars=['first name', 'gender'], value_vars=['2012', '2016', '2020'])
    
    # Sort df
    df_allyears_melt = df_allyears_melt.sort_values(by=['gender', 'first name'])
    
    # PLOT (female)
    df_female = df_allyears_melt.query("gender=='w'")
    fig21 = px.line(df_female,
                  x='variable',
                  y='value',
                  color='first name',
                  color_discrete_map={
                    "Charlotte": "rgb(233, 8, 53)",
                    "Elisabeth": "rgb(233, 8, 109)",
                    "Emilia": "rgb(219, 102, 98)",
                    "Maria": "rgb(255, 155, 47)",
                    "Marie": "rgb(241, 102, 151)",
                    "Sophie": "rgb(241, 102, 200)",
                  },
                  labels={"value": "share of name out of all names",
                          "variable": "year"},
                  title='Development of top female names 2012 - 2020'
                  )
    fig21.update_traces(line=dict(width=2), mode='lines+markers')

    # PLOT (male)
    df_male = df_allyears_melt.query("gender=='m'")
    fig22 = px.line(df_male,
                  x='variable',
                  y='value',
                  color='first name',
                  color_discrete_map={
                    "Alexander": "rgb(35, 156, 158)",
                    "David": "rgb(4, 191, 146)",
                    "Elias": "rgb(4, 97, 234)",
                    "Jakob": "rgb(4, 233, 146)",
                    "Maximilian": "rgb(35, 156, 252)",
                    "Noah": "rgb(35, 197, 252)",
                    "Paul": "rgb(35, 235, 252)",
                  },
                  labels={"value": "share of name out of all names",
                          "variable": "year"},
                  title='Development of top male names 2012 - 2020',
                  )
    fig22.update_traces(line=dict(width=2), mode='lines+markers')
    
    # ------------------------------------------------------------------#
    # ------------------------- TOPIC 3 --------------------------------#
    # -------------------------newcomers--------------------------------# 

    # DATA WRANGLING
    
    # Fill NaN values with 0
    df_newcomers = df_newcomers.fillna(0)
    
    # Create column that shows growth
    df_newcomers['increase'] = df_newcomers['2020'] - df_newcomers['2012']

    # Sort dataframe
    df_newcomers = df_newcomers.sort_values(by=['increase'], ascending=False)

    # Get top male and female names to then filter df_newcomers (next step)
    female_list = list(
        df_newcomers.loc[df_newcomers['gender'] == 'w', 'first name'])[:4]
    male_list = list(
        df_newcomers.loc[df_newcomers['gender'] == 'm', 'first name'])[:4]
    top_newcomers_list = female_list + male_list

    # Filter df_newcomers
    df_newcomers = df_newcomers.loc[df_newcomers['first name'].isin(
        top_newcomers_list)]

    # Stack data
    df_newcomers_melt = df_newcomers.melt(
        id_vars=['first name', 'gender', 'increase'], value_vars=['2012', '2016', '2020'])

    # Sort df
    df_newcomers_melt = df_newcomers_melt.sort_values(by=['gender', 'first name'])

    # PLOT
    fig3 = px.line(df_newcomers_melt,
                  x='variable',
                  y='value',
                  color='first name',
                  color_discrete_map={
                    "Karl": "rgb(35, 156, 158)",
                    "Adam": "rgb(4, 191, 146)",
                    "Nael": "rgb(4, 97, 234)",
                    "Matteo": "rgb(4, 233, 146)",
                    "Lea": "rgb(233, 8, 53)",
                    "Liya": "rgb(233, 8, 109)",
                    "Frida": "rgb(255, 155, 47)",
                    "Mathilda": "rgb(241, 102, 200)",
                  },
                  labels={"value": "share of name out of all names",
                          "variable": "year"},
                  title='Newcomers',
                  )
    fig3.update_traces(line=dict(width=2), mode='lines+markers')
    
    # COLLECT ALL FIGURES
    figures = [fig1, figt1, figt2, figt3, fig21, fig22, fig3]
    
    return figures
   