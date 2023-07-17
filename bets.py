from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import json
import numpy as np
import scipy

dupes = {"anthony davis":"02", "jaylen brown":"02", "jalen green":"05", "keldon johnson":"04", 
         "bojan bogdanovic":"02", "danny green":"02"
         , "harrison barnes":"02", "isaiah thomas":"02", "jeff green":"02", "josh jackson":"02", 
         "markieff morris":"02", "miles bridges":"02",
         "sterling brown":"02", "tobias harris":"02", "derrick jones":"02", "gary payton":"02", 
         "gary trent":"02", "jaren jackson":"02", "larry nance":"02",
         "tim hardaway":"02", "patty mills":"02", "damion lee":"03", "damian jones":"03", 
         "marcus morris":"03", "dennis smith":"03", "kenrich williams":"04",
         "robert williams":"04", "stanley johnson":"04", "jaylin williams":"07", 
         "jalen williams":"06", "jaden hardy":"02", "keegan murray":"02",
         "kevin porter":"02", "jalen johnson":"05", }


p = input("Enter first and last name of player: ")
c = input("Enter a category: points, assists, rebounds, steals, or blocks: ")
a = input("Enter how many " + c + " " + p + " must get: ")
temp = p.lower()
p = p.lower().split()
p = str(p[1][:5]) + str(p[0][:2])
p += dupes[temp] if temp in dupes else "01"


def getProb(player, category, amount):
    lefile = client.regular_season_player_box_scores(
        player_identifier=player, season_end_year=2023, output_type=OutputType.JSON
    )

    data = json.loads(lefile)

    # Iterating through the json
    # list

    points = []
    for i in data:
        if i["active"]:
            if category == "points":
                points.append(i["points_scored"])
            elif category == "assists":
                points.append(i["assists"])
            elif category == "steals":
                points.append(i["steals"])
            elif category == "blocks":
                points.append(i["blocks"])
            elif category == "rebounds":
                points.append(i["defensive_rebounds"] + i["offensive_rebounds"])
    points = np.array(points)
    average = np.mean(points)
    stdev = np.std(points)
    return 1 - scipy.stats.norm(average, stdev).cdf(int(amount))


chance = getProb(p, c, a)
cutoff = (100 - 100 * chance) / chance
print(chance)
if chance < 0.5:
    cutoff = int(cutoff) - 1
    print("make the bet if the line is +" + str(cutoff) + " or more favorable")
else:
    cutoff = 100 * chance / (1 - chance)
    cutoff = int(cutoff) + 1
    print("make the bet if the line is -" + str(cutoff) + " or more favorable")
