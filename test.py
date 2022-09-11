from bs4 import BeautifulSoup
import requests
import csv
from io import StringIO

def firewatch():
    info_list = []
    url = "https://www.fire.ca.gov/incidents/2022/"
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")
    scripts = soup.find_all("script")
    str_scripts = str(scripts)
    with open("califire.txt", "w") as f:
        f.write(str_scripts)
        f.close()
    with open("califire.txt", "r") as read:
        for line in read:
            info_list.extend(line.split())

    for idx, v in enumerate(info_list):
        if "Latitude" in v:
            line1 = info_list[idx]

            reader = csv.reader(StringIO(line1))
            out = next(reader)
            try:
                if "Longitude" in out[1]:
                    # print(out[0] + "||" + out[1] + ".")
                    lat = out[0].split(':')[-1]
                    lon = out[1].split(":")[-1]
                    print(lat + "||" + lon )
                else:
                    # print(out[1]+"| |" + out[2] + "..")
                    lat = out[1].split(':')[-1]
                    lon = out[2].split(":")[-1]
                    print(lat + "||" + lon )

                if "PercentContainedDisplay" in out[3]:
                    print(out[2] + "||" + out[3] + ".")
                else:
                    print(out[3] + "||" + out[4] + "..")
                    print("-----------------------------------------------------------")
            except:
                print("latitude not in index")
# print(info_list[1619])
# line = info_list[1619]
# reader = csv.reader(StringIO(line))
# out = next(reader)
# print(out[1])
# print(out[2])
    # if word == '"Latitude"':
    #     index = index(word)
    #     print(index)
    # else:
    #     print("no word")
        # act_list.append(word)
        # index
        # print(info_list[dtx])
        # print("................................................................")



# with open("califire.txt", "w") as f:
#     f.write(scripts)
#     f.close()



# for line in act_doc:
#     print(line)
    # x = x + 1 
    # print(line)
    # if x > 1000:
    #     break


# tag = doc.find("script")
# print(tag)

# for line in result:
#     for word in line.split():
#         string_word = str(word)
#         if '"Name":' in string_word:
# print(list)
#         string_word = str(line)
#         x = x+1
#         list.append(word)
#         if word == "Name":
#             print(x)
# print(list)
            

    

    # if "Fire" in line:
    #     print(line)
    # else:
    #     print("no fire")