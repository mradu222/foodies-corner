$('form').validate({
  rules: {
    newpassword: {
      required: true,
      minlength: 8
    },
    conpassword: {
      required: true,
      equalTo: "#newpassword"
    }
  },
  messages: {
    newpassword: "<p style='color:red;'>Veuillez entrer un mot de passe avec au moins 8 caractères</p>",
    conpassword: "<p style='color:red;'>les mots de passe ne correspondent pas</p>"
  }
});
