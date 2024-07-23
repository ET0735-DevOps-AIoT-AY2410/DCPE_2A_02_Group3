function setup(){
    document.getElementById('date').textContent=(new Date()).toLocaleDateString('en-US',{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
}