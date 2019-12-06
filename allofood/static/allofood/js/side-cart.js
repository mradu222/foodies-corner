$(function(){

function calculateTotalPrice(){
	var totalPrice = 0;
		$(".eachPrice").each(function (){
			var cenaEach = parseInt($(this).text());
			totalPrice+=cenaEach;
		});
		$(".cd-cart-total").html("<p>Prix total: <span>" + totalPrice + " DA</span></p>");
}
calculateTotalPrice();
				$(document).on('click', '.button-add', function () {
					var nameId = $(this).parent().children(".legend2n").children("h4").text().split(" ").join("-");
					var name = $(this).parent().children(".legend2n").children("h4").text();
					var price = parseInt($(this).parent().children(".prix2n").text().split(".",1).join());
					var itemsCount = parseInt($(".badge-panier").text());
					$(".badge-panier").text(++itemsCount);
					$.ajax({
							url: 'session.php?action=add',
							type: 'POST',
							data: {
									name1: name,
									price1: price,
									nameId1: nameId
							},
							success: function(msg) {
								$('.cd-cart-items').html(msg);
							}
					});
					var newTotal = parseInt($(".cd-cart-total").children().children().text()) + price;
					$(".cd-cart-total").html("<p>Prix total: <span>" + newTotal + " DA</span></p>");
				});

			$(document).on('click', '.cart-info.action', function () {
				var itemsCount = parseInt($(".badge-panier").text());
				var itemCount = $(this).parent().children(".cart-info.quantity").children("input").val();
				var newCount = itemsCount - parseInt(itemCount);
				var nameId = $(this).parent().attr('class');
				$.ajax({
	          url: 'session.php?action=delete',
	          type: 'POST',
	          data: {
								nameId1: nameId,
	          },
	          success: function(msg) {
	            $('.cd-cart-items').html(msg);
	          }
	      });
				$(".badge-panier").text(newCount);
				$(this).parent().remove();
		    calculateTotalPrice();

			});
			$(document).on('click', '.btn-increment', function () {
				var itemsCount = parseInt($(".badge-panier").text());
				var nameId = $(this).parent().parent().attr('class');
				$.ajax({
	          url: 'session.php?action=inc',
	          type: 'POST',
	          data: {
								nameId1: nameId
	          },
	          success: function(msg) {
	            $('.cd-cart-items').html(msg);
	          }
	      });
				var individualPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) / parseInt($(this).parent().children("input").val());
				var newPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) + individualPrice;
				$(this).parent().parent().children(".cart-info.price").children(".eachPrice").text(newPrice);
				$(".badge-panier").text(++itemsCount);
				calculateTotalPrice();
			});
			$(document).on('click', '.btn-decrement', function () {
				var itemsCount = parseInt($(".badge-panier").text());
				var oldQte = $(this).parent().children("input").val();
				if(oldQte == 1){
					$(this).parent().parent().children(".cart-info.action").trigger("click");
					return;
				}
				var nameId = $(this).parent().parent().attr('class');
				$.ajax({
	          url: 'session.php?action=dec',
	          type: 'POST',
	          data: {
								nameId1: nameId
	          },
	          success: function(msg) {
	            $('.cd-cart-items').html(msg);
	          }
	      });
				var individualPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) / parseInt($(this).parent().children("input").val());
				var newPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) - individualPrice;
				$(this).parent().parent().children(".cart-info.price").children(".eachPrice").text(newPrice);
				$(".badge-panier").text(--itemsCount);
				calculateTotalPrice();
			});

			setTimeout(function(){
			$(document).on('focus', '.input-quantity', function () {
    	$(this).attr('oldValue',parseInt($(this).val()));

        });});
				$(document).on('change', '.input-quantity', function () {
				var prev = parseInt($(this).attr('oldValue'));
				var current = parseInt($(this).val());
				if(current < 1)
				{
					alert('veuillez insérer une valeur positive');
					$(this).val(prev);
					return;
				}
				var nameId = $(this).parent().parent().attr('class');
				var individualPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) / prev;
				var price = individualPrice * current;
				var itemsCount = parseInt($(".badge-panier").text());
				var panier;
				if(current > prev){
					$(".badge-panier").text(itemsCount + (current - prev));
					panier = itemsCount + (current - prev);
					var individualPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) / prev;
					$(this).parent().parent().children(".cart-info.price").children(".eachPrice").text(price);
					calculateTotalPrice();
				}
				else{
					$(".badge-panier").text(itemsCount - (prev - current));
					panier = itemsCount - (prev - current);
					var individualPrice = parseInt($(this).parent().parent().children(".cart-info.price").children(".eachPrice").text()) / prev;
					$(this).parent().parent().children(".cart-info.price").children(".eachPrice").text(price);
					calculateTotalPrice();
				}
				$.ajax({
	          url: 'session.php?action=change',
	          type: 'POST',
	          data: {
								nameId1: nameId,
								price1: price,
								quantity1: current,
								panier1: panier
	          },
	          success: function(msg) {
	            $('.cd-cart-items').html(msg);
	          }
	      });
				$(this).attr('oldValue',current);
			});

});
