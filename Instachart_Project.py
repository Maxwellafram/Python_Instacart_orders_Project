#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis (EDA) on Instacart Orders Dataset
# 
# ## Introduction
# This project aims to analyze customer shopping behavior using the Instacart dataset. The dataset contains transactional data, including details about orders, products, aisles, and departments. Through **data cleaning, preprocessing, and visualization**, we uncover insights about purchasing patterns, reorder behaviors, and shopping trends.
# 
# ## Project Objectives
# 1. **Data Cleaning & Preprocessing**  
#    - Handle missing values, duplicate entries, and ensure data integrity.  
# 2. **Exploratory Data Analysis (EDA)**  
#    - Identify trends in shopping behavior (e.g., peak shopping hours, most purchased items).  
#    - Analyze reorder patterns and customer purchasing habits.  
# 3. **Business Insights**  
#    - Provide actionable insights that can help Instacart optimize inventory, marketing, and customer retention strategies.
# 
# ## Dataset Overview
# - `orders.csv`: Contains details about each customer order (order ID, user ID, time of order, etc.).
# - `products.csv`: Includes product information (product ID, name, aisle, department).
# - `aisles.csv`: Maps each product to its respective aisle.
# - `departments.csv`: Categorizes products into broader department groups.
# - `order_products`: Link products to orders and indicate reorder status.
# 
# 
# This EDA project will utilize **Python, Pandas, and Matplotlib** to extract meaningful patterns from the data. The findings will help in understanding customer behavior, optimizing operations, and improving user experience.
# 

# In[2]:


import pandas as pd


# In[3]:


#reading the orders Data
orders = pd.read_csv('C:/Users/kwame/Downloads/instacart_orders.csv', sep=';')


# In[4]:


orders.head()


# In[5]:


#reading the orders_products data
order_products = pd.read_csv('C:/Users/kwame/Downloads/order_products.csv',sep=';')


# In[6]:


order_products.head()


# In[7]:


products = pd.read_csv('C:/Users/kwame/Downloads/products.csv',sep=';')


# In[8]:


products.head()


# In[9]:


aisles = pd.read_csv('C:/Users/kwame/Downloads/aisles.csv',sep=';')


# In[10]:


aisles.head()


# In[11]:


departments = pd.read_csv('C:/Users/kwame/Downloads/departments.csv',sep=';')


# In[12]:


departments.head()


# ## Find and remove duplicate values in the orders dataframe

# ## Reasons for this process
# - **If duplicates exist, they could indicate errors in data collection or processing**.
# - **Duplicates could lead to double-counting orders in any subsequent analysis, such as customer purchase patterns and reorder rates.**

# In[13]:


# Check for duplicated in orders dataframe
duplicate_orders = orders[orders.duplicated()]
print(f"Number of duplicate rows in orders: {duplicate_orders.shape[0]}")


# In[14]:


# Check for all orders placed Wednesday at 2:00 AM
wednesday_2am_orders = orders[(orders['order_dow'] == 3) & (orders['order_hour_of_day'] == 2)]

print(f"Number of orders placed on Wednesday at 2:00 AM: {wednesday_2am_orders.shape[0]}")
print(wednesday_2am_orders.head())


# In[15]:


# Remove duplicate orders

# Check for duplicate order IDs
duplicate_orders = orders[orders.duplicated(subset=['order_id'], keep=False)]
print(f"Number of duplicate orders: {duplicate_orders.shape[0]}")

# Remove duplicate orders while keeping the first occurrence
orders_cleaned = orders.drop_duplicates(subset=['order_id'], keep='first')

# Verify duplicates are removed
print(f"Number of unique orders after cleaning: {orders_cleaned.shape[0]}")


# In[16]:


# Double check for duplicate order IDs only
duplicate_rows = orders_cleaned[orders_cleaned.duplicated(keep=False)]

print(f"Number of fully duplicate rows: {duplicate_rows.shape[0]}")


# ## Find and remove duplicate values in the order_products dataframe

# In[17]:


# Check for fullly duplicate rows

duplicate_rows = order_products[order_products.duplicated(keep=False)]

print(f"Number of fully duplicate rows: {duplicate_rows.shape[0]}")


# In[18]:


# Check for duplicate order_id and product_id pairs
duplicate_order_product_pairs = order_products[order_products.duplicated(subset=['order_id', 'product_id'], keep=False)]
print(f"Number of duplicate order-product pairs: {duplicate_order_product_pairs.shape[0]}")

# Check for any duplicate rows with slight variations (e.g., whitespace issues)
stripped_order_products = order_products.map(lambda x: x.strip() if isinstance(x, str) else x)
duplicate_rows_stripped = stripped_order_products[stripped_order_products.duplicated(keep=False)]
print(f"Number of duplicate rows after stripping whitespace: {duplicate_rows_stripped.shape[0]}")

# If any tricky duplicates are found, we can drop them
order_products_cleaned = stripped_order_products.drop_duplicates()
print(f"Number of rows after removing tricky duplicates: {order_products_cleaned.shape[0]}")


# ## Find and remove duplicate values in the products dataframe

# ## Reasons for this processes 
# - **Check for duplicate product IDs**
# - **Each product should be uniquely identified by 'product_id'.**
# - **If duplicate product IDs exist, it could mean duplicate product entries in the catalog,leading to data inconsistencies and potential errors in analysis.**

# In[19]:


# Check for fully duplicate rows
duplicate_products = products[products.duplicated(keep=False)]

print(f"Number of fully duplicate rows in Products DataFrame: {duplicate_products.shape[0]}")


# In[20]:


 #Check for just duplicate product IDs
duplicate_product_ids = products[products.duplicated(subset=['product_id'], keep=False)]

print(f"Number of duplicate product IDs: {duplicate_product_ids.shape[0]}")


# In[21]:


# Check for just duplicate product names (convert names to lowercase to compare better)

# Convert product names to lowercase and check for duplicates
duplicate_product_names = products[products.duplicated(subset=['product_name'], keep=False)]

print(f"Number of duplicate product names (case-sensitive): {duplicate_product_names.shape[0]}")

# Convert product names to lowercase for better comparison
products['product_name_lower'] = products['product_name'].str.lower()

# Check for duplicate product names (case-insensitive)
duplicate_product_names_lower = products[products.duplicated(subset=['product_name_lower'], keep=False)]

print(f"Number of duplicate product names (case-insensitive): {duplicate_product_names_lower.shape[0]}")


# In[22]:


# Check for duplicate product names that aren't missing
# Drop missing values in 'product_name'
non_missing_products = products.dropna(subset=['product_name']).copy()

# Convert product names to lowercase for better comparison
non_missing_products.loc[:, 'product_name_lower'] = non_missing_products['product_name'].str.lower()

# Find duplicate product names (ignoring case)
duplicate_product_names = non_missing_products[non_missing_products.duplicated(subset=['product_name_lower'], keep=False)]

print(f"Number of duplicate product names (excluding missing values): {duplicate_product_names.shape[0]}")


# ## Find and remove duplicate values in the aisle dataframe

# ## Reasons for this process
# - **Check for duplicate aisle IDs**
# - **Each aisle should be uniquely identified by aisle_id.**
# - **Duplicates could indicate data mismanagement or duplicate aisle names.**

# In[23]:


# Check for fully duplicate rows in the aisles dataframe
duplicate_aisles = aisles[aisles.duplicated(keep=False)]

# Print the number of fully duplicate rows
print(f"Number of fully duplicate rows: {duplicate_aisles.shape[0]}")

# Display duplicate rows if any
duplicate_aisles


# In[24]:


# Remove fully duplicate rows from the aisles dataframe
aisles = aisles.drop_duplicates()

# Print confirmation
print(f"Number of rows after removing duplicates: {aisles.shape[0]}")


# ## Find and remove duplicate values in the department dataframe

# ## Reasons for this process
# 
# - **Check for duplicate department IDs**
# - **Each department should be uniquely identified by department_id.**
# - **Duplicates could indicate data integrity issues and inconsistencies in department labeling.**

# In[25]:


# Check for fully duplicate rows in the department dataframe
duplicate_departments = departments[departments.duplicated(keep=False)]

# Print the number of fully duplicate rows
print(f"Number of fully duplicate rows: {duplicate_departments.shape[0]}")

# Display duplicate rows if any
duplicate_departments


# In[26]:


# Remove fully duplicate rows from the department dataframe
departments = departments.drop_duplicates()

# Print confirmation
print(f"Number of rows after removing duplicates: {departments.shape[0]}")


# 

# ## Find and remove missing values
# 
# ## products data frame

# In[27]:


# Check for missing values in the products DataFrame
missing_values = products.isnull().sum()
print("Missing values per column:\n", missing_values)

# Drop rows where product_name is missing and create a copy to avoid SettingWithCopyWarning
products_cleaned = products.dropna(subset=['product_name']).copy()

# Fill missing aisle_id and department_id safely
products_cleaned.loc[:, ['aisle_id', 'department_id']] = products_cleaned[['aisle_id', 'department_id']].fillna(-1)

# Check if missing values are removed
print("Missing values after cleaning:\n", products_cleaned.isnull().sum())


# In[28]:


# Are all of the missing product names associated with aisle ID 100?
missing_products = products[products['product_name'].isna()]  # Filter missing product names

# Check if all missing product names have aisle_id 100
all_aisle_100 = missing_products['aisle_id'].eq(100).all()

print(f"Are all missing product names associated with aisle ID 100? {all_aisle_100}")


# In[29]:


# Are all of the missing product names associated with department ID 21?

# Check if all missing product names have department_id 21
all_department_21 = missing_products['department_id'].eq(21).all()

print(f"Are all missing product names associated with department ID 21? {all_department_21}")


# In[30]:


# What is this ailse and department?
# Get the aisle name for ID 100
aisle_name = aisles.loc[aisles['aisle_id'] == 100, 'aisle'].values[0]

# Get the department name for ID 21
department_name = departments.loc[departments['department_id'] == 21, 'department'].values[0]

print(f"Aisle ID 100 corresponds to: {aisle_name}")
print(f"Department ID 21 corresponds to: {department_name}")


# In[31]:


# Fill missing product names with 'Unknown'
# Fill missing product names with 'Unknown'
products['product_name'].fillna('Unknown', inplace=True)

# Verify that there are no missing values left
missing_count = products['product_name'].isna().sum()
print(f"Number of missing product names after filling: {missing_count}")


# ## orders data frame

# In[32]:


# Check for missing values in the orders DataFrame
missing_values = orders.isnull().sum()
print("Missing values in each column:\n", missing_values)


# In[33]:


# Are there any missing values where it's not a customer's first order?
# Check for missing values in 'days_since_prior_order'
missing_orders = orders[orders['days_since_prior_order'].isnull()]
print(f"Total missing values in 'days_since_prior_order': {missing_orders.shape[0]}")


# Check if all missing values belong to first orders (order_number == 1)
non_first_order_missing = missing_orders[missing_orders['order_number'] != 1]

# Display the results
if non_first_order_missing.shape[0] == 0:
    print("✅ All missing values in 'days_since_prior_order' belong to first orders.")
else:
    print(f"⚠️ There are {non_first_order_missing.shape[0]} missing values in non-first orders.")
    print(non_first_order_missing)


# 

# ## order_products data frame

# In[34]:


# Check for missing values in order_products dataframe
missing_values = order_products.isnull().sum()
print("Missing values in order_products dataframe:\n", missing_values)


# In[35]:


# What are the min and max values in this column?

min_value = order_products['add_to_cart_order'].min()
max_value = order_products['add_to_cart_order'].max()

print(f"Minimum add_to_cart_order: {min_value}")
print(f"Maximum add_to_cart_order: {max_value}")


# In[36]:


# Save all order IDs with at least one missing value in 'add_to_cart_order'

# Find order_ids with missing values in 'add_to_cart_order'
orders_with_missing = order_products[order_products['add_to_cart_order'].isna()]['order_id'].unique()

# Save to a CSV file
pd.DataFrame(orders_with_missing, columns=['order_id']).to_csv("orders_with_missing_add_to_cart_order.csv", index=False)

print(f"Saved {len(orders_with_missing)} orders with missing 'add_to_cart_order' values.")


# In[37]:


# Do all orders with missing values have more than 64 products?

# Count the number of products per order
order_counts = order_products.groupby('order_id')['product_id'].count()

# Get orders with missing 'add_to_cart_order' values
orders_with_missing = order_products[order_products['add_to_cart_order'].isna()]['order_id'].unique()

# Check if all these orders have more than 64 products
all_above_64 = (order_counts[orders_with_missing] > 64).all()

print(f"Do all orders with missing values have more than 64 products? {all_above_64}")


# In[38]:


# Replace missing values with 999 and convert column to integer type

# Convert to nullable integer type (allows missing values to remain as NaN)
order_products['add_to_cart_order'] = order_products['add_to_cart_order'].astype('Int64')

# Verify changes
print(order_products['add_to_cart_order'].dtype)  # Should print 'Int64'
print(order_products['add_to_cart_order'].isna().sum())  # This will show the count of missing values


# 

# 

# ## Verify that the 'order_hour_of_day' and 'order_dow' values in the orders tables are sensible (i.e. 'order_hour_of_day' ranges from 0 to 23 and 'order_dow' ranges from 0 to 6)

# In[39]:


# Check the range of order_hour_of_day
min_hour = orders['order_hour_of_day'].min()
max_hour = orders['order_hour_of_day'].max()

# Check the range of order_dow
min_dow = orders['order_dow'].min()
max_dow = orders['order_dow'].max()

# Print results
print(f"order_hour_of_day ranges from {min_hour} to {max_hour}")
print(f"order_dow ranges from {min_dow} to {max_dow}")

# Check for unexpected values
unexpected_hours = orders[~orders['order_hour_of_day'].between(0, 23)]
unexpected_dow = orders[~orders['order_dow'].between(0, 6)]

# Display any problematic rows
if not unexpected_hours.empty:
    print("Unexpected values found in order_hour_of_day:")
    print(unexpected_hours)

if not unexpected_dow.empty:
    print("Unexpected values found in order_dow:")
    print(unexpected_dow)


# 

# ## What time of day do people shop for groceries?

# In[40]:


import matplotlib.pyplot as plt
import seaborn as sns

# Count orders by hour of the day
order_hour_counts = orders['order_hour_of_day'].value_counts().sort_index()

# Plot the distribution
plt.figure(figsize=(10, 5))
sns.barplot(x=order_hour_counts.index, y=order_hour_counts.values, color="royalblue")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")
plt.title("Grocery Shopping Trends by Hour of Day")
plt.xticks(range(0, 24))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# ### Insights from Grocery Shopping Trends by Hour of Day
# - Most grocery orders are placed between **10 AM and 4 PM**, with a peak around **12 PM (noon)**.
# - Shopping activity starts increasing around **8 AM** and drops sharply after **8 PM**.
# - **Early morning (0–6 AM)** sees very few orders, likely due to store closures or low demand.
# 
# ## Business Implications:
# - Retailers can schedule staff shifts to match peak hours and ensure adequate stock.
# - Promotions and targeted ads can be more effective during high-traffic hours (10 AM–4 PM).
# - Midnight and early morning orders could indicate demand for 24/7 delivery options.

# 

# ## What day of the week do people shop for groceries?

# In[41]:


# Count orders by day of the week
order_dow_counts = orders['order_dow'].value_counts().sort_index()

# Plot the distribution
plt.figure(figsize=(8, 5))
sns.barplot(x=order_dow_counts.index, y=order_dow_counts.values, color="royalblue")
plt.xlabel("Day of the Week (0 = Sunday, 6 = Saturday)")
plt.ylabel("Number of Orders")
plt.title("Grocery Shopping Trends by Day of the Week")
plt.xticks(range(0, 7), ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# ## Insights from Grocery Shopping Trends by Day of the Week
# The highest number of grocery orders are placed on Saturdays and Sundays, indicating that most people prefer shopping over the weekend.
# Order volume starts decreasing from Monday to Friday, suggesting that weekdays are less busy for grocery shopping.
# The lowest number of orders are typically placed on Tuesdays and Wednesdays.
# ## Business Implications
# Stock Optimization: Grocery stores and delivery services should stock up and optimize staffing for weekends to handle the high demand.
# Weekday Promotions: Retailers can run weekday promotions or discounts to encourage shopping on slower days like Tuesday and Wednesday.
# Delivery Logistics: Delivery services may need more drivers on weekends to meet the higher order volume.

# 

# ## How long do people wait until placing another order?

# In[42]:


# Count occurrences of each unique value in 'days_since_prior_order'
days_counts = orders['days_since_prior_order'].value_counts().sort_index()

# Plot the distribution
plt.figure(figsize=(10, 5))
sns.barplot(x=days_counts.index, y=days_counts.values, color="royalblue")
plt.xlabel("Days Since Prior Order")
plt.ylabel("Number of Orders")
plt.title("Time Between Grocery Orders")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# ## Insights from Time Between Grocery Orders
# The distribution of days since the prior order shows clear peaks at 7, 14, 21, and 30 days, suggesting that many customers follow a weekly or monthly shopping cycle.
# A significant portion of customers place orders exactly one week apart, likely due to weekly meal planning or grocery restocking habits.
# There is another noticeable peak around 30 days, which could indicate monthly bulk shoppers or customers who make large purchases less frequently.
# ## Business Implications
# Targeted Promotions: Retailers can offer weekly or monthly reminders and promotions to encourage repeat purchases.
# Subscription Services: Grocery stores could introduce weekly or monthly subscription-based grocery delivery plans to match customer buying patterns.
# Inventory Management: Stores can optimize inventory and restocking schedules to align with customer shopping habits, ensuring key products are available at peak times.

# 

#  ## Is there a difference in 'order_hour_of_day' distributions on Wednesdays and Saturdays? Plot the histograms for both days and describe the differences that you see.

# In[43]:


import matplotlib.pyplot as plt
import seaborn as sns

# Filter data for Wednesday (3) and Saturday (6)
wednesday_orders = orders[orders['order_dow'] == 3]['order_hour_of_day']
saturday_orders = orders[orders['order_dow'] == 6]['order_hour_of_day']

# Plot histograms
plt.figure(figsize=(12, 6))
sns.histplot(wednesday_orders, bins=24, color='blue', label='Wednesday', kde=True, alpha=0.6)
sns.histplot(saturday_orders, bins=24, color='orange', label='Saturday', kde=True, alpha=0.6)

# Labels and title
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")
plt.title("Distribution of Orders by Hour on Wednesday vs. Saturday")
plt.legend()
plt.xticks(range(0, 24))
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.show()


# ## Insights from Order Distribution on Wednesday vs. Saturday
# 
# - **Peak Hours:**  
#   - On **Wednesdays**, order activity gradually **increases after 7 AM**, peaking around **12 PM - 3 PM**, before declining in the evening.  
#   - On **Saturdays**, order volume starts increasing **earlier in the morning** and stays **higher for an extended period**, with a peak around **10 AM - 2 PM**.  
# 
# - **Differences in Shopping Behavior:**  
#   - **Weekday Shopping (Wednesday):** Likely influenced by **lunch breaks** or quick mid-week restocks.  
#   - **Weekend Shopping (Saturday):** Higher morning activity suggests **leisurely grocery trips** or **bulk shopping** for the upcoming week.  
# 
# 
# 
# ## Business Implications
# - **Optimize Promotions:** Retailers can schedule **weekday lunchtime promotions** for Wednesday shoppers and **weekend bundle deals** for Saturday customers.  
# - **Delivery Planning:** More delivery slots should be available in the **morning and midday on weekends** to accommodate the higher demand.  
# - **Staff Scheduling:** Grocery stores should **increase staffing on Saturday mornings** to handle peak traffic efficiently.  
# 

# 

# ### What's the distribution for the number of orders per customer?

# In[44]:


import matplotlib.pyplot as plt
import seaborn as sns

# Count number of orders per customer
customer_order_counts = orders.groupby('user_id')['order_number'].max()

# Plot the distribution
plt.figure(figsize=(12, 6))
sns.histplot(customer_order_counts, bins=50, kde=True, color="purple", alpha=0.7)

# Labels and title
plt.xlabel("Number of Orders per Customer")
plt.ylabel("Number of Customers")
plt.title("Distribution of Orders per Customer")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.show()


# ## Insights from the Distribution of Orders per Customer
# Customer Ordering Behavior:
# The majority of customers place only a few orders, indicating that many may be new users or infrequent shoppers.
# A smaller group of loyal customers places a high number of orders, demonstrating repeat purchasing behavior over time.
# The distribution likely follows a right-skewed pattern, with most users on the lower end and a few heavy shoppers on the higher end.
# ## Business Implications
# Customer Retention: Implement loyalty programs or personalized promotions to encourage repeat purchases among less frequent shoppers.
# High-Value Customers: Identify and reward loyal customers with exclusive deals, discounts, or subscription-based perks.
# Marketing Strategies: Segment customers based on their order frequency and tailor marketing campaigns to engage both occasional and frequent shoppers.

# 

# ## What are the top 20 popular products (display their id and name)?

# In[45]:


# Count the number of times each product appears in orders
top_products = order_products['product_id'].value_counts().reset_index()
top_products.columns = ['product_id', 'order_count']

# Merge with product names
top_products = top_products.merge(products[['product_id', 'product_name']], on='product_id', how='left')

# Display the top 20 products
top_20_products = top_products.head(20)
print(top_20_products)


# 

# ## How many items do people typically buy in one order? What does the distribution look like?

# In[46]:


# Count the number of products per order
order_sizes = order_products.groupby('order_id')['product_id'].count()

# Summary statistics
print(order_sizes.describe())


# In[47]:


# Plot histogram
plt.figure(figsize=(10, 5))
plt.hist(order_sizes, bins=50, edgecolor='black')
plt.xlabel("Number of Items in an Order")
plt.ylabel("Frequency")
plt.title("Distribution of Items per Order")
plt.xlim(0, 100)  # Limit x-axis for readability
plt.yscale('log')  # Log scale for better visualization of distribution
plt.show()


# ## Insights from the Distribution of Items per Order
# Order Size Variability:
# Most grocery orders contain a moderate number of items, with a declining frequency as order size increases.
# A long tail is observed, where some customers place very large orders, though they are relatively rare.
# The logarithmic scale highlights that small to mid-sized orders are the most common, while bulk shopping occurs less frequently.
# ## Business Implications
# Cart Optimization: Encourage larger basket sizes through bundling offers, discounts on bulk purchases, or free shipping thresholds.
# Stocking Strategy: Retailers can adjust inventory planning by focusing on frequently purchased item quantities to reduce stockouts.
# Logistics & Delivery: Understanding order sizes can help optimize packaging, delivery schedules, and fulfillment strategies for online grocery services.

# 

# ## What are the top 20 items that are reordered most frequently (display their names and product IDs)?

# In[48]:


# Count reorders for each product_id
reorder_counts = order_products[order_products['reordered'] == 1] \
    .groupby('product_id')['reordered'].count() \
    .reset_index() \
    .rename(columns={'reordered': 'reorder_count'})

# Merge with products dataframe to get product names
top_reordered_products = reorder_counts.merge(products, on='product_id')

# Sort by reorder count and select top 20
top_20_reordered = top_reordered_products.sort_values(by='reorder_count', ascending=False).head(20)

# Display results
print(top_20_reordered[['product_id', 'product_name', 'reorder_count']])


# 

# ## For each product, what proportion of its orders are reorders?

# In[49]:


# Total orders per product
total_orders = order_products.groupby('product_id').size().reset_index(name='total_orders')

# Total reorders per product
reorder_counts = order_products[order_products['reordered'] == 1] \
    .groupby('product_id').size().reset_index(name='total_reorders')

# Merge both datasets on product_id
reorder_proportion = total_orders.merge(reorder_counts, on='product_id', how='left')

# Fill missing values (some products may have zero reorders)
reorder_proportion['total_reorders'] = reorder_proportion['total_reorders'].fillna(0)

# Compute reorder proportion
reorder_proportion['reorder_proportion'] = reorder_proportion['total_reorders'] / reorder_proportion['total_orders']

# Merge with product names
reorder_proportion = reorder_proportion.merge(products[['product_id', 'product_name']], on='product_id')

# Display results sorted by reorder proportion
print(reorder_proportion[['product_id', 'product_name', 'reorder_proportion']].sort_values(by='reorder_proportion', ascending=False))


# 

# ## For each customer, what proportion of their products ordered are reorders?

# In[50]:


# Merge orders with order_products to get user_id
orders_merged = order_products.merge(orders[['order_id', 'user_id']], on='order_id')

# Total products ordered per customer
total_products_per_user = orders_merged.groupby('user_id').size().reset_index(name='total_products')

# Total reorders per customer
reordered_products_per_user = orders_merged[orders_merged['reordered'] == 1] \
    .groupby('user_id').size().reset_index(name='total_reorders')

# Merge both datasets
reorder_proportion_per_user = total_products_per_user.merge(reordered_products_per_user, on='user_id', how='left')

# Fill missing values (some users may have zero reorders)
reorder_proportion_per_user['total_reorders'] = reorder_proportion_per_user['total_reorders'].fillna(0)

# Compute reorder proportion
reorder_proportion_per_user['reorder_proportion'] = reorder_proportion_per_user['total_reorders'] / reorder_proportion_per_user['total_products']

# Display results
print(reorder_proportion_per_user.sort_values(by='reorder_proportion', ascending=False))


# 

# ## What are the top 20 items that people put in their carts first?

# In[51]:


# Filter for first item added to the cart
first_added = order_products[order_products['add_to_cart_order'] == 1]

# Count occurrences of each product
first_added_counts = first_added['product_id'].value_counts().reset_index()
first_added_counts.columns = ['product_id', 'first_added_count']

# Merge with product names
top_20_first_added = first_added_counts.merge(products[['product_id', 'product_name']], on='product_id')

# Display top 20 products
top_20_first_added.head(20)


# 

# # Conclusion: Instacart Grocery Shopping Analysis
# 
# ## Project Objectives 
# This project aimed to analyze Instacart’s online grocery shopping data to uncover key trends in **customer behavior, shopping habits, and reorder patterns**. By leveraging exploratory data analysis (EDA), we examined how customers interact with the platform, which products are most popular, and the frequency of repeat purchases.
# 
# 
# ## Key Findings and Insights 
# 
# ### Shopping Behavior Patterns
# - **Peak Shopping Times:** Most orders are placed during the **late morning and early afternoon**, with activity peaking around **10 AM - 3 PM**.  
# - **Weekday vs. Weekend Trends:** **Saturdays and Sundays** see the highest order volumes, while **Tuesdays and Wednesdays** are the least busy shopping days.  
# 
# ### Reorder Trends
# - **Frequent Reordering:** Many customers reorder items they previously purchased, with certain **staples like fresh produce and dairy products** being re-bought often.  
# - **Time Between Orders:** A significant number of customers reorder within **7 to 30 days**, indicating a regular grocery shopping cycle.  
# 
# ###  Product Popularity and Ordering Trends
# - **Top Products:** The most frequently purchased items include **bananas, organic strawberries, and whole milk**.  
# - **First-to-Cart Products:** Some items consistently appear as the **first product added to the cart**, possibly due to **habitual purchasing patterns**.  
# 
# ### Order Size and Customer Engagement
# - **Typical Cart Size:** Most customers buy between **5 to 20 items per order**, but some place **bulk orders with over 50 items**.  
# - **Customer Lifetime Orders:** Many users have placed multiple orders, with some reaching over **100 orders** on the platform.  
# 
# ## Challenges and Learnings
# - **Handling Missing Data:** The dataset contained missing values in columns such as `days_since_prior_order`, which required careful imputation or exclusion strategies.  
# - **Dealing with Duplicates:** Ensuring **unique product, aisle, and department identifiers** was critical for accurate analysis.  
# - **Computational Efficiency:** Processing millions of orders required **efficient use of Pandas and Seaborn** to avoid performance bottlenecks.  
# 
# 
# ## Business Impact & Recommendations
# ### For Retailers & Instacart
# - **Optimize Inventory for Peak Hours:** Ensure sufficient stock and efficient restocking for high-demand time slots (late mornings and weekends).  
# - **Encourage Weekday Shopping:** Offer **weekday discounts** or **loyalty incentives** to spread demand more evenly.  
# - **Personalized Recommendations:** Utilize reorder patterns to suggest frequently purchased items to customers, reducing friction in the shopping experience.  
# 
# ### For Delivery & Logistics
# - **Weekend Workforce Planning:** Scale up delivery personnel on **Saturdays and Sundays** to handle peak order volumes.  
# - **Optimize Last-Mile Delivery:** Understanding reorder frequencies can **improve fulfillment strategies**, ensuring faster deliveries for recurring customers.  
# 
# 
# ## Future Work & Next Steps
# - **Advanced Predictive Modeling:** Develop a **reorder prediction model** using machine learning to forecast which products a customer is likely to buy next.  
# - **Customer Segmentation:** Perform clustering analysis to **categorize customers** based on their shopping habits and order frequency.  
# - **Deeper Product Analysis:** Investigate **cross-category purchase behavior**, such as whether customers who buy baby products also purchase organic foods.  
# 

# ### Final Thoughts 
# This project successfully uncovered key **shopping behaviors, reorder patterns, and product 
# trends** in the Instacart dataset. The findings have valuable implications for **retailers, 
# logistics teams, and data-driven decision-making** in e-commerce grocery platforms. 

# In[ ]:




