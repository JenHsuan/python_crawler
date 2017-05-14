# python_crawler
### 1.Introduction
* Idea
	* 1.Yahoo store (https://tw.buy.yahoo.com/) has 337 kind of products, each category has their own hotest product, so I use crawler to get the no.1 product's information (category, name, priice, original price, discount) from the webpage.
	* 2.After got these product, we can sort these products ascend by the discount and export to csv file. 
	* 3.We can analysis according to the chart generated by **draw_product_discount.ipynb**. 
* files
	* 1.**yahoo_buy_crawler.py** is python crawler for e-commerce in order to analysis what kind of product was popular, this scrpt can generate the popular product list for each **category to product_list.csv**.
	* 2.**draw_product_discount.ipynb** generate the diagram from crawled data.

### 2.Limitation 
* 1.Need Yahoo's account, password, you will be not allowed to get some category's information (such as 情趣專區) if you provide incorrect account and password.
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
	* 1.python yahoo_buy_crawler.py -h: help
	<img width="562" alt="2017-05-13 8 58 01" src="https://cloud.githubusercontent.com/assets/13972975/26025652/df8818ae-381e-11e7-9357-8dca212b853c.png">
	
        * --
	* 2.python yahoo_buy_crawler.py <mail> <passowrd>: start to crawl
	<img width="606" alt="2017-05-13 11 11 21" src="https://cloud.githubusercontent.com/assets/13972975/26026645/c2e19e10-3831-11e7-8d4f-24de5e22b2c1.png">
	
* draw_product_discount.ipynb
	* 1.start ipython notebook
	* 2.run draw_product_discount.ipynb
	![figure_1](https://cloud.githubusercontent.com/assets/13972975/26025717/36dd0adc-3820-11e7-92e6-22ce358dec61.png)
### 5.Analysis
* We can know that the top 20 category or brand were almost apparel or cloth brand form **product_list.csv**
<img width="758" alt="2017-05-13 9 12 50" src="https://cloud.githubusercontent.com/assets/13972975/26025758/0cdf00ae-3821-11e7-9cde-d78cf4837d42.png">

### 6.Challenge
* 1.因為無從得到使用者的喜好以及訂單資料, 現在是從官方所推薦的排行版第一名來抓取資料
* 2.有些頁面會被重新導到新的頁面, 因此在這些excecption的頁面時就必須使用不同的parse pattern
* 3.有些頁面會審核使用者是否有滿18歲, 因此必須自動登入並且確認已滿18歲, 才可以進去parse資料
* 4.常會抓取到重複的資料, 因此必須判斷並過濾掉有疑義的資料
