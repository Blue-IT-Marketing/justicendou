

var thisSendMessageButt = document.getElementById("SendMessageButt");

thisSendMessageButt.addEventListener("click", function () {
                var vstrChoice = 0;
                var vstrComment = document.getElementById("comment").value;
                var vstrTicketID = document.getElementById("ticket_id").value;
                var vstrThreadID = document.getElementById("thread_id").value;
                var vstrUserID = document.getElementById("uid").value;
                var dataString = "&vstrChoice=" + vstrChoice + '&vstrComment=' + vstrComment + '&vstrTicketID=' + vstrTicketID +
                    '&vstrThreadID=' + vstrThreadID + '&vstrUserID=' + vstrUserID;
                $.ajax({
                    type: "post",
                    url: "/contact/tickets/" + vstrTicketID,
                    data: dataString,
                    cache: false,
                    success: function (data) {
                        $('#TicketSystemINFDIV').html(data);
                        document.getElementById("comment").value = "";
                    }
                });
            });

function UpdateChat() {
                var vstrChoice = 1;
                var vstrTicketID = document.getElementById("ticket_id").value;
                var vstrThreadID = document.getElementById("thread_id").value;
                var vstrUserID = document.getElementById("uid").value;

                var dataString = "&vstrChoice=" + vstrChoice + '&vstrTicketID=' + vstrTicketID +
                    '&vstrThreadID=' + vstrThreadID;
                $.ajax({
                    type: "post",
                    url: "/contact/tickets/" + vstrTicketID,
                    data: dataString,
                    cache: false,
                    success: function (data) {
                        $('#TicketSystemINFDIV').html(data)
                    }
                });
                };
// TODO- Note it might be easier to just implement push notifications as this methods uses up resources
setInterval(UpdateChat,5000);