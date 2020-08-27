import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            print(request.form['content'])
            org_searchString = request.form['content']
            searchString=org_searchString.replace(" ", "%20")
            print(searchString)
            #searchString="plum face tone"
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            print(flipkart_url)
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_3O0U0u"})
            print(len(bigboxes))
            for kk in range(0, len(bigboxes)):
                #pass
                #print(bigboxes[kk])
                print(bigboxes[kk].div.div.a['href'])
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.a['href']
            print("product link is ",  productLink)
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            #print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            #print(commentboxes)
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            limit=0;
            for commentbox in commentboxes:
                name=rating=commentHead=comtag=None
                if limit==10:
                    break
                #pass
                print("new entry")
                #print(commentbox)
                try:
                    # name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('div', {'class': 'row _2pclJg'})[0].div.p.text
                    print("name is ",name)

                except:
                    check=commentbox.div.div.find_all('div', {'class': 'row _2pclJg'})[0].div
                    print("no name:" ,check)
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    rating = commentbox.find_all('div', {'class': 'hGSR34'})[0].text
                    print("rating is ", rating)


                except:
                    check=commentbox.find_all('div', {'class': 'hGSR34'})
                    print("no rating",check)
                    rating = 'No Rating'

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.find_all('p',{'class':'_2xg6Ul'})[0].text
                    print("comment is ",commentHead)

                except:
                    check = commentbox.div.div.div.div.p
                    print("no comment head",check)
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': 'qwjRop'})
                    # custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                    print("customer comment is ",custComment)
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Product": org_searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                reviews.append(mydict)
                limit=limit+1
            print(reviews)
            return render_template('results.html', reviews=reviews[0:(len(reviews))])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


#port = int(os.getenv("PORT"))
#print(os.getenv("PORT"))

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
