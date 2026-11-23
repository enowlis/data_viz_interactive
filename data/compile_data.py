import pathlib
import pandas as pd

DATA_FILEPATH = "/home/elies/data_viz_interactive/data"
OUTPUT_FILEPATH = "/home/elies/data_viz_interactive/web/data"

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

def rename_countries(data):
    data["reporter_area_label"] = data["reporter_area_label"].replace(
        {"Antigua and Barbuda" : "Antigua and Barb.",
            "Bolivia (Plurinational State of)" : "Bolivia",
            "Bosnia and Herzegovina" : "Bosnia and Herz.",
            "British Virgin Islands" : "British Virgin Is.",
            "Brunei Darussalam" : "Brunei",
            "Cayman Islands" : "Cayman Is.",
            "Central African Republic" : "Central African Rep.",
            "Cook Islands" : "Cook Is.",
            "CÃ´te dâ€™Ivoire" : "Côte d'Ivoire",
            "CuraÃ§ao" : "Curaçao",
            "Democratic Republic of the Congo" : "Dem. Rep. Congo",
            "Dominican Republic" : "Dominican Rep.",
            "Equatorial Guinea" : "Eq. Guinea",
            "French Polynesia" : "Fr. Polynesia",
            "China, Hong Kong Special Administrative Region" : "Hong Kong",
            "Iran (Islamic Republic of)" : "Iran",
            "Lao People's Democratic Republic" : "Laos",
            "China, Macao Special Administrative Region" : "Macao",
            "North Macedonia" : "Macedonia",
            "Marshall Islands" : "Marshall Is.",
            "Micronesia (Federated States of)" : "Micronesia",
            "Republic of Moldova" : "Moldova",
            "Netherlands (Kingdom of the)" : "Netherlands",
            "Northern Mariana Islands" : "N. Mariana Is.",
            "State of Palestine" : "Palestine",
            "Russian Federation" : "Russia",
            "South Sudan" : "S. Sudan",
            "Sao Tome and Principe" : "São Tomé and Principe",
            "Sint Maarten (Dutch part)" : "Sint Maarten",
            "Solomon Islands" : "Solomon Is.",
            "Republic of Korea" : "South Korea",
            "Saint Kitts and Nevis" : "St. Kitts and Nevis",
            "Saint Vincent and the Grenadines" : "St. Vin. and Gren.",
            "Syrian Arab Republic" : "Syria",
            "Taiwan Province of China" : "Taiwan",
            "United Republic of Tanzania" : "Tanzania",
            "TÃ¼rkiye" : "Turkey",
            "Turks and Caicos Islands" : "Turks and Caicos Is.",
            "United States Virgin Islands" : "U.S. Virgin Is.",
            "United Kingdom of Great Britain and Northern Ireland" : "United Kingdom",
            "Venezuela (Bolivarian Republic of)" : "Venezuela",
            "Viet Nam" : "Vietnam",
            "Wallis and Futuna Islands" : "Wallis and Futuna Is."
        }
    )

    return data

if __name__ == "__main__":
    compiled_data = add_regions_and_geometry(read_in_data())
    compiled_data = rename_countries(compiled_data)
    compiled_data.to_json(f"{OUTPUT_FILEPATH}/compiled_tourism_data.json",
                          orient="records")
