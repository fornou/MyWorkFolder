import formattatore_csv as fc
# C:\Users\mattia.forneron\Desktop\myfolder\MyWorkFolder\eurofork\prj_02\csv_files\Tonno Callipo\file_originali\MissionHistory3.csv
# C:\Users\mattia.forneron\Desktop\myfolder\MyWorkFolder\eurofork\prj_02\csv_files\Tonno Callipo\file_formattati\AlarmsHistory_elaborato.csv

url = input('Inserisci percorso file .csv:\n')
# colonne_date = ['Data\\Ora TX','Data\\Ora RX','Data\\Ora inizio']
colonna_data = ['Data\\Ora']

# print("Commesse presenti:\n -1 Bosal \n -2 Tonno Callipo")
# commessa = input('Di quale commessa sono i dati:\n')
# tabella = input("In quale tabella vuoi pushare i dati")

# f = fc.formattatore_csv(url, colonne_date, 3)
f = fc.formattatore_csv(url, colonna_data)
print("Colonne originali:", f.df.columns)

# f.traduci_colonne(f.url)


# f.testa_conversione()

print(f.df.columns)

f.converti_date(colonna_data)
# f.aggiungi_campo()
f.esporta_file()



