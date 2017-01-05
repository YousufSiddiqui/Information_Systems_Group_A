# reading external csv for market cap (industry) onto a data frame
market_cap_industry= read.csv("marketcap_data_industry.csv", as.is=T,header=F,sep=",")
names(market_cap_industry)= c("industry_type","market_cap")

#deleting columns with NA values
market_cap_industry = market_cap_industry[, colSums(is.na(market_cap_industry)) != nrow(market_cap_industry)]

#writing job posting per industry into a separate dataframe

#Saving Variables
industry_type = c('IT','Finance','Consumer','Health',
                  'Services','OilandGas','Telecom','Industrial')
industry_posts = c(nrow(IT),nrow(Finance),nrow(Consumer),nrow(Health),nrow(Services),nrow(OilandGas),nrow(Telecom),nrow(Industrial))

#Writing onto dataframe
job_postings_industry = data.frame(industry_type,industry_posts)

#Merging the two data frames to give one with market cap and job posts (industry)
correlation_data_industry = merge(market_cap_industry,job_postings_industry,by="industry_type")


#Converting currencies to numeric values
install.packages("lucr")
library(lucr)

correlation_data_industry$market_cap = from_currency(correlation_data_industry$market_cap,
                                            decimal_delim = ".")

########Industry Co-Relation######

cor(correlation_data_industry$market_cap,correlation_data_industry$industry_posts)


##Spearman Correlation
cor.test(rank(correlation_data_industry$market_cap),rank(correlation_data_industry$industry_posts),method = "spearman")

##Kendall Correlation
cor.test(rank(correlation_data_industry$market_cap),rank(correlation_data_industry$industry_posts),method = "kendall")


