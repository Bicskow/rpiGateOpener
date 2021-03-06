let timeout;

$(document).ready(function () {
    $(window).on("orientationchange", function () {
        if ($(window).innerHeight() > $(window).innerWidth()) {
            $(".cust_col").removeClass("col-md-12").addClass("col-md-4");

        } else {
            $(".cust_col").removeClass("col-md-4").addClass("col-md-12");
        }
    });
    $("#vh_acc_btn").prop("disabled", true);
    $("#ped_acc_btn").prop("disabled", true);
    $("#svg_locked").show();
    $("#svg_unlocked").hide();
    $('#svg_unlocked').removeAttr('hidden');   
});

function unlockClicked() {
    $("#vh_acc_btn").prop("disabled", false);
    $("#ped_acc_btn").prop("disabled", false);
    $("#svg_locked").hide();
    $("#svg_unlocked").show();

    setTimeout(function () {
        $("#vh_acc_btn").prop("disabled", true);
        $("#ped_acc_btn").prop("disabled", true);
        $("#svg_locked").show();
        $("#svg_unlocked").hide();
    }, 1000);
}

function vehAccClicked() {
    $("#vh_acc_btn").prop("disabled", true);
    $("#ped_acc_btn").prop("disabled", true);
    $("#svg_locked").show();
    $("#svg_unlocked").hide();
    triggerGate("vehicle_access");
}

function pedAccClicked() {
    $("#vh_acc_btn").prop("disabled", true);
    $("#ped_acc_btn").prop("disabled", true);
    $("#svg_locked").show();
    $("#svg_unlocked").hide();
    triggerGate("pedestrian_access");
}

function triggerGate(command) {
    let token = getCookie("csrftoken");
    $.ajax({
        url: "triggerGate",
        type: "POST",
        data: { csrfmiddlewaretoken: token, command: command },
        success: function (data) {
            $(".bi-x").hide();
            $(".bi-check").show();
            $('#modal').modal();
            setTimeout(()=>{$('#modal').modal('hide');}, 750);
        },
        error: function (jXHR, textStatus, errorThrown) {
            $(".bi-x").show();
            $(".bi-check").hide();
            $('#modal').modal();
            //alert(`There was an error communicating with the server: ${errorThrown}.`);
        }
    });
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}