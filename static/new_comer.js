function new_comer(email) {

    email = email || document.getElementById('reg_email').value;

    var url = "/new-comers-gift";
    // var url = "https://cpn-manager.herokuapp.com/new-comers-gift";
    var method = "POST";
    var postData = JSON.stringify({email: email});
    var shouldBeAsync = true;

    var request = new XMLHttpRequest();
    request.onload = function () {

       var status = request.status; // HTTP response status, e.g., 200 for "200 OK"
       var data = request.responseText; // Returned data, e.g., an HTML document.
    }

    request.open(method, url, shouldBeAsync);

    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Access-Control-Allow-Credentials", true);
    request.setRequestHeader("Access-Control-Allow-Origin", "https://cpn-manager.herokuapp.com/new-comers-gift");
    request.send(postData);

    // $.ajax({ 
    //     url: "/new-comers-gift",
    //     data: { email: email },
    //     method: "POST",
    //     success: function(data) {
    //         alert(data);
    //         console.log("Proceed to submitting the form");
    //     }
    //  });

    return true;
}
var reg = document.getElementsByClassName('woocommerce-form woocommerce-form-register register')
for ( var i = 0; i < reg.length; i++ ){
    reg[i].onsubmit = new_comer;
}
// reg.onsubmit = new_comer;