console.log("im in the homepage")



$("form#signup-form").submit(() => {
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var full_name = $('input[name="full-name"]').val();
    var email = $('input[name="email"]').val();
    var pass1 = $('input[name="password1"]').val();
    var pass2 = $('input[name="password2"]').val();
    console.log(csrf)
    console.log(full_name)
    console.log(email)
    console.log(pass1)
    console.log(pass2)

    if(pass1 !== pass2){
        alert("Your password do not match")
    }

    const fd = new FormData
    fd.append('name', full_name)
    fd.append('email', email)
    fd.append('password1', pass1)
    fd.append('password2', pass2)
    fd.append('csrfmiddlewaretoken', csrf)

    console.log(fd)

    console.log("here")    // Create Ajax Call
    $.ajax({
        method: 'post',
        url: '{% url "farm:signup_user" %}',
        enctype: 'multipart/form-data',
        data: fd,
        cache: false,
        contentType: false,
        processData: false,

        beforeSend: function(){
            console.log("about to send")
            // spinnerBox.classList.add('visible')
        },
        success: function(response){
            console.log(response.message)
            return false;
        },
        error: function(error){
            console.log(error)
        },
    });

    
});
