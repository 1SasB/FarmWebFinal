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
            $("#alert-boxx").show();
            // spinnerBox.classList.add('visible')
        },
        success: function(response){
            if(response.message){
                if(response.message == "Success"){
                    $('#alert-boxx').html("PAYMENT SUCCESSFUL, redirecting ...")
                    window.location = "/finance"
                }
                else{
                    $("#alert-boxx").hide();
                    $("#alert-boxx1").show();
                }
            }
            return false;
        },
        error: function(error){
            console.log(error)
        },
    });
})

    