#! /usr/bin/python3
#kira
from bs4 import BeautifulSoup
import requests
from termcolor import colored
import pandas as pd 
#headers that will allow the access
global headers
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip', 
    'DNT' : '1', # Do Not Track Request Header 
    'Connection' : 'close'
    }
#global upc
global urls
urls=[]
global rate
rate=[]
global upc_value
upc_value=[]
global amazon_truth
amazon_truth=False
def outer(name):#function that will scrape link of product that we search from name
    prd_name=[]
    source=requests.get(f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={name}&_sacat=0',headers=headers)
    soup=BeautifulSoup(source.text,'lxml')
    links=soup.find_all('a',class_='s-item__link')
    for link in links:
        urls.append(link.get('href'))
    prices=soup.find_all('span',class_='s-item__price')
    for price in prices:
        
        char='$ to $'
        price=price.text.replace(char,'')
        price=price.strip('$').split()
        #price=price.strip('$')
        price=float(price[0])
        rate.append(price)
    names=soup.find_all('h3',class_='s-item__title')
    for name in names:
        name=name.text.strip()
        prd_name.append(name)
    data={
        "LINK":urls,
        'PRICE':rate,
        'NAME':prd_name
    }
    ebay_df=pd.DataFrame.from_dict(data, orient='index')
    ebay_df=ebay_df.transpose()
    ebay_df1=ebay_df.dropna(subset=['NAME'])
    a=ebay_df1['PRICE'].values.tolist()
    small=min(a)
    c=[]
    for x in a:
        if x==small:
            c.append(True)
        else:
            c.append(False)
    check=pd.Series(c)
    df=ebay_df1[check]
    main_url=df["LINK"].str.replace("['']"," ").values
    main_price=df["PRICE"].values
    return main_price,main_url
    #at the end it will append the links to the our list
def ebay(price_1,url_2,name):#the inner function is for get more detail about the project 
    print('$$ Searching for product on EBAY')
    
    for url in urls:
        source=requests.get(url,headers=headers)
        soup=BeautifulSoup(source.text, 'lxml')
        upc=soup.find('h2',{'itemprop':"gtin13"}) #finding upc code
        if upc=='Does not apply'or upc=='does not apply'or upc==None:
            pass
        else:
            upc=upc.text.strip()
            upc_value.append(upc)
    
    #print(upc_value)
    #printing all the required value
    print("--------------------------------------------")
    print(colored('Product_link:','yellow'),url_2[0])
    print(colored('Product_Name:','yellow'),name)
    print(colored('Product_price:$','yellow'),price_1[0])
    #print(colored('Product_UPC:','yellow'),upc)
    print("--------------------------------------------")


def amazon(value,product_name):#sraching for the product on amazon
    
    #print(upc)
    global amazon_truth
    url=[]
    name_1=[]
    price_1=[]
    source=requests.get(f'https://www.amazon.com/s?k={value}&ref=nb_sb_noss',headers=headers)
    #print(source.status_code)
    if source.content!='Not found':
        #source=requests.get(f'https://www.amazon.com/s?k={product_name}&ref=nb_sb_noss',headers=headers)

        soup=BeautifulSoup(source.text,'lxml')
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
        for link in links:
            link=link.get('href')
            main_link=f'https://www.amazon.com'+link
            url.append(main_link)
        names=soup.find_all('a',class_='a-link-normal a-text-normal')
        for name in names:
            name=name.text.strip()
            name_1.append(name)
        for new in name_1:
            if new==product_name:
                continue
            else:
                pass
        #print(nam)
        prices=soup.find_all('span',class_='a-offscreen')
        for price in prices:
            price=price.text.strip('$')
            price=float(price)
            price_1.append(price)
        data={
            'NAME':name_1,
            'PRICE':price_1,
            'LINK':url
        }
        amazon_df=pd.DataFrame.from_dict(data, orient='index')
        amazon_df=amazon_df.transpose()
        amazon_df1=amazon_df.dropna(subset=['LINK'])
        amazon_df1=amazon_df.dropna(subset=['PRICE'])
        #print(amazon_df1)
        nw=amazon_df1.empty
        if nw:
            pass
        else:
            a=amazon_df1['PRICE'].values.tolist()
            small=min(a)
            if small==0.0:
                pass
            else:
                print('$$ Searching for product on AMAZON')
                amazon_truth=True
                c=[]
                for x in a:
                    if x==small:
                        c.append(True)
                    else:
                        c.append(False)
                check=pd.Series(c)
                df=amazon_df1[check]
                print("--------------------------------------------")
                print(colored('Product_link:','yellow'), df["LINK"].str.replace("['']"," ").values)
                print(colored('Product_Name:','yellow'), df["NAME"].str.replace("['']"," ").values)
                print(colored('Product_price:$','yellow'), df["PRICE"].values)
                #print(colored('Product_UPC:','yellow'),upc)
                print("--------------------------------------------")
    return amazon_truth
#driver code
if __name__ == "__main__":
    #i/p as prodct name
    name=input('Enter the name:')#change here
    print(colored(name,'red'))
    #print('\n')
    main_price,main_url=outer(name)
    ebay(main_price,main_url,name)
    #urls.clear()#clearing the list in order to get rid of previous link
    #i=1
    #print(len(upc_value))
    for y in upc_value:
        #print(i)
        if y=='Does not apply':
            #print('skip')
            pass
            #my=amazon(name,name)   
        else:
            #print('nor')
            truth=amazon(y,name)
            if truth==True:
                break 
    last=input('Are u satsified with amazon result(yess/no)')
    if last=='no':
        a=amazon(name,name)
    else:
        print('thanks for using')