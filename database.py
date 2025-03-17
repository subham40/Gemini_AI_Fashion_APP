import pandas as pd


class FashionDB:
    def __init__(self, file_path="products.csv"):
        """Load product catalog from CSV."""
        self.df = pd.read_csv(file_path)

        # Ensure Gender and PrimaryColor columns are properly stripped of spaces and lowercased
        self.df['Gender'] = self.df['Gender'].astype(str).str.strip().str.lower()
        self.df['PrimaryColor'] = self.df['PrimaryColor'].astype(str).str.strip().str.lower()

    def get_products(self, gender=None, primary_color=None):
        """Retrieve products filtered by gender and primary color."""
        filtered_df = self.df

        # Filter by gender (include Unisex products as well)
        if gender:
            gender = gender.strip().lower()
            filtered_df = filtered_df[filtered_df['Gender'].isin([gender, 'unisex'])]

        # Filter by primary color
        if primary_color:
            primary_color = primary_color.strip().lower()
            filtered_df = filtered_df[filtered_df['PrimaryColor'] == primary_color]

        return filtered_df

    def get_product_details(self, product_id):
        """Retrieve product details by ID."""
        product = self.df[self.df['ProductID'] == product_id]
        return product.to_dict(orient="records")[0] if not product.empty else None


# Test database connection
if __name__ == "__main__":
    db = FashionDB()

    # Check all products
    print("All Products:\n", db.get_products().head())

    # Test gender filter
    print("\nFiltered Products (Gender = Men):\n", db.get_products(gender="Men").head())

    # Test gender + color filter
    print("\nFiltered Products (Gender = Women, PrimaryColor = Black):\n",
          db.get_products(gender="Men", primary_color="Black").head())

    # Fetch a product by ID
    # print("\nProduct Details (ID = 10017413):\n", db.get_product_details(10017413))
