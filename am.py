import requests
from bs4 import BeautifulSoup
import json
import csv
# from concurrent.futures import ThreadPoolExecutor
# Define the JSON data
# Define the path to your JSON file
# json_file_path = 'euabc.json'
json_file_path = 'america-name-address.json'


# def process_item(item, writer):

#     # Extract the DetailsDispatch variable from the JSON data
    
# output_csv_file_path = 'europe_data.csv'
# # Write the data to the new CSV file with separate columns for "Name" and "Age"
# with open(output_csv_file_path, 'a', newline='') as csv_output_file:
#     writer = csv.writer(csv_output_file)
    
#     # Write the header row
#     writer.writerow(['Name', 'Address', 'Phone', 'Email'])
    
#     # Read and parse the JSON file
#     with open(json_file_path, 'r') as json_file:
#         json_data = json.load(json_file)

#         with ThreadPoolExecutor(max_workers=2) as executor:
#             # Submit each JSON item for processing
#             for item in json_data:
#                 executor.map(process_item, item)
#         # Iterate through the JSON data


import asyncio
import aiohttp
import csv

# Define the list of elements for which API calls will be made


# Function to make an asynchronous API call
async def fetch_element_data(session, item):
    id = item.get("Id")
    details_dispatch = item.get("DetailsDispatch")
    name = item.get("Name")
    address = item.get("FullAddress")
    max_retries = 3
    url = f'https://cafa.iphiview.com/cafa/Organizations/OrganizationView/tabid/437/dispatch/{details_dispatch}/Default.aspx'
    for retry in range(max_retries):
        try:
            async with session.get(url) as response:
                phone = ""
                email = ""
                try:
                    # Check if the request was successful (status code 200)
                    if response.status == 200:
                        # Parse the HTML response
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        
                        # Find all <td> elements
                        all_communications_div = soup.find('div', class_='AllCommunications')
                        td_tags = all_communications_div.find_all('td')
                        
                        try:
                            phone = td_tags[1].get_text()
                        except:
                            1
                        
                        try:
                            email = td_tags[3].get_text()
                        except:
                            1
                        
                            # Print the text content of the 2nd and 4th <td> tags
                        data = [name, address, phone, email, url]
                        with open("am_data.csv", mode="a", newline="") as csv_file:
                            writer = csv.writer(csv_file, delimiter = '*')
                            writer.writerow(data)
                        return None
                        
                    else:
                        print(id)
                        print(f"HTTP request failed with status code {response.status_code}")
                except Exception as e:
                    print(id)
                    print(e)
                    data = [name, address, phone, email, url]
                    with open("am_data.csv", mode="a", newline="") as csv_file:
                        writer = csv.writer(csv_file, delimiter = '*')
                        writer.writerow(data)
                    return None


        except:
            if retry < max_retries - 1:
                await asyncio.sleep(1)  # Wait for 1 second before retrying
            else:
                print(f"Failed to connect after {max_retries} retries.")
                return None


        

    

async def main():
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for item in json_data:
                tasks.append(fetch_element_data(session, item))

            await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
