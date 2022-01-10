const cancelBtn = document.getElementsByClassName('cancel-order');

for (let i = 0; i < cancelBtn.length; i++) {
	cancelBtn[i].addEventListener('click', function(){
		var orderId = this.dataset.order
		var action = this.dataset.action
		console.log('orderId:', orderId, 'Action:', action)

		updateUserOrder(orderId, action)

	})
}

function updateUserOrder(orderId, action){

    const url = '/update-order/';

    fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'orderId':orderId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}