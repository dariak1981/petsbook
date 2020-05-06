var sBrowser, sUsrAg = navigator.userAgent;

 if (sUsrAg.indexOf("Trident") > -1) {
    var txt ="Internet Explorer detected :( <br><br>To get better experience open the website in Chrome or Firefox. <br>Пожалуйста, используйте другой браузер!";
    var i = document.createElement("i");
    i.className = 'fa fa-smile-o';

    var ie=document.createElement('div');
    ie.setAttribute("style", "width:100%;height:100%;z-index:2147483647;text-align:center;font-size:30px; padding-top:200px; background:rgba(240,240,240,.9); position: fixed; top:0px; left:0px;");

    var label = document.createElement('label');
    label.innerHTML = txt;
    ie.appendChild(label);
    // e.innerHTML = '<i class="fa fa-trash-o" aria-hidden="true"></i>';
    // ie.appendChild(e);
    document.body.appendChild(ie);
}
