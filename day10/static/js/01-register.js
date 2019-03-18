/**
 * Created by tarena on 19-3-15.
 */

function checkuname(){
        //1.获取xhr
        var xhr = createXhr();
        //2.创建请求
        //请求地址: /01-checkuname?uname=xxx
        var url = "/01-checkuname?uname="+$("#uname").val();
        xhr.open('get',url,true);
        //3.设置回调函数
        xhr.onreadystatechange = function(){
            if(xhr.readyState==4&&xhr.status==200){
                //服务器端响应回: 用户名称已存在　/ 通过
                $("#uname-tip").html(xhr.responseText);
            }
        }
        //4.发送请求
        xhr.send(null);
}

$(function(){
    /**
     * 为#uname元素绑定失去焦点事件
     * 使用ajax验证uname的值在数据库中是否存在
     * */
    $("#uname").blur(function(){
        checkuname();
    });


    /**
     * 为btnReg绑定click事件
     * 完成注册功能
     * */
    $("#btnReg").click(function(){
        var xhr = createXhr();
        xhr.open('post','/01-reg',true);
        xhr.onreadystatechange = function(){
            if(xhr.readyState==4&&xhr.status==200){
                alert(xhr.responseText);
            }
        }
        xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
        var uname = $("#uname").val();
        var upwd = $("#upwd").val();
        var nickname = $("#nickname").val();
        var data = "uname="+uname+"&upwd="+upwd+"&nickname="+nickname;
        xhr.send(data);

    });
});







