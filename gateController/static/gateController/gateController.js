$( document ).ready(function() {
    $( "#vh_acc_btn" ).prop( "disabled", true );
    $( "#ped_acc_btn" ).prop( "disabled", true );
    $( "#svg_locked").show();
    $( "#svg_unlocked").hide();
    $('#svg_unlocked').removeAttr('hidden');
});

function unlockClicked(){
    $( "#vh_acc_btn" ).prop( "disabled", false );
    $( "#ped_acc_btn" ).prop( "disabled", false );
    $( "#svg_locked").hide();
    $( "#svg_unlocked").show();

    setTimeout(function(){ 
        $( "#vh_acc_btn" ).prop( "disabled", true );
        $( "#ped_acc_btn" ).prop( "disabled", true );
        $( "#svg_locked").show();
        $( "#svg_unlocked").hide();
    }, 1000);
}

function vehAccClicked(){
    $( "#vh_acc_btn" ).prop( "disabled", true );
    $( "#ped_acc_btn" ).prop( "disabled", true );
    $( "#svg_locked").show();
    $( "#svg_unlocked").hide();
}

function pedAccClicked(){
    $( "#vh_acc_btn" ).prop( "disabled", true );
    $( "#ped_acc_btn" ).prop( "disabled", true );
    $( "#svg_locked").show();
    $( "#svg_unlocked").hide();
}