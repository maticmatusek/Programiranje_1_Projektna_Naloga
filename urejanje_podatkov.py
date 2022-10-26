import csv
import os
import requests
import re
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
    r'<a href="/title/tt(?P<id>\d+)/.*?".*?'
    r'img alt="(?P<naslov>.+?)".*?'
    r'lister-item-year text-muted unbold">.*?\((?P<leto>\d{4})\)</span>.*?'
    r'runtime">(?P<dolzina>\d+?) min</.*?'
    r'<span class="genre">(?P<zanri>.*?)</span>.*?'
    r'<strong>(?P<ocena>.+?)</strong>.*?'
    r'<p class="text-muted">(?P<opis>.+?)</p.*?'
    r'Directors?:(?P<reziserji>.+?)(<span class="ghost">|</p>).*?'
    r'Votes:.*?data-value="(?P<glasovi>\d+)"',
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
        kosarkar["ukradene zoge"] = int(steal.replace(",",""))
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

        #  zmage, porazi, procent_zmag, procent_porazov, zmage_v_napadu, zmage_v_obrambi, dodatne_zmage
    if vrsta_statistike == "Averages":
        pass
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
                            print(igralec)
                    if j == "Totals":
                        for igralec in vzorec_totals.findall(blok.group(0)):
                            kosarkarji_totals.append(uredi_igralca(igralec,j))
                    if j == "Averages":
                        pass
                    
print(kosarkarji_misc[1],len(kosarkarji_misc))