var updateBtns = document.getElementsByClassName('update-cart')
var cookieQty = $('#id_quantity')

for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var shopId = this.dataset.shop
        var productId = this.dataset.product
        var itemId = this.dataset.item
        var action = this.dataset.action

        if (action === 'add') {
            addOrderProduct(shopId, productId, action)
        } else if (action === 'increase' || action === 'decrease') {
            editOrderProduct(shopId, productId, itemId, action)
        } else {
            console.log('Remove')
        }
    })
}

function addOrderProduct(shopId, productId, action) {
    console.log('User is logged in, sending data...')
    var form = $('form').serializeArray()
    var url = '/shops/' + String(shopId) + '/products/' + String(productId) + '/add/'
    var next_url = '/shops/' + String(shopId) + '/products/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken, 
        },
        body: JSON.stringify({'form':form, 'shopId':shopId, 'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.text()
    })

    .then((data) => {
        console.log("data: ", data)
        setTimeout(function() {
            window.location.href = next_url
        }, 2000)
    })
}

function editOrderProduct(shopId, productId, itemId, action) {
    console.log('User is logged in, editing product...')

    var url = '/shops/' + String(shopId) + '/products/' + String(productId) + '/update/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken, 
        },
        body: JSON.stringify({'itemId':itemId, 'shopId':shopId, 'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.text()
    })
    .then((data) => {
        location.reload()
        console.log("data: ", data)
    })
}