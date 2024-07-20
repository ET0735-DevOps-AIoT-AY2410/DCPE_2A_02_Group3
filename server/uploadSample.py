import requests
stuff=[
  {
    "name": "Apple",
    "price": "$1",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShunsUsdt_BYBr2f0Hpv-h2MDig1Lo1aEzUA&s"
  },
  {
    "name": "Bananas",
    "price": "$5",
    "img": "https://www.bobtailfruit.co.uk/media/mageplaza/blog/post/4/2/42e9as7nataai4a6jcufwg.jpeg"
  },
  {
    "name": "Tomatoes(1kg)",
    "price": "$1.50",
    "img": "https://upload.wikimedia.org/wikipedia/commons/8/89/Tomato_je.jpg"
  },
  {
    "name": "Cauliflower",
    "price": "$4",
    "img": "https://domf5oio6qrcr.cloudfront.net/medialibrary/5299/h1018g16207257715328.jpg"
  },
  {
    "name": "Rice(1kg)",
    "price": "$6",
    "img": "https://s.alicdn.com/@sc04/kf/A536d1011573a4ad8bba92eb2314bfeceI.png_300x300.jpghttps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1rR-UgbdnqKIFuUATEsgLPdB1Efz-jNPu3A&s"
  },
  {
    "name": "Cabbage",
    "price": "$1",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQltKav52elm05u-AJbm4fw4jyJNtCBaWrxuA&s"
  },
  {
    "name": "Beetroot",
    "price": "$2",
    "img": "https://lyofood.com/cdn/shop/articles/LYOFOOD-freeze-dried-organic-beetroot-powders-EU-01.jpg?v=1490710701"
  },
  {
    "name": "Capsicum",
    "price": "$2",
    "img": "https://seed2plant.in/cdn/shop/products/greencapsicum.jpg?v=1606107907"
  },
  {
    "name": "Tamarind(500g)",
    "price": "$3",
    "img": "https://bigshopper.juzapps.com/image/cache/catalog/grocery/Gemini%20sp%20Tamarind%20500g-700x700.jpg"
  },
  {
    "name": "Ginger",
    "price": "$2",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSj4xZt2T3bEhrF7lzSzG8ft7qUx-hVgjwLjw&s"
  },
  {
    "name": "Salmon(300g)",
    "price": "$20",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMzIE3cGhzdADTMtYDLTH-zEarnjGZoJHGYQ&s"
  },
  {
    "name": "Chicken(1kg)",
    "price": "$10",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpaxtLsEs9Y5ZWYp-ecV-ztZAtRNlBhL2myA&s"
  },
  {
    "name": "Prawns(1kg)",
    "price": "$12",
    "img": "https://costi.com.au/cdn/shop/files/0A4A5385.jpg?v=1686629196"
  },
  {
    "name": "Eggs(1pkt of 10)",
    "price": "$3",
    "img": "https://cdn.britannica.com/94/151894-050-F72A5317/Brown-eggs.jpg"
  },
  {
    "name": "Milk(2ltr)",
    "price": "$5",
    "img": "https://www.heritagefoods.in/blog/wp-content/uploads/2020/12/shutterstock_539045662.jpg"
  },
  {
    "name": "Yogurt",
    "price": "$3",
    "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Turkish_strained_yogurt.jpg/220px-Turkish_strained_yogurt.jpg"
  },
  {
    "name": "Corn",
    "price": "$2.50",
    "img": "https://s30386.pcdn.co/wp-content/uploads/2019/08/FreshCorn_HNL1309_ts135846041.jpg.optimal.jpg"
  },
  {
    "name": "Carrots(3px)",
    "price": "$2",
    "img": "https://www.freshpoint.com/wp-content/uploads/commodity-carrot.jpg"
  },
  {
    "name": "Watermelon(medium)",
    "price": "$4",
    "img": "https://blog-images-1.pharmeasy.in/2020/08/28152823/shutterstock_583745164-1.jpg"
  },
  {
    "name": "Longans(500g)",
    "price": "$4.50",
    "img": "https://static.onecms.io/wp-content/uploads/sites/19/2018/08/13/longan.jpg"
  },
  {
    "name": "Durian(1kg)",
    "price": "$6.50",
    "img": "https://www.foodie.com/img/gallery/what-is-durian-and-how-do-you-eat-it/l-intro-1703105258.jpg"
  },
  {
    "name": "Brinjal(1kg)",
    "price": "$4",
    "img": "https://seed2plant.in/cdn/shop/products/violetbrinjalseeds.jpg?v=1603436778"
  },
  {
    "name": "Papaya(medium)",
    "price": "$7",
    "img": "https://www.healthxchange.sg/sites/hexassets/Assets/food-nutrition/papaya-health-benefits.jpg"
  },
  {
    "name": "Cherry(500g)",
    "price": "$6",
    "img": "https://cdn.britannica.com/60/174560-050-5A33606F/cherries-Cluster.jpg"
  },
  {
    "name": "Maggie noodles(1kg)",
    "price": "$1.50",
    "img": "https://media.nedigital.sg/fairprice/fpol/media/images/product/XL/13039423_XL1_20220629.jpg"
  },
  {
    "name": "Brown Rice(2kg)",
    "price": "$11",
    "img": "https://media.nedigital.sg/fairprice/fpol/media/images/product/XL/11698846_XL1_20220405.jpg?w=1200&q=70"
  },
  {
    "name": "Cashew nuts(1kg)",
    "price": "$18",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnrTKxABfRV_DqtKO0DxBDr0UZMFn-1iGoog&s"
  },
  {
    "name": "Almonds(1kg)",
    "price": "$21",
    "img": "https://www.shutterstock.com/image-photo/group-almonds-isolated-on-white-260nw-353214818.jpg"
  },
  {
    "name": "Cucumber",
    "price": "$3",
    "img": "https://t4.ftcdn.net/jpg/02/67/76/39/360_F_267763934_k5iD6W5kVqVouviBbggj7oXBIKUt9MTj.jpg"
  },
  {
    "name": "Pears(500g)",
    "price": "$5",
    "img": "https://www.shutterstock.com/image-photo/pear-isolated-on-white-260nw-62158969.jpg"
  },
  {
    "name": "Tomatoes(indivudal)",
    "price": "$0.50",
    "img": "https://t4.ftcdn.net/jpg/05/37/04/61/360_F_537046123_s8JVn2NrClPQDOryhSm8jonYZPfIzPRX.jpg"
  },
  {
    "name": "Black Pepper(100g)",
    "price": "$2",
    "img": "https://assets.clevelandclinic.org/transform/65ddb397-7835-4b21-b30b-d123be3cb5c8/blackPepper-185067429-770x533-1_jpg"
  },
  {
    "name": "Cinamon sticks(100g)",
    "price": "$1.50",
    "img": "https://t4.ftcdn.net/jpg/00/68/59/21/360_F_68592144_S3FKn9bOGS5b6mGPfdKhkhtrvKFbzHjH.jpg"
  },
  {
    "name": "Cardemon(100g)",
    "price": "$1.50",
    "img": "https://t4.ftcdn.net/jpg/00/55/21/41/360_F_55214174_1lv6vosMKaps20lnyKVH01hsetlXJIFA.jpg"
  },
  {
    "name": "Pomogrenate",
    "price": "$3",
    "img": "https://t3.ftcdn.net/jpg/02/41/79/66/360_F_241796635_n8mD5j88GU4e6fgdyK65jceEZKvvydzc.jpg"
  },
  {
    "name": "Blueberry(100g)",
    "price": "$3",
    "img": "https://www.freshpoint.com/wp-content/uploads/commodity-blueberry.jpg"
  },
  {
    "name": "Strawberry(400g)",
    "price": "$11.50",
    "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Strawberries.jpg/1280px-Strawberries.jpg"
  },
  {
    "name": "Blackberry(400g)",
    "price": "$10",
    "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Blackberry_fruit.jpg/1907px-Blackberry_fruit.jpg"
  },
  {
    "name": "Cramberry(400g)",
    "price": "$12",
    "img": "https://www.shutterstock.com/image-photo/cranberry-leaves-isolated-on-white-600nw-560888800.jpg"
  }
]
for item in stuff:
	paramss={
		"Name": item['name'],
		"Quantity": 100,
		"Price":float(item['price'][1:]),
		"ImageUrl":item['img']	
	}
	print(requests.post("http://localhost:5000/newproduct", params=paramss))
