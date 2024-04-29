# main.py
import os
from medium_api import MediumAPI
import pandas as pd

graph_query = open('searchquery.qu', 'r').read()
search_keywords = ['Health and Fitness', 'Fashion and Beauty', 'Travel']
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
}

def main():
    for keyword in search_keywords:
        count = 0
        folder_path = f'{keyword}_data'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        medium_api = MediumAPI(headers)
        dics = medium_api.search_posts(keyword, graph_query, results_limit=50, max_pages=10)
        
        for dic in dics:
            try:
                content = medium_api.get_post_content(dic['medium_url'])
                if content:
                    count += 1
                    file_path = os.path.join(folder_path, f'{count}.docx')
                    f = open(file_path, 'w', encoding='utf-8')
                    f.write(content)
                    f.flush()
                    f.close()

            except Exception as e:
                print(f"Error processing post: {e}")

    folders = ["Fashion and Beauty_data", "Health and Fitness_data", "Travel_data"]

    # Read data from each folder
    all_data = []
    for folder in folders:
        folder_path = os.path.join(os.getcwd(), folder)
        folder_data = read_text_files(folder_path, folder)
        all_data.extend(folder_data)

    # Create DataFrame
    df = pd.DataFrame(all_data, columns=["Serial Number", "Text Data", "Category"])

    # Write DataFrame to Excel
    output_excel_path = "Data.xlsx"
    df.to_excel(output_excel_path, index=False)


def read_text_files(folder_path, folder_name, max_files=15):
    file_data = []
    serial=1
    category=folder_name.replace("_data","")
    for idx, filename in enumerate(os.listdir(folder_path)):
        if idx >= max_files:
            break
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                file_data.append((serial, text, category))
                serial+=1
    return file_data

if __name__ == "__main__":
    main()