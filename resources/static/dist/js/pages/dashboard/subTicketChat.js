function UpdateChat() {
    var vstrChoice = 2;
    var vstrTicketID = document.getElementById("ticket_id").value;
    var vstrThreadID = document.getElementById("thread_id").value;
    var vstrUserID = document.getElementById("uid").value;


    var dataString = "&vstrChoice=" + vstrChoice + '&vstrTicketID=' + vstrTicketID +
        '&vstrThreadID=' + vstrThreadID + '&vstrUserID=' + vstrUserID;
    $.ajax({
        type: "post",
        url: "/dashboard/tickets",
        data: dataString,
        cache: false,
      success: function(data){
        $('#TicketSystemINFDIV').html(data)
      }
    });
}
// TODO- Note it might be easier to just implement push notifications as this methods uses up resources
