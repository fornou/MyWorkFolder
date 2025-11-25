import formattatore_csv as fc
###
### C:\Users\mattia.forneron\Desktop\forneron_orangina_9_15_05\AlarmsHistory_20250516_170243.csv
###
url = input('Inserisci percorso file .csv:\n')
colonna_data = ['Data\\Ora']

f = fc.formattatore_csv(url, colonna_data)
f.converti_date(colonna_data)
f.esporta_file()



