const reader = new FileReader();
const parser = new DOMParser();
let extension;
let input;
let names = [];
let xs = [];
let ys = [];
let plt;
var layout;
let deltaX = 0;
let value;
var table;
function load(){
    // when the body of the page is loaded, an event listener is attached to the file input
    input = document.getElementById("file1");
    value = document.getElementById("value");
    value.addEventListener('change', updateTable);
    table = document.getElementById("myTable");
    // the event listener triggers when the file changes and calls the read function
    input.addEventListener('change', read);
    plt = document.getElementById('tester');
    var row = table.insertRow(0);
}

function read(){
    const [file] = input.files;
    fileName = input.value;
    extension = fileName.split('.').pop();
    reader.addEventListener("load",() => {
        parse(reader.result);
        document.getElementById("values").style.visibility = "visible";
    },false);

    if (file) {
        reader.readAsText(file);
    }
}
function parse(fileString){
    // set the names, xs and ys variables to an empty array
    names = [];
    xs = [];
    ys = [];
    // read the string as an xml document
    let xmlDoc = parser.parseFromString(fileString,"text/xml");
    // get each <curve> from the xml
    curves = xmlDoc.getElementsByTagName("curve");

    // iterate over each curve
    for(let i = 0;i < curves.length;i++){
        names.push(curves[i].getElementsByTagName("name")[0].innerHTML);
        xs.push(separate(curves[i].getElementsByTagName(xdef(extension))[0].innerHTML));
        ys.push(separate(curves[i].getElementsByTagName("i1")[0].innerHTML));
    }
    traces = []
    for(let i = 0;i < curves.length;i++){
        traces.push(
            {
                x: xs[i],
                y: ys[i],
                type: 'scatter',
                name: names[i],
                line: {shape: 'spline'}
            }
        )
    }
    layout = {
        title: fileName.split("\\").slice(-1)+" data",
        paper_bgcolor:"#EDEADE",
        plot_bgcolor:"#EDEADE",
        hovermode:'x',
        showlegend:false,
        xaxis:{
            showspikes : true,
            spikemode  : 'across',
            spikesnap : 'cursor',
            showline:true,
            showgrid:true,
            fixedrange: true
        },
        yaxis: {fixedrange: true}
    }
    Plotly.newPlot(plt,traces,layout,{displayModeBar: false})
    plt.on('plotly_click', function(data){
        var dX = 0;
        for(var i=0; i < data.points.length; i++){
            dX = data.points[i].x;
        }
        deltaX = dX;
        value.value = deltaX;
        updateTable();
    });
}

function xdef(ext){
    if(ext=="mta")
    {
        return "time";
    }
    return "potential";
}

function separate(stringOfNumbers){
    let strings = stringOfNumbers.split(",");
    let nums = [];
    for(let i = 0; i < strings.length;i++){
        nums.push(parseFloat(strings[i]));
    }
    return nums;
}

function updateTable(){
    table.innerHTML = "";
    var row = table.insertRow(0);
    var cell1 = row.insertCell(0);
    cell1.innerHTML = "curve";
    var cell2 = row.insertCell(1);
    cell2.innerHTML = "y1";
    if(extension=="mtc"){
        var cell3 = row.insertCell(2);
        cell3.innerHTML = "y2";
    }
    for (let i = 0;i < names.length;i++) {
        console.log(ys[i][xs[i].indexOf(deltaX)]);
        var row = table.insertRow(i+1);
        var cell1 = row.insertCell(0);
        cell1.innerHTML = names[i];
        var cell2 = row.insertCell(1);
        cell2.innerHTML = ys[i][xs[i].indexOf(deltaX)];
        if(extension=="mtc"){
            var cell3 = row.insertCell(2);
            cell3.innerHTML = ys[i][xs[i].lastIndexOf(deltaX)];
        }
    }
    table.style.visibility = "visible";
}
