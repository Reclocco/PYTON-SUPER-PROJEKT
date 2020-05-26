function createTable() {
    let dane = document.getElementById("data")
        .innerHTML
        .toString()
        .replace(/\[/g, '')
        .replace(/]/g, '')
        .split(',');
    let html = '<table id="data-table" class="col-sm-10 col-md-9 col-lg-8">' +
        '<tr>' +
        '<td>Data</td><td>Treść</td><td>Retweet</td><td>Favourite</td>' +
        '</tr>';
    for(let i = 0; i < dane.length/4; i++){
        let row = '<tr>';
        for (let j = 0; j < 4; j++) {
            d = dane[4 * i + j];
            row += '<td>' + d + '</td>';
        }
        row += '</td>';
        html += row;
    }
    html += '</table>';
    document.getElementById("data").innerHTML = html;
}
createTable();