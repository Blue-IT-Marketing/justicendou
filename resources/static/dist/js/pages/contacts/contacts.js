try{
var config =
{
  apiKey: "AIzaSyAjcO6wmvJ29XNZrw50hFRLyXzkpN6GHL0",
  authDomain: "justice-ndou.firebaseapp.com",
  databaseURL: "https://justice-ndou.firebaseio.com",
  projectId: "justice-ndou",
  storageBucket: "justice-ndou.appspot.com",
  messagingSenderId: "3221236137"
};
if (!firebase.apps.length) {
    firebase.initializeApp(config);
}else {
}
}catch (err){

}



var thisUploadContactsButt = document.getElementById("UploadContactsButt");

thisUploadContactsButt.addEventListener("click", function () {
    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            user.getIdToken().then(function (accessToken) {
                // User is signed in.
                var displayName = user.displayName;
                var email = user.email;
                var photoURL = user.photoURL;
                var isAnonymous = user.isAnonymous;
                var providerData = user.providerData;
                var struid = user.uid;


                var vstrChoice = 0;
                var vstrNames = document.getElementById('names').value;
                var vstrSurname = document.getElementById('surname').value;
                var vstrCell = document.getElementById('cell').value;
                var vstrTel = document.getElementById('tel').value;
                var vstrFax = document.getElementById('strFax').value;
                var vstrEmail = document.getElementById('email').value;
                var vstrWebsite = document.getElementById('website').value;
                var vstrTitle = document.getElementById('strTitle').value;
                var vstrDateCreated = document.getElementById('date_created').value;

                var dataString = '&vstrChoice=' + vstrChoice + '&vstrNames=' + vstrNames + '&vstrSurname=' + vstrSurname + '&vstrSurname=' + vstrSurname +
                    '&vstrCell=' + vstrCell + '&vstrTel=' + vstrTel + '&vstrFax=' + vstrFax + '&vstrEmail=' + vstrEmail + '&vstrWebsite=' + vstrWebsite +
                    '&vstrDateCreated=' + vstrDateCreated + '&vstrTitle=' + vstrTitle + '&vstrUserID=' + struid + '&vstrAccessToken=' + accessToken;
                $.ajax({
                    type: "post",
                    url: "/admin/contacts",
                    data: dataString,
                    cache: false,
                    success: function (html) {
                        $('#UploadContactINFDIV').html(html)
                    }
                });

            })
        }
    })
});
