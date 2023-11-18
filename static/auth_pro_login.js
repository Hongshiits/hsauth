function commit_login(){
    
    var user_info_data={
        'email':document.getElementById("email").value,
        'password':SHA256(document.getElementById("password").value),
        'is_long_term_login':false,
    };
    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(user_info_data));
    XHR.open('POST','/api/auth/login/');
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );
    XHR.close();
}