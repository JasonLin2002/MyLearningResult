//Ctrl + K + C	切換行註解
//Ctrl + K + U	取消行註解


//變數宣告
var AQIData = [{}]; //AQI 資料物件
var cityList = []; //縣市列表陣列
var SiteList = []; //測站列表陣列
var City = ""; //縣市名稱
var SiteName = ""; //測站名稱
var AQI = ""; //AQI 數值
var PM_25 = ""; //PM_25 數值
var Longitude = ""; //測站位置 x: 經度
var Latitude = ""; //測站位置 y: 緯度度

//陣列處理方式
//https://www.casper.tw/javascript/2017/06/29/es6-native-array/
//filter(), find(), forEach(), map(), every(), some(), reduce()

//產生縣市列表進階作法
function getCityList1() {

    //清除縣市陣列
    cityList = [];

    //map(item, [index] (可省略), [array] (可省略))回傳County 屬性陣列 
    let cityListMap = AQIData.map(item => item.County);
    console.log(cityListMap);

    let uniqueSet = new Set (cityListMap);
    console.log(uniqueSet);
    //Set ->轉換成陣列
    cityList = [...new Set (cityListMap)];
    console.log(cityList);



    //要確保有取到縣市資料時才更新
    if (cityList.length > 0) {
        //產生縣市下拉是選單
        function CreateCityListHTML() {
        let DOMCityList = document.getElementById("CityList");
        let SelectList = "<option value=''>請選擇縣市</option>";
        for (let i=0; i < cityList.length; i++) {
            // "<option value='基隆市'>基隆市</option>";
            SelectList += "<option value='" + cityList[i] + ">" + cityList[i] + "</option>";
        }
        // for (let i=0; i < 10; i++) {
        //     SelectList += "<option value='基隆市'>基隆市</option>";
        // }
        DOMCityList.innerHTML = SelectList;
        //清除測站列表
        let DOMSiteList = document.getElementById("SiteList");
        SelectList = "<option value=''>請選擇測站</option>";
        
        DOMSiteList.innerHTML = SelectList;
        }
    }
}

//產生縣市列表
function getCityList() {
    //清除縣市陣列
    cityList = [];

    //掃描AQIData
    for (let i = 0; i < AQIData.length; i++) {
        if (i=0)
        {
        //https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global Objects/Array/push 
        cityList.push(AQIData[i]["County"]);
        }
        else
        {   //搜尋是否重複
            let index = cityList.findIndex(cityList > cityList === AQIData[i]["County"]);
            //搜尋不到 index = -1
            if (index=== -1){
            cityList.push(AQIData[i]["County"]);
            }
        }
    }
    //要確保有取到縣市資料時才更新
    if (cityList.length > 0) {
        //產生縣市下拉是選單
        CreateCityListHTML();
        
    }
}


//選縣市 --> 產生測站列表 City-> Site
function getSiteList(selectObject) {
    //設定選取縣市 --> City 變數
    City=selectObject.value;
    console.log(City);
    //清除測站陣列
    SiteList = [];
    //要確保有取到測站資料時才更新
    if (City !=''){
        //filter 回傳篩選符合條件的資料
        let SiteList_filterCity = AQIData.filter(item => item.County === City);
        //只取item.SiteName 站名資料
        SiteList = SiteList_filterCity.map(item => item.SiteName);

        console.log(SiteList);
    }
    if (SiteList.length > 0){
        //產生測站下拉是選單
        CreateSiteListHTML(SiteList);
    }
}

//產生測站下拉是選單
function CreateSiteListHTML() {
    let DOMSiteList = document.getElementById ("SiteList");
    let SelectList = "<option value=''>請選擇測站</option>";
    for (let i=0; i < SiteList.length; i++) {
        //"<option value='萬里'>萬里</option>";
        SelectList += "<option value='" + SiteList[i] + "'>" + SiteList[i] + "</option>";
    }

    DOMSiteList.innerHTML = SelectList;
}

//取得測站AQI資訊
function getAQIData(selectObject) {
    //設定選擇站名 --> SiteName 變數
    SiteName = selectObject.value; console.log(SiteName);
    //確認有選擇縣市及測站
    if (City != '' && SiteName !='')
    {
        //搜尋所以有AQI資料
        for(let i=0; i<AOIData.length; i++)
        {
            //找尋 AQI資料 Record County 欄位 = 縣市,SiteName = 欄位站名
            if (City === AQIData[i]["County"] && SiteName === AQIData[i] ["SiteName"]) 
            {
                AQI = AQIData[i]["AQI"];//取得AQI欄位 數值
                console.log(AQI);
                PM_25 = AQIData[i]["PM2.5"];//取得 PM2.5欄位數值 
                console.log(PM_25);
                //顯示資訊
                document.getElementById ("City").innerHTML = City;
                document.getElementById ("Site").innerHTML = SiteName;
                document.getElementById ("AQI").EnnerHTML = "AQI:" + AQIData;
                document.getElementById ("MP_25").innerHTML = "PM2.5: " + PM_25;
                //找到資料就中斷
                break;
            }
        }
    }
}

//移動地圖到測站位置
function GotoSitePosMap(City_SiteData) {
    let DOMSiteMap = document.getElementById("SiteMap");

    DOMSiteMap.src = "https://maps.google.com/maps?q=" + City_SiteData.Latitude +
        "," + City_SiteData.Longitude +
        "(" + City + SiteName + "站)&t=h&z=18&output=embed";
}