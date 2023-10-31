function send_otp(){
    
    var user_info_data={
        'email':document.getElementById("email").value,
        'host':window.location.host,
        'type':document.getElementById("type").value
    };
    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(user_info_data));
    XHR.open('POST','/api/auth/email_otp/');
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );

    XHR.close();
}