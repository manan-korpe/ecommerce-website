var productListContainer = document.querySelector(".blog");
var defaultOrder = Array.from(productListContainer.children);

console.log(productListContainer);
console.log(defaultOrder);

function sortProducts() {
    console.log("Sorting products");
    var sortOption = document.getElementById('sort').value;

    // Sorting logic based on the selected option
   if (sortOption === 'name') {
        console.log("Sorting by name");
        sortByName();
    } else if (sortOption === 'nameZtoA') {
        console.log("Sorting by name");
        sortByNameZtoA();
    } else {
        console.log("Default sorting");
        // Default sorting
        resetOrder();
    }
}


function sortByName() {
    console.log("Sorting by name");
    var sortedList = Array.from(productListContainer.children)
        .sort((a, b) => a.querySelector('.blog-text h4').innerText.localeCompare(b.querySelector('.blog-text h4').innerText));

    updateProductList(sortedList);
}

function sortByNameZtoA() {
    console.log("Sorting by name");
    var sortedList = Array.from(productListContainer.children)
        .sort((a, b) => b.querySelector('.blog-text h4').innerText.localeCompare(a.querySelector('.blog-text h4').innerText));

    updateProductList(sortedList);
}

function resetOrder() {
    console.log("Resetting order");
    updateProductList(defaultOrder);
}

function updateProductList(newOrder) {
    console.log("Updating product list");
    newOrder.forEach(item => productListContainer.appendChild(item));
}