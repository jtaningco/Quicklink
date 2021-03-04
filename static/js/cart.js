var updateBtns = document.getElementsByClassName('update-cart')

for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var shopId = this.dataset.shop
        var productId = this.dataset.product
        var action = this.dataset.action

        if (user === 'AnonymousUser') {
            console.log('Not logged in')
        } else {
            updateUserOrder(shopId, productId, action)
        }
    })
}

function updateUserOrder(shopId, productId, action) {
    console.log('User is logged in, sending data...')

    var form = $('form').serializeArray()
    var url = '/shops/' + String(shopId) + '/products/' + String(productId) + '/add/'

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