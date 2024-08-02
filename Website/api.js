export default class Api
{
	constructor(baseurl)
	{
		this.baseurl=baseurl
		this.headers={
			"Access-Control-Allow-Origin":"*",
			'Accept': 'application/json',
		        'Content-Type': 'application/json'
		}

	}
	
	
	async getProducts(){
		if(localStorage.getItem("timeCreated")==null){
			localStorage.setItem("timeCreated",new Date().getTime()+1000000000)
		}
		if (new Date().getTime() + 100000> parseInt(localStorage.getItem("timeCreated"))){
			return JSON.parse(localStorage.getItem("data"))
		}
		const res=fetch(`${this.baseurl}/products`,{method:"GET",headers:this.headers})
			.then(response =>
			{
			if (response.ok){
				let jso=response.json()
				
				return jso;
			}else {throw new Error("Is the backend running?")}
			}).then(response=>{

				localStorage.setItem("timeCreated",new Date().getTime())
				localStorage.setItem("data",JSON.stringify(response))

				return response
			})
		return res 
	}
	async createProducts(name,amt){
		const res=fetch(`${this.baseurl}/newproduct?Name=${name}&Quantity=${amt}`,{method:"POST",headers:this.headers})
			.then(response =>
			{
			if (response.ok){
				return response.json();
			}
			else {throw new Error("Is the backend running?")}
			})
		return res 
	}
	async editProducts(id, quantity){
		const res=fetch(`${this.baseurl}/products?id=${id}&Quantity=${quantity}`,{method:"PUT",headers:this.headers})
			.then(response => 
			{
			if (response.ok){
				return true;}
			else {throw new Error("Is the backend running?")}
			})
		return res 
	}
	async getOrders(){
		const res=fetch(`${this.baseurl}/orders`,{method:"GET",headers:this.headers})
			.then(response =>{
			if (response.ok){return response.json();}
			else {throw new Error("Is the backend running?")}
			})
		return res 
	}
	async createOrders(deliver, items){
		const data={
		    "Deliver":deliver,
		    "Items":items
		}
		const res=fetch(`${this.baseurl}/orders`,{method:"POST",headers:this.headers, body: JSON.stringify(data)})
			.then(response =>{
			if (response.ok){return response.json();}
			else {throw new Error("Is the backend running?")}
			})
		return res 
	}
	async collectedOrder(id){
		const res=fetch(`${this.baseurl}/collected/${id}`,{method:"GET",headers:this.headers})
			.then(response =>{
			if (response.ok){return true;}
			else {throw new Error("Is the backend running?")}
			})
		return res 
	}
	async paidOrder(id){
		const res=fetch(`${this.baseurl}/paid/${id}`,{method:"GET",headers:this.headers})
			.then(response =>{
			if (response.ok){return true;}
			else {throw new Error("Is the backend running?")}
			})
		return res 
	}
}

