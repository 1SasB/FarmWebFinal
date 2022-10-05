console.log("Inside CHeckout")

var url =  $('#checkout-form').attr('action');

$("#paySpons-btn").on('click',function(){
    $.ajax({
        method: 'post',
        url: url,
        cache: false,
        contentType: false,
        processData: false,

        beforeSend: function(){
            console.log("about to send")
            // spinnerBox.classList.add('visible')
        },
        success: function(response){
            if(response.message){
                if(response.message == "Success"){
                    window.location = "/finance"
                }
            }
            return false;
        },
        error: function(error){
            console.log(error)
        },
    });
})

    