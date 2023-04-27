import openai
import os
import pandas as pd

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def classify_transaction(transaction_data):
    prompt = f"""PROMPT:

You will classify transactions. You will be send a row which contains transaction data. Respond ONLY with the relevant category. Do not respond with any commentary or extra text.

CATEGORIES:

Groceries: Supermarkets, local grocery stores, and food markets
Dining Out: Restaurants, cafes, fast food, and takeaway meals
Entertainment: Movies, concerts, theater, and events
Utilities: Electricity, water, gas, and telecommunications
Transportation: Public transport, taxis, rideshares, and fuel
Health & Fitness: Gym memberships, personal training, and supplements
Insurance: Health, car, home, and life insurance premiums
Subscriptions & Services: Streaming services, magazines, newspapers, and software (e.g., Adobe Photog)
Travel: Flights, accommodation, and travel-related expenses
Shopping: Clothing, electronics, and other retail purchases
Home & Maintenance: Rent, mortgage, home repairs, and furnishings
Education: Tuition fees, textbooks, and course materials
Gifts & Donations: Charitable donations, birthdays, and holidays
Medical: Doctor visits, prescription medication, and health-related expenses
Miscellaneous: Any other transactions that don't fit into the above categories

DATA:

{transaction_data}
"""
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=30,
        n=1,
        stop=None,
        temperature=0.7,
    )

    category = response.choices[0].text.strip()
    return category

def process_csv_directory(directory_path):
    all_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.csv')]
    
    # Join all CSV files into a single DataFrame
    df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)
    
    # Add "ai_classification" column
    df["ai_classification"] = ""
    
    for index, row in df.iterrows():
        transaction_data = row.to_string(index=False, header=False)
        category = classify_transaction(transaction_data)
        df.at[index, "ai_classification"] = category
        print(f"Category for transaction {index}: {category}")
        
        # Save the DataFrame to an xlsx file after each API call
        df.to_excel("final_data.xlsx", index=False)

directory_path = "path/to/csv_files"
process_csv_directory(directory_path)
