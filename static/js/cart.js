var updateBtns = document.getElementsByClassName('update-cart')

for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var shopId = this.dataset.shop
        var productId = this.dataset.product
        var itemId = this.dataset.item
        var action = this.dataset.action

        if (user === 'AnonymousUser') {
            if (action === 'add') {
                console.log('Not logged in')
            } else {
                console.log('Not logged in')
            }
        } else {
            if (action === 'add') {
                addOrderProduct(shopId, productId, action)
            } else if (action === 'increase') {
                editQuantity(shopId, productId, itemId, action)
            } else if (action === 'decrease') {
                editQuantity(shopId, productId, itemId, action)
            } else {
                console.log('Remove')
            }
        }
    })
}

function addOrderProduct(shopId, productId, action) {
    console.log('User is logged in, sending data...')

    var form = $('form').serializeArray()
    var url = '/shop/orders/shops/' + String(shopId) + '/products/' + String(productId) + '/add/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken, 
        },
        body: JSON.stringify({'form':form, 'shopId':shopId, 'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) => {
        // location.reload()
        console.log("data: ", data)
    })
}

function editQuantity(shopId, productId, itemId, action) {
    console.log('User is logged in, editing product...')

    var url = '/shop/orders/shops/' + String(shopId) + '/products/' + String(productId) + '/edit/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken, 
        },
        body: JSON.stringify({'itemId':itemId, 'shopId':shopId, 'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) => {
        location.reload()
        console.log("data: ", data)
    })
}