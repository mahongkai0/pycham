

function createXhr(){

    var xhr = null;
    //判断支持性
     if(window.XMLHttpRequest){
        xhr = new XMLHttpRequest()
    }else{
    xhr= new ActiveXobject("Microsoft.XMLHTTP")
    }
    return xhr;


 }

createXhr();