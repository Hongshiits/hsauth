
function flex_pro(api_path){
    
    var req={
        'token':document.getElementById('token').value,
        'table':document.getElementById('table').value,
        'column':document.getElementById('column').value,
        'value':document.getElementById('value').value,
    };
    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(req));
    XHR.open('POST',api_path);
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );
    XHR.close();
}
function flex_insert(){
    
    var req={
        'token':document.getElementById('token').value,
        'table':document.getElementById('table').value,
        'column':document.getElementById('column').value,
        'value':document.getElementById('value').value,
    };
    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(req));
    XHR.open('POST','/api/flex/insert_info/');
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );
    XHR.close();
}