var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId', productId, 'action', action);
        console.log('user:', user);

        if (user === "AnonymousUser") {
            console.log('User is not logged in');
            alert('Bạn cần đăng nhập để thực hiện hành động này.');
        } else {
            console.log('user logged in, success add');
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('data added');
        console.log('data', data);
        
        // Reload the page to reflect the updated cart
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error)
    })
}
