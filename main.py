import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from database import FashionDB
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google Gemini-Pro Vision
genai.configure(api_key=GOOGLE_API_KEY)


class FashionAgent:
    def __init__(self):
        """Initialize AI model and database."""
        self.db = FashionDB()

    def analyze_outfit(self, image_path):
        """Analyze uploaded outfit image and suggest matching items."""
        try:
            # Load image
            with open(image_path, "rb") as img_file:
                image = Image.open(BytesIO(img_file.read()))

            # Call Google Gemini-Pro Vision
            model = genai.GenerativeModel("gemini-1.5-pro-001")
            response = model.generate_content(
                [image, "Analyze this outfit and describe its style, colors, and gender suitability."]
            )

            # Check if AI returned anything meaningful
            outfit_description = response.text if response and response.text else "General Casual Style"
            print("\n🔹 Detected Outfit:", outfit_description)  # Debug Output

            # Extract gender and primary color from AI response (Basic NLP extraction)
            gender = None
            primary_color = None
            response_lower = outfit_description.lower()

            # Detect Gender
            if "women" in response_lower:
                gender = "women"
            elif "men" in response_lower:
                gender = "men"
            elif "unisex" in response_lower:
                gender = "unisex"

            # Detect Primary Color (List can be expanded)
            color_list = ["black", "white", "red", "blue", "green", "yellow", "pink", "purple", "grey", "brown", "orange"]
            for color in color_list:
                if color in response_lower:
                    primary_color = color
                    break  # Pick the first detected color

            print(f"🔹 Extracted Gender: {gender}, Primary Color: {primary_color}")  # Debug Output

            # Fetch matching products from DB
            products = self.db.get_products(gender=gender, primary_color=primary_color)

            # If no exact matches, fetch general recommendations
            if products.empty:
                print("⚠️ No specific matches found! Showing general recommendations.")
                products = self.db.get_products().sample(n=3)

            # Convert products to dictionary format
            product_list = products.head(5).to_dict(orient="records")

            # Ensure `ProductID` is removed from each product
            for product in product_list:
                product.pop("ProductID", None)

            # Debug: Print filtered product list
            print("\n✅ Filtered Product List for AI (Without ID):")
            print(product_list)

            # AI Recommendation Prompt
            recommendation_prompt = f"""
            Based on this outfit: {outfit_description}
            Extracted Gender: {gender}, Primary Color: {primary_color}
            Here are 5 relevant products from the catalog: {product_list}

            Suggest 3 items that best match this outfit considering:
            - Style
            - Color coordination
            - Occasion suitability
            """

            rec_model = genai.GenerativeModel("gemini-1.5-pro-001")
            recommendation = rec_model.generate_content(recommendation_prompt)

            # If AI fails, return default products without `product_id`
            if not recommendation or not recommendation.text:
                print("⚠️ AI could not generate recommendations! Showing default items.")
                return f"Here are some matching products:\n{product_list}"

            return recommendation.text

        except Exception as e:
            # Fallback: Return products without `product_id`
            fallback_products = self.db.get_products().head(3).to_dict(orient="records")

            # Ensure `product_id` is removed from each fallback product
            for product in fallback_products:
                product.pop("ProductID", None)

            return f"⚠️ Error processing image: {str(e)}\nHere are some products instead:\n{fallback_products}"


# Test Image Analysis Feature
if __name__ == "__main__":
    agent = FashionAgent()
    image_path = "test_2.jpg"  # Replace with actual image
    print("\n🔹 AI Recommendations:\n", agent.analyze_outfit(image_path))
