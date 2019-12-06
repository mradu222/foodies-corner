jQuery(document).ready(function($){
	//if you change this breakpoint in the style.css file (or _layout.scss if you use SASS), don't forget to update this value as well
	var $L = 1200,
		$menu_navigation = $('#main-nav'),
		$cart_trigger = $('#cd-cart-trigger'),
		$hamburger_icon = $('#cd-hamburger-menu'),
		$lateral_cart = $('#cd-cart'),
		$shadow_layer = $('#cd-shadow-layer');
		var flech = $(".flech");
         var form = $(".connecter");
         //var popupDiv = $(".sign-up");
         var arriereplan = $(".arriere-plan");
         var status =false;
         var sinscrire = false;
         var problem = false;

         //sign in 
     $("#login").click(function(event)
         {
           event.preventDefault();
           if(status == false)
           {
            flech.fadeIn();
            form.fadeIn();
            status = true;
            $("body").on('click','.page',function(event)
                {
                      flech.fadeOut();
                      form.fadeOut();
                      status = false;
               })
             /*$("#buttons").click(function(event)
                {
                  event.preventDefault();
                
                  popupDiv.fadeIn();
                  arriereplan.fadeIn();
                  flech.fadeOut();
                  form.fadeOut();
                  status = false;
                    
                  $("#closes").click(function(event)
                  {
                    event.preventDefault();
                     popupDiv.fadeOut();
                     arriereplan.fadeOut();
                  })  
                   
            })*/
           }
           else
           {
            flech.fadeOut();
            form.fadeOut();
            status = false;
           }
         })
      $("#sedeconnecter").click(function(event)
         {
           event.preventDefault();
           if(status == false)
           {
            flech.fadeIn();
            form.fadeIn();
            status = true;
            $("body").on('click','.page',function(event)
                {
                      flech.fadeOut();
                      form.fadeOut();
                      status = false;
					 
					  
               })
             /*$("#buttons").click(function(event)
                {
                  event.preventDefault();
                
                  popupDiv.fadeIn();
                  arriereplan.fadeIn();
                  flech.fadeOut();
                  form.fadeOut();
                  status = false;
                    
                  $("#closes").click(function(event)
                  {
                    event.preventDefault();
                     popupDiv.fadeOut();
                     arriereplan.fadeOut();
                  })  
                   
            })*/
           }
           else
           {
            flech.fadeOut();
            form.fadeOut();
            status = false;
           }
         })
	//open lateral menu on mobile
	$("#login").click(function(event){
		event.preventDefault();
		//close cart panel (if it's open)
	$lateral_cart.removeClass('speed-in');
		toggle_panel_visibility($menu_navigation, $shadow_layer, $('body'));
	});

  $("body").on('click','.page',function(event)
           {
             //event.preventDefault();        
		 			$lateral_cart.removeClass('speed-in');
		 			if( problem == true){
		             toggle_panel_visibility($menu_navigation, $shadow_layer, $('body')); 
		 			}					  
               })
	//open cart
	$cart_trigger.on('click', function(event){
		event.preventDefault();
		//close lateral menu (if it's open)
		if(status == true)
    {
      flech.fadeOut();
            form.fadeOut();
            status = false;
    }
		toggle_panel_visibility($lateral_cart, $shadow_layer, $('body'));
	});

	//close lateral cart or lateral menu
	$shadow_layer.on('click', function(){
		$lateral_cart.removeClass('speed-in');
		$menu_navigation.removeClass('speed-in');
		$shadow_layer.removeClass('is-visible');
		$('body').removeClass('overflow-hidden');
	});

	//move #main-navigation inside header on laptop
	//insert #main-navigation after header on mobile
	move_navigation( $menu_navigation, $L);
	$(window).on('resize', function(){
		move_navigation( $menu_navigation, $L);

		if( $(window).width() >= $L && $menu_navigation.hasClass('speed-in')) {
			$menu_navigation.removeClass('speed-in');
			$shadow_layer.removeClass('is-visible');
			$('body').removeClass('overflow-hidden');
		}

	});
});

function toggle_panel_visibility ($lateral_panel, $background_layer, $body) {
	if( $lateral_panel.hasClass('speed-in') ) {
		$lateral_panel.removeClass('speed-in');
		$background_layer.removeClass('is-visible');
		$body.removeClass('overflow-hidden');
	    problem = true;
	} else {
		$lateral_panel.addClass('speed-in');
		$background_layer.addClass('is-visible');
		$body.addClass('overflow-hidden');
	    problem = false;
	}
}

function move_navigation( $navigation, $MQ) {
	if ( $(window).width() >= $MQ ) {
		$navigation.detach();
		$navigation.appendTo('header');
	} else {
		$navigation.detach();
		$navigation.insertAfter('header');
	}
}
