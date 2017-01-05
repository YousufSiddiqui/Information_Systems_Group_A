# reading external csv for market cap onto a data frame
market_cap= read.csv("marketcap_data.csv", as.is=T,header=F,sep=",")
names(market_cap)= c("company_name","market_cap")

#deleting columns with NA values
market_cap = market_cap[, colSums(is.na(market_cap)) != nrow(market_cap)]

#writing job posting per company into a separate dataframe
job_postings = data.frame(table(data$company_name))
names(job_postings)= c("company_name","no.of_jobs")

#Merging the two data frames to give one with market cap and job posts
correlation_data = merge(market_cap,job_postings,by="company_name")

########Company Co-Relation######

#Converting currencies to numeric values
install.packages("lucr")
library(lucr)

correlation_data$market_cap = from_currency(correlation_data$market_cap,
                                            decimal_delim = ".")
##Pearson Correlation
cor(correlation_data$market_cap,correlation_data$no.of_jobs)
cor.test(correlation_data$market_cap,correlation_data$no.of_jobs)

##Spearman Correlation
cor.test(rank(correlation_data$market_cap),rank(correlation_data$no.of_jobs),method = "spearman",exact = FALSE )

##Kendall Correlation
cor.test(rank(correlation_data$market_cap),rank(correlation_data$no.of_jobs),method = "kendall",exact = FALSE)

