//Ctrl + K + C	切換行註解
//Ctrl + K + U	取消行註解

//HTML 使用到的 DOM 物件 

var csvtable = document.getElementById("csvtable");



//讀取csv資料
async function ReadCsvFileUrl(Filename) {
    // As with JSON, use the Fetch API & ES6
    return await fetch(Filename)
        .then(response => response.text())
        .then(data => {
            // Do something with your data

            var csvobject = csvToJSON(data);
            return csvobject;
        });

    //return dataPromise;


}

//讀取JSON資料
async function ReadjosnFileUrl(Filename) {
    // As with JSON, use the Fetch API & ES6
    return await fetch(Filename)
        .then(response => response.json())
        .then(data => {
            // Do something with your data

            var jobj = data;
            return jobj;
        });

}




//https://phpwolf.blogspot.com/2018/03/javascript-csv-json.html
//var csv is the CSV file with headers
function csvToJson(csv) {

    //debugger;
    //字串分割(split)後 回傳陣列
    // '\r\n' OR '\r' 換行符號
    var lines = csv.split("\r\n");

    //回傳csv物件陣列
    var result = [];

    //lines[0] csv 第一行 欄位定義 
    // ',' 欄位分隔
    var headers = lines[0].split(",");

    for (var i = 1; i < lines.length; i++) {

        //可能多一行空白
        if (lines[i] != "") {
            var obj = {};
            var currentline = lines[i].split(",");

            for (var j = 0; j < headers.length; j++) {
                obj[headers[j]] = currentline[j];
            }
            result.push(obj);
        }



    }

    //return result; //JavaScript object
    //物件變 JSON string
    //return JSON.stringify(result); //JSON
    return result; //JSON OBJECT
}


//迴圈 for(變數 in 物件)
function array_object_Process(json_object) {

    //for(變數 in 物件) 存取 陣列
    //csvObject is Array 變數為陣列 Index
    for (inx in json_object) {

        //console.log(inx);

        let Record = json_object[inx];

        //console.log(Record);

        //for(變數 in 物件) 存取 物件
        //Record is object 變數為物件 屬性
        for (property in Record) {
            //console.log(property);
            //console.log(Record[property]);

        }
    }


}

//迴圈 for(變數 in 物件)
function object_Process(jobject) {

    //for(變數 in 物件) 存取 陣列
    //object is Array[] 變數為陣列 Index
    //object is object{} 變數為物件 property Name ;
    for (property in jobject) {

        //console.log(property);

        let obj_property = jobject[property];

        //console.log(obj_property);

        if (typeof obj_property === 'object') {
            object_Process(obj_property);
        }
    }

}


//Array obj [{},{},...]轉成 HTML Table 呈現在網頁上
function objToHtmlTable(Obj, HeaderNames) {

    csvtable = document.getElementById("csvtable");

    //console.log(Obj);
    //console.log(HeaderNames);

    let outTable = '';
    let ObjTable = '';
    let Headtemplate = '';
    //Table 欄位名稱 HTML
    //-----------------------------------------------------
    let Headers = [];

    //判斷輸入物件是否有資料
    if (Obj && Obj.length > 0) {
        Headers = Object.keys(Obj[0]);


        if (HeaderNames == undefined || !Array.isArray(HeaderNames) || HeaderNames.length < Headers.length) {
            Headtemplate =
                `<tr>
                ${Headers.map(item => `<th>${item}</th>`).join('')}
                </tr> 
                `;
        } else {
            Headtemplate =
                `<tr>
                ${HeaderNames.map(item => `<th>${item}</th>`).join('')}
                </tr> 
                `;
        }
        //-----------------------------------------------------

        //console.log(Headtemplate);

        ObjTable = Obj.map(item => {
            return `<tr>
                        ${Headers.map(AttrHeader => `<td>${item[`${AttrHeader}`]}</td>`).join('')}
                    </tr> 
                    `;
        }).join('\r\n');
    } else {

        Headtemplate =
            `<tr>
                ${HeaderNames.map(item => `<th>${item}</th>`).join('')}
                </tr> 
                `;
    }

    //console.log(ObjTable);


    outTable = `<table class="table table-striped table-bordered"><thead>${Headtemplate}</thead><tbody>${ObjTable}</tbody></table>`;


    csvtable.innerHTML = outTable;


}

//Array obj [{},{},...]轉成 HTML Table 呈現在網頁上
function objToHtmlTable2(Obj) {

    //空陣列不執行
    if (Obj.length === 0)
        return;



    csvtable = document.getElementById("csvtable");


    let Headers = Object.keys(Obj[0]);

    let Headtemplate =
        `<tr>
        ${Headers.map(item => `<th>${item}</th>`).join('')}
    </tr> 
    `;

    console.log(Headtemplate);

    let ObjTable = Obj.map(item => {
        return `<tr>
                    ${Headers.map(Attrkey => `<td>${item[`${Attrkey}`]}</td>`).join('')}
                </tr> 
                `;
    }).join('');


    console.log(ObjTable);

    let outTable = "";
    outTable = `<table class="table table-striped table-bordered">${Headtemplate}${ObjTable}</table>`;


    csvtable.innerHTML = outTable;


}

//Array obj [{},{},...]轉成 HTML Table 呈現在網頁上
function objToHtmlTable1(Obj) {

    var Headers = Object.keys(Obj[0]);

    //console.log(Headers);





    var outTable = "";
    outTable = "<table>";
    outTable += "<tr>";
    for (let i = 0; i < Headers.length; i++) {
        outTable += "<th>" + Headers[i] + "</th>";
        Total.push(0);
        AVG.push(0);
    }
    outTable += "</tr>";



    for (let j = 0; j < Obj.length; j++) {
        //取一筆csv Record ;
        let csvRecord = Obj[j];

        outTable += "<tr>";
        for (let i = 0; i < Headers.length; i++) {
            //取得屬性名稱
            let PropertyName = Headers[i];
            //output += "<th>" + csvObject[j][Headers[i]] + "</th>" ;
            //object['Property'] = object.Property :取得物件屬性值 
            outTable += "<td>" + csvRecord[PropertyName] + "</td>";

            if (i > 0) {
                //字串轉數字
                //Total[i] += parseInt(csvObject[j][Headers[i]], 10); ;
                Total[i] += parseInt(csvRecord[PropertyName], 10);
            }
        }

        outTable += "</tr>";
    }


    outTable += "</table>";

    csvtable.innerHTML = outTable;


}


//通用 物件轉 HTML <Select> <Option> 
function objToHtmlSelect(Obj, SelText, SelVal) {


    let selectHTML = `
        <select class ='pretty-select' >
        ${Obj.map(item => `<Option value='${item[`${SelVal}`]}'>${item[`${SelText}`]}</Option>`).join('\r\n')}
        </select>
        `;

    console.log(selectHTML);
    return selectHTML;

}