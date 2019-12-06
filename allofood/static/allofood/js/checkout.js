var form = $("form");
form.validate({
  rules: {
    numerotelephone: {
      required: true,
      minlength: 8,
      maxlength: 10,
      number: true
    },
    commandpasss: {
      required: true,
      minlength: 8
    },
    Adresse: {
      required: true,
      minlength: 4
    }
  },
  messages: {
    numerotelephone:    "<p>Veuillez spécifier un numéro de téléphone valide</p>",
    commandpasss:  "<p>Veuillez entrer un mot de passe avec au moins 8 caractères</p>",
    Adresse:   "<p>Veuillez insérer votre adresse</p>"
  }
});
