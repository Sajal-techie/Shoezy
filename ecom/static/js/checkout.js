$(document).ready(function (){

    $('.razor').click(function (e){
        e.preventDefault();
        var selectedValue = $('input[name="address"]:checked').val();
        var total_prize = $('input[name="total_prize"]').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

                var options = {
                    "key": "rzp_test_ja90f2UETSDOKd",
                    "amount": total_prize * 100, 
                    "currency": "INR",
                    "name": "Shoezy",
                    "description": "Thank you for buying from us ",
                    "image": "https://imgs.search.brave.com/EF6YntA6IJLW85LIWBz8pQfw5BpeNOdleik58EunoJs/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9keW5h/bWljLmJyYW5kY3Jv/d2QuY29tL2Fzc2V0/L2xvZ28vZjgzODFi/NjQtZGRmZC00MDI4/LWE3MDUtNDdkOTc3/ZGQzNzhhL2xvZ28t/c2VhcmNoLWdyaWQt/MXg_bG9nb1RlbXBs/YXRlVmVyc2lvbj0x/JnY9NjM4MzAxOTEz/Nzk5NDAwMDAw.jpeg",
        
                    "handler": function (response1){
                            if (response1.razorpay_payment_id){
                                $.ajax({
                                    method : 'POST',
                                    url: '/razor_pay/',
                                    data: {
                                        'address': selectedValue,
                                        csrfmiddlewaretoken:token

                                            },
                                    success : function (data){
                                        window.location.href = data.redirect_url  + data.order_id1;
                                }
                            });
                        }
                        else{
                            alert("payment failed")
                        }

                    },
                    "prefill": {
                        "name": 'name', 
                        "email": "sample123@gmail.com", 
                        "contact": 9876543219 , 
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                  var rzp1 = new Razorpay(options);
                rzp1.open();
       
    });
});