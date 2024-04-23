import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

headers = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style", "drive-wheels",
           "engine-location", "wheel-base", "length", "width", "height", "curb-weight", "engine-type", "num-of-cylinders",
           "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"]

""" auto.csv sample rows
3,?,alfa-romero,gas,std,two,convertible,rwd,front,88.6,168.8,64.1,48.8,2548,dohc,four,130,mpfi,3.47,2.68,9.0,111,5000,21,27,13495
3,?,alfa-romero,gas,std,two,convertible,rwd,front,88.6,168.8,64.1,48.8,2548,dohc,four,130,mpfi,3.47,2.68,9.0,111,5000,21,27,16500
1,?,alfa-romero,gas,std,two,hatchback,rwd,front,94.5,171.2,65.5,52.4,2823,ohcv,six,152,mpfi,2.68,3.47,9.0,154,5000,19,26,16500
2,164,audi,gas,std,four,sedan,fwd,front,99.8,176.6,66.2,54.3,2337,ohc,four,109,mpfi,3.19,3.40,10.0,102,5500,24,30,13950
2,164,audi,gas,std,four,sedan,4wd,front,99.4,176.6,66.4,54.3,2824,ohc,five,136,mpfi,3.19,3.40,8.0,115,5500,18,22,17450
"""

class Data:
    def __init__(self, file_path, headers=None):
        self.file_path = file_path
        self.headers = headers
        self.df = self.read_data()
    
    def __str__(self):
        return self.df.head(5).to_string()
    
    def read_data(self):
        try:
            if self.headers:
                df = pd.read_csv(self.file_path, header=None, names=self.headers)
            else:
                df = pd.read_csv(self.file_path)
            print("import successful")
            return df
        except OSError as e:
            print(e.strerror)
            from sys import exit
            exit(1)

    def clean_data(self):
        self.df.replace(["?", ""], np.nan, inplace=True)

        # Convert column type to numeric if possible
        numeric_columns = []
        for col in self.df.columns:
            try:
                self.df[col] = self.df[col].astype(float)
                numeric_columns.append(col)
            except ValueError:
                pass

        for make in self.df["make"].unique():
            # Get the indices of rows where "make" equals the current make
            rows_by_make = self.df["make"] == make   # Selects e.g. alfa-romero rows/indices
            
            # Calculate mean values for the specific make
            mean_values = self.df[rows_by_make][numeric_columns].mean().round(2)  # List of mean values for a given made
            
            # Fill missing values with the mean values using .loc
            self.df.loc[rows_by_make, numeric_columns] = self.df.loc[rows_by_make, numeric_columns].fillna(mean_values)  # Iterative behaviour without for-loop
            
            # Calculate mean of each numerical column
            mean_values = self.df[numeric_columns].mean().round(2)
            
            # Replace missing values in numerical columns with the mean
            self.df[numeric_columns] = self.df[numeric_columns].fillna(mean_values)
        
        # Replace by make-independent average in case of insufficient data
        # Calculate mean of each numerical column
        mean_values = self.df[numeric_columns].mean().round(2)
        # Replace missing values in numerical columns with the mean
        self.df[numeric_columns] = self.df[numeric_columns].fillna(mean_values)
        
        print("cleanup successful")
    
    def save_cleaned_data(self, output_file):
        self.df.to_csv(output_file, index=False)
        print("export successful")

    def filter_by(self, conditions):
        # Accepts conditions expressed as a dictionary, e.g. {"fuel-type": "diesel", "make": "volkswagen"}
        df_filtered = self.df.copy()
        for column_name, value in conditions.items():
            df_filtered = df_filtered[df_filtered[column_name] == value]
        return df_filtered
    
    def total_price(self, df=None):
        # If no argument is provided, the function returns the total turnover of the dealership
        # If a DataFrame argument is provided, it returns the total turnover for the given filtered DataFrame.
        if df is None:
            df_to_sum = self.df
        else:
            df_to_sum = df
            
        print(f"The total price is {df_to_sum['price'].sum().round(2)}")
        return df_to_sum['price'].sum().round(2)
        
    def search_rows(self, *args):
        # Search engine that returns rows containing all provided arguments
        result = self.df.copy()
        for arg in args:
            result = result[result.eq(arg).any(axis=1)]
        print(result)
        
    def plot(self, x, y1, y2=None):
        # Used to create a scatter plot of 1-2 variables
        font1={"size":40}
        if y2 is None:
            plt.title(f"{y1} as a function of {x}", fontdict=font1)
            plt.scatter(self.df[x], self.df[y1], label=y1)
        else:
            plt.title(f"{y1} and {y2} as a function of {x}", fontdict=font1)
            plt.scatter(self.df[x], self.df[y1], label=y1)
            plt.scatter(self.df[x], self.df[y2], label=y2)
        plt.legend(fontsize=font1["size"])
        plt.grid()
        plt.show()
        

df = Data("auto.csv", headers)
df.clean_data()

# df.save_cleaned_data("auto_cleaned.csv")
# print(df.filter_by({"fuel-type": "diesel", "make": "volkswagen", "aspiration": "turbo"}))
# df.total_price(df.filter_by(fuel_type="diesel", make="volkswagen", aspiration="turbo"))
# df.total_price()
# df.search_rows("volkswagen","gas",122,"four")
# df.plot("horsepower", "highway-mpg", "city-mpg")
