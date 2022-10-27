import csv
import os
import requests
import re
import json

"</thead>.*?<tbody>.*?(.*)<p class='footnote'>"

vzorec_bloka = re.compile(
    r"</thead>.*?<tbody>.*?(.*)<p class='footnote'>",
    flags=re.DOTALL
)


vzorec_totals = re.compile(
    r"/Summary/(?P<id>\d+)\">(?P<ime>[\w\s,\.\-']+?)</a>( \*)*</td><td>(?P<ekipa>\w{3}|-)</td><td>(?P<GP>[\d,]+)</td><td>(?P<MIN>[1234567890\.,]*)</td><td>(?P<pike>[\d,]+)</td><td>(?P<FGM>[\d,]+)</td><td>(?P<FGA>[\d,]+)</td><td>(?P<FG_procent>[0-9\.]+)</td><td>(?P<triPM>[\d,]+)</td><td>(?P<triPA>[\d,]+)</td><td>(?P<tri_procent>[0-9\.]+)</td><td>(?P<FTM>[\d,]+)</td><td>(?P<FTA>[\d,]+)</td><td>(?P<FT_procent>[0-9\.]+)</td><td>(?P<OREB>[\d,]+)</td><td>(?P<DREB>[\d,]+)</td><td>(?P<REB>[\d,]+)</td><td>(?P<ASIST>[\d,]+)</td><td>(?P<STEAL>[\d,]+)</td><td>(?P<BLOK>[\d,]+)</td><td>(?P<TURNOVER>[\d,]+)</td><td>(?P<FPF>[\d,]+)</td></tr>",
    flags=re.DOTALL
)

vzorec_misc = re.compile(
    r"/Summary/(?P<id>\d+)\">(?P<ime>[\w\s,\.\-']+?)</a>( \*)*</td><td>(?P<ekipa>\w{3}|-)</td><td>(?P<dbl>[\d,]+)</td><td>(?P<tpl>[\d,]+)</td><td>(?P<tpl1>[\d,]+)</td><td>(?P<tp2l>[\d,]+)</td><td>(?P<tp3l>[\d,]+)</td><td>(?P<t4pl>[\d,]+)</td><td>(?P<t5pl>[\d,]+)</td><td>(?P<tp6l>[\d,]+)</td><td>(?P<t7pl>[\d,]+)</td><td>(?P<Hob>[0-9\.]+)</td><td>(?P<asttov>[0-9\.]+)</td><td>(?P<FT_procent>[0-9\.]+)</td><td>(?P<asttv>[0-9\.]+)</td><td>(?P<DREB>[\d,]+)</td><td>(?P<REB>[\d,]+)</td><td>(?P<FT_pfrocent>[0-9\.]+)</td><td>(?P<FT_gprocent>[0-9\.\-]+)</td><td>(?P<FTh_procent>[0-9\.\-]+)</td><td>(?P<FT_projcent>[0-9\.\-]+)</td>",
    flags=re.DOTALL
)

vzorec_averages = re.compile(
    r"/Summary/(?P<id>\d+)\">(?P<ime>[\w\s,\.\-']+?)</a>( \*)*</td><td>(?P<ekipa>\w{3}|-)</td><td>(?P<stevilka>[\d,]+)</td><td>(?P<procent1>[1234567890\.,]*)</td><td>(?P<procent2>[1234567890\.,]*)</td><td>(?P<procent3>[1234567890\.,]*)</td><td>(?P<procent4>[1234567890\.,]*)</td><td>(?P<procent5>[1234567890\.,]*)</td><td>(?P<procent6>[1234567890\.,]*)</td><td>(?P<procent7>[1234567890\.,]*)</td><td>(?P<procent8>[1234567890\.,]*)</td><td>(?P<procent9>[1234567890\.,]*)</td><td>(?P<procent10>[1234567890\.,]*)</td><td>(?P<procent11>[1234567890\.,]*)</td><td>(?P<procent12>[1234567890\.,]*)</td><td>(?P<procent13>[1234567890\.,]*)</td><td>(?P<procent14>[1234567890\.,]*)</td><td>(?P<procent15>[1234567890\.,]*)</td><td>(?P<procent16>[1234567890\.,]*)</td><td>(?P<procent17>[1234567890\.,]*)</td><td>(?P<procent18>[1234567890\.,]*)</td><td>(?P<procent19>[1234567890\.,]*)</td></tr>",
    flags=re.DOTALL
)

def uredi_igralca(igralec,vrsta_statistike):
    kosarkar = dict()
    if vrsta_statistike == "Totals":
        id_igralca ,ime ,aktivnost,ekipa, stevilo_igranih_iger, minutaza, stevilo_tock, field_goal_made, field_goal_attempt, field_goal_procantage, three_point_made, three_point_attempt, three_point_percentage, free_throws_made, free_throws_attempted, free_throws_percentage, offensive_rebound, deffensive_rebound, rebound, assist, steal, block, turn_over, personal_fouls = igralec
        kosarkar["id_igralca"] = int(id_igralca)
        kosarkar["ime"] = ime
        if "*" in aktivnost:
            kosarkar["trenutna_aktivnost"] = "Da"
        else:
            kosarkar["trenutna_aktivnost"] = "Ne"
        kosarkar["ekipa"] = ekipa
        kosarkar["stevilo_igranih_iger"] = int(stevilo_igranih_iger.replace(",",""))
        kosarkar["minute_na_parketu"] = float(minutaza.replace(",",""))
        kosarkar["dosezene_tocke"] = int(stevilo_tock.replace(",",""))
        kosarkar["zadeti_meti_na_kos"] = int(field_goal_made.replace(",",""))
        kosarkar["poskusi_meta_na_kos"] = int(field_goal_attempt.replace(",",""))
        kosarkar["procent_zadetih_metov"] = float("0"+field_goal_procantage)
        kosarkar["zadeti_meti_za_tri_tocke"] = int(three_point_made.replace(",",""))
        kosarkar["poskusi_meta_za_tri_tocke"] = int(three_point_attempt.replace(",",""))
        kosarkar["procent_meta_za_tri_tocke"] = float("0"+three_point_percentage)
        kosarkar["zadeti_prosti_meti"] = int(free_throws_made.replace(",",""))
        kosarkar["poskusi_prostega_meta"] = int(free_throws_attempted.replace(",",""))
        kosarkar["procent_zadetih_prostih_metov"] = float("0"+free_throws_percentage)
        kosarkar["napadalni_skok"] = int(offensive_rebound.replace(",",""))
        kosarkar["obrambni_skok"] = int(deffensive_rebound.replace(",",""))
        kosarkar["skok"] = int(rebound.replace(",",""))
        kosarkar["podaje"] = int(assist.replace(",",""))
        kosarkar["ukradene_zoge"] = int(steal.replace(",",""))
        kosarkar["blokade"] = int(block.replace(",",""))
        kosarkar["izgubljene_zoge"] = int(turn_over.replace(",",""))
        kosarkar["osebne_napake"] = int(personal_fouls.replace(",",""))
    if vrsta_statistike == "Misc_Stats":
        id_igralca ,ime ,aktivnost,ekipa, dvojni_dvojcek, trojni_dvojcek, igre_40_tock, igre_20_skokov, igre_20_asistenc,igre_5_ukradenih, igre_5_blokov, najvec_tock_v_eni_igri, tehnicna_napaka, HOB, assist_turnover, steal_turnover, freethrows_to_fieldgoalattempt, zmage, porazi, procent_zmag, procent_porazov, zmage_v_napadu, zmage_v_obrambi = igralec
        kosarkar["id_igralca"] = int(id_igralca)
        kosarkar["ime"] = ime
        if "*" in aktivnost:
            kosarkar["trenutna_aktivnost"] = "Da"
        else:
            kosarkar["trenutna_aktivnost"] = "Ne"
        kosarkar["ekipa"] = ekipa
        kosarkar["dvojni_dvojcek"] = int(dvojni_dvojcek)
        kosarkar["trojni_dvojcek"] = int(trojni_dvojcek)  
        kosarkar["40+_tock"] = int(igre_40_tock)
        kosarkar["20+_skokov"] = int(igre_20_skokov)
        kosarkar["20+_asistenc"] = int(igre_20_asistenc)
        kosarkar["5+_ukradenih_zog"] = int(igre_5_ukradenih)
        kosarkar["5+_blokov"] = int(igre_5_blokov)
        kosarkar["max_tock_v_igri"] = int(najvec_tock_v_eni_igri)
        kosarkar["stevilo_tehnicnih_napak"] = int(tehnicna_napaka)
        kosarkar["hands_on_bucket_HOB"] = float("0"+ HOB)
        kosarkar["asistence_proti_izgubljenim_zogam"] = float(assist_turnover)
        kosarkar["ukradene_zoge_proti_izgubljenim"] = float(steal_turnover)
        kosarkar["prosti_meti_proti_poskuom_meta_na_kos"] = float(freethrows_to_fieldgoalattempt)
        kosarkar["zmage"] = int(zmage.replace(",",""))
        kosarkar["porazi"] = int(porazi.replace(",",""))
        kosarkar["procent_zmag"] = float("0"+ procent_zmag)
    if vrsta_statistike == "Averages":
        id_igralca ,ime ,aktivnost,ekipa,igrane_igre, minute_na_igro, tocke_na_igro, zadeti_meti_na_kos_na_igro, poskus_meta_na_kos_na_igro,procent_zdetih_metov, zadeti_meti_za_tri_tocke_na_igro, poskusi_meta_za_tri_tocke_na_igro, procent_zadetih_metov_za_tri_tocke, zadeti_prosti_meti_na_igro, poskusi_prostega_meta_na_igro, procent_zadetih_prostih_metov, napdalni_skoki_na_igro, obrambni_skoki_na_igro, skoki_na_igro, asistence_na_igro, ukradene_zoge_na_igro, blokade_na_igro, izgubljene_zoge_na_igro, osebne_napake_na_igro  = igralec
        kosarkar["id_igralca"] = int(id_igralca)
        kosarkar["ime"] = ime
        if "*" in aktivnost:
            kosarkar["trenutna_aktivnost"] = "Da"
        else:
            kosarkar["trenutna_aktivnost"] = "Ne"
        kosarkar["ekipa"] = ekipa
        kosarkar["stevilo_igranih_iger"] = int(igrane_igre.replace(",",""))
        kosarkar["minute_na_parketu_na_igro"] = float(minute_na_igro) 
        kosarkar["tocke_na_igro"] = float(tocke_na_igro)
        kosarkar["zadeti_meti_na_igro"] = float(zadeti_meti_na_kos_na_igro)
        kosarkar["poskusi_meta_na_kos_na_igro"] = float(poskus_meta_na_kos_na_igro)
        kosarkar["procent_zadetih_metov_na_kos"] = float(procent_zdetih_metov)
        kosarkar["zadeti_meti_za_tri_tocke_na_igro"] =float(zadeti_meti_za_tri_tocke_na_igro) 
        kosarkar["poskusi_meta_za_tri_tocke_na_igro"] = float(poskusi_meta_za_tri_tocke_na_igro)
        kosarkar["procent_zadetih_metov_za_tri_tocke"] = float(procent_zadetih_metov_za_tri_tocke)
        kosarkar["zadeti_prosti_meti_na_igro"] = float(zadeti_prosti_meti_na_igro)
        kosarkar["poskusi_prostega_meta_na_igro"] = float(poskusi_prostega_meta_na_igro)
        kosarkar["procent_zadetih_prostih_metov"] = float(procent_zadetih_prostih_metov)
        kosarkar["napadalni_skoki_na_igro"] = float(napdalni_skoki_na_igro)
        kosarkar["obrambni_skoki_na_igro"] = float(obrambni_skoki_na_igro)
        kosarkar["skoki_na_igro"] = float(skoki_na_igro)
        kosarkar["asistence_na_igro"] = float(asistence_na_igro)
        kosarkar["ukradene_zoge_na_igro"] = float(ukradene_zoge_na_igro)
        kosarkar["blokade_na_igro"] = float(blokade_na_igro)
        kosarkar["izgubljene_zoge_na_igro"] = float(izgubljene_zoge_na_igro)
        kosarkar["osebne_napake_na_igro"] = float(osebne_napake_na_igro)
    return kosarkar

kosarkarji_totals = []
kosarkarji_misc = []
kosarkarji_averages = []

for j in ["Totals","Misc_Stats", "Averages"]:
    for i in range(1,19):
        if j != "Misc_Stats" and i > 16:
            pass
        else:
            with open(f"kosarkarji-{j}-stran{i}") as dat:
                vsebina = dat.read()
                for blok in vzorec_bloka.finditer(vsebina):
                    if j =="Misc_Stats":
                        for igralec in vzorec_misc.findall(blok.group(0)):
                            kosarkarji_misc.append(uredi_igralca(igralec,j))
                    if j == "Totals":
                        for igralec in vzorec_totals.findall(blok.group(0)):
                            kosarkarji_totals.append(uredi_igralca(igralec,j))
                    if j == "Averages":
                        for igralec in vzorec_averages.findall(blok.group(0)):
                            kosarkarji_averages.append(uredi_igralca(igralec,j))

with open("kosarkarji-misc.json", "w") as dat:
    json.dump(kosarkarji_misc, dat, indent=4, ensure_ascii=False)                 
with open("kosarkarji-averages.json", "w") as dat:
    json.dump(kosarkarji_averages, dat, indent=4, ensure_ascii=False)                 
with open("kosarkarji-totals.json", "w") as dat:
    json.dump(kosarkarji_totals, dat, indent=4, ensure_ascii=False)                 

with open("kosarkarji-misc.csv", "w") as dat:
    writer = csv.DictWriter(dat, [
        "id_igralca",
        "ime",
        "trenutna_aktivnost",
        "ekipa",
        "dvojni_dvojcek",
        "trojni_dvojcek",
        "40+_tock",
        "20+_skokov",
        "20+_asistenc",
        "5+_ukradenih_zog",
        "5+_blokov",
        "max_tock_v_igri",
        "stevilo_tehnicnih_napak",
        "hands_on_bucket_HOB",
        "asistence_proti_izgubljenim_zogam",
        "ukradene_zoge_proti_izgubljenim",
        "prosti_meti_proti_poskuom_meta_na_kos",
        "zmage",
        "porazi",
        "procent_zmag"
        ])
    writer.writeheader()
    writer.writerows(kosarkarji_misc)

with open("kosarkarji-totals.csv", "w") as dat:
    writer = csv.DictWriter(dat, [
        "id_igralca",
        "ime",
        "trenutna_aktivnost",
        "ekipa",
        "stevilo_igranih_iger",
        "minute_na_parketu",
        "dosezene_tocke",
        "zadeti_meti_na_kos",
        "poskusi_meta_na_kos",
        "procent_zadetih_metov",
        "zadeti_meti_za_tri_tocke",
        "poskusi_meta_za_tri_tocke",
        "procent_meta_za_tri_tocke",
        "zadeti_prosti_meti",
        "poskusi_prostega_meta",
        "procent_zadetih_prostih_metov",
        "napadalni_skok",
        "obrambni_skok",
        "skok",
        "podaje",
        "ukradene_zoge",
        "blokade",
        "izgubljene_zoge",
        "osebne_napake"
        ])

    writer.writeheader()
    writer.writerows(kosarkarji_totals)

with open("kosarkarji-averages.csv", "w") as dat:
    writer = csv.DictWriter(dat, [
        "id_igralca",
        "ime",
        "trenutna_aktivnost",
        "ekipa",
        "stevilo_igranih_iger",
        "minute_na_parketu_na_igro",
        "tocke_na_igro",
        "zadeti_meti_na_igro",
        "poskusi_meta_na_kos_na_igro",
        "procent_zadetih_metov_na_kos",
        "zadeti_meti_za_tri_tocke_na_igro",
        "poskusi_meta_za_tri_tocke_na_igro",
        "procent_zadetih_metov_za_tri_tocke",
        "zadeti_prosti_meti_na_igro",
        "poskusi_prostega_meta_na_igro",
        "procent_zadetih_prostih_metov",
        "napadalni_skoki_na_igro",
        "obrambni_skoki_na_igro",
        "skoki_na_igro",
        "asistence_na_igro",
        "ukradene_zoge_na_igro",
        "blokade_na_igro",
        "izgubljene_zoge_na_igro",
        "osebne_napake_na_igro"
        ])
    writer.writeheader()
    writer.writerows(kosarkarji_averages)

print(len(kosarkarji_averages),len(kosarkarji_totals),len(kosarkarji_misc))

