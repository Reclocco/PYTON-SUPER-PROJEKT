function checkDate() {
    let today = new Date();
    let h = ("0" + today.getHours()).slice(-2);
    let M = ("0" + today.getMinutes()).slice(-2);
    let d = ("0" + today.getDay()).slice(-2);
    let m = today.toLocaleString('en-EN', { month: 'short' })
    let y = today.getFullYear();
    let datetext = h + ':' + M + ' | ' + d + '.' + m + '.' + y;
    document.getElementById("data").innerHTML = datetext;
}
checkDate();