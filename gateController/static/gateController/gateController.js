$(document).ready(function () {
    $(window).on("orientationchange",function(){
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
}

function pedAccClicked() {
    $("#vh_acc_btn").prop("disabled", true);
    $("#ped_acc_btn").prop("disabled", true);
    $("#svg_locked").show();
    $("#svg_unlocked").hide();
}