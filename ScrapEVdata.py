from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

response = requests.get("https://www.zigwheels.com/newbikes/electric-bikes")
soup = bs(response.content, 'html.parser')
 
model_div = soup.findAll('li', attrs= {'class', 'modelItem'})

# Getting links from anchor tag and storing it as a list
ev_vehical_links=[]

for vehicle in model_div:
    all_a = vehicle.find_all('a')
    link = all_a[1]['href'] + '/specifications'
    if "price" in link:
        continue
    ev_vehical_links.append(all_a[1]['href'] + '/specifications')

# Creating dataframe for data
df = pd.DataFrame()

how =0
for ev in ev_vehical_links:
    response = requests.get(ev)
    soup = bs(response.content, 'html.parser')


    val_div = soup.findAll('div',attrs = {'class', 'read-more'})
    label_span = soup.findAll('span', attrs = {'class', 'pull-left'})



    val_dict1 = {}
    for i in range(0,len(val_div)-2):
        try:
            val_dict1[label_span[i +1].text] = val_div[i].div.text.strip("\n \t")  
        except:
            print('Error at {} on {}'.format(i,ev))
        

    # Getting price and Adding it to dict
    price = soup.find_all('span', attrs ={'class','vChangePrice'})
    price = price[0].text.strip()

    if '-' in price:
        temp = price.split('-')
        temp= temp[1].strip('Lakh')
        if "," in temp :
            temp1 = temp.split(",")
            temp =int(temp1[0]+temp1[1])/100000
        price = int(float(temp)*100000)
    elif 'Lakh' in price:
        temp = price.strip(' Rs. Lakh .00')
        price = int(float(temp)*100000)
    else:
        price = price.strip('Rs.')

    val_dict1['Price'] = price
    
    df = df.append(val_dict1, ignore_index = True)
    
    how = how+1
    print("{} completed {}".format(how,ev))
    
print('Dataframe creation is completed')

df.to_csv('~/Desktop/scrap_data.csv',index=False)

    