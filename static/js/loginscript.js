$("form[name=signup_form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/daftarakun";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=login_form").submit(function(e) {
    
    var $form = $(this);
    // this is error variable to send text if there is an error
    var $error = $form.find(".error");
    // this is a data object that gets all of the fields from the form, bundles them up so we can send them off to our back-end (user/signup route)
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=userupdate_form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/update",
        type: "PATCH",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/editprofile";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=userupdate_specific_form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/update/specific",
        type: "PATCH",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/daftarakun";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=password_form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/update/password",
        type: "PATCH",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.reload();
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=user_password_form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/admin/update/changepassword",
        type: "PATCH",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/daftarakun";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

function del(ID, name){
    if (confirm("Apakah anda yakin ingin menghapus user '" + name + "'")){
        window.location.href = '/delete/user/' + ID;
    }
}

function update(ID){
    window.location.href = '/daftarakun/' + ID;
}