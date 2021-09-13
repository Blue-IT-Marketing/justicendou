
//CreateTicketINFDIV
var thisCreateTicketButt = document.getElementById("CreateTicketButt");
thisCreateTicketButt.addEventListener("click", function(){

                var vstrChoice = 3;
                var vstrNames = document.getElementById('names').value;
                var vstrSurname = document.getElementById('surname').value;
                var vstrCell = document.getElementById('cell').value;
                var vstrEmail = document.getElementById('email').value;
                var vstrSubject = document.getElementById('strSubject').value;
                var vstrBody = document.getElementById('strBody').value;

                var vstrTicketPreference = document.getElementById('strTicketPreference').value;
                var vstrDepartment = document.getElementById('strDepartment').value;
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

