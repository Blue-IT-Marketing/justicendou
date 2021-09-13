
//CreateTicketINFDIV
var thisCreateTicketButt = document.getElementById("CreateTicketButt");
thisCreateTicketButt.addEventListener("click", function(){

                var vstrChoice = 3;
                var vstrNames = document.getElementById('names').value;
                var vstrSurname = document.getElementById('surname').value;
                var vstrCell = document.getElementById('cell').value;
                var vstrEmail = document.getElementById('email').value;
                var vstrSubject = document.getElementById('subject').value;
                var vstrBody = document.getElementById('body').value;

                var vstrTicketPreference = document.getElementById('ticket_preference').value;
                var vstrDepartment = document.getElementById('department').value;
                var dataString = '&vstrChoice=' + vstrChoice + '&vstrSubject=' + vstrSubject + '&vstrBody=' + vstrBody +
                    '&vstrTicketPreference=' + vstrTicketPreference + '&vstrDepartment=' + vstrDepartment + '&vstrNames=' + vstrNames +
                    '&vstrSurname=' + vstrSurname + '&vstrCell=' + vstrCell + '&vstrEmail=' + email ;
                $.ajax({
                    type: "post",
                    url: "/contact",
                    data: dataString,
                    cache: false,
                    success: function (html) {
                        $('#CreateTicketINFDIV').html(html)
                    }
                });
            });

