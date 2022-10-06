//floating icons start
// document.querySelector('.fab').addEventListener('click', function(e) {
//     document.querySelector('.box').classList.toggle('box-active');
//     document.querySelector('.fab').classList.toggle('fab-active');
// });
//floating icons end
//owl carousel-start
// $('.owl-carousel').owlCarousel({
//     loop: true,
//     margin: 10,
//     autoplay: true,
//     navSpeed: 1000,
//     smartSpeed: 800,
//     autoplayTimeout: 2000,
//     autoplayHoverPause: true,
//     responsive: {
//         0: {
//             items: 1
//         },
//         800: {
//             items: 2
//         },
//         1000: {
//             items: 3
//         }
//     }

// });

//owl carousel-end

//show calculator
$(document).ready(function() {
    $(".show-calculator").click(function() {
        $(".calculator").slideDown("slow");
        $(".show-calculator").addClass('hide')
    });
});
//hide calculator

$(document).ready(function() {
    $(".hide-calculator").click(function() {
        $(".calculator").slideUp("slow");
    });
});

function openNav(value) {
    document.getElementById("myNav").style.display = "block";
}
  
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}

ros_arr = []

function unit_ch(value){
    if(!value){
        value = 1
    }
    ross = ros_arr
    console.log(ross)
    const cost_per_unit = $("#cost_per_unit_hidden").text()
    
    const cost_of_production_per_unit = value * parseFloat(cost_per_unit)
    const service_charge = 0.1 * cost_of_production_per_unit
    const total_pay = cost_of_production_per_unit + service_charge

    const initial_ros = (ross[0]/100) * total_pay
    const last_ros = (ross[1]/100) * total_pay

    $("#rosGHC").html(initial_ros+ " - " + last_ros)
    $("#unit_number").html(value +" Unit(s)")
    $("#cost_per_unit").html(cost_of_production_per_unit)
    $("#total_payable").html("GH&#8373;"+total_pay)
    $('#total_amount').val(total_pay)
    console.log("unit changed",value)
}



function get_ros(ros){
    var ar = ros.split("%-%")

    const initial = parseInt(ar[0])
    const last = parseInt(ar[1])

    ar = [initial,last]
    return ar
}

function get_new_farm_data(farm_value){
    console.log(farm_value)
    $.ajax({
        method: 'get',
        url: '/get_farmdetails/'+farm_value+'/',
        // data: JSON.stringify({'farm_id': farm_value}),
        cache: false,
        contentType: "application/json",

        beforeSend: function(){
            console.log("about to send")
            document.getElementById("myNav").style.display = "block";
        },
        success: function(response){
            console.log(response.message)
            if(response.message == 'Success'){
                $("#unit_number").html(1)
                $("#cost_per_unit_hidden").text(response.data.cost_per_unit)
                $('#total_cost_per_unit').val(response.data.cost_per_unit)
                ross = get_ros(response.data.ROS)
                ros_arr = ross
                $('#total_ROS').val(response.data.ROS)
                $('input[name=crop_type]').val(response.data.product)
                unit_ch(1,ross)
                document.getElementById("myNav").style.display = "none";
            }
            else{
                $("#alert-box").hide();
                $("#alert-box2").html("Couldnt retrieve data");
                $("#alert-box2").show();
            }
        },
        error: function(error){
            console.log(error)
        },
    });
}