var form = $("form");
jQuery.validator.addMethod("alphanumeric", function(value, element) {
	return this.optional(element) || /^\w+$/i.test(value);
}, "Letters, numbers, and underscores only please");
form.validate({
  rules: {
    email: {
      required: true,
      email: true
    },
    subject: {
      required: true,
      minlength: 3
    },
    message: {
      required: true,
      minlength: 8
    }
  },
  messages: {
    email:     "<p>Veuillez spécifier une adresse e-mail valide</p>",
    subject:    "<p>Veuillez spécifier un sujet</p>",
    message:  "<p>Veuillez écrire un méssage</p>"
  }
});
