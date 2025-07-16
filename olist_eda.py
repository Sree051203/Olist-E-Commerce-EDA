import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


customers = pd.read_csv('data/olist_customers_dataset.csv')
orders = pd.read_csv('data/olist_orders_dataset.csv')
order_items = pd.read_csv('data/olist_order_items_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')
sellers = pd.read_csv('data/olist_sellers_dataset.csv')
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')
geolocation = pd.read_csv('data/olist_geolocation_dataset.csv')
payments = pd.read_csv('data/olist_order_payments_dataset.csv')

print("Data Loaded!")


print(customers.head())
print(orders.head())
print(order_items.head())


cust_orders = pd.merge(customers, orders, on='customer_id', how='inner')
items_products = pd.merge(order_items, products, on='product_id', how='inner')
cust_orders_items = cust_orders.merge(items_products, on='order_id', how='inner')
full_data = cust_orders_items.merge(payments, on='order_id', how='inner')

print("Merged Data Shape:", full_data.shape)
print(full_data.head())


print(full_data.isnull().sum())


orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_purchase_date'] = orders['order_purchase_timestamp'].dt.date

daily_orders = orders.groupby('order_purchase_date')['order_id'].count().reset_index()
daily_orders.rename(columns={'order_id': 'num_orders'}, inplace=True)

plt.figure(figsize=(15,5))
sns.lineplot(data=daily_orders, x='order_purchase_date', y='num_orders')
plt.title('Daily Orders Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/daily_orders.png')
plt.show()


prod_cat = pd.merge(order_items, products, on='product_id', how='inner')
top_cats = prod_cat['product_category_name'].value_counts().head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_cats.values, y=top_cats.index, palette="viridis")
plt.title('Top 10 Product Categories by Orders')
plt.xlabel('Number of Orders')
plt.tight_layout()
plt.savefig('output/top_categories.png')
plt.show()


payment_types = payments['payment_type'].value_counts()

plt.figure(figsize=(8,5))
sns.barplot(x=payment_types.index, y=payment_types.values, palette="pastel")
plt.title('Payment Methods Breakdown')
plt.xlabel('Payment Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('output/payment_methods.png')
plt.show()


status_counts = orders['order_status'].value_counts()

plt.figure(figsize=(8,5))
sns.barplot(x=status_counts.index, y=status_counts.values, palette="coolwarm")
plt.title('Order Status Distribution')
plt.xlabel('Status')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('output/order_status.png')
plt.show()


full_data.to_csv('output/merged_data.csv', index=False)
print("Cleaned & Merged Data Saved to output/merged_data.csv")
