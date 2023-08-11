var allPasswordInp = [];

(function() {

  $("input[type=password]").each(function(idx, ele) {
    allPasswordInp.push(ele)
  })

  routie({
    '': function() {
      showProgress()
      $("#passwordDiv").addClass("scale-out")
      $(".formTitle").html("Sign In")
      /* Show Login Form */
      $("#formContainer").removeClass("goLeft").addClass("goRight")

    },

    'hasPassword': function() {
      showProgress()
      $("#passwordDiv").addClass("pulse").removeClass("scale-out")
      $(".loginNextBtn").addClass("hide")
      $(".loginBtn").removeClass("hide")
    },


    'createAccountNow': function() {
      $(".formTitle").html("Sign Up")
      showProgress()
      /* Show Signup Form */
      $("#formContainer").removeClass("goRight").addClass("goLeft")
    }
  });

})()

function showProgress() {
  $("#progress-bar").removeClass("hidden")
  setTimeout(function() {
    $("#progress-bar").addClass("hidden")
  }, 500)
}

function showPassword() {
  var iconText = $(".showPassword i").text();
  var input_type = (iconText == "visibility") ? "text" : "password";

  if(input_type == "text") {
    $(".showPassword i").text("visibility_off");
  }else{
    $(".showPassword i").text("visibility");
  }

  $.each(allPasswordInp, function(idx, ele) {
    $(ele).attr("type", input_type);
  })
}






function validate() {
  var validationField = document.getElementById('validation-txt');
  var password = document.getElementById('reg_pass_word');
  var password2 = document.getElementById("re_pass_word")
  var regBtn = document.getElementById("reg__btn")

  var content = password.value;
  var content2 = password2.value;
  var errors = [];

  console.log(content);
  console.log(content2);

  console.log(content);
  if (content.length < 8) {
    errors.push("Your password must be at least 8 characters");
    regBtn.classList.add("gray-out")
  } else {
    regBtn.classList.remove("gray-out")
  }


  if (content2 !== content && content !== content2) {
    errors.push("Password does not match");
    regBtn.classList.add("gray-out")

  }else {
    regBtn.classList.remove("gray-out")
  }

  if (content.search(/[a-z]/i) < 0) {
    errors.push("Your password must contain at least one letter.");
    regBtn.classList.add("gray-out")

  } else {
    regBtn.classList.remove("gray-out")
  }



  if (content.search(/[0-9]/i) < 0) {
    errors.push("Your password must contain at least one digit.");
    regBtn.classList.add("gray-out")

  }else {
    regBtn.classList.remove("gray-out")
  }
  if (errors.length > 0) {
    validationField.innerHTML = errors.join('');

    return false;
  }
  validationField.innerHTML = errors.join('');
  return true;

}