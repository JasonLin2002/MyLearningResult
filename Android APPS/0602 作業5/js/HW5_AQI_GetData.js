//Ctrl + K + C	切換行註解
//Ctrl + K + U	取消行註解

// https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json -->
//https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON -->
//url = "http://140.134.196.194/WebDataServer/GetAQIData.aspx";

function GetAQIJson() {

    //正式網站 有cros 跨站存取的問題
    let url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON&callback=?'

    //Proxy Server
    url = "http://140.134.196.194/WebDataServer/GetAQIData.aspx";

    //url = "http://127.0.0.1/WebDataServer/GetAQIData.aspx";

    fetch(
        url
    )
        .then(response => response.json())
        .then(data => {
            //data 是Json 物件
            console.log(data);
            AQIData = data.records;
            console.log(data.records);
            //產生縣市列表
            getCityList();
            alert("資料更新完成!");

        })
    // .catch(err => {
    //     console.log(err);
    // });
}

async function GetAQIJson2() {

    let url =
        "https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON&callback=?";
    // url =
    //"https://data.epa.gov.tw/api/v2/aqx_p_432?limit=1000&api_key=2e95a1a9-b394-4891-b046-7f1c8d75138d&sort=siteid%20asc&format=json";

    url = "http://140.134.196.194/WebDataServer/GetAQIData.aspx";

    //1.status :回傳狀態 2.data:URL回應的資料內容
    fetchUrlParmData(url, Urlcallback);
}



//https://developer.mozilla.org/zh-TW/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest
//XMLHttpRequest API
//1.url:網址 2.callback 回調函式(資料讀取完成後執行)
var getJSON = function (url, callback) {
    //https://stackoverflow.com/questions/12460378/how-to-get-json-from-url-in-javascript
    //使用XMLHttpRequest API
    var xhr = new XMLHttpRequest();



    //設定URL請求 1.GET、POST 2.url:網址 
    //3. false: 同步、true: 非同步 預設非同步
    xhr.open('GET', url, true);

    //回應資料型態:json 格式
    xhr.responseType = 'json';

    //資料讀取完成->onload 事件
    xhr.onload = function () {
        //回傳狀態    
        var status = xhr.status;
        //200 回傳資料正常
        if (status === 200) {
            //xhr.response :接收到的資料
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    //送出URL要求
    xhr.send();
};



//URL 資料讀取完成
function Urlcallback(status, data) {
    if (status === null) //讀取資料成功
    {
        //data 是 Json 物件
        console.log(data);
        AQIData = data.records;
        //資料載入AQIData 變數
        AQIData = data['records'];
        console.log(AQIData);
        //產生縣市列表
        getCityList();

        alert("資料更新完成!");
    } else
        alert("資料接收錯誤!");
}

function GetAQIJson1() {

    let url =
        "https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON";
    // url =
    //
    "https://data.epa.gov.tw/api/v2/aqx_p_432?limit=1000&api_key=2e95a1a9-b394-4891-b046-7f1c8d75138d&sort=siteid%20asc&format=json";
    // // //function (status, data) :callback function
    //1.status :回傳狀態 2.data:URL回應的資料內容
    getJSON(url, Urlcallback);
}



var inputFile = document.getElementById("files");


console.log("加入監聽事件(Event)");
console.log("change:事件 物件內容改變時");
//inputFile.addEventListener("change", handleFiles, false);

function handleFiles() {
    var selectedFile = document.getElementById("files").files[0]; //獲取讀取的File物件
    var name = selectedFile.name; //讀取選中檔案的檔名
    var size = selectedFile.size; //讀取選中檔案的大小
    console.log("檔名:" + name + "大小：" + size);
    var reader = new FileReader(); //這裡是核心！！！讀取操作就是由它完成的。
    reader.readAsText(selectedFile); //讀取檔案的內容

    //當讀取完成之後會Callbak這個函式
    reader.onload = function () {
        //this.result 是文字
        console.log("讀取結果：", this.result); //當讀取完成之後會Callbak這個函式，然後此時檔案的內容儲存到了result中。直接操作即可。

        console.log("讀取結果轉為JSON：");
        //讀取Text結果轉為JSON 物件
        let json_object = JSON.parse(this.result);
        console.log(json_object);

        AQIData = json_object.records;
        console.log(AQIData);
        //資料載入AQIData 變數
        AQIData = json_object['records'];
        console.log(AQIData);

        //產生縣市列表
        getCityList();

        alert("檔案:" + selectedFile.name + "讀取完成!")

    };

}