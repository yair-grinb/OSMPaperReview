import pandas as pd
import itertools
import operator

inp_file = 'OSM_Paper_Review.csv'

# read file and remove unincluded papers
df = pd.read_csv(inp_file)

columns = ["Authors’ disciplines", "Journal’s discipline", "Topics", 
          "Authors' Geography (countries)", "Authors' Geography (continents)", "Study Area Geography (countries)", 
          "Perspective on the community", "Evidence of engagement", "Geographic Correspondence"] 

# harmonize the data - remove white spaces, new lines, etc. and transform strings to lists
for c in columns[:-1]:
    df[c] = df[c].str.replace('\r', '')
    df[c] = df[c].str.replace('\n', '')
    df[c] = df[c].str.strip()
    df[c] = df[c].str.split(',')

# transfrom null values to string/lists of string
df.loc[df[columns[5]].isnull(),[columns[5]] = df.loc[
    df[columns[5]].isnull(),columns[5]].apply(lambda x: ['NA'])
df.loc[df[columns[-1]].isna(), [columns[-1]]] = 'NA'

# remove whitespaces
for c in columns[:-1]:
    df[c] = df[c].map(lambda l:list(map(str.strip, l)))
        
# print the values for each variable, to verify these are in order
for c in columns[:-1]:
    print(c)
    print(sorted(list(set(itertools.chain.from_iterable(df[c])))))

# add study area continents column
study_area_continent = {'Argentina': 'South America', 'Asia': 'Asia', 'Australia': 'Australia & Oceania', 
                        'Austria': 'Europe', 'Bahrain': 'Asia', 'Belgium': 'Europe', 
                        'Bolivia': 'South America', 'Brazil': 'South America', 'Burkina Faso': 'Africa', 
                        'Canada': 'North America', 'Chile': 'South America', 'China': 'Asia', 
                        'Colombia': 'South America', 'Cuba': 'North America', 'Cyprus': 'Europe', 
                        'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Ecuador': 'South America', 
                        'Egypt': 'Africa', 'Europe': 'Europe', 'Finland': 'Europe', 'France': 'Europe', 
                        'French Guiana': 'South America', 'Germany': 'Europe', 'Ghana': 'Africa', 
                        'Global': 'Global', 'Greece': 'Europe', 'Guam': 'Australia & Oceania', 
                        'Guinea': 'Africa', 'Guyana': 'South America', 'Haiti': 'North America', 
                        'Hong Kong': 'Asia', 'Hungary': 'Europe', 'Iceland': 'Europe', 'India': 'Asia', 
                        'Indonesia': 'Asia', 'Iran': 'Asia', 'Ireland': 'Europe', 'Israel': 'Asia', 
                        'Italy': 'Europe', 'Japan': 'Asia', 'Kazakhstan': 'Asia', 'Kenya': 'Africa', 
                        'Latvia': 'Europe', 'Liberia': 'Africa', 'Lithuania': 'Europe', 
                        'Luxembourg': 'Europe', 'Madgascar': 'Africa', 'Malawi': 'Africa', 
                        'Mali': 'Africa', 'Mexico': 'North America', 'Mozambique': 'Africa', 
                        'Namibia': 'Africa', 'Nepal': 'Asia', 'Netherlands': 'Europe', 
                        'New Zealand': 'Australia & Oceania', 'Nigeria': 'Africa', 'Norway': 'Europe', 
                        'Palestine': 'Asia', 'Panama': 'North America', 'Paraguay': 'South America', 
                        'Peru': 'South America', 'Philippines': 'Asia', 'Poland': 'Europe', 
                        'Portugal': 'Europe', 'Qatar': 'Asia', 'Romania': 'Europe', 'Russia': 'Europe', 
                        'Saudi Arabia': 'Asia', 'Senegal': 'Africa', 'Serbia': 'Europe', 
                        'Singapore': 'Asia', 'Slovenia': 'Europe', 
                        'South Africa': 'Africa', 'South Korea': 'Asia', 'Spain': 'Europe', 
                        'Suriname': 'South America', 'Sweden': 'Europe', 'Switzerland': 'Europe', 
                        'Taiwan': 'Asia', 'Tanzania': 'Africa', 'Thailand': 'Asia', 'Turkey': 'Asia', 
                        'Uganda': 'Africa', 'Ukraine': 'Europe', 'United Arab Emirates': 'Asia', 
                        'United Kingdom': 'Europe', 'United States': 'North America', 
                        'Uruguay': 'South America', 'Venezuela': 'South America', 'NA': 'None', 
                        'Zimbabwe': 'Africa'}

continent_rows = []
for idx, row in df.iterrows():
    continent_rows.append(list(set([study_area_continent[i] for i in row[columns[5]]])))
df['Study Area Geography (continent)'] = continent_rows

# create Table 3
tab3 = pd.DataFrame(columns=['variable','value','papers','%'])
for n in [0, 1, 2, 4, 6, 7, 9]:
    counts = {}
    for idx, row in df.iterrows():
        for i in row[columns[n]]:
            if i not in counts:
                counts[i] = 0
            counts[i] += 1
    for i in counts:
        tab3 = tab3.append({'variable':columns[n], 
                            'value':i, 
                            'papers': counts[i], 
                            '%': round(counts[i]*100/df.shape[0], 1)},
                           ignore_index=True)

counts = df[columns[-2]].value_counts().to_dict()
for i in counts:
    tab3 = tab3.append({'variable':columns[-2], 
                        'value':i, 
                        'papers': counts[i], 
                        '%': round(counts[i]*100/df.shape[0], 1)},
                       ignore_index=True)
tab3.to_csv('Table3.csv')

# statistics for text
# 1. number of papers by number of authors' disciplines
for i in range(1, 5):
    k = len([idx for idx, row in df.iterrows() if len(row[columns[0]])==i])
    print('Authors from '+str(i)+' Disciplines:', k, round(k*100/df.shape[0], 1))

# 2. number of papers by number of affiliated countries
for i in range(1, 6):
    k = len([idx for idx, row in df.iterrows() if len(row[columns[3]])==i])
    print('Authors from '+str(i)+' Countries:', k, round(k*100/df.shape[0], 1))

# 3. number of papers by affiliated country
country_counts = {}
for idx, row in df.iterrows():
    for i in set(row[columns[3]]):
        if i not in country_counts:
            country_counts[i] = 0
        country_counts[i] += 1
for k in sorted(country_counts.items(), key=operator.itemgetter(1), reverse=True):
    print(k[0], k[1], round(k[1]*100/df.shape[0], 1))

# 4. number of papers by number of case study countries
k = len([idx for idx, row in df.iterrows() 
         if len(row[columns[5]])==1
         and row[columns[5]] != ['Global']
         and row[columns[5]] != ['NA']
         and row[columns[5]] != ['Europe']
         and row[columns[5]] != ['Asia']])
print('1 case study', k, round(k*100/df.shape[0], 1))
for i in range(2, 7):
    k = len([idx for idx, row in df.iterrows() if len(row[columns[5]])==i])
    print(str(i) + ' case studies:', k, round(k*100/df.shape[0], 1))
k = len([idx for idx, row in df.iterrows() if len(row[columns[5]])>6])
print('more than 6 case studies:', k, round(k*100/df.shape[0], 1))
print('maximal number of case studies:', max([len(row[columns[5]]) 
                                              for idx, row in df.iterrows()]))

# 5. number of papers using entire continent as a case study
for cont in ['Europe', 'Asia']:
    k = len([idx for idx, row in df.iterrows() if row[columns[5]]==[cont]])
    print('Paper using '+cont+' as case study', k, round(k*100/df.shape[0], 1))

# 6. number of papers by case study country
country_counts = {}
for idx, row in df.iterrows():
    for i in set(row[columns[5]]):
        if i not in country_counts:
            country_counts[i] = 0
        country_counts[i] += 1
for k in sorted(country_counts.items(), key=operator.itemgetter(1), reverse=True):
    print(k[0], k[1], round(k[1]*100/df.shape[0], 1))

# create files for producing Alluvial Diagrams
indices = [0, 1, 2, 6, 7]
for c1 in range(len(indices)-1):
    for c2 in range(c1+1, len(indices)):
        data = []
        for idx, row in df.iterrows():
            for i in row[columns[indices[c1]]]:
                for j in row[columns[indices[c2]]]:
                    data.append([i,j])
        temp_df = pd.DataFrame(data, columns=[columns[indices[c1]], columns[indices[c2]]])
        temp_df.to_csv('Alluvial_'+columns[indices[c1]]+'_'+columns[indices[c2]]+'.csv')

# create Alluvial diagrams files for the geographic correspondence variable
for c2 in indices:
    data = []
    for idx, row in df.iterrows():
        for i in row[columns[c2]]:
            data.append([row[columns[-2]], i])
    temp_df = pd.DataFrame(data, columns=[columns[-2], columns[c2]])
    temp_df.to_csv('Alluvial_'+columns[-2]+'_'+columns[c2]+'.csv')
