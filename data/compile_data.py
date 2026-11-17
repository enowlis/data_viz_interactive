import pathlib
import pandas as pd

DATA_FILEPATH = "/home/elies/data_viz_interactive/data"

def read_in_data():
    tourism_folder = pathlib.Path(f"{DATA_FILEPATH}/UN_tourism_data")
    file_paths = list(tourism_folder.glob("**/*.xlsx"))

    data_list = []

    for i, path in enumerate(file_paths):
        data_i = pd.read_excel(path, sheet_name="Data")
        data_list.append(data_i)

    return pd.concat(data_list, sort=False)

def add_regions_and_geometry(data):
    # Add regions to the data
    # Source: Composition of UN Tourism regions
    regions = pd.read_excel(f"{DATA_FILEPATH}/UN_Tourism_regions_composition.xlsx", header=4)
    regions = regions[["UNWTO_region_label_English", "area_label_M49_EN", "area_code_M49"]]
    regions = regions.rename(columns={"UNWTO_region_label_English" : "region",
                                    "area_label_M49_EN" : "reporter_area_label"}
                            )

    # Add in the latitude and longitude for these countries
    # Source: GitHub Gists
    geometry = pd.read_csv("https://gist.githubusercontent.com/metal3d/5b925077e66194551df949de64e910f6/raw/c5f20a037409d96958553e2eb6b8251265c6fd63/country-coord.csv")
    geometry = geometry.rename(columns={"Numeric code" : "area_code_M49"})
    geometry = geometry[["area_code_M49", "Latitude (average)", "Longitude (average)"]]
    to_add = pd.merge(regions, geometry, on = "area_code_M49", how = "left")

    return pd.merge(data, to_add, on = "reporter_area_label", how = "left")

if __name__ == "__main__":
    compiled_data = add_regions_and_geometry(read_in_data())
    compiled_data.to_csv(f"{DATA_FILEPATH}/compiled_tourism_data.csv")
    compiled_data.to_json(f"{DATA_FILEPATH}/compiled_tourism_data.json",
                          orient="records")
