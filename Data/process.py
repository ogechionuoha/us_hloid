import os
import pandas as pd
from geopy.geocoders import Nominatim
import requests
from warnings import filterwarnings
import logging

logger ='../logs/usimage_process.log'

filterwarnings("ignore")


def download_images(input_file, image_file, output_folder, hierarchy):
    """
    Takes input csv file of locccation details
    downloads images from image_file to output folder 
    according to hierarchy provided
    """

    assert os.path.exists(input_file), "Input file not found"
    assert os.path.exists(image_file), "Image file not found"

    location_data = pd.read_csv(input_file)
    image_data = pd.read_csv(image_file, names=['image_id', 'hotel_id', 'image_url', 'image_source', 'upload_timestamp'])

    assert set(hierarchy).intersection(set(location_data.columns)) == set(hierarchy), "missing one or more hierarchy keys in location data"

    hotel_info = {row['hotel_id']: [row[key] for key in hierarchy] for ind, row in location_data.iterrows()}

    print(list(hotel_info.keys())[0] , hotel_info[list(hotel_info.keys())[0]])

    for ind, img_row in image_data.iterrows():

        info = hotel_info.get(img_row['hotel_id'], None)
        if info is None: continue
        img_id = img_row['image_id']
        image_url = img_row['image_url']

        out_path = os.path.join(output_folder, *info)

        if ind%200 == 0:
            print("Process continues...")

        if not os.path.exists(os.path.join(out_path,str(img_id)+".jpg")):
            os.makedirs(out_path, exist_ok=True)
            try:
                img_data = requests.get(image_url, verify = False).content
                with open(os.path.join(out_path,str(img_id)+".jpg"), 'wb') as handler:
                    handler.write(img_data)
            except Exception as e:
                log("DOWNLOAD ERROR", str(img_id), image_url, *info)

    print("Images downloaded")


def get_country(country_codes, input_file, output_file, keys=None):
    """Takes a list of country codes and returns a csv file with the data corresponding to those countries"""

    assert os.path.exists(input_file), "Input file not Found"

    location_data = pd.read_csv(input_file)

    # calling the nominatim tool
    geoLocator = Nominatim(user_agent="USLoc")

    new_data = pd.DataFrame(columns = ['hotel_id', 'hotel_name', 'chain_id', 'latitude', 'longitude',\
        'country', 'postcode', 'state', 'county', 'road', 'house_number'])

    for ind, row in location_data.iterrows():
        try:
            
            # passing the coordinates
            location = geoLocator.reverse(f"{row['latitude']},{row['longitude']}")

            location_info = location.raw['address']

            if location_info['country_code'] in country_codes:
                # write entry to file
                location_info.update(row.to_dict())
                rem_list = [key for key in location_info.keys() if key not in new_data.columns]
                [location_info.pop(key) for key in rem_list]
                new_data = pd.concat([new_data, pd.DataFrame([location_info])], ignore_index=True) #new_data.append(location.raw['address'], ignore_index=True)

        except Exception as e:
            print(e)

        if ind%200 == 0:
            print("Process continues...")

    new_data.to_csv(output_file, index=False)

    print('Process complete!')

def log(*msgs):
    with open(logger, "a") as logfile:
        logfile.write(",".join(msgs))
        logfile.write("\n")


if __name__ == "__main__":
    #get_country(["us"], r"/Users/ogechoonuoha/Documents/Work/US_states_classifier/Data/dataset/hotel_info.csv", "./US_dataset/location_info.csv")
    download_images('/Users/ogechoonuoha/Documents/Work/US_states_classifier/Data/US_dataset/location_info.csv', '/Users/ogechoonuoha/Documents/Work/US_states_classifier/Data/dataset/train_set.csv', './usimages', ['state', 'county'])




