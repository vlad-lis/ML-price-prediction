import pandas as pd
import numpy as np
import statistics as stats
from sklearn.preprocessing import PowerTransformer, StandardScaler

from scipy.stats import iqr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


df1 = pd.read_csv('./data/CAR DETAILS FROM CAR DEKHO.csv')
df2 = pd.read_csv('./data/Car details v3.csv')
df3 = pd.read_csv('./data/car details v4.csv')

df1['name'] = df1['name'].apply(lambda x: x.split()[0])
df2['name'] = df2['name'].apply(lambda x: x.split()[0])
df1['owner'] = df1['owner'].apply(lambda x: x.split()[0])
df2['owner'] = df2['owner'].apply(lambda x: x.split()[0])

df3.rename(columns=
           {"Year": "year",
            "Price": "selling_price",
            "Kilometer": "km_driven", 
            "Fuel Type": "fuel", 
            "Seller Type": "seller_type", 
            "Transmission": "transmission", 
            "Make": "name",
            "Owner": "owner"},inplace=True)

df1["selling_price"] /= 100
df1["selling_price"] = df1["selling_price"].astype(int)
df2["selling_price"] /= 100
df2["selling_price"] = df2["selling_price"].astype(int)
df3["selling_price"] /= 100
df3["selling_price"] = df3["selling_price"].astype(int)


df2.drop(['mileage', 'engine', 'max_power', 'torque', 'seats'], axis=1, inplace=True)
df3.drop(['Model', 'Location', 'Color', 'Engine', 'Max Power', 'Max Torque', 
          'Drivetrain', 'Length', 'Width', 'Height', 'Seating Capacity', 'Fuel Tank Capacity'], axis=1, inplace=True)

df = pd.concat([df1, df2, df3], ignore_index=True)

#check for duplicates
dup = df[df.duplicated(keep=False)].sort_values(by=['selling_price'])

#drop duplicates
df.drop_duplicates(inplace=True, ignore_index=True)

#change 'year' to 'age' (and count it)
df.rename(columns={'year': 'age'}, inplace=True)
df['age'] = df['age'].apply(lambda x: df['age'].max()+1-x)

#clean values in 'fuel' column
def clean_fuel(value):
    if 'CNG' in value:
        value = 'CNG'
    elif 'Petrol' in value:
        value = 'Petrol'
    return value

df['fuel'] = df['fuel'].apply(lambda x: clean_fuel(x))

#transform values in 'owner' column
def clean_owner(value):
    if value == 'Test' or value == 'UnRegistered Car':
        value = 0
    elif value == 'First':
        value = 1
    elif value == 'Second':
        value = 2
    elif value == 'Third':
        value = 3
    elif value == 'Fourth':
        value = 4
    elif value == '4 or More':
        value = 5
    return value

df['owner'] = df['owner'].apply(lambda x: clean_owner(x))


#clean 'seller_type' column
def clean_seller(value):
    if 'Dealer' in value:
        value = 'Dealer'
    elif value == 'Commercial Registration':
        value = 'Corporate'
    return value

df['seller_type'] = df['seller_type'].apply(lambda x: clean_seller(x))


#remove outliers
def remove_outliers(df):
    for c in df.columns:
            pct_75 = np.percentile(df[c], 75)
            pct_25 = np.percentile(df[c], 25)
            upper_bound = pct_75 + 1.5*iqr(df[c])
            lower_bound = pct_25 - 1.5*iqr(df[c])
            condition = (df[c] < upper_bound) & (df[c] > lower_bound)
            df[c] = df[c][condition]
    return df


numerical = df.select_dtypes(include=[np.number])
categorical = df.select_dtypes(include=[object])

numerical = remove_outliers(numerical)

df = pd.concat([numerical, categorical], axis=1)
df.dropna(inplace=True)


#X, y & train, test split
X = df.drop('selling_price', axis=1)
y = df[['selling_price']].copy()

numericalX = X.select_dtypes(include=[np.number])
categoricalX = X.select_dtypes(include=[object])
catX = X.select_dtypes(include=[object])

numericalX_columns = numericalX.columns

#dummies
numericalX = pd.DataFrame(numericalX, columns=numericalX_columns)
categoricalX = pd.get_dummies(categoricalX, drop_first=True)

numericalX.reset_index(drop=True, inplace=True)
categoricalX.reset_index(drop=True, inplace=True)

X = pd.concat([categoricalX, numericalX], axis=1, copy=False)


#train, test split
tt_ratio = 0.3
rand_seed = 40



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=tt_ratio, random_state=rand_seed)
X_train = pd.DataFrame(X_train)
X_test = pd.DataFrame(X_test)



#scaler & transformer (train data)
X_train_num = X_train[numericalX_columns]
X_train_cat = X_train.drop(numericalX_columns, axis=1)

scaler = StandardScaler()
scaler.fit(X_train_num)
X_train_num = scaler.transform(X_train_num)

pt = PowerTransformer()
pt.fit(X_train_num)
X_train_num = pt.transform(X_train_num)
X_train_num = pd.DataFrame(X_train_num, columns=numericalX_columns)

X_train_num.reset_index(drop=True, inplace=True)
X_train_cat.reset_index(drop=True, inplace=True)
X_train = pd.concat([X_train_cat, X_train_num], axis=1, copy=False)

#scaler & transformer (test data)
X_test_num = X_test[numericalX_columns]
X_test_cat = X_test.drop(numericalX_columns, axis=1)

X_test_num = scaler.transform(X_test_num)
X_test_num = pt.transform(X_test_num)
X_test_num = pd.DataFrame(X_test_num, columns=numericalX_columns)

X_test_num.reset_index(drop=True, inplace=True)
X_test_cat.reset_index(drop=True, inplace=True)
X_test = pd.concat([X_test_cat, X_test_num], axis=1, copy=False)


### Input -> prediction

# function for numerical column input
def ask_input_num(question, options):
    while True:
        prompt = input(f'enter {question}: ') 
        try:
            if int(prompt) not in options:
                print(f' ! pick something between {min(options)} and {max(options)}')
            else:
                return prompt
        except ValueError:
            print(' ! enter a number with no decimals')     
        

#function for categorical column input
def ask_input_cat(question, options):
    while True:
        prompt = input(f'enter {question}: ')
        if (prompt not in options):
            print(f' ! pick one of these: {options} ')
        else:
            return prompt


#prediction with input
def prediction():
    print("""
    ******************************
    *    CAR PRICE PREDICTION    *
    ******************************
    """)
    t = X_test.iloc[:1].copy()
    t = pd.DataFrame(t)
    t.iloc[:] = 0
    
    list_of_models = list(df['name'].unique())
    list_of_age = list(range(51))
    list_of_km = list(range(300001))
    list_of_owners = list(df['owner'].unique())
    list_of_fuel = list(df['fuel'].unique())
    list_of_sellers = list(df['seller_type'].unique())
    list_of_transmission = list(df['transmission'].unique())
    
    model = ask_input_cat('model name', list_of_models)
    age = ask_input_num('car\'s age', list_of_age)
    km = ask_input_num('car\'s distance travelled', list_of_km)
    owner = ask_input_num('number of previous owners', list_of_owners)
    fuel = ask_input_cat('fuel type', list_of_fuel)
    seller = ask_input_cat('seller type', list_of_sellers)
    transmission = ask_input_cat('transmission type', list_of_transmission)
    
    t.at[0, f'name_{model}'] = 1
    t.at[0, 'age'] = age
    t.at[0, 'km_driven'] = km
    t.at[0, 'owner'] = owner
    t.at[0, f'fuel_{fuel}'] = 1
    t.at[0, f'seller_type_{seller}'] = 1
    t.at[0, f'transmission_{transmission}'] = 1
    
    if model == 'Ambassador':
        t.drop(['name_Ambassador'], axis=1, inplace=True)
    if fuel == 'CNG':
        t.drop(['fuel_CNG'], axis=1, inplace=True)
    if seller == 'Corporate':
        t.drop(['seller_type_Corporate'], axis=1, inplace=True)
    if transmission == 'Automatic':
        t.drop(['transmission_Automatic'], axis=1, inplace=True)
    
    t_num = t[numericalX_columns]
    t_cat = t.drop(numericalX_columns, axis=1)

    t_num = scaler.transform(t_num)
    t_num = pt.transform(t_num)
    t_num = pd.DataFrame(t_num, columns=numericalX_columns)

    t = pd.concat([t_cat, t_num], axis=1, copy=False) 
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    price = model.predict(t).tolist()[0][0]
    
    if price < 0:
        price = 0
    else:
        price = round(price)
    
    if price == 0:
        output = 'Sorry, but the model says this car is a worthless piece of junk :('
    else:
        output = f'Predicted price is: {price} $'
    
    out = print(f"""
    *******************************
    {output}
    *******************************
    """)
        
    return out


#wrapper function for multiple runs
def wrapper(func):
    while True:
        ask = input('Run the script? (yes/no) ')
        if ask == 'yes':
            func()
        elif ask == 'no':
            print("""
        Done:)
            """)
            break
        else:
            print(' ! type "yes" or "no"')

wrapper(prediction)





