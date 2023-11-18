
function fileToBlob(file) {
    // 创建 FileReader 对象
    let reader = new FileReader();
    return new Promise(resolve => {
      // FileReader 添加 load 事件
      reader.addEventListener('load', (e) => {
        let blob;
        if (typeof e.target.result === 'object') {
          blob = new Blob([e.target.result])
        } else {
          blob = e.target.result
        }
        console.log(Object.prototype.toString.call(blob));
        resolve(blob)
      })
      // FileReader 以 ArrayBuffer 格式 读取 File 对象中数据
      reader.readAsArrayBuffer(file)
    })
  }

function upload_avatar(){
    var url_parse=new URL(window.location.href);

    var user_info_data={
        'token':document.getElementById("token").value
    };
    //const blob = fileToBlob(document.getElementById("avatar_file").files[0])

    var XHR=new XMLHttpRequest();
    
    var FD=new FormData();
    FD.append('data',JSON.stringify(user_info_data));
    FD.append('avatar',document.getElementById('avatar_file').files[0]);


    XHR.open('POST','/api/public/upload_avatar/');
    XHR.send(FD);
    XHR.addEventListener('loadend',()=>{
        document.getElementById('result').innerHTML=XHR.responseText;}
    );
    XHR.close();
}

