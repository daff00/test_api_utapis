$("form[name=newsinput_form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    tinyMCE.triggerSave();
    var data = $form.serialize();

    $.ajax({
        url: "/news/input",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/inputberita";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

//Berita admin
$("#saveBtn").click(function() {
    $("form[name=newsupdate_specific").click(function(e) {
    
        var $form = $(this);
        var $error = $form.find(".error");
        tinyMCE.triggerSave();
        var data = $form.serialize();
    
        $.ajax({
            url: "/news/update/specific/save",
            type: "PATCH",
            data: data,
            dataType: "json",
            success: function(resp) {
                window.location.href = "/daftarberita";
            },
            error: function(resp) {
                console.log(resp);
                $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
        });
    
        e.preventDefault();
    });
});

$("#reloadBtn").click(function() {
    $("form[name=newsupdate_specific").click(function(e) {
    
        var $form = $(this);
        var $error = $form.find(".error");
        tinyMCE.triggerSave();
        var data = $form.serialize();
        var ID = $(this).attr('itemid')

        $.ajax({
            url: "/news/update/specific",
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
});

//Berita editor riwayat
$("#saveBtnriwayat").click(function() {
    $("form[name=newsupdate_specific").click(function(e) {
    
        var $form = $(this);
        var $error = $form.find(".error");
        tinyMCE.triggerSave();
        var data = $form.serialize();
    
        $.ajax({
            url: "/news/update/specific/save",
            type: "PATCH",
            data: data,
            dataType: "json",
            success: function(resp) {
                window.location.href = "/riwayateditor";
            },
            error: function(resp) {
                console.log(resp);
                $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
        });
    
        e.preventDefault();
    });
});

$("#reloadBtnriwayat").click(function() {
    $("form[name=newsupdate_specific").click(function(e) {
    
        var $form = $(this);
        var $error = $form.find(".error");
        tinyMCE.triggerSave();
        var data = $form.serialize() ;
        var ID = $(this).attr('itemid')

        $.ajax({
            url: "/news/update/specific",
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
});

//Berita editor approval
$("#saveBtnapproval").click(function() {
    $("form[name=newsupdate_specific").click(function(e) {
    
        var $form = $(this);
        var $error = $form.find(".error");
        tinyMCE.triggerSave();
        var data = $form.serialize();
    
        $.ajax({
            url: "/news/update/specific/save",
            type: "PATCH",
            data: data,
            dataType: "json",
            success: function(resp) {
                window.location.href = "/riwayateditor";
            },
            error: function(resp) {
                console.log(resp);
                $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
        });
    
        e.preventDefault();
    });
});

$("#reloadBtnapproval").click(function() {
    $("form[name=newsupdate_specific").click(function(e) {
    
        var $form = $(this);
        var $error = $form.find(".error");
        tinyMCE.triggerSave();
        var data = $form.serialize();
        var ID = $(this).attr('itemid')

        $.ajax({
            url: "/news/update/specific",
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
});

function del(ID, title){
    if (confirm("Apakah anda yakin ingin menghapus berita '" + title + "'")){
        window.location.href = '/delete/news/' + ID;
    }
}

function update_news_admin(ID){
    window.location.href = '/daftarberita/' + ID;
}

function update_pending_news_editor(ID){
    window.location.href = '/approval/' + ID;
}

function view_news_reporter(ID){
    window.location.href = '/riwayatrep/' + ID;
}

function update_saved_news_editor(ID){
    window.location.href = '/riwayateditor/' + ID;
}