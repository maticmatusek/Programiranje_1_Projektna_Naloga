import csv
import os
import requests
import re

modeli = [
    "Amarok","Arteon","Arteon Shooting Brake","Beetle","Bora","Caddy","California",
    "Caravelle","CC","Corrado","CrossPolo","CrossTouran","Eos","Fox","Golf","Golf Plus",
    "Golf Sportsvan","Golf Variant","Hrošč","ID.3","ID.4","ID.5","Jetta","Karmann Ghia",
    "Lupo","Multivan","Passat","Passat Alltrack","Passat CC","Passat Variant","Phaeton",
    "Polo","Scirocco","Sharan","Taigo","T-Cross","Tiguan","Tiguan Allspace","Touareg",
    "Touran","Transporter","T-Roc","T-Roc Cabriolet","up!"
    ]

url_kosarka = r"https://basketball.realgm.com/nba/stats/Historical/Misc_Stats/Qualified/dbl_dbl/All/desc/18/Regular_Season"
urll =         "https://basketball.realgm.com/nba/stats/Historical/Misc_Stats/Qualified/points/All/desc/18/Regular_Season"

# season : historical
# stat_type : average(1787), total(1584), misc. (1787)
# strani od 1 do 16-18
# združi tabele skupaj

def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        page_content = requests.get(url)
    except Exception as e:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print(f"NAPAKA PRI PRNOSU: {url} ::",e)
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    return page_content.text

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


for i in range(1,19):
    if i > 16:
        stran3 = download_url_to_string(f"https://basketball.realgm.com/nba/stats/Historical/Misc_Stats/Qualified/points/All/desc/{i}/Regular_Season")
        save_string_to_file(stran3,filename = f"kosarkarji-Misc_Stats-stran{i}",directory=r"C:\Users\matic\Documents\sola\3.Letnik\Zimski_semester\Programiranje_1\projektna_naloga\Programiranje_1_Projektna_Naloga" )

    else:
        stran1 = download_url_to_string(f"https://basketball.realgm.com/nba/stats/Historical/Averages/Qualified/dbl_dbl/All/desc/{i}/Regular_Season")
        save_string_to_file(stran1,filename = f"kosarkarji-Averages-stran{i}",directory=r"C:\Users\matic\Documents\sola\3.Letnik\Zimski_semester\Programiranje_1\projektna_naloga\Programiranje_1_Projektna_Naloga" )
        stran2 = download_url_to_string(f"https://basketball.realgm.com/nba/stats/Historical/Totals/Qualified/points/All/desc/{i}/Regular_Season")
        save_string_to_file(stran2,filename = f"kosarkarji-Totals-stran{i}",directory=r"C:\Users\matic\Documents\sola\3.Letnik\Zimski_semester\Programiranje_1\projektna_naloga\Programiranje_1_Projektna_Naloga" )
        stran3 = download_url_to_string(f"https://basketball.realgm.com/nba/stats/Historical/Misc_Stats/Qualified/points/All/desc/{i}/Regular_Season")
        save_string_to_file(stran3,filename = f"kosarkarji-Misc_Stats-stran{i}",directory=r"C:\Users\matic\Documents\sola\3.Letnik\Zimski_semester\Programiranje_1\projektna_naloga\Programiranje_1_Projektna_Naloga" )

        
        