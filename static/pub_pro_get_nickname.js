function get_nickname(){
    
    var req={
        'uuid':document.getElementById('uuid').value
    };
    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(req));
    XHR.open('POST','/api/public/get_info/');
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );
    XHR.close();
}