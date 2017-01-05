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

    # increse one for the level
    level= worksheet.cell_value(i, 4)
    if loc not in locDic:
        # if the location is new, initialize sub entry
        locDic[loc]= {"entry_level":0, "mid_level":0, "senior_level":0}
    subDic= locDic[loc]
    if level not in subDic:
        subDic[level]= 1
    else:
        subDic[level]= subDic[level]+1

# print the result   

workbookW= xlwt.Workbook(encoding="UTF-8")
worksheetW= workbookW.add_sheet("test")

locKeys= locDic.keys()
row=0

for akey in locKeys:
    subDic= locDic[akey]
    enum= subDic["entry_level"]
    mnum= subDic["mid_level"]
    snum= subDic["senior_level"]
    print("%10s, %5d, %5d, %5d" % (akey, enum, mnum, snum))

    worksheetW.write(row, 0, akey)
    worksheetW.write(row, 1, enum)
    worksheetW.write(row, 2, mnum)
    worksheetW.write(row, 3, snum)
    row= row+1

workbookW.save("bylevel_result_jmlee.csv")


