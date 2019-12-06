$(function(){
				$(document).on('click', '.chan', function (e) {
					e.preventDefault();
					$(this).parent().children("p").css("display","none");
					$(this).css("display","none");
					$(this).parent().children("input").css("display","");
				});

jQuery.validator.addMethod("alphanumeric", function(value, element) {
	return this.optional(element) || /^\w+$/i.test(value);
}, "Letters, numbers, and underscores only please");
$('#contact').validate({
  rules: {
    firstname: {
      required: true,
      minlength: 3,
      alphanumeric: true
    },
    lastname: {
      required: true,
      minlength: 3,
      alphanumeric: true
    },
    numtel: {
      required: true,
      minlength: 8,
      maxlength: 10,
      number: true
    },
    conpassword: {
      required: true,
      minlength: 8
    },
    address: {
      required: true,
    }
  },
  messages: {
    firstname: "<p style=\"color:red;\">Veuillez préciser votre prénom (seules les lettres et numéros sont autorisés)</p>",
    lastname:  "<p style=\"color:red;\">Veuillez préciser votre nom de famille (seules les lettres sont autorisés)</p>",
    numtel:    "<p style=\"color:red;\">Veuillez spécifier un numéro de téléphone valide</p>",
    conpassword:"<p style=\"color:red;\">Veuillez entrer un mot de passe avec au moins 8 caractères</p>",
    address:   "<p style=\"color:red;\">Veuillez insérer votre adresse</p>"
  }
});



});
