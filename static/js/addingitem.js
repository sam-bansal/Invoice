console.log('Hello world');

// constructor
function Item(description,quantity,rate){
    this.description = description;
    this.quantity = quantity;
    this.rate = rate;
}

function Display(){

}

// add methods to display prototype

Display.prototype.add = function (item,index) {
    console.log("Adding to UI");
    tableBody = document.getElementById('tableBody');
    let uiString = `<tr>
                        <th scope="row">1</th>
                        <td>${item.description}</td>
                        <td>${item.quantity}</td>
                        <td>${item.rate}</td>
                        <td> ${item.quantity} * ${item.rate} </td>
                    </tr>`;
    tableBody.innerHTML += uiString;
}

Display.prototype.clear = function(){
 let itemForm = document.getElementById('itemForm');
 itemForm.reset()
}


// add submit event listener to itemform

let itemForm = document.getElementById('itemForm');
itemForm.addEventListener('submit', itemFormSubmit);

function itemFormSubmit(e){
    console.log('You have submitted itemform');

    let quantity = document.getElementById('quantity').value;
    let rate = document.getElementById('rate').value;
    let description = document.getElementById('description').value;


    let item = new Item(description, quantity, rate);
    console.log(item);

    let display = new Display();
    display.add(item);
    display.clear();

    e.preventDefault();

}
