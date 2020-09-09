import urllib.request
import re
import logging
import csv
import argparse
import datetime

                   
def downloadData(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.URLError as u:
        print("Reason: " + u.reason)
    except urllib.error.HTTPError as h:
        print("Reason" + h.reason)
    else:
        return html
        
def processData(html):
    
    csvfile=html.decode('utf-8')
    file = csvfile.strip().split("\n")
    reader = csv.reader(file)
    data = []

    for row in reader:
        row[1]=datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        data.append(row)
    return data


def imgHits(data):
    pattern = r'\.(jpeg|gif|png|jpg|JPG|PNG|GIF|JPEG)'
    count=0
    total=0
    for i in data:
        if(re.search(pattern,i[0])):
            count+=1
        total+=1
        
    perc=((count/total)*100)
    print("Image requests account for " + str(perc) +"% " + " of all requests")
    
def bHits(data):
    Ccount=0
    Fcount=0
    IEcount=0
    Scount=0
    
    for i in data:
        if(re.search(r'Chrome/[\d]{2}\.[\d]\.[\d]{4}\.[\d]',i[2])):
            Ccount+=1
        elif(re.search(r'Firefox/[\d]{2}\.[\d]',i[2])):
            Fcount+=1
        elif(re.search(r'MSIE [\d][\d]?\.?[\d]',i[2])):
            IEcount+=1
        elif(re.search(r'Version/[\d]\.[\d]\.?[\d]? (Safari/|Mobile/)', i[2])):
            Scount+=1
            
    mostPop=max(Ccount,Fcount,IEcount,Scount)
    browser=""
    
    if(mostPop==Ccount):
        browser="Chrome"
    elif(mostPop==Fcount):
        browser="Firefox"
    elif(mostPop==IEcount):
        browser="Internet Explorer"
    elif(mostPop==Scount):
        browser="Safari"
    
    print("The most popular browser for the day is " + browser)
    
def hHits(data):
    H=0
    count=0
  
    while(H<24):
        for i in data:
            if(i[1].hour==H):
                count+=1
        print("Hour " + str(H) + " has " + str(count) + " hits")
        count=0
        H+=1
    
 
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="URL needed")
    parser.add_argument("--url", help="The website name", type=str)
    args = parser.parse_args()

    csvData=downloadData("http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv")
    #csvData=downloadData(args.url)
    csvList = processData(csvData)
    imgHits(csvList)
    bHits(csvList)
    hHits(csvList)
    
    
    