let timeout;
let socket;

const statuses = {
	CONNECTING: "connecting",
	OK: "ok",
	ERROR: "error",
}

$(document).ready(function () {
    $(window).on("orientationchange", function () {
        if ($(window).innerHeight() > $(window).innerWidth()) {
            $(".cust_col").removeClass("col-md-12").addClass("col-md-4");

        } else {
            $(".cust_col").removeClass("col-md-4").addClass("col-md-12");
        }
    });
    setLock(true)
    $('#svg_unlocked').removeAttr('hidden');   
    
    socket = initWebsocket();
});

function unlockClicked() {
    setLock(false)
    setTimeout(function () {
        setLock(true)
    }, 1000);
}

function vehAccClicked() {
    setLock(true)
    triggerGate("vehicle_access");
}

function pedAccClicked() {
    setLock(true)
    triggerGate("pedestrian_access");
}

function triggerGate(command) {
    socket.send(JSON.stringify({command}));
}

function setLock(locked){
    if(!locked){
        $("#vh_acc_btn").prop("disabled", false);
        $("#ped_acc_btn").prop("disabled", false);
        $("#svg_locked").hide();
        $("#svg_unlocked").show();
    } else {
        $("#vh_acc_btn").prop("disabled", true);
        $("#ped_acc_btn").prop("disabled", true);
        $("#svg_locked").show();
        $("#svg_unlocked").hide();
    }
}

function showStatusModal(status){
    switch(status){
        case statuses.CONNECTING:
            $(".bi-x").hide();
            $(".bi-check").hide();
            $(".bi-arrow-repeat").show();
            break
        case statuses.OK:
            $(".bi-x").hide();
            $(".bi-check").show();
            $(".bi-arrow-repeat").hide();
            break
        case statuses.ERROR:
            $(".bi-x").show();
            $(".bi-check").hide();
            $(".bi-arrow-repeat").hide();
            break  
    }
    $('#modal').modal();
}

function initWebsocket() {
    showStatusModal(statuses.CONNECTING)
    socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/'
    );

    socket.onopen = function() {
        $('#modal').modal('hide');
    }

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.result === 'gate_triggered'){
            showStatusModal(statuses.OK)
            setTimeout(()=>{$('#modal').modal('hide');}, 750);
        } else {
            showStatusModal(statuses.ERROR)
        }
    };

    socket.onclose = function(e) {
        socket = initWebsocket();
    };

    return socket;
}