const copyBtn = document.getElementsByClassName("copy-btn")[0];
const uniqueInp = document.getElementById("unique-id");
var shareText = document.getElementsByClassName("share-text")[0];

copyBtn.onclick = function() {
    uniqueInpVal = uniqueInp.getAttribute("value");

    navigator.clipboard.writeText(uniqueInpVal).then(function(){
        //copying to clipboard successfull
        shareText.innerHTML = "ID Copied successfully"
        uniqueInp.focus();
        uniqueInp.select();
    },function(){
        //copying to clipboard failed
    });
}