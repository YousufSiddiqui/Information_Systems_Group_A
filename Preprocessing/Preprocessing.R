library(data.table)

# Importing CSV in R
data_init=read.csv("1220.csv", as.is=T,header=F,sep=",")
names(data_init)

# Removing Unwanted Variables
data_init = subset(data_init, select = -c(V1,V2,V4,V9,V10,V11,V12,V13) )

# Changing name of variables 
names(data_init)= c("company_name","experience_level","location","posting_date","job_title")

#Deleting 1st row which contains column headers
data_init = data_init[ which(data_init$company_name != 'comp_name'),]

# Removing Job Postings older than 30 days
data= data_init[ which(data_init$posting_date!= '30+ days ago'),]

####Changing affiliate company names to main name####

#Identifying company names
unique(data$company_name)

#Nestle
data$company_name[data$company_name %like%"Nestl"] = "Nestle"

#Amazon
data$company_name[data$company_name %like% "Amazon"] = "Amazon"
data$company_name[data$company_name %like% "AMZN"] = "Amazon"

#McDonalds
data$company_name[data$company_name %like% "McDonald"] = "Mcdonalds"
data$company_name[data$company_name %like% "MCDONALD"] = "Mcdonalds"

#Johnson & Johnson
data$company_name[data$company_name %like% "Johnson & Johnson"] = "Johnson & Johnson"

#UPS
data$company_name[data$company_name %like% "United Parcel Services"] = "UPS"
data$company_name[data$company_name %like% "UNITED PARCEL SERVICE"] = "UPS"
data$company_name[data$company_name %like% "The UPS Store"] = "UPS"

#Microsoft
data$company_name[data$company_name %like% "Microsoft"] = "Microsoft"

#CocaCola
data$company_name[data$company_name %like% "Coca"] = "CocaCola"

#Anheuser-Busch
data$company_name[data$company_name %like% "Anheuser-Busch"] = "Anheuser-Busch"


# List all unique company names
unique(data$company_name)
#Removing space between company names
data$company_name = gsub(" ","",data$company_name)


# subseting data into smaller data sets according to company name
list_comp = split(data, data$company_name)
list2env(list_comp, envir= .GlobalEnv)

# aggregate data according to industry sector
IT = rbind(Apple,Google,Microsoft,Facebook,Oracle,Intel,IBM) 
Finance = rbind(WellsFargo,JPMorganChase,Visa,BankofAmerica,HSBC,Citi,MasterCard) 
Consumer = rbind(Nestle,`P&G`,CocaCola,`Anheuser-Busch`,Toyota,Samsung,Philips)
Health = rbind(`Johnson&Johnson`,NovartisPharmaceuticals,PfizerInc.,Merck,GileadSciences,UnitedHealthGroup,Amgen)
Services = rbind(Amazon,Walmart,TheHomeDepot,TheWaltDisneyCompany,Comcast,CVSHealth,Mcdonalds)
OilandGas = rbind(ExxonMobil,Shell,ChevronStationsInc.,BP,Schlumberger,ConocoPhillips)
Telecom = rbind(`AT&T`,Verizon,Vodafone)
Industrial = rbind(`3M`,UPS,Siemens,Honeywell,BOEING)
