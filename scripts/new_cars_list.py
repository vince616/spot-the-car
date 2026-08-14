# Final list of new car photos to add, after user decisions:
# - Keep all 3 Mini-family classics
# - Keep all RAV4 generations, but drop the exact duplicate GR Sport photo (keep IMG_9891)
# - Keep Twingo III / Renault 4L as distinct variants (distinguishing name TBD by user in the calibration tool)
# - Skip both interior shots (Multipla console centrale, Twingo Initiale interior)
#
# "name_guess" is a rough starting point only -- the user finalizes the exact
# name (and generation/trim wording) themselves in the calibration tool.

NEW_CARS = [
    {"wikiFile": "2025_Opel_Mokka-e_Auto_Zuerich_2024_DSC_6710.jpg", "name_guess": "Opel Mokka-e"},
    {"wikiFile": "Opel_Grandland_1X7A7184.jpg", "name_guess": "Opel Grandland"},
    {"wikiFile": "Opel_Grandland_X_Monrepos_2018_IMG_0066.jpg", "name_guess": "Opel Grandland X"},
    {"wikiFile": "Renault_Kangoo_Red.jpg", "name_guess": "Renault Kangoo"},
    {"wikiFile": "Renault_Kangoo_III_1X7A1519.jpg", "name_guess": "Renault Kangoo III"},
    {"wikiFile": "Nissan_Leaf_-_Mondial_de_l%27Automobile_de_Paris_2012_-_006.jpg", "name_guess": "Nissan Leaf"},
    {"wikiFile": "2019_Nissan_Leaf_rear.jpg", "name_guess": "Nissan Leaf (2019)"},
    {"wikiFile": "Jaguar_F-Pace_Shishi_02_2022-06-08.jpg", "name_guess": "Jaguar F-Pace"},
    {"wikiFile": "Jaguar_F-Pace_IMG_8000.jpg", "name_guess": "Jaguar F-Pace (2)"},
    {"wikiFile": "Aston_Martin_DB7_Vantage_IMG_7854.jpg", "name_guess": "Aston Martin DB7 Vantage"},
    {"wikiFile": "Aston_Martin_DB12_1X7A1934.jpg", "name_guess": "Aston Martin DB12"},
    {"wikiFile": "Range_Rover_Sport_SVR,_IAA_2017,_Frankfurt_(1Y7A3071).jpg", "name_guess": "Range Rover Sport SVR"},
    {"wikiFile": "Range_Rover_1X7A8034.jpg", "name_guess": "Range Rover"},
    {"wikiFile": "Morris_Mini-Minor_1959_(621_AOK).jpg", "name_guess": "Morris Mini-Minor (1959)"},
    {"wikiFile": "2021_Mini_Hatch_(F56)_John_Cooper_Works_1X7A0150.jpg", "name_guess": "Mini John Cooper Works"},
    {"wikiFile": "Mini_Cooper_(1._Generation).JPG", "name_guess": "Mini Cooper (1ere generation)"},
    {"wikiFile": "Cupra_Formentor_Facelift_IMG_0665.jpg", "name_guess": "Cupra Formentor (restylee)"},
    {"wikiFile": "Cupra_Formentor_IMG_9668.jpg", "name_guess": "Cupra Formentor"},
    {"wikiFile": "Renault_Twingo_3.jpg", "name_guess": "Renault Twingo III (2)"},
    {"wikiFile": "Renault_4L_Mk2.jpg", "name_guess": "Renault 4L (Mk2)"},
    {"wikiFile": "Audi_100_5311527.jpg", "name_guess": "Audi 100"},
    {"wikiFile": "BYD_Dolphin_(Global_version)_IMG_9507.jpg", "name_guess": "BYD Dolphin"},
    {"wikiFile": "2018_Kia_Sportage_(QL_II_MY19)_Si_2WD_wagon_(2018-11-26)_02.jpg", "name_guess": "Kia Sportage"},
    {"wikiFile": "Renault_M%C3%A9gane_E-Tech_IMG_8435_(cropped).jpg", "name_guess": "Renault Megane E-Tech"},
    {"wikiFile": "Renault_Espace_Initiale,_GIMS_2019,_Le_Grand-Saconnex_(GIMS1310).jpg", "name_guess": "Renault Espace V"},
    {"wikiFile": "Renault_Espace_VI_IMG_9423.jpg", "name_guess": "Renault Espace VI"},
    {"wikiFile": "Renault_Espace_III_en_Valencia.jpg", "name_guess": "Renault Espace III"},
    {"wikiFile": "Volkswagen_Beetle_9.jpg", "name_guess": "Volkswagen Beetle"},
    {"wikiFile": "Volkswagen_Golf_R_(2).jpg", "name_guess": "Volkswagen Golf R"},
    {"wikiFile": "2018_Volkswagen_Tiguan_SE_Nav_TDI_-_1968cc_2.0_(150PS)_Diesel_-_Indium_Grey_-_03-2024,_Front.jpg", "name_guess": "Volkswagen Tiguan"},
    {"wikiFile": "Ford_Kuga_PHEV_1X7A6291_(cropped).jpg", "name_guess": "Ford Kuga"},
    {"wikiFile": "Toyota_RAV4_(XA10)_IMG_1260.jpg", "name_guess": "Toyota RAV4 (1994)"},
    {"wikiFile": "Toyota_RAV4_Plug-in_Hybrid_GR_Sport_IMG_9891.jpg", "name_guess": "Toyota RAV4 GR Sport"},
    {"wikiFile": "Toyota_RAV4_XA40_Shishi_02_2022-05-25.jpg", "name_guess": "Toyota RAV4 (2013)"},
    {"wikiFile": "Toyota_RAV4_Hybrid,_GIMS_2019,_Le_Grand-Saconnex_(GIMS0518).jpg", "name_guess": "Toyota RAV4 Hybrid (2019)"},
    {"wikiFile": "Fiat_Multipla_front_20080825.jpg", "name_guess": "Fiat Multipla"},
    {"wikiFile": "Orange_Lamborghini_Gallardo_LP560_fl.JPG", "name_guess": "Lamborghini Gallardo"},
    {"wikiFile": "Lamborghini_Urus_rear_view_dllu.jpg", "name_guess": "Lamborghini Urus"},
    {"wikiFile": "Bentley_Continental_GT_(II)_%E2%80%93_Frontansicht_(3),_30._August_2011,_D%C3%BCsseldorf.jpg", "name_guess": "Bentley Continental GT"},
    {"wikiFile": "Rolls-Royce_Silver_Cloud_III,_Bj._1964_(ret).jpg", "name_guess": "Rolls-Royce Silver Cloud III"},
]

print(len(NEW_CARS), "new cars queued")
