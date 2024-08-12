import polars as pl
import pandas as pd

## https://www.google.com/search?q=polars+python+examples
## https://www.datacamp.com/blog/an-introduction-to-polars-python-s-tool-for-large-scale-data-analysis

data = pl.read_csv('https://raw.githubusercontent.com/pycaret/pycaret/master/datasets/diamond.csv')
df = data

# check the head
data.head()

# Select specific columns: carat, cut, and price
selected_df = df.select(['Carat Weight', 'Cut', 'Price'])


# show selected_df head
selected_df.head()


# filter the df with condition
filtered_df = df.filter(pl.col('Carat Weight') > 2.0)


# show filtered_df head
filtered_df.head()


# sort the df by price
sorted_df = df.sort(by='Price')


# show sorted_df head
sorted_df.head()


# drop missing values
cleaned_df = df.drop_nulls()


# show cleaned_df head
cleaned_df.head()


# group by cut and calc mean of price
grouped_df = df.groupby(by='Cut').agg(pl.col('Price').mean())


# show grouped_df head
grouped_df.head()


# Create the first DataFrame
df1 = pl.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David']
})


# Create the second DataFrame
df2 = pl.DataFrame({
    'id': [2, 3, 5],
    'age': [25, 30, 35]
})


# Perform an inner join on the 'id' column
joined_df = df1.join(df2, on='id')


# Display the joined DataFrame
joined_df


# Create a Polars DataFrame
df_polars = pl.DataFrame({
    'column_A': [1, 2, 3],
    'column_B': ['apple', 'banana', 'orange']
})


# Convert Polars DataFrame to Pandas DataFrame
df_pandas = df_polars.to_pandas()


# Display the Pandas DataFrame
df_pandas