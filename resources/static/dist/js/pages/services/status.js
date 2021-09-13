

document.getElementById('requeststatusbutt').addEventListener("click", function(){

    const projectid = document.getElementById('referenceid').value;
    const route = "request-this-status";
    const mydata = '&route=' + route + '&project_id=' + projectid;
    $.ajax({
        type: "post",
        url : "/services/request-status",
        data : mydata,
        cache : false,
        success: function(response){
            $('#statusinfdiv').html(response)
        }
    })
})