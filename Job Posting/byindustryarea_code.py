# Importing excel file
import xlrd
import xlwt

#changing state name
states={
"Alabama":"AL",
"Alaska":"AK",
"Arizona":"AZ",
"Arkansas":"AR",
"California":"CA",
"Colorado":"CO",
"Connecticut":"CT",
"Delaware":"DE",
"Florida":"FL",
"Georgia":"GA",
"Hawaii":"HI",
"Idaho":"ID",
"Illinois":"IL",
"Indiana":"IN",
"Iowa":"IA",
"Kansas":"KS",
"Kentucky":"KY",
"Louisiana":"LA",
"Maine":"ME",
"Maryland":"MD",
"Massachusetts":"MA",
"Michigan":"MI",
"Minnesota":"MN",
"Mississippi":"MS",
"Missouri":"MO",
"Montana":"MT",
"Nebraska":"NE",
"Nevada":"NV",
"New Hampshire":"NH",
"New Jersey":"NJ",
"New Mexico":"NM",
"New York":"NY",
"North Carolina":"NC",
"North Dakota":"ND",
"Ohio":"OH",
"Oklahoma":"OK",
"Oregon":"OR",
"Pennsylvania":"PA",
"Rhode Island":"RI",
"South Carolina":"SC",
"South Dakota":"SD",
"Tennessee":"TN",
"Texas":"TX",
"Utah":"UT",
"Vermon":"VT",
"Virginia":"VA",
"Washington":"WA",
"West Virginia":"WV",
"Wisconsin":"WI",
"Wyoming":"WY",
"Washington, DC":"DC",
"United States":"US",
"PR":"Others",
"Work at Home":"Others",
"Home Based":"Others"
}

# changing area name
areas={
"Apple":"Tech",
"Google":"Tech",
"Microsoft":"Tech",
"Facebook":"Tech",
"Oracle":"Tech",
"Intel":"Tech",
"IBM":"Tech",
"Wells Fargo":"Finance",
"JPMorgan Chase":"Finance",
"Visa":"Finance",
"Bank of America":"Finance",
"HSBC":"Finance",
"Citi":"Finance",
"MasterCard":"Finance",
"Nestle Toll House Cafe by Chip":"Consumer Goods",
"Nestl__ Nutrition":"Consumer Goods",
"P&G":"Consumer Goods",
"CocaCola":"Consumer Goods",
"Coca-Cola":"Consumer Goods",
"Great Plains Coca-Cola":"Consumer Goods",
"Anheuser-Busch":"Consumer Goods",
"Anheuser-Busch-Metal Container Corporation":"Consumer Goods",
"Toyota":"Consumer Goods",
"Samsung":"Consumer Goods",
"Philips":"Consumer Goods",
"Johnson":"Consumer Goods",
"Novartis":"Health Care",
"Pfizer":"Health Care",
"Merck":"Health Care",
"Gilead Sciences":"Health Care",
"UnitedHealth":"Health Care",
"Amgen":"Health Care",
"Amazon":"Consumer Services",
"Walmart":"Consumer Services",
"The Home Depot":"Consumer Services",
"The Walt Disney":"Consumer Services",
"Comcast":"Consumer Services",
"COMCAST":"Consumer Services",
"CVS Health":"Consumer Services",
"McDonalds":"Consumer Services",
"McDonald":"Consumer Services",
"Mcdonald's":"Consumer Services",
"Exxon Mobil":"Oil&Gas",
"Shell":"Oil&Gas",
"Chevron":"Oil&Gas",
"BP":"Oil&Gas",
"Schlumberger":"Oil&Gas",
"ConocoPhilips":"Oil&Gas",
"AT&T":"Telecommunications",
"Verizon":"Telecommunications",
"Vodafone":"Telecommunications",
"General Electric":"industrials",
"3M":"industrials",
"UNITED PARCEL SERVICE":"industrials",
"Honeywell":"industrials",
"BOEING":"industrials",
}

# import scrapped data from excel
workbook=xlrd.open_workbook("sourcedata.xls")
worksheet=workbook.sheet_by_index(0)
num_rows=worksheet.nrows
num_cols=worksheet.ncols
print(num_rows)
print(num_cols)

locDic={}
for i in range(1,num_rows):
    # pass if it passed 30 days
    days= worksheet.cell_value(i,6)
    if "30" in days:
        continue


    # find location
    loc= worksheet.cell_value(i, 5)
    stateKeys= states.keys()
    for state in stateKeys:

        # convert a state to abbreviation
        abbreviation= states[state]
        if(abbreviation in loc):
            loc= abbreviation
            break
        if(state in loc):
            loc= states[state]
            break
    # end of location

    # find area
    area=worksheet.cell_value(i,2)
    areaKeys= areas.keys()
    for anarea in areaKeys:
        if(anarea in area):
            area= areas[anarea]
            break

    if loc not in locDic:
        locDic[loc]= {"Tech":0, "Finance":0, "Consumer Goods":0, "Health Care":0, "Consumer Services":0, "Oil&Gas":0, "Telecommunications":0, "industrials":0} 
    subDic= locDic[loc]
    if area not in subDic:
        subDic[area]=1
    else:
        subDic[area]=subDic[area]+1

# print the result
        
workbookW= xlwt.Workbook(encoding="UTF-8")
worksheetW= workbookW.add_sheet("test")

locKeys= locDic.keys()
row=0

for akey in locKeys:
    subDic= locDic[akey]
    Tnum= subDic["Tech"]
    Fnum= subDic["Finance"]
    CGnum= subDic["Consumer Goods"]
    Hnum= subDic["Health Care"]
    CSnum= subDic["Consumer Services"]
    Onum= subDic["Oil&Gas"]
    TELEnum= subDic["Telecommunications"]
    Inum= subDic["industrials"]
    print("%10s, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" % (akey, Tnum, Fnum, CGnum, Hnum, CSnum, Onum, TELEnum, Inum))

    worksheetW.write(row, 0, akey)
    worksheetW.write(row, 1, Tnum)
    worksheetW.write(row, 2, Fnum)
    worksheetW.write(row, 3, CGnum)
    worksheetW.write(row, 4, Hnum)
    worksheetW.write(row, 5, CSnum)
    worksheetW.write(row, 6, Onum)
    worksheetW.write(row, 7, TELEnum)
    worksheetW.write(row, 8, Inum)
    row=row+1

workbookW.save("byindustryarea_result_jmlee.csv")
print("alldone")
