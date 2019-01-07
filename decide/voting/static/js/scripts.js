function countdown_redirect(n){
    var l = document.getElementById("number");
    if(n>=0){
        l.innerHTML = n;
        window.setTimeout(function(){
            countdown_redirect(n-1)
        },1000);
    }else{
        location.href = "../admin/voting/voting";
    }
}
