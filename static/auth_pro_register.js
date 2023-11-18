

function commit_register(){
    var url_parse=new URL(window.location.href);

    var user_info_data={
        'email':url_parse.searchParams.get('email'),
        'username':document.getElementById("username").value,
        'password':SHA256(document.getElementById("password").value),
        'otp':url_parse.searchParams.get('otp'),
    };
    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(user_info_data));
    XHR.open('POST','/api/auth/register/');
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );
    XHR.close();
}

