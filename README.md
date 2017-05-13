# python_crawler
### 1.Introduction
* Idea
	* 1.Yahoo store (https://tw.buy.yahoo.com/) has 337 kind of products, each category has their own hotest product, so I use crawler to get the no.1 product's information (category, name, priice, original price, discount) from the webpage.
	* 2.After got these product, we can sort these products ascend by the discount and export to csv file. 
	* 3.We can analysis according to the chart generated by **draw_product_discount.ipynb**. 
* files
	* 1.**yahoo_buy_crawler.py** is python crawler for e-commerce in order to analysis what kind of product was popular, this scrpt can generate the popular product list for each category.
	* 2.**draw_product_discount.ipynb** generate the diagram from crawled data.

### 2.Limitation 
* 1.Need Yahoo's account, password.
* 2.Need connected to internet before execute **yahoo_buy_crawler.py**.
### 3.Environment preparation
* Something you need to install before execute **yahoo_buy_crawler.py**:
	* 1.Python 2.7
		* please refer to the website: https://www.python.org/download/releases/2.7/
	* 2.requests
		* pip install requests

	* 3.BeautifulSoup4 
		* pip install beautifulsoup4
* Something you need to install before execute **draw_product_discount.ipynb**:
	* 1.Ipython notebook
		* Install Anaconda: https://www.continuum.io/downloads
		* Refer some introduction: https://jenhsuan.gitbooks.io/python/content/chapter-2build-develope-environment/23jupyteripython-notebook/231introduction.html 
	
					
### 4.Functions and usage
* yahoo_buy_crawler.py:
	* 1.python yahoo_buy_crawler.py -h
	* 2.User can specify a number and get the top few products list which was sorted ascend by the discount.  
