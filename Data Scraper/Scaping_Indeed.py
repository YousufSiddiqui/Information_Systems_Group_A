# load the library
from bs4 import BeautifulSoup as Soup
import urllib, requests, re, pandas as pd
import ssl
import urllib2

pd.set_option('max_colwidth',500) #remove column limit
df = pd.DataFrame() #create a new data frame

def extractFromUrl(aurl, adf, elevel):
    global df
    count=1
    prev_comp_name=""
    prev_job_title=""
    prev_job_addr=""
    

    for page in range(1,201):
        page1 = (page-1) * 10
        urlstr= aurl+ "&start=%d" % page1 + "&limit=100"
        print(urlstr)

        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        target=""
        try:
            uopen=  urllib2.urlopen(urlstr, context=gcontext, timeout=2000);
            target = Soup(uopen, "lxml")        
        except urllib2.URLError, e:
            print("urlopen")
            break;

        targetElements = target.findAll('div', attrs={'class' : ' row result'})
        x = target.findAll('div', attrs={'class' : 'lastRow row result'})
        targetElements= targetElements+x

        # get individual job information
        if(len(targetElements) == 0):
            break;

        isfirst=1
        for elem in targetElements:
            comp_name = elem.find('span', attrs={'itemprop':'name'}).getText().strip()
            job_title = elem.find('a', attrs={'class':'turnstileLink'}).attrs['title']
            home_url = "http://www.indeed.com"
            job_addr = elem.find('span', attrs={'itemprop':'addressLocality'}).getText()
            job_posted = elem.find('span', attrs={'class': 'date'}).getText()


            if(isfirst == 1):
                if(prev_comp_name == comp_name and prev_job_title == job_title and prev_job_addr == job_addr):
                    isfirst= 3
                    break;
                prev_comp_name= comp_name
                prev_job_title= job_title
                prev_job_addr= job_addr
                isfirst= 2
                
            comp_link_overall = elem.find('span', attrs={'itemprop':'name'}).find('a')
            if comp_link_overall != None:
                comp_link_overall = "%s%s" % (home_url, comp_link_overall.attrs['href'])
            else: comp_link_overall = None

        # Data Frame
            print("count=%d     (%s, %s, %s)" % (count, comp_name, job_title, job_addr))
            count += 1

            df=df.append({'comp_name': comp_name, 'job_title': job_title, 'job_posted': job_posted, 'overall_link': comp_link_overall, 'job_location': job_addr, 'exp_level': elevel, 'overall_rating': None, 'wl_bal_rating': None, 'benefit_rating': None, 'jsecurity_rating': None, 'mgmt_rating': None, 'culture_rating': None }, ignore_index=True)
        if(isfirst == 3):
            break

        
    print("exit the first loop")

# get a detailed company information from the job link 
def convertDf(adf):
    df_received = adf
# get all the company details
    for i in range(0,len(df_received)):
        target_comp_name = df_received.iloc[i]['comp_name']
        url_2nd = adf.iloc[i]['overall_link']

        if url_2nd != None:
            target_2nd = Soup(urllib.urlopen(url_2nd), "lxml")
            comp_logo = target_2nd.find("div", {"id": "cmp-header-logo"}).find('img')

        if comp_logo != None:
            comp_logo = target_2nd.find("div", {"id": "cmp-header-logo"}).find('img').attrs['src']
        else: comp_logo = None

    df_received=adf
    df_received.to_csv('/Users/jmlee/Documents/1220.csv', encoding='utf-8')


# all the urls
urls=[
"https://www.indeed.com/jobs?q=company%3Aapple&l=United+States&rbc=Apple&jcid=c1099851e9794854",
"https://www.indeed.com/jobs?q=company%3Agoogle&l=United+States&rbc=Google&jcid=a5b4499d9e91a5c6",
"https://www.indeed.com/jobs?q=microsoft&l=United+States&rbc=Microsoft&jcid=734cb5a01ee60f80",
"https://www.indeed.com/jobs?q=company%3Afacebook&l=United+States&rbc=Facebook&jcid=1639254ea84748b5",
"https://www.indeed.com/jobs?q=oracle&l=United+States&rbc=Oracle&jcid=cd22d01053af7669",
"https://www.indeed.com/jobs?q=intel&l=United+States&rbc=Intel&jcid=f1374be6a45f4b8a",
"https://www.indeed.com/jobs?q=IBM&l=United+States&rbc=IBM&jcid=de71a49b535e21cb",
"https://www.indeed.com/jobs?q=Wells+Fargo+%26+Co&l=United+States&rbc=Wells+Fargo&jcid=78bbcd26e39621f5",
"https://www.indeed.com/jobs?q=JPMorgan+chase&l=United+States&rbc=JPMorgan+Chase&jcid=c46d0116f6e69eae",
"https://www.indeed.com/jobs?q=visa&l=United+States&rbc=Visa&jcid=a3f737e511d9fc8c&fromage=15",
"https://www.indeed.com/jobs?q=bank+of+america&l=United+States&rbc=Bank+Of+America&jcid=5bd99dfa21c8a490",
"https://www.indeed.com/jobs?q=HSBC&l=United+States&rbc=HSBC&jcid=04c9b139c84ea1b5",
"https://www.indeed.com/jobs?q=citigroup&l=United+States&rbc=Citi&jcid=5bcd1ef0a7f4fb99",
"https://www.indeed.com/jobs?q=mastercard&l=United+States&rbc=MasterCard&jcid=10b5c722d846df43",
"https://www.indeed.com/jobs?q=Nestle&l=United+States&rbc=Nestl%C3%A9+Nutrition&jcid=88267c567629bb56",
"https://www.indeed.com/jobs?q=Procter+%26+Gamble+Co&l=United+States&rbc=P%26G&jcid=ea6f370a3068f3db",
"https://www.indeed.com/jobs?q=The+Coca-Cola&l=United+States&rbc=CocaCola&jcid=0fe83faa4435898d",
"https://www.indeed.com/jobs?q=Anheuser-Busch+InBev&l=United+States&rbc=Anheuser-Busch&jcid=84c67dd9d990e840",
"https://www.indeed.com/jobs?q=Toyota&l=United+States&rbc=Toyota&jcid=90f0cbc4a30f8dba",
"https://www.indeed.com/jobs?q=samsung&l=United+States&rbc=Samsung&jcid=4c8f1cd901f84ca7",
"https://www.indeed.com/jobs?q=philips&l=United+States&rbc=Philips&jcid=e4af9ca5b6d3a604",
"https://www.indeed.com/jobs?q=Johnson+%26+Johnson&l=United+States&rbc=Johnson+%26+Johnson+Vision+Care,+Inc.&jcid=90d4817fd1263bc2",
"https://www.indeed.com/jobs?q=Novartis+Pharmaceuticals&l=United+States&rbc=Novartis+Pharmaceuticals&jcid=07382f9068cf892f",
"https://www.indeed.com/jobs?q=Pfizer&l=United+States&rbc=Pfizer+Inc.&jcid=5e118f74384e090a",
"https://www.indeed.com/jobs?q=Merck+%26+Co&l=United+States&rbc=Merck&jcid=c38b7d5e0419a6a7",
"https://www.indeed.com/jobs?q=Gilead+Sciences&l=United+States&rbc=Gilead+Sciences&jcid=e4b075354d7c2865",
"https://www.indeed.com/jobs?q=UnitedHealth+Group&l=United+States&rbc=UnitedHealth+Group&jcid=d3d3520998346837",
"https://www.indeed.com/jobs?q=Amgen&l=United+States&rbc=Amgen&jcid=ec34037a9c92d805",
"https://www.indeed.com/jobs?q=amazon&l=United+States&rbc=Amazon+Corporate+LLC&jcid=db9f9b9d28743c59",
"https://www.indeed.com/jobs?q=Wal-Mart&l=United+States&rbc=Walmart&jcid=822bc5d9a49270ea",
"https://www.indeed.com/jobs?q=Home+Depot&l=United+States&rbc=The+Home+Depot&jcid=82e58e9861d48566",
"https://www.indeed.com/jobs?q=Walt+Disney&l=United+States&rbc=The+Walt+Disney+Company&jcid=4ed80f3a97849f22",
"https://www.indeed.com/jobs?q=Comcast&l=United+States&rbc=Comcast&jcid=ea25315ee9da22e5",
"https://www.indeed.com/jobs?q=CVS+Health&l=United+States&rbc=CVS+Health&jcid=1419e52fd7c725ce",
"https://www.indeed.com/jobs?q=McDonald%27s&l=United+States&rbc=McDonald%27s&jcid=f753bb1a40104d82",
"https://www.indeed.com/jobs?q=Exxon+Mobil&l=United+States&rbc=Exxon+Mobil&jcid=7ca80c512850c9cd",
"https://www.indeed.com/jobs?q=Royal+Dutch+Shell&l=United+States&rbc=Shell&jcid=167aa4ca2fe7d8e6",
"https://www.indeed.com/jobs?q=Chevron&l=United+States&rbc=Chevron+Stations+Inc.&jcid=852e0296771df99f",
"https://www.indeed.com/jobs?q=BP&l=United+States&rbc=BP&jcid=03cacc905f5db444",
"https://www.indeed.com/jobs?q=Schlumberger&l=United+States&rbc=Schlumberger&jcid=1a6c05c38b3b5549",
"https://www.indeed.com/jobs?q=ConocoPhillips&l=United+States&rbc=ConocoPhillips&jcid=b1022d646fa0c95b",
"https://www.indeed.com/jobs?q=AT%26T&l=United+States&rbc=AT%26T&jcid=25b5166547bbf543",
"https://www.indeed.com/jobs?q=Verizon+Communications&l=United+States&rbc=Verizon&jcid=f7029f63fe5c906e",
"https://www.indeed.com/jobs?q=Vodafone&l=United+States&rbc=Vodafone&jcid=374d720d3973ca1c",
"https://www.indeed.com/jobs?q=General+Electric&l=United+States&rbc=General+Electric&jcid=0f2ee88943b9e35b",
"https://www.indeed.com/jobs?q=3m&l=United+States&rbc=3M&jcid=595d42593839d3a2",
"https://www.indeed.com/jobs?q=United+Parcel+Service&l=United+States&rbc=UNITED+PARCEL+SERVICE&jcid=3a37758dda1e2ff7",
"https://www.indeed.com/jobs?q=Siemens+AG&l=United+States&rbc=Siemens&jcid=ea6bb53f0b18b8f2",
"https://www.indeed.com/jobs?q=Honeywell+International&l=United+States&rbc=Honeywell&jcid=50208b5bf45ee3b8",
"https://www.indeed.com/jobs?q=The+Boeing+Company&l=United+States&rbc=BOEING&jcid=edae4285faf6c2f0"

]


explevel=["entry_level", "mid_level", "senior_level"]
#explevel=["senior_level"]

for url in urls:
    for level in explevel:
        alevel= "&explvl=%s" % level
        aurl= url + alevel

        extractFromUrl(aurl, df, level)
        print(len(df))

#convertDf(df)    
df_received = df
print(len(df_received))

#save as csv
df_received=df
df_received.to_csv('/Users/jmlee/Documents/1220.csv', encoding='utf-8')
