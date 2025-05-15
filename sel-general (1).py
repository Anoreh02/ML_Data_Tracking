from seleniumwire import webdriver # <-- Import from seleniumwire
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time
import random
import csv
from datetime import datetime
import os
import json 

# Configuration
OUTPUT_FOLDER = "behavior_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
TIMESTAMP_NOW = datetime.now().strftime('%Y%m%d_%H%M%S')
BEHAVIOR_LOG_FILE = os.path.join(OUTPUT_FOLDER, f"behavior_log_{TIMESTAMP_NOW}.csv")
NETWORK_LOG_FILE = os.path.join(OUTPUT_FOLDER, f"network_log_{TIMESTAMP_NOW}.csv") 

service = Service('C:/Users/anore/Downloads/chromedriver-win64/chromedriver.exe') 
driver = webdriver.Chrome(service=service) # Basic selenium-wire initialization
action = ActionChains(driver)

# Recipe websites to visit
RECIPE_SITES = [
    "https://www.allrecipes.com/gallery/camping-recipes-with-few-ingredients/",
    "https://www.allrecipes.com/article/easy-weekend-camping-menu/",
    "https://www.allrecipes.com/recipe/245713/bacon-and-egg-tacos/",
    "https://www.allrecipes.com/gallery/big-batch-camping-recipes/",
    "https://www.allrecipes.com/recipe/216742/dutch-oven-mountain-man-breakfast/",
    "https://www.allrecipes.com/recipe/51051/cowboy-casserole/",
    "https://www.allrecipes.com/recipe/257054/big-rays-kielbasa-cabbage-skillet-for-a-crowd/",
    "https://www.allrecipes.com/recipe/231130/moms-campfire-stew/",
    "https://www.allrecipes.com/recipe/106888/toasty-campfire-cookies/",
    "https://www.allrecipes.com/recipe/106933/sugared-campfire-donuts/",
    "https://www.allrecipes.com/recipe/257055/bacon-apples/",
    "https://www.allrecipes.com/recipe/205632/quick-camping-pineapple-cakes/",
    "https://www.allrecipes.com/recipe/20038/campfire-banana-splits/",
    "https://www.allrecipes.com/recipe/232173/campfire-smores-in-a-cone/",
    "https://www.allrecipes.com/recipe/258911/grilled-smores-pizza/",
    "https://www.allrecipes.com/recipe/143267/a-peanutty-smore/",
    "https://www.allrecipes.com/recipe/258911/grilled-smores-pizza/",
    "https://www.allrecipes.com/recipe/215151/grilled-fruit-kabobs/",
    "https://www.allrecipes.com/recipe/27184/apples-by-the-fire/",
    "https://www.allrecipes.com/gallery/grilled-mexican-food/",
    "https://www.allrecipes.com/recipe/47844/grilled-mexican-steak/",
    "https://www.allrecipes.com/recipe/233399/mexican-grilled-corn/",
    "https://www.allrecipes.com/recipe/231174/easy-chicken-fajita-marinade/",
    "https://www.allrecipes.com/recipe/60111/margarita-grilled-shrimp/",
    "https://www.allrecipes.com/recipe/254279/chef-johns-yucatan-style-grilled-pork/",
    "https://www.allrecipes.com/recipe/221935/fish-tacos-ultimo/",
    "https://www.allrecipes.com/recipe/234270/grilled-pork-tacos-al-pastor/",
    "https://www.allrecipes.com/recipe/186691/lisas-favorite-carne-asada-marinade/",
    "https://www.allrecipes.com/recipe/214827/mexican-steak-torta/",
    "https://www.allrecipes.com/recipe/254449/grilled-grapefruit-paloma-cocktail/",
    "https://www.allrecipes.com/gallery/best-tex-mex-recipes/",
    "https://www.allrecipes.com/recipe/217843/kris-amazing-shredded-mexican-beef/",
    "https://www.allrecipes.com/recipe/258223/tex-mex-ultimate-carnitas-grilled-cheese/",
    "https://www.allrecipes.com/recipe/237508/south-texas-borracho-beans/",
    "https://www.allrecipes.com/recipe/70343/slow-cooker-chicken-taco-soup/",
    "https://www.allrecipes.com/recipe/8694/chicken-enchiladas-ii/",
    "https://www.allrecipes.com/recipe/14270/spicy-tex-mex-salad/",
    "https://www.allrecipes.com/recipe/26589/beef-enchiladas-ii/",
    "https://www.allrecipes.com/recipe/231447/spicy-beef-fajitas/",
    "https://www.allrecipes.com/recipe/41638/avocado-tacos/",
    "https://www.allrecipes.com/recipe/219931/quick-enchilada-sauce/",
    "https://www.allrecipes.com/gallery/mexican-flan-recipes/",
    "https://www.allrecipes.com/recipe/214091/flan-mexicano-mexican-flan/",
    "https://www.allrecipes.com/recipe/260650/original-mexican-flan-napolitano/",
    "https://www.allrecipes.com/recipe/254217/impossible-cake/",
    "https://www.allrecipes.com/recipe/20524/flan-ii/",
    "https://www.allrecipes.com/recipe/219066/coconut-cheese-flan-flan-de-coco-y-queso/",
    "https://www.allrecipes.com/recipe/246830/flan-de-queso-cream-cheese-flan/",
    "https://www.allrecipes.com/recipe/44497/baked-flan/",
    "https://www.allrecipes.com/gallery/agua-fresca-recipes/",
    "https://www.allrecipes.com/recipe/230153/agua-fresca/",
    "https://www.allrecipes.com/recipe/246118/agua-fresca-de-pepino-cucumber-limeade/",
    "https://www.allrecipes.com/recipe/214366/agua-de-jamaica-hibiscus-water/",
    "https://www.allrecipes.com/recipe/246117/watermelon-lime-agua-fresca/",
    "https://www.allrecipes.com/recipe/246116/tamarind-agua-fresca/",
    "https://www.allrecipes.com/recipe/275544/agua-fresca-de-pina-y-espinacas-pineapple-spinach-agua-fresca/",
    "https://www.allrecipes.com/recipe/234681/chia-fresca/",
    "https://www.allrecipes.com/recipe/258234/spinach-strawberry-agua-fresca/",
    "https://www.allrecipes.com/gallery/easy-mexican-dishes/",
    "https://www.allrecipes.com/recipe/16700/salsa-chicken/",
    "https://www.allrecipes.com/recipe/257865/easy-chorizo-street-tacos/",
    "https://www.allrecipes.com/recipe/16560/5-ingredient-mexican-casserole/",
    "https://www.allrecipes.com/recipe/202784/easy-spicy-mexican-american-chicken/",
    "https://www.allrecipes.com/recipe/145271/suegras-tomatillo-chicken/",
    "https://www.allrecipes.com/gallery/fruity-margarita-recipes/",
    "https://www.allrecipes.com/recipe/24494/ultimate-frozen-strawberry-margarita/",
    "https://www.allrecipes.com/recipe/221229/jewels-watermelon-margaritas/",
    "https://www.allrecipes.com/recipe/170757/strawberry-basil-margarita/",
    "https://www.allrecipes.com/recipe/22738/banana-margaritas/",
    "https://www.allrecipes.com/recipe/174283/rhubarb-margarita/",
    "https://www.allrecipes.com/recipe/217011/laurens-grapefruit-margaritas/",
    "https://www.allrecipes.com/recipe/147225/kiwi-margarita/",
    "https://www.food.com/",
    "https://www.food.com/ideas/quick-easy-chicken-dinners-6013",
    "https://www.food.com/recipe/quick-and-easy-chicken-enchiladas-75758",
    "https://www.food.com/recipe/30-minute-chicken-and-dumplings-111257",
    "https://www.food.com/recipe/spinach-and-cheese-stuffed-chicken-breast-rsc-495271",
    "https://www.food.com/recipe/chicken-quesadillas-3978",
    "https://www.food.com/recipe/copycat-recipe-for-carrabbas-chicken-marsala-50979",
    "https://www.food.com/recipe/cheddar-bar-b-q-chicken-breasts-26339",
    "https://www.food.com/recipe/lemon-chicken-milanese-360913",
    "https://www.food.com/recipe/cheesy-chicken-parm-volcanos-534900",
    "https://www.food.com/recipe/chicken-breast-with-honey-balsamic-glaze-151829",
    "https://www.food.com/recipe/butter-chicken-88578",
    "https://www.food.com/recipe/one-dish-chicken-and-rice-bake-54393",
    "https://www.food.com/recipe/cajun-chicken-strips-241623",
    "https://www.food.com/recipe/fried-chicken-sandwich-with-hot-honey-535321",
    "https://www.food.com/recipe/chicken-lazone-65768",
    "https://www.food.com/recipe/korean-inspired-popcorn-chicken-535320",
    "https://www.food.com/ideas/favorite-french-toast-recipes-6097",
    "https://www.food.com/recipe/cream-cheese-stuffed-french-toast-w-strawberries-and-whip-cream-58497",
    "https://www.food.com/recipe/bagel-french-toast-casserole-362199",
    "https://www.food.com/recipe/stuffed-french-toast-535617",
    "https://www.food.com/recipe/easy-french-toast-435246",
    "https://www.food.com/recipe/honey-pecan-french-toast-210621",
    "https://www.food.com/recipe/french-toast-59791",
    "https://www.food.com/recipe/sheet-pan-strawberry-banana-bread-french-toast-bake-537798",
    "https://www.food.com/recipe/crisp-french-toast-366688",
    "https://www.food.com/recipe/peanut-butter-chocolate-stuffed-french-toast-with-jam-syrup-301848",
    "https://www.food.com/recipe/caramel-french-toast-284545",
    "https://www.food.com/recipe/french-toast-roll-ups-533191",
    "https://www.food.com/recipe/parmesan-french-toast-535666",
    "https://www.food.com/recipe/easy-banana-french-toast-199743",
    "https://www.food.com/recipe/lighter-french-toast-waffles-192425",
    "https://www.food.com/recipe/berry-stuffed-french-toast-with-vanilla-yogurt-sauce-244039",
    "https://www.food.com/ideas/main-dish-salads-6136",
    "https://www.food.com/recipe/asian-style-chicken-salad-264185",
    "https://www.food.com/recipe/warm-chicken-and-white-bean-salad-diabetic-189838",
    "https://www.food.com/recipe/citrusy-kale-salad-w-blueberries-and-pepitas-variations-462594",
    "https://www.food.com/recipe/couscous-chickpea-salad-54593",
    "https://www.food.com/recipe/cobb-salad-with-brown-derby-dressing-51555",
    "https://www.food.com/recipe/portabella-and-blue-cheese-salad-202693",
    "https://www.food.com/recipe/bok-choy-salad-184840",
    "https://www.food.com/recipe/chicken-salad-stolen-from-a-rylstone-cafe-47616",
    "https://www.food.com/recipe/cote-dazur-fruit-and-greens-salad-with-honey-lemon-dressing-383328",
    "https://www.food.com/ideas/comfort-food-6505",
    "https://www.food.com/ideas/comfort-food-6505/one-pot-recipes-6506",
    "https://www.food.com/ideas/comfort-food-6505/family-recipes-6507",
    "https://www.food.com/ideas/comfort-food-6505/slow-cooker-6508",
    "https://www.food.com/ideas/top-comfort-food-recipes-6929#c-791310",
    "https://www.food.com/ideas/how-to-make-pizza-babka-7098",
    "https://www.food.com/ideas/how-to-make-meatball-sub-kolaches-7151",
    "https://www.food.com/ideas/how-to-make-garlic-bread-7174",
    "https://www.food.com/ideas/amazing-bacon-recipes-6185#c-14409",
    "https://www.food.com/ideas/best-cheesy-recipes-6401#c-613125",
    "https://www.food.com/ideas/curry-recipes-7087#c-861843",
    "https://www.food.com/ideas/ooey-gooey-desserts-7089",
    "https://www.food.com/recipe/beignets-86144",
    "https://www.food.com/recipe/slow-cooker-shrimp-sausage-jambalaya-208039",
    "https://www.food.com/recipe/king-cake-90932",
    "https://www.food.com/ideas/ham-dinner-recipes-7180#c-981121",
    "https://www.food.com/ideas/international-food-6822",
    "https://www.food.com/ideas/french-food-at-home-7129",
    "https://www.food.com/ideas/mexican-food-at-home-6830",
    "https://www.food.com/recipe/pasta-alla-cacio-e-pepe-411364",
    "https://www.food.com/recipe/easy-stracciatella-italian-soup-275229",
    "https://www.food.com/recipe/alessis-tiramisu-72179",
    "https://www.food.com/ideas/chinese-food-at-home-6807",
    "https://www.food.com/ideas/how-to-make-kimchi-7165",
    "https://www.food.com/recipe/chapchae-noodles-with-beef-and-mixed-vegetables-321457",
    "https://www.food.com/ideas/breakfast-brunch-recipes-6514",
    "https://www.food.com/ideas/community-6816",
    "https://www.food.com/ideas/quick-and-easy-dinners-6510",
    "https://www.food.com/ideas/copycat-recipes-6576",
    "https://www.food.com/recipe/tender-pot-roast-22137",
    "https://www.food.com/recipe/chocolate-mousse-8995",
    "https://www.food.com/recipe/bacony-deviled-eggs-90941",
    "https://www.food.com/recipe/carrot-cake-19841",
    "https://www.food.com/ideas/mediterranean-diet-recipes-6794",
    "https://www.food.com/ideas/ultimate-nachos-recipes-6315",
    "https://www.food.com/ideas/essential-italian-pastas-6037",
    "https://www.epicurious.com/",
    "https://www.epicurious.com/recipes/food/views/calamari-salad",
    "https://www.epicurious.com/recipes/food/views/ba-syn-dill-pickle-potato-salad",
    "https://www.epicurious.com/recipes/food/views/ba-syn-crispy-rice-salad-spicy-tahini-dressing",
    "https://www.epicurious.com/recipes/food/views/ba-syn-coffee-cake-scones",
    "https://www.epicurious.com/expert-advice/types-of-onions-gallery",
    "https://www.epicurious.com/recipes-menus/most-saved-recipes-may-2025",
    "https://www.epicurious.com/recipes-menus/picnic-food-ideas-recipe-gallery",
    "https://www.epicurious.com/expert-advice/salt-sugar-msg-eggs",
    "https://www.epicurious.com/ingredients/differences-mineral-water-tonic-club-soda-seltzer-article",
    "https://www.epicurious.com/recipes/food/views/dry-rubbed-grilled-pork-chops",
    "https://www.epicurious.com/recipes/food/views/ba-syn-green-falafel-smash-burgers",
    "https://www.epicurious.com/recipes/food/views/ba-syn-surprisingly-satisfying-cauliflower-chowder",
    "https://www.epicurious.com/recipes/food/views/ba-syn-scallion-speckled-rice",
    "https://www.epicurious.com/recipes/food/views/ba-syn-popover-topped-pot-pie",
    "https://www.epicurious.com/recipes/food/views/ba-syn-scallops-with-creamy-spinach-sauce",
    "https://www.epicurious.com/recipes/food/views/ba-syn-oyakodon",
    "https://www.epicurious.com/recipes/food/views/ba-syn-cashew-chicken-asparagus",
    "https://www.epicurious.com/recipes/food/views/pasta-primavera",
    "https://www.epicurious.com/recipes/food/views/ba-syn-saucy-spiced-shrimp-white-beans",
    "https://www.epicurious.com/recipes/food/views/chorizo-cauliflower",
    "https://www.epicurious.com/recipes/food/views/angel-hair-bibimguksu",
    "https://www.epicurious.com/recipes/food/views/leeks-with-sumac-parm-and-pine-nuts",
    "https://www.epicurious.com/recipes/food/views/hawaij-sweet-potatoes-lemon-relish-yogurt",
    "https://www.epicurious.com/recipes/food/views/mushroom-tofu-sisig",
    "https://www.epicurious.com/recipes/food/views/hong-kong-egg-scramble",
    "https://www.epicurious.com/recipes/food/views/charred-cabbage-with-shrimp-paste-butter",
    "https://www.epicurious.com/recipes/food/views/okonomiyaki-tater-tots",
    "https://www.epicurious.com/recipes/food/views/borani-banjan-afghan-style-fried-eggplant-yogurt",
    "https://www.epicurious.com/expert-advice/best-nonstick-pan-to-buy-reviews-article",
    "https://www.epicurious.com/expert-advice/best-electric-kettles-for-tea-article",
    "https://www.epicurious.com/expert-advice/best-mandoline-slicer-article",
    "https://www.epicurious.com/recipes/food/views/spring-risotto",
    "https://www.epicurious.com/recipes-menus/spring-cocktails",
    "https://www.epicurious.com/ingredient/pea",
    "https://www.epicurious.com/ingredient/rhubarb",
    "https://www.epicurious.com/recipes-menus/most-saved-recipes-this-week-april-2025",
    "https://www.epicurious.com/recipes/food/views/homemade-corn-dogs",
    "https://www.epicurious.com/simple-cooking/weeknight-meals",
    "https://www.epicurious.com/recipes-menus/most-saved-recipes-this-week-march-2025",
    "https://www.epicurious.com/gallery/spring-pasta-recipes-dinners-ideas",
    "https://www.epicurious.com/recipes-menus/most-saved-recipes-february-2025",
    "https://www.epicurious.com/recipes-menus/air-fryer-recipes-dinner-ideas",
    "https://www.epicurious.com/recipes-menus/most-saved-recipes-january-2025",
    "https://www.epicurious.com/recipes/food/views/smoked-mackerel-udon",
    "https://www.epicurious.com/recipes/food/views/spicy-honey-orange-shrimp",
    "https://www.epicurious.com/recipes/food/views/shrimp-scampi-pasta",
    "https://www.epicurious.com/recipes/food/views/kung-pao-chicken",
    "https://www.epicurious.com/ingredients/ground-chicken-recipes-gallery",
    "https://www.epicurious.com/recipes-menus/most-saved-recipes-this-week-december-2024",
    "https://www.epicurious.com/recipes/food/views/fettuccine-alfredo",
    "https://www.epicurious.com/recipes-menus/most-popular-recipes-gallery",
    "https://www.epicurious.com/recipes/food/views/philly-fluff-cake",
    "https://www.epicurious.com/recipes/food/views/3-ingredient-peanut-butter-cookies",
    "https://www.epicurious.com/recipes/food/views/salmon-patties-dill-sauce",
    "https://www.epicurious.com/recipes/food/views/spiced-moroccan-vegetable-soup-with-chickpeas-cilantro-and-lemon-harira",
    "https://www.epicurious.com/recipes/food/views/honey-glazed-roasted-carrots-and-parsnips-233404",
    "https://www.epicurious.com/recipes/food/views/roast-pork-loin-and-potatoes-103438",
    "https://www.epicurious.com/recipes/food/views/caramelized-onion-pasta",
    "https://www.epicurious.com/recipes/food/views/homemade-ginger-ale",
    "https://www.epicurious.com/recipes/food/views/simple-one-skillet-chicken-alfredo-pasta",
    "https://www.epicurious.com/recipes/food/views/oven-risotto-with-crispy-roasted-mushrooms",
    "https://www.epicurious.com/recipes/food/views/vegetarian-skillet-stuffed-shells",
    "https://www.epicurious.com/recipes/food/views/cioppino-seafood-stew-with-gremolata-toasts-51248830",
    "https://www.epicurious.com/recipes/food/views/rack-of-lamb-with-garlic-and-herbs-1222178",
    "https://www.epicurious.com/recipes/food/views/easy-lemon-curd",
    "https://www.epicurious.com/recipes/food/views/nanaimo-bars",
    "https://www.epicurious.com/recipes/food/views/low-country-boil-with-shrimp-corn-and-sausage",
    "https://www.epicurious.com/recipes/food/views/garlic-mayonnaise-13734",
    "https://www.epicurious.com/recipes/food/views/quinoa-tabbouleh-395939",
    "https://www.epicurious.com/recipes/food/views/easy-egg-custard-239229",
    "https://www.epicurious.com/recipes/food/views/duck-a-lorange-233535",
    "https://www.epicurious.com/recipes/food/views/basic-method-for-cooking-corn-on-the-cob-40047",
    "https://www.epicurious.com/recipes/food/views/how-to-temper-chocolate-356869",
    "https://www.epicurious.com/recipes/food/views/simple-candied-orange-peel-350798",
    "https://www.epicurious.com/recipes/food/views/crisp-roast-duck-235744",
    "https://www.epicurious.com/recipes/food/views/old-fashioned-raspberry-jam-230700",
    "https://www.epicurious.com/recipes/food/views/ras-el-hanout-101070",
    "https://www.epicurious.com/recipes-menus/30-minute-meals-gallery",
    "https://www.epicurious.com/recipes/food/views/easy-yogurt-and-spice-roasted-salmon-sabrina-ghayour",
    "https://www.epicurious.com/recipes/food/views/simple-one-skillet-chicken-alfredo-pasta",
    "https://www.epicurious.com/recipes/food/views/vegetarian-three-bean-chili",
    "https://www.epicurious.com/recipes/food/views/10-minute-sausage-skillet-with-cherry-tomatoes-and-broccolini",
    "https://www.epicurious.com/recipes/food/views/steamed-winter-veggie-bowls",
    "https://www.epicurious.com/recipes/food/views/sweet-and-saucy-pork-chops",
    "https://www.epicurious.com/recipes/food/views/dahi-dal-yogurt-lentil-spinach-chetna-makan",
    "https://www.epicurious.com/recipes/food/views/baked-mustard-crusted-salmon-with-asparagus-and-tarragon-56389444",
    "https://www.epicurious.com/recipes/food/views/quick-baked-chicken-parmesan",
    "https://www.epicurious.com/recipes/food/views/one-pot-pasta-primavera-with-shrimp",
    "https://www.epicurious.com/recipes/food/views/savory-dutch-baby-for-two",
    "https://www.epicurious.com/recipes/food/views/instant-pot-japchae",
    "https://www.epicurious.com/recipes/food/views/clams-with-sherry-and-olives-rebekah-peppler-a-table",
    "https://www.epicurious.com/recipes/food/views/salmon-patties-dill-sauce",
    "https://www.epicurious.com/recipes/food/views/jammy-eggs-and-feta-flatbreads-with-herbs",
    "https://www.epicurious.com/recipes/food/views/10-minute-shrimp-with-green-beans-and-creamy-lemon-dill-dip",
    "https://www.epicurious.com/recipes/food/views/butter-beans-paprika-and-piquillo-peppers",
    "https://www.epicurious.com/recipes/food/views/peppery-creamy-greens-with-eggs-brunch",
    "https://www.epicurious.com/recipes/food/views/fried-garlic-noodles-sheldon-simeon",
    "https://www.epicurious.com/recipes-menus/5-ingredient-meals-gallery",
    "https://www.epicurious.com/recipes/food/views/my-mothers-butter-tomato-and-onion-sauce-395730",
    "https://www.epicurious.com/recipes/food/views/my-favorite-simple-roast-chicken-231348",
    "https://www.epicurious.com/recipes/food/views/slow-baked-salmon-with-lemon-and-thyme-365151",
    "https://www.epicurious.com/recipes/food/views/twice-baked-potatoes",
    "https://www.epicurious.com/recipes/food/views/3-ingredient-garlic-herb-grilled-chicken-wings",
    "https://www.epicurious.com/recipes/food/views/garlic-fried-rice-sinangag",
    "https://www.epicurious.com/recipes/food/views/simplest-kale-salad",
    "https://www.epicurious.com/recipes/food/views/3-ingredient-pesto-fried-chicken",
    "https://www.epicurious.com/recipes/food/views/hoppin-john",
    "https://www.epicurious.com/recipes/food/views/creamy-polenta",
    "https://www.epicurious.com/recipes/food/views/3-ingredient-tomato-soup",
    "https://www.epicurious.com/recipes/food/views/air-fryer-turkey-cutlets",
    "https://www.epicurious.com/recipes/food/views/big-batch-roasted-kale",
    "https://www.epicurious.com/recipes/food/views/big-batch-instant-pot-white-beans",
    "https://www.epicurious.com/recipes/food/views/matzo-brei-recipe",
    "https://www.epicurious.com/recipes/food/views/quick-potato-gnocchi-joy-of-cooking",
    "https://www.epicurious.com/recipes-menus/make-ahead-weeknight-dinners-stew-soup-freezer-casserole-quick-easy-recipes-gallery",
    "https://www.epicurious.com/recipes/food/views/make-ahead-sheet-pan-meatballs",
    "https://www.epicurious.com/recipes/food/views/sunday-stash-braised-beef",
    "https://www.epicurious.com/recipes/food/views/quick-chicken-tikka-masala-56389806",
    "https://www.epicurious.com/recipes/food/views/hummus-dinner-bowls-with-spiced-ground-beef-and-tomatoes",
    "https://www.epicurious.com/recipes/food/views/curried-chickpea-and-lentil-dal",
    "https://www.epicurious.com/recipes/food/views/beef-chili",
    "https://www.epicurious.com/recipes/food/views/slow-cooker-chicken-congee",
    "https://www.epicurious.com/recipes/food/views/cold-beef-tenderloin-with-tomatoes-and-cucumbers",
    "https://www.epicurious.com/recipes/food/views/baked-sweet-potatoes",
    "https://www.epicurious.com/recipes/food/views/vegetarian-miso-tahini-squash-soup-with-brown-rice",
    "https://www.epicurious.com/recipes/food/views/herby-chicken-kofta-meatballs",
    "https://www.epicurious.com/recipes/food/views/slow-cooker-green-chicken-chili",
    "https://www.epicurious.com/recipes/food/views/make-ahead-baked-crispy-chicken-cutlets",
    "https://www.epicurious.com/recipes/food/views/spicy-black-bean-and-corn-tacos",
    "https://www.epicurious.com/recipes/food/views/sunday-stash-marinara-sauce",
    "https://www.epicurious.com/recipes/food/views/calzones-with-chorizo-and-kale",
    "https://www.epicurious.com/recipes/food/views/very-versatile-baked-beans-with-cabbage",
    "https://www.epicurious.com/recipes/food/views/easy-chicken-tortilla-soup-with-bean-and-cheese-nachos",
    "https://www.epicurious.com/recipes/food/views/one-pot-curried-cauliflower-with-couscous-and-chickpeas",
    "https://www.epicurious.com/recipes/food/views/beef-and-potato-pasties",
    "https://www.epicurious.com/recipes/food/views/stuffed-sweet-potatoes-with-curried-chickpeas-and-mushrooms",
    "https://www.epicurious.com/recipes-menus/our-favorite-one-pot-dinners-gallery",
    "https://www.epicurious.com/recipes/food/views/hot-honey-pork-chops-with-escarole-and-white-beans",
    "https://www.epicurious.com/recipes/food/views/cast-iron-pizza-with-fennel-and-sausage",
    "https://www.epicurious.com/recipes/food/views/chicken-stew-with-potatoes-and-radishes",
    "https://www.epicurious.com/recipes/food/views/salmon-and-bok-choy-green-coconut-curry",
    "https://www.epicurious.com/recipes/food/views/stir-fried-chicken-with-black-beans",
    "https://www.epicurious.com/recipes/food/views/curried-lentil-tomato-and-coconut-soup",
    "https://www.epicurious.com/recipes/food/views/coconut-apple-ginger-dal",
    "https://www.epicurious.com/recipes/food/views/squash-au-vin",
    "https://www.epicurious.com/recipes/food/views/roast-chicken-thighs-with-peas-and-mint",
    "https://www.epicurious.com/recipes/food/views/butternut-squash-steaks-with-brown-buttersage-sauce",
    "https://www.epicurious.com/recipes/food/views/za-atar-chicken-with-garlicky-yogurt",
    "https://www.epicurious.com/recipes-menus/best-breakfast-recipes-gallery",
    "https://www.epicurious.com/recipes/food/views/mashed-plantains-with-fried-eggs-mangu-de-platanos",
    "https://www.epicurious.com/recipes/food/views/power-butter",
    "https://www.epicurious.com/recipes/food/views/mushroom-and-kale-breakfast-skillet",
    "https://www.epicurious.com/recipes/food/views/coconut-date-power-breakfast-bars",
    "https://www.epicurious.com/recipes/food/views/brown-butter-steel-cut-oatmeal",
    "https://www.epicurious.com/recipes/food/views/breakfast-egg-sandwich-on-english-muffin-charred-red-onions-herbs-and-cheddar",
    "https://www.epicurious.com/recipes/food/views/overnight-porridge-congee-chao-andrea-nguyen-vietnamese-rice-soup",
    "https://www.epicurious.com/recipes/food/views/trout-toast-with-soft-scrambled-eggs",
    "https://www.epicurious.com/recipes/food/views/caramelized-plantain-parfait",
    "https://www.epicurious.com/recipes/food/views/butternut-squash-and-chorizo-hash",
    "https://www.epicurious.com/recipes/food/views/breakfast-nachos-julia-turshen",
    "https://www.epicurious.com/recipes/food/views/salad-for-breakfast",
    "https://www.epicurious.com/recipes-menus/vegetarian-lunch-ideas",
    "https://www.epicurious.com/recipes/food/views/classic-tomato-toast-with-mayonnaise-and-chives-56389808",
    "https://www.epicurious.com/recipes/food/views/vegetarian-muffulettas-with-pickled-iceberg",
    "https://www.epicurious.com/recipes/food/views/pasta-salad-recipe",
    "https://www.epicurious.com/recipes/food/views/butter-beans-paprika-and-piquillo-peppers",
    "https://www.epicurious.com/recipes/food/views/crunchy-quinoa-salad",
    "https://www.epicurious.com/recipes/food/views/grilled-ratatouille-pasta-salad",
    "https://www.epicurious.com/recipes/food/views/egg-salad-grilled-broccoli-and-chili-crisp",
    "https://www.epicurious.com/recipes/food/views/chickpea-salad-sandwich-with-creamy-carrot-radish-slaw",
    "https://www.epicurious.com/recipes/food/views/smoky-spanish-potatoes-and-eggs",
    "https://www.epicurious.com/recipes/food/views/basic-hummus-ottolenghi",
    "https://www.epicurious.com/recipes/food/views/insalata-caprese-13232",
    "https://www.epicurious.com/recipes/food/views/power-butter",
    "https://www.epicurious.com/expert-advice/sweet-potato-toppings-ideas-article",
    "https://www.epicurious.com/recipes/food/views/black-eyed-pea-salad-with-hot-sauce-vinaigrette",
    "https://www.epicurious.com/recipes-menus/71-easy-dessert-recipes-for-baking-beginners-and-tired-cooks-gallery",
    "https://www.epicurious.com/recipes-menus/easy-cocktails-recipes-drinks-gallery",
    "https://www.kitchenaid.com/recipes.html",
    "https://www.kitchenaid.com/pinch-of-help/stand-mixers/stand-mixer-recipes.html",
    "https://www.kitchenaid.com/content/dam/business-unit/kitchenaid/en-us/digital-assets/quickstart/ksmsfta/KSMSFTA_Recipes.pdf",
    "https://www.recipetineats.com/chicken-pot-pie/",
    "https://www.recipetineats.com/",
    "https://www.recipetineats.com/crispy-oven-baked-quesadillas/",
    "https://www.recipetineats.com/puttanesca-fish-tray-bake/",
    "https://www.recipetineats.com/b85-beef-sausage-rolls/",
    "https://www.recipetineats.com/melting-afghani-chickpea-curry/",
    "https://www.recipetineats.com/bake-with-brooki-penguin-plagiarism-allegations-statement/",
    "https://www.recipetineats.com/whipped-ricotta-one-pot-chicken-pasta/",
    "https://www.recipetineats.com/slow-roast-easter-stuffed-lamb/",
    "https://www.recipetineats.com/pikelets/",
    "https://www.recipetineats.com/beef-in-black-bean-sauce/",
    "https://www.recipetineats.com/lebanese-lemon-garlic-chicken-al-aseel-copycat/",
    "https://www.recipetineats.com/comeback-post/",
    "https://www.recipetineats.com/the-chocolate-chip-cookies-of-my-dreams/",
    "https://www.recipetineats.com/one-pot-chicken-risoni-with-crispy-salami/",
    "https://www.recipetineats.com/thai-coconut-pumpkin-soup/",
    "https://www.recipetineats.com/arayes-lebanese-meat-stuffed-pita/",
    "https://www.recipetineats.com/beef-chow-mein-noodles/",
    "https://www.recipetineats.com/chicken-marsala/",
    "https://www.recipetineats.com/chicken-rissoles-chicken-patties/",
    "https://www.recipetineats.com/moroccan-baked-eggplant-with-beef/",
    "https://www.recipetineats.com/category/quick-and-easy/",
    "https://www.recipetineats.com/category/no-cook-food/",
    "https://www.recipetineats.com/category/one-pot-recipes/",
    "https://www.recipetineats.com/category/fish-recipes/",
    "https://www.recipetineats.com/category/collections/quick-dinner-ideas-15-minute-meals/",
    "https://www.recipetineats.com/category/collections/asian-takeout/",
    "https://www.recipetineats.com/category/one-pot-recipes/",
    "https://www.recipetineats.com/category/stews/",
    "https://www.recipetineats.com/category/slow-cooker-recipes/",
    "https://www.recipetineats.com/category/pasta-recipes/",
    "https://www.recipetineats.com/one-pot-chili-mac-and-cheese/",
    "https://www.recipetineats.com/quick-broccoli-pasta/",
    "https://www.recipetineats.com/spaghetti-alla-puttanesca/",
    "https://www.recipetineats.com/spicy-chilli-prawn-pasta/",
    "https://www.recipetineats.com/carbonara/",
    "https://www.recipetineats.com/orecchiette-sausage-pasta-in-creamy-tomato-sauce/",
    "https://www.recipetineats.com/canned-tuna-pasta/",
    "https://www.recipetineats.com/creamy-mushroom-pasta/",
    "https://www.recipetineats.com/creamy-garlic-prawn-pasta/",
    "https://www.recipetineats.com/spicy-wontons-in-chilli-sauce-din-tai-fung/",
    "https://www.recipetineats.com/thai-green-curry/",
    "https://www.recipetineats.com/vindaloo/",
    "https://www.recipetineats.com/penne-all-arrabbiata-spicy-tomato-pasta/",
    "https://www.recipetineats.com/spicy-asian-cucumber-salad/",
    "https://www.recipetineats.com/asian-chilli-garlic-prawns-shrimp/",
    "https://www.recipetineats.com/thai-red-curry-pot-roast-chicken/",
    "https://www.recipetineats.com/spicy-firecracker-beef/",
    "https://www.recipetineats.com/laksa-soup/",
    "https://www.recipetineats.com/easy-spicy-korean-noodle-soup/",
    "https://www.recipetineats.com/baked-brie-with-maple-syrup-thyme/",
    "https://www.recipetineats.com/thai-stir-fried-noodles-pad-see-ew/",
    "https://www.recipetineats.com/how-to-cook-fish-with-crispy-skin/",
    "https://www.recipetineats.com/asian-chilli-chicken/",
    "https://www.recipetineats.com/thai-chicken-peanut-noodles-mince/",
    "https://www.recipetineats.com/asian-slaw/",
    "https://www.recipetineats.com/classic-pumpkin-soup/",
    "https://www.recipetineats.com/chicken-stir-fry-chop-suey/",
    "https://www.recipetineats.com/honey-garlic-chicken/",
    "https://www.recipetineats.com/chinese-broccoli-with-oyster-sauce/",
    "https://www.recipetineats.com/fennel-salad/",
    "https://www.recipetineats.com/puttanesca-fish-tray-bake/",
    "https://www.recipetineats.com/whipped-ricotta-one-pot-chicken-pasta/",
    "https://www.recipetineats.com/one-pot-cajun-beef-pasta/",
    "https://www.recipetineats.com/one-pot-moussaka-beef-rice-pilaf/",
    "https://www.recipetineats.com/tray-bake-dinner-lamb-kofta-meatballs/",
    "https://www.recipetineats.com/lemon-garlic-salmon-tray-bake-easy-healthy/",
    "https://www.recipetineats.com/one-pot-chicken-risoni-with-crispy-salami/",
    "https://www.recipetineats.com/one-pan-baked-butter-chicken/",
    "https://www.recipetineats.com/one-pot-creamy-tomato-beef-pasta/",
    "https://www.recipetineats.com/creamy-baked-fish-on-potato-gratin/",
    "https://www.recipetineats.com/thai-red-curry-pot-roast-chicken/",
    "https://www.recipetineats.com/cheesy-mexican-beef-bean-bake/",
    "https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/",
    "https://www.recipetineats.com/one-pot-mexican-chicken-rice/",
    "https://www.recipetineats.com/french-sausage-bean-casserole/",
    "https://www.recipetineats.com/one-pot-sausage-meatball-pasta/",
    "https://www.recipetineats.com/whipped-ricotta-one-pot-chicken-pasta/",
    "https://www.recipetineats.com/creamy-goat-cheese-roasted-red-pepper-risoni-orzo/",
    "https://www.seriouseats.com/lazy-daisy-cake-recipe-11734164",
    "https://www.seriouseats.com/material-non-toxic-silicone-spatula-amazon-11734426",
    "https://www.seriouseats.com/smashed-potatoes-tonnato-sauce-recipe-11733019",
    "https://www.seriouseats.com/",
    "https://www.seriouseats.com/carrot-harissa-rissotto-11731297",
    "https://www.seriouseats.com/exploration-of-ph-and-cooking-vegetables-11699945",
    "https://www.seriouseats.com/recipes-by-course-5117906",
    "https://www.seriouseats.com/grilled-smoked-brownie-recipe-7568650",
    "https://www.seriouseats.com/dirty-martini-dip-recipe-11732107",
    "https://www.seriouseats.com/beef-braciole-recipe-7561806",
    "https://www.seriouseats.com/causa-peruvian-cold-mashed-potato-casserole-with-tuna-or-chicken",
    "https://www.seriouseats.com/yogurt-marinated-chicken-thighs-pickled-nectarines",
    "https://www.seriouseats.com/omelette-souffle-with-cheese",
    "https://www.seriouseats.com/pasta-chi-vruoccoli-arriminati-sicilian-pasta-with-cauliflower",
    "https://www.seriouseats.com/the-easiest-fluffiest-pancake-recipe-from-a-pro-who-s-flipped-thousands-of-them-11729596",
    "https://www.seriouseats.com/mother-s-day-brunch-recipes-11702113",
    "https://www.seriouseats.com/chive-and-cheddar-drop-biscuits-recipe-11722605",
    "https://www.seriouseats.com/baked-bacon-and-cheese-egg-bites-recipe-11718150",
    "https://www.seriouseats.com/easter-brunch-recipes-11713762",
    "https://www.seriouseats.com/banana-nut-muffins-recipe-11712941",
    "https://www.seriouseats.com/asparagus-quiche-recipe-11711495",
    "https://www.seriouseats.com/matzo-pancake-recipe-11709817",
    "https://www.seriouseats.com/kale-and-mushroom-egg-bites-recipe-11703113",
    "https://www.seriouseats.com/almond-rolls-recipe-11701148",
    "https://www.seriouseats.com/banana-bread-pancakes-recipe-11691938",
    "https://www.seriouseats.com/bananas-foster-oatmeal-recipe-11689126",
    "https://www.seriouseats.com/maritozzi-recipe-11684437",
    "https://www.seriouseats.com/morning-glory-muffins-recipe-11683642",
    "https://www.seriouseats.com/churros-recipe-11680433",
    "https://www.seriouseats.com/hk-style-spam-and-egg-sandwich-recipe-11680136",
    "https://www.seriouseats.com/beignets-recipe-8788234",
    "https://www.seriouseats.com/microwave-granola-recipe-8778659",
    "https://www.seriouseats.com/kolaches-recipe-11715658",
    "https://www.seriouseats.com/savory-turmeric-oats-recipe-8772455",
    "https://www.seriouseats.com/smashed-potato-tart-recipe-11713997",
    "https://www.seriouseats.com/rice-cooker-oatmeal-8766231",
    "https://www.seriouseats.com/green-shakshuka-recipe-11710818",
    "https://www.seriouseats.com/yeasted-coffee-cake-recipe-8754688",
    "https://www.seriouseats.com/ployes-buckwheat-pancakes-recipe-11704538",
    "https://www.seriouseats.com/apple-pie-pancakes-recipe-8752129",
    "https://www.seriouseats.com/pohe-spiced-indian-flattened-rice-breakfast-recipe-11699365",
    "https://www.seriouseats.com/double-caramel-sticky-buns-recipe-8751530",
    "https://www.seriouseats.com/best-breakfast-recipes-8778579",
    "https://www.seriouseats.com/apple-pie-muffin-recipe-8749759",
    "https://www.seriouseats.com/goetta-recipe-11694309",
    "https://www.seriouseats.com/fan-tuan-recipe-8739042",
    "https://www.seriouseats.com/colombian-arepas-de-huevo-recipe-11692079",
    "https://www.seriouseats.com/bostock-recipe-11688115",
    "https://www.seriouseats.com/new-jersey-crumb-buns-recipe-8707010",
    "https://www.seriouseats.com/quick-and-easy-breakfast-recipes-8778563",
    "https://www.seriouseats.com/shoofly-pie-recipe-8701529",
    "https://www.seriouseats.com/valentines-day-breakfast-recipes-11679078",
    "https://www.seriouseats.com/instant-coffee-granola-recipe-8701349",
    "https://www.seriouseats.com/recipes-by-ingredient-recipes-5117749",
    "https://www.seriouseats.com/bacon-egg-and-cheese-breakfast-burrito",
    "https://www.seriouseats.com/creamy-bean-dip-roasted-tomato-salad-recipe-11729700",
    "https://www.seriouseats.com/cannellini-bean-recipes-8778572",
    "https://www.seriouseats.com/salmon-bean-salad-recipe-8682948",
    "https://www.seriouseats.com/breakfast-sopes-recipe-8639442",
    "https://www.seriouseats.com/jamaican-stew-peas-recipe-8411264",
    "https://www.seriouseats.com/lentil-recipes-7565962",
    "https://www.seriouseats.com/natto-japanese-fermented-soybeans-recipe-7376348",
    "https://www.seriouseats.com/recipes-by-ingredient-recipes-5117749",
    "https://www.seriouseats.com/mapo-beans",
    "https://www.seriouseats.com/pasta-with-beans-and-greens",
    "https://www.seriouseats.com/breakfast-burrito-with-scrambled-egg-chorizo-and-refried-beans",
    "https://www.seriouseats.com/tacu-tacu-peruvian-rice-and-beans-cake-recipe-7229046",
    "https://www.seriouseats.com/double-bean-mazemen-broth-less-ramen-with-savory-beans",
    "https://www.seriouseats.com/bean-salad-recipes-for-summer",
    "https://www.seriouseats.com/white-bean-tuna-salad",
    "https://www.seriouseats.com/bean-soup-recipes-7965768",
    "https://www.seriouseats.com/recipes-by-world-cuisine-5117277",
    "https://www.seriouseats.com/nigerian-beef-suya",
    "https://www.seriouseats.com/cuban-style-pollo-a-la-plancha-marinated-and-griddled-chicken",
    "https://www.seriouseats.com/spaghetti-with-canned-clam-sauce",
    "https://www.seriouseats.com/meatball-style-guide-varieties-around-the-world",
    "https://www.seriouseats.com/chicken-and-dried-fig-tagine-with-pistachios-and-chickpeas",
    "https://www.seriouseats.com/obe-ata-nigerian-red-pepper-sauce",
    "https://www.seriouseats.com/homemade-merguez-sausage-recipe",
    "https://www.seriouseats.com/somali-sambusas-fried-pockets-stuffed-with-spiced-beef-recipe",
    "https://www.seriouseats.com/eggplant-and-tomato-sauce-with-israeli-couscous-recipe",
    "https://www.seriouseats.com/bharazi-pigeon-peas-in-coconut-cream",
    "https://www.seriouseats.com/recipes-by-method-5117399",
    "https://www.seriouseats.com/recipes-to-make-with-new-gear-8768782",
    "https://www.seriouseats.com/galam-plee-nam-pla-thai-stir-fried-cabbage-with-fish-sauce-and-garlic",
    "https://www.seriouseats.com/panang-neua-thai-panang-curry-with-beef",
    "https://www.seriouseats.com/recipes-by-diet-5117779",
    "https://www.seriouseats.com/gluten-free-dairy-free-recipes-7371079",
    "https://www.seriouseats.com/vegan-cashew-milk-braised-green-plantains",
    "https://www.seriouseats.com/gluten-free-fried-chicken-japanese-ideas-in-food-recipe",
    "https://www.seriouseats.com/holiday-season-recipes-5117984",
    "https://www.seriouseats.com/the-best-roast-potatoes-ever-recipe",
    "https://www.seriouseats.com/pistachio-white-hot-chocolate-recipe-11678772",
    "https://www.seriouseats.com/bacon-wapped-shrimp-recipe-8766097",
    "https://www.seriouseats.com/techniques-5118032",
    "https://www.seriouseats.com/how-to-make-the-perfect-salad-11722529",
    "https://www.seriouseats.com/the-safest-and-fasted-way-to-dice-an-onion-11727531",
    "https://www.seriouseats.com/exploration-of-ph-and-cooking-vegetables-11699945",
    "https://www.seriouseats.com/tips-trouble-shooting-5118014",
    "https://www.seriouseats.com/grilling-guides-5118026",
    "https://www.seriouseats.com/hot-smoked-salmon-recipe-11718524",
    "https://www.seriouseats.com/the-serious-eats-guide-to-grilling",
    "https://www.seriouseats.com/grilling-how-hot-heat-fire-temperature",
    "https://www.seriouseats.com/stovetop-guides-5118016",
    "https://www.seriouseats.com/fluffy-rice-trick-11686236",
    "https://www.seriouseats.com/how-to-butter-baste-steaks-chops-fish",
    "https://www.seriouseats.com/just-add-water-how-to-make-a-pan-sauce-and-how-to-fix-a-broken-one",
    "https://www.seriouseats.com/baking-guides-5118031",
    "https://www.seriouseats.com/baking-with-skim-milk-11718956",
    "https://www.seriouseats.com/why-you-should-use-a-stand-mixer-8767163",
    "https://www.seriouseats.com/6-measuring-mistakes-that-derail-dessert-8766207",
    "https://www.seriouseats.com/entertaining-5118033",
    "https://www.seriouseats.com/essential-french-cheese-board-guide-8729696",
    "https://www.seriouseats.com/how-to-pair-beer-and-cheese-8704489",
    "https://www.seriouseats.com/best-mosquito-repellents-8652137",
    "https://www.seriouseats.com/african-cuisine-guides-5117176",
    "https://www.seriouseats.com/asian-cuisine-guides-5117164",
    "https://www.seriouseats.com/caribbean-cuisine-guides-5117113",
    "https://www.seriouseats.com/central-american-cuisine-guides-5117136",
    "https://www.seriouseats.com/european-cuisine-guides-5117108",
    "https://www.seriouseats.com/middle-eastern-cuisine-guides-5117157",
    "https://www.seriouseats.com/north-american-cuisine-guides-5117134",
    "https://www.seriouseats.com/oceanic-cuisine-guides-5117084",
    "https://www.seriouseats.com/south-american-cuisine-guides-5117118",
    "https://smittenkitchen.com/",
    "https://smittenkitchen.com/2025/05/challah-french-toast/",
    "https://smittenkitchen.com/2025/04/charred-salt-and-vinegar-cabbage/",
    "https://smittenkitchen.com/2025/04/simplest-brisket-with-braised-onions/",
    "https://smittenkitchen.com/2025/02/ziti-chickpeas-with-sausage-and-kale/",
    "https://smittenkitchen.com/2025/02/classic-lemon-curd-tart/",
    "https://smittenkitchen.com/2025/01/potato-leek-soup/",
    "https://smittenkitchen.com/2024/12/invisible-apple-cake/",
    "https://smittenkitchen.com/2024/12/chicken-meatball-and-noodle-soup/",
    "https://smittenkitchen.com/2024/11/halloumi-and-fall-vegetable-roast/",
    "https://smittenkitchen.com/2024/11/skillet-baked-macaroni-and-cheese/",
    "https://smittenkitchen.com/2025/04/charred-salt-and-vinegar-cabbage/",
    "https://smittenkitchen.com/2025/04/simplest-brisket-with-braised-onions/",
    "https://smittenkitchen.com/2024/06/blistered-peas-in-the-pod-with-lemon-and-salt/",
    "https://smittenkitchen.com/2024/04/steamed-artichokes/",
    "https://smittenkitchen.com/2023/04/hash-brown-patties/",
    "https://smittenkitchen.com/2023/01/cauliflower-salad-with-dates-and-pistachios/",
    "https://smittenkitchen.com/2022/08/grilled-nectarines-with-gorgonzola-and-hazelnuts/",
    "https://smittenkitchen.com/2022/07/buttered-noodles-for-frances/",
    "https://smittenkitchen.com/2022/07/roasted-tomatoes-with-white-beans/",
    "https://smittenkitchen.com/2022/04/snacky-asparagus/",
    "https://www.budgetbytes.com/",
    "https://www.budgetbytes.com/homemade-simple-syrup/",
    "https://www.budgetbytes.com/kung-pao-chicken/",
    "https://www.budgetbytes.com/sopa-de-fideo/",
    "https://www.budgetbytes.com/category/recipes/cost-per-recipe/recipes-under-10/",
    "https://www.budgetbytes.com/category/recipes/meat/chicken/",
    "https://www.budgetbytes.com/category/recipes/pasta/",
    "https://www.budgetbytes.com/category/recipes/one-pot/",
    "https://www.budgetbytes.com/category/recipes/vegetarian/",
    "https://www.budgetbytes.com/category/recipes/slow-cooker/",
    "https://www.budgetbytes.com/category/recipes/quick/",
    "https://www.budgetbytes.com/category/recipes/dessert/",
    "https://www.budgetbytes.com/chicken-alfredo/",
    "https://www.budgetbytes.com/creamy-garlic-chicken/",
    "https://www.budgetbytes.com/pasta-salad/",
    "https://www.budgetbytes.com/nicoise-salad/",
    "https://www.budgetbytes.com/cilantro-lime-rice/",
    "https://www.budgetbytes.com/pasta-primavera/",
    "https://www.budgetbytes.com/avocado-toast/",
    "https://www.budgetbytes.com/air-fryer-asparagus/",
    "https://panlasangpinoy.com/filipino-cuban-spanish-food-chicken-empanada-picadillo-recipe/",
    "https://panlasangpinoy.com/",
    "https://panlasangpinoy.com/how-to-make-home-made-siopao-asado-recipe/",
    "https://panlasangpinoy.com/brazo-de-mercedes-cake-recipe/",
    "https://panlasangpinoy.com/filipino-food-bread-of-salt-pandesal-recipe/",
    "https://panlasangpinoy.com/how-to-make-pasta-cheese-baked-macaroni-recipe/",
    "https://panlasangpinoy.com/embutido/",
    "https://panlasangpinoy.com/filipino-food-max-style-fried-chicken-recipe/",
    "https://panlasangpinoy.com/filipino-egg-pie-recipe/",
    "https://panlasangpinoy.com/how-to-make-kfc-style-gravy-recipe/",
    "https://panlasangpinoy.com/asian-vegetable-dish-fresh-spring-roll-lumpiang-sariwa-recipe/",
    "https://www.yummy.ph/",
    "https://www.yummy.ph/recipe/steak-with-truffle-fries-recipe?ref=home_featured_big",
    "https://www.yummy.ph/lessons/baking/strawberry-dessert-recipes-a00249-20200206-lfrm",
    "https://www.yummy.ph/lessons/baking/how-to-make-heart-shaped-shortbread-cookies-video",
    "https://www.yummy.ph/lessons/cooking/how-to-rest-meat-a150-a00261-20190508",
    "https://www.yummy.ph/news-trends/heinz-tomato-ketchup-burger-adv-con?ref=home_featured_recipe",
    "https://www.yummy.ph/news-trends/noche-not-so-buena-let-this-app-help-with-your-christmas-meals-adv-con?ref=home_featured_recipe",
    "https://www.yummy.ph/recipe/batangas-lomi-recipe-tagalog-recipe-20241219?ref=home_featured_recipe",
    "https://www.yummy.ph/recipe/adobong-puti-recipe-tagalog-version-20241219?ref=home_featured_recipe",
    "https://www.yummy.ph/recipe/kare-kare-sauce-recipe-tagalog-version-20241219?ref=home_featured_recipe",
    "https://www.yummy.ph/recipe/balbacua-recipe-tagalog-version-20241209?ref=home_featured_recipe",
    "https://www.yummy.ph/recipe/pork-bulalo-recipe-a1793-20211107?ref=category_readmore",
    "https://www.yummy.ph/recipe/batangas-lomi-recipe-tagalog-recipe-20241219",
    "https://www.angsarap.net/",
    "https://www.angsarap.net/2025/05/14/pancit-estacion/",
    "https://www.angsarap.net/2025/05/13/master-pig-auckland-cbd-new-zealand/",
    "https://www.angsarap.net/2025/05/12/loslos/",
    "https://www.angsarap.net/2025/05/09/braised-tofu-hapuka/",
    "https://www.angsarap.net/2025/05/02/picanha/",
    "https://www.angsarap.net/2025/05/05/ube-halo-halo/",
    "https://www.angsarap.net/2025/05/07/beef-pater/",
    "https://www.angsarap.net/2025/05/01/sri-mahkota-browns-bay-north-shore-city-new-zealand/",
    "https://www.angsarap.net/tag/beef/",
    "https://www.angsarap.net/2025/03/24/gyusuji-curry/",
    "https://www.angsarap.net/tag/chicken/",
    "https://www.angsarap.net/2025/04/04/bang-bang-chicken/",
    "https://www.angsarap.net/2025/04/02/chicken-dinakdakan/",
    "https://www.angsarap.net/2025/02/26/chicken-paitan-ramen/",
    "https://www.angsarap.net/2025/02/28/dim-sum-chicken-feet/",
    "https://www.angsarap.net/2025/02/05/chicken-burritos/",
    "https://www.angsarap.net/2025/02/12/lo-mai-gai/",
    "https://www.angsarap.net/2025/01/15/creamy-spinach-and-pumpkin-chicken/",
    "https://www.angsarap.net/2025/01/08/kanto-fried-chicken/",
    "https://www.angsarap.net/2025/05/09/braised-tofu-hapuka/",
    "https://www.angsarap.net/2025/04/09/thai-fish-cakes/",
    "https://www.angsarap.net/tag/fish/",
    "https://www.angsarap.net/2025/03/26/seared-fish-with-green-gazpacho-sauce/",
    "https://www.angsarap.net/2025/03/10/baja-fish-tacos/",
    "https://www.angsarap.net/2025/02/03/fish-tofu-soup/",
    "https://www.angsarap.net/2025/03/05/spicy-ginisang-okra-with-tinapa/",
    "https://www.angsarap.net/2025/01/17/crispy-fried-golden-pompano/",
    "https://www.angsarap.net/2024/12/30/beef-balls-and-fishballs-misua/",
    "https://www.angsarap.net/tag/pork/",
    "https://www.angsarap.net/2025/04/28/sopas-de-upo/",
    "https://www.angsarap.net/2025/03/03/grilled-pork-scotch-with-blackberry-nectarine-cherry-salsa/",
    "https://www.angsarap.net/2025/03/21/ginataang-kalabasa-at-pechay/",
    "https://www.angsarap.net/2024/12/18/cheesy-pork-croquettes/",
    "https://www.angsarap.net/2024/12/11/sisig-pasta/",
    "https://www.angsarap.net/2024/11/13/bacon-cuchifrito/",
    "https://www.kawalingpinoy.com/category/recipe-index/meat-and-poultry/",
    "https://www.kawalingpinoy.com/",
    "https://www.kawalingpinoy.com/category/recipe-index/sweets-and-desserts/",
    "https://www.kawalingpinoy.com/category/side-dishes/",
    "https://www.kawalingpinoy.com/category/recipe-index/breakfast-and-brunch/",
    "https://www.kawalingpinoy.com/category/recipe-index/appetizers/",
    "https://www.kawalingpinoy.com/category/recipe-index/cocktails-and-beverages-recipe-index/",
    "https://www.kawalingpinoy.com/category/main-dishes/",
    "https://www.kawalingpinoy.com/category/appetizers/",
    "https://www.kawalingpinoy.com/recipe-index/",
    "https://www.kawalingpinoy.com/category/breakfast-and-brunch/",
    "https://www.kawalingpinoy.com/beef-tapa/",
    "https://www.kawalingpinoy.com/skinless-longganisa/",
    "https://www.kawalingpinoy.com/chicken-tocino/",
    "https://www.kawalingpinoy.com/pork-tocino/",
    "https://www.kawalingpinoy.com/category/eggs-and-dairy/",
]

# Data collection structure
behavior_data = []
network_data = [] # <-- New list for network events

def get_main_domain(url_str):
    """
    Extracts the main domain (e.g., 'example.com') from a full URL.
    Handles cases with and without schemes, and common subdomains like 'www'.
    """
    if not url_str:
        return None
    try:
        # Ensure the URL has a scheme for urlparse
        if not url_str.startswith(('http://', 'https://', '//')):
            # If scheme is missing and it's not a protocol-relative URL, prepend http
            if not url_str.startswith('//'):
                 url_str = 'http://' + url_str
            else: # For protocol-relative URLs like //example.com/path
                url_str = 'http:' + url_str


        parsed_url = urlparse(url_str)
        hostname = parsed_url.hostname
        if not hostname:
            return None

        parts = hostname.split('.')
        if len(parts) > 1:
            # Handle cases like 'www.example.com' -> 'example.com'
            # Handle 'example.co.uk' -> 'example.co.uk'
            # This is a simplification; for true eTLD+1, 'tldextract' library is more robust
            if parts[0] == 'www' and len(parts) > 2:
                return ".".join(parts[-2:]) if len(parts[-2:]) > 1 else ".".join(parts[-3:]) if len(parts) >2 else hostname # handles .co.uk etc.
            elif len(parts) >=2 :
                 return ".".join(parts[-2:]) if len(parts[-2:]) > 1 else ".".join(parts[-3:]) if len(parts) >2 else hostname # handles .co.uk etc.
        return hostname
    except Exception:
        return None
    
def log_interaction(event_type, element=None, pos_x=None, pos_y=None, details=None):
    """Logs user interaction data"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    current_url = "N/A"
    try:
        current_url = driver.current_url
    except Exception:
        pass # Driver might be closed or in an invalid state

    element_text_val = "N/A"
    element_tag_val = "N/A"

    if element:
        try:
            element_text_val = element.text.replace('\n', ' ').strip()[:100] if element.text else "N/A"
            element_tag_val = element.tag_name
        except Exception: # Catch StaleElementReferenceException or others
            element_text_val = "Error retrieving text"
            element_tag_val = "Error retrieving tag"

    behavior_data.append([
        timestamp,
        current_url,
        event_type,
        pos_x if pos_x else "N/A",
        pos_y if pos_y else "N/A",
        element_tag_val,
        element_text_val,
        details if details else "N/A"
    ])

def log_network_requests(page_url, associated_action="page_load"):
    """
    Logs network requests, focusing on potential third-party tracking
    and excluding common static assets.
    """
    timestamp_capture = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    current_site_main_domain = get_main_domain(page_url)

    # Define patterns for static assets and common benign requests
    # More specific content types to ignore.
    IGNORE_CONTENT_TYPES_START = (
        'image/', 'font/', 'text/css', 'video/', 'audio/'
    )
    # Extensions to ignore (case-insensitive)
    IGNORE_EXTENSIONS = (
        '.css', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico',
        '.woff', '.woff2', '.ttf', '.otf', '.eot',
        '.mp4', '.webm', '.ogg', '.mp3', '.wav'
    )
    # Known CDNs or utility domains you might consider "less suspicious" or want to exclude
    # This list needs careful curation and depends on your definition of "unauthorized"
    KNOWN_BENIGN_DOMAINS_SUFFIXES = (
        # Content Delivery Networks (CDNs) often host JS/CSS for many sites
        # 'bootstrapcdn.com', 'cloudflare.com', 'jsdelivr.net', 'unpkg.com',
        # 'googleapis.com', # Can be for fonts, APIs, but also analytics
        # 'gstatic.com',    # Often for fonts or static Google content
    )


    new_network_events = []

    for request in driver.requests:
        if not request.response:  # Skip requests without responses
            continue

        request_url_lower = request.url.lower()
        response_content_type = request.response.headers.get('Content-Type', '').lower()
        request_main_domain = get_main_domain(request.url)

        # --- STAGE 1: Basic Asset Filtering ---
        # Filter by common static file extensions
        if any(request_url_lower.endswith(ext) for ext in IGNORE_EXTENSIONS):
            continue
        # Filter by common static content types in response
        if any(response_content_type.startswith(ct_start) for ct_start in IGNORE_CONTENT_TYPES_START):
            continue

        # --- STAGE 2: Third-Party Identification ---
        is_third_party = True # Assume third-party unless proven otherwise
        if current_site_main_domain and request_main_domain:
            if current_site_main_domain == request_main_domain:
                is_third_party = False
            # Handle subdomains of the current site as first-party
            elif request_main_domain.endswith("." + current_site_main_domain):
                 is_third_party = False


        # --- STAGE 3: Filtering out "known benign" or focusing only on third-party ---
        # If you only want third-party tracking requests:
        if not is_third_party:
            # You *might* want to log first-party POST requests if they send a lot of data
            # or if you suspect first-party overreach. For now, we skip all first-party.
            continue

        # Optional: Filter out requests to known benign third-party utility domains (CDNs, etc.)
        # This is tricky as these can also be used for tracking indirectly
        # if any(request_main_domain.endswith(suffix) for suffix in KNOWN_BENIGN_DOMAINS_SUFFIXES):
        #     continue

        # --- STAGE 4: Selective Body/Header Logging (Criteria for "suspicious") ---
        req_body_short = "N/A"
        log_this_request = False

        # Criteria for logging a request:
        # 1. It's a POST/PUT/DELETE request (more likely to send data)
        if request.method in ('POST', 'PUT', 'DELETE'):
            log_this_request = True
            if request.body: # Only get body if method suggests data sending
                 try:
                     # Check if body looks like JSON or form data (often used for tracking payloads)
                     req_content_type_lower = request.headers.get('Content-Type', '').lower()
                     if 'json' in req_content_type_lower or 'x-www-form-urlencoded' in req_content_type_lower or 'text/plain' in req_content_type_lower:
                        req_body_short = request.body.decode('utf-8', errors='ignore')[:200] # Truncate
                     else:
                        req_body_short = f"[Non-text Body Present - Size: {len(request.body)} bytes, Type: {req_content_type_lower}]"
                 except Exception:
                     req_body_short = f"[Binary or Undecodable Body - Size: {len(request.body)} bytes]"

        # 2. It's a GET request to a third-party that looks like a tracking pixel/beacon
        #    (often small, might have query params with PII or identifiers)
        elif request.method == 'GET' and is_third_party:
            # Heuristics for tracking beacons:
            # - URL contains common tracking parameters (e.g., 'utm_', 'gclid', 'uid', 'idfa')
            # - URL is very long (often due to encoded data)
            # - Response is often tiny (e.g., 1x1 pixel image, or 204 No Content)
            if '?' in request.url and len(request.url) > 150: # Arbitrary length, adjust
                log_this_request = True
            elif any(tracker_param in request_url_lower for tracker_param in ['utm_','gclid=','client_id=','user_id=','uid=','event=','beacon']):
                log_this_request = True
            elif request.response.status_code == 204 or \
                 (response_content_type.startswith('image/') and request.response.body and len(request.response.body) < 500): # Small image
                log_this_request = True


        # --- STAGE 5: Log if it meets criteria ---
        if log_this_request:
            new_network_events.append([
                timestamp_capture,
                page_url,
                associated_action,
                request.method,
                request.url, # Crucial for identifying trackers
                request.response.status_code,
                request.response.reason,
                request.headers.get('Referer', 'N/A'), # Referer can be interesting for tracking
                response_content_type, # What kind of data was returned
                req_body_short, # Only populated if criteria met
            ])

    if new_network_events:
        network_data.extend(new_network_events)
    del driver.requests

def collect_mouse_movements(duration=10):
    start_time = time.time()
    last_x, last_y = None, None
    try:
        while time.time() - start_time < duration:
            current_x = driver.execute_script("return window.mouseX")
            current_y = driver.execute_script("return window.mouseY")

            if (current_x is not None and current_y is not None) and \
               (current_x != last_x or current_y != last_y):
                log_interaction("mouse_move", pos_x=current_x, pos_y=current_y)
                last_x, last_y = current_x, current_y
            time.sleep(0.1)
    except Exception as e:
        print(f"Error during mouse movement collection: {e}")
        log_interaction("error", details=f"Mouse movement collection: {str(e)}")


def setup_mouse_tracking():
    driver.execute_script("""
    window.mouseX = null; // Initialize to null
    window.mouseY = null;
    document.addEventListener('mousemove', function(e) {
        window.mouseX = e.clientX;
        window.mouseY = e.clientY;
    }, true); // Use capture phase
    """)

try:
    # Create CSV files and write headers
    with open(BEHAVIOR_LOG_FILE, 'w', newline='', encoding='utf-8') as f_behavior:
        writer_behavior = csv.writer(f_behavior)
        writer_behavior.writerow([
            "timestamp", "url", "event_type",
            "pos_x", "pos_y", "element_tag",
            "element_text", "details"
        ])

    with open(NETWORK_LOG_FILE, 'w', newline='', encoding='utf-8') as f_network:
        writer_network = csv.writer(f_network)
        writer_network.writerow([
            "capture_timestamp", "page_url", "associated_action",
            "request_method", "request_url", "response_status", "response_reason",
            "request_referer", "response_content_type", "request_body_snippet" # Changed headers
        ])

    for site_url in RECIPE_SITES:
        print(f"Processing site: {site_url}")
        try:
            del driver.requests

            driver.get(site_url)
    
            setup_mouse_tracking() # Setup mouse tracking for each new page

            log_interaction("page_visit", details=f"Navigated to {site_url}")
            time.sleep(random.uniform(2, 4)) # Allow page to load, initial scripts to run
            log_network_requests(driver.current_url, "initial_page_load") # <-- Log network activity

            collect_mouse_movements(random.uniform(3, 6))

            # Attempt to handle cookie banners (very basic example)
            cookie_banners_selectors = [
                "button[id*='consent']", "button[class*='consent']",
                "button[id*='cookie']", "button[class*='cookie']",
                "div[aria-label*='cookie'] button",
                "button:contains('Accept')", "button:contains('Agree')", # May need jQuery for :contains
                "//button[contains(text(),'Accept') or contains(text(),'Agree') or contains(text(),'Got it')]" # XPath
            ]
            for selector in cookie_banners_selectors:
                try:
                    # Using a short timeout for cookie banners
                    if "//" in selector: # XPath
                         banner_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else: # CSS Selector
                        banner_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    if banner_button.is_displayed():
                        log_interaction("attempt_cookie_banner_dismiss", banner_button)
                        banner_button.click()
                        log_interaction("cookie_banner_dismissed", banner_button)
                        time.sleep(random.uniform(1, 2))
                        log_network_requests(driver.current_url, "after_cookie_dismiss") # Log network after this
                        break # Stop after first successful dismissal
                except Exception:
                    continue # Banner not found or not clickable with this selector

            clickables = []
            try:
                clickables = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a, button, input[type='submit'], [role='button']"))
                )
                clickables = [el for el in clickables if el.is_displayed() and el.is_enabled()] # Filter for visible & enabled
            except Exception as e:
                log_interaction("error", details=f"Could not find clickables on {driver.current_url}: {str(e)}")
                print(f"Warning: No clickable elements found on {driver.current_url} or error: {e}")


            for i in range(random.randint(1, 3)): # Reduced interactions for faster testing
                if not clickables:
                    break
                try:
                    element_to_click = random.choice(clickables)
                    if not element_to_click.is_displayed() or not element_to_click.is_enabled():
                        log_interaction("skip_interaction", element_to_click, details="Element not visible/enabled")
                        clickables.remove(element_to_click) # Avoid re-selecting stale/hidden element
                        continue

                    action.move_to_element(element_to_click).perform()
                    location = element_to_click.location_once_scrolled_into_view # Ensure it's in view
                    size = element_to_click.size
                    center_x = location['x'] + size['width']/2
                    center_y = location['y'] + size['height']/2
                    log_interaction("mouse_move_to_element", element_to_click, center_x, center_y)
                    time.sleep(random.uniform(0.5, 1.0))

                    # Clear requests before a click to isolate network activity for that click
                    del driver.requests
                    current_url_before_click = driver.current_url
                    element_to_click.click()
                    log_interaction("click", element_to_click, center_x, center_y)
                    time.sleep(random.uniform(2, 4)) # Wait for page to potentially reload or AJAX
                    
                    # Log network requests triggered by the click
                    # If URL changed, log with new URL, otherwise old one
                    page_after_click = driver.current_url if driver.current_url != current_url_before_click else current_url_before_click
                    log_network_requests(page_after_click, f"after_click_{i+1}")

                    collect_mouse_movements(random.uniform(2, 4))

                    # Update clickable elements list as page might have changed
                    clickables = driver.find_elements(By.CSS_SELECTOR, "a, button, input[type='submit'], [role='button']")
                    clickables = [el for el in clickables if el.is_displayed() and el.is_enabled()]
                except Exception as e:
                    log_interaction("error", details=f"Interaction failed: {str(e)}")
                    print(f"Interaction failed: {e}")
                    # If an error occurs, try to refresh the clickables list
                    try:
                        clickables = driver.find_elements(By.CSS_SELECTOR, "a, button, input[type='submit'], [role='button']")
                        clickables = [el for el in clickables if el.is_displayed() and el.is_enabled()]
                    except:
                        clickables = [] # Reset if page is too broken
                    continue
        except Exception as e:
            print(f"Major error processing site {site_url}: {e}")
            log_interaction("error", details=f"Major error on site {site_url}: {str(e)}")
            # Ensure driver.requests is cleared even on major site error
            try:
                del driver.requests
            except:
                pass # driver might already be dead

finally:
    # Save all collected data
    with open(BEHAVIOR_LOG_FILE, 'a', newline='', encoding='utf-8') as f_behavior:
        writer_behavior = csv.writer(f_behavior)
        writer_behavior.writerows(behavior_data)

    with open(NETWORK_LOG_FILE, 'a', newline='', encoding='utf-8') as f_network:
        writer_network = csv.writer(f_network)
        writer_network.writerows(network_data)

    if driver:
        driver.quit()
    print(f"Data collection complete.")
    print(f"Behavior log saved to: {BEHAVIOR_LOG_FILE} ({len(behavior_data)} records)")
    print(f"Network log saved to: {NETWORK_LOG_FILE} ({len(network_data)} records)")