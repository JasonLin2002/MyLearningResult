//Ctrl + K + C	切換行註解
//Ctrl + K + U	取消行註解

//測驗題庫 Json 物件 <-- CSV 
var ExamRecord = {};
//題庫Index 題目指標 
var QuesIndex = 0;
//統計得分數
var score = 0.0;
//題目分數 100 /題目數
var QuesPoints = 0;
//答題陣列列表
var AnswerList = [];
//答案陣列列表
var SolutionList = [];


//選擇題庫檔案
var inputFile = document.getElementById("files");
var csvtable = document.getElementById("csvtable");
//訊息資訊區塊
var MessageBlock = document.getElementById("MessageBlock");

//測驗題目
var QuestionList = document.getElementById("QuestionList");

var Message = document.getElementById("Message");
//目前題號 / 題目總數
var QuesNumber = document.getElementById("QuesNumber");
//分數資訊
var ScoreMsg = document.getElementById("ScoreMsg");




//檔案處理 使用 <input type="file" id="files"/> 開啟檔案選擇器
function handleFiles() {
    var selectedFile = document.getElementById("files").files[0]; //獲取讀取的File物件
    var name = selectedFile.name; //讀取選中檔案的檔名
    var size = selectedFile.size; //讀取選中檔案的大小
    console.log("檔名:" + name + "大小：" + size);

    var reader = new FileReader(); //這裡是核心！！！讀取操作就是由它完成的。
    reader.readAsText(selectedFile, 'UTF8'); //讀取檔案的內容

    //當讀取完成之後會Callbak這個函式
    reader.onload = function () {

        var CsvText = this.result;

        console.log("讀取結果：", this.result); //當讀取完成之後會Callbak這個函式，然後此時檔案的內容儲存到了result中。直接操作即可。

        //csv to Json Record 
        ExamRecord = csvToJson(CsvText);
        console.log(JSON.stringify(ExamRecord));

        //100分


        //console.log(ExamRecord);

        LoadSolution();

        /*顯示CSV HTML Table 
        objToHtmlTable(ExamRecord);

        csvtable.style.display = "block";
        */

        //https://medium.com/itsems-frontend/javascript-json-stringify-and-json-parse-7a1251d3824c
        console.log("讀取結果轉為JSON：");
        //let json = JSON.parse(this.result);
        //console.log(json);

    };
}



//讀取檔案方法 2 可讀URL FILE 
// As with JSON, use the Fetch API & ES6
fetch('./data/108年自評活動題目5.csv')
    .then(response => response.text())
    .then(data => {
        // Do something with your data
        //console.log(data);
        ExamRecord = csvToJson(data);
        LoadSolution();
    });

//開始測驗 顯示單題
function StartExam() {

    //問題Index 
    QuesIndex = 0;
    //統計得分數
    score = 0.0;
    //答題列表
    AnswerList = [];
    //題目分數
    QuesPoints = 100.0 / ExamRecord.length;
    //目前題目編號/總共幾題
    QuesNumber.innerHTML = '1/' + ExamRecord.length;
    //顯示分數訊息
    ScoreMsg.innerHTML = '';
    MessageBlock.style.cssText = "display:flex;"

    //載入問題


}




//載入答案
function LoadSolution(){
    SolutionList = []
    for(i in ExamRecord) {
        SolutionList.push(ExamRecord[i].答案);
}
console.log(SolutionList)
}

function StartExam0() {


}

//顯示全部題目
function StartExam4() {



}






//讀取Qindex 題目資訊產生HTML 
function LoadQuestion(Qindex) {
    let QuestionHtml = '';
    let OtpList = ["A", "B", "C", "D"];
    let OtpLabel = ["(a)","(b)","(c)","(d)"];

    let Record = ExamRecord[Qindex];

    QuestionHtml += `<hr/>
    <H3>${Record.序號 + '.' + Record.題目}</H3>`;
    for (i in OtpList) {
        QuestionHtml += `<input id="${OtpList[i] + Record.序號}" name="GroupOpt${Record.序號}" type="radio"/>
        <label class="RadioOpt">${OtpLabel[i] + Record["選項"+OtpList[i]]}</label>
        <br/>`;
    }
    QuestionHtml += `<hr/>`;
    console.log(QuestionHtml);
    QuesNumber.innerHTML = (Qindex + 1) + "/" + ExamRecord.length;
    QuestionList.innerHTML = QuestionHtml;
}

//顯示下一題
function NextQuestion() {
    let OtpList = ["A", "B", "C", "D"];

    let bChecked = false;
    let Record = ExamRecord[QuesIndex];

    for (i in OtpList) {
        if(document.getElementById(OtpList[i] + Record.序號).checked === true) {
            console.log(OtpList[i] + Record.序號);
            bChecked = true
            AnswerList.push(i);

            break;
        } 
    }
    if (bChecked) {
        QuesIndex++;
        LoadQuestion(QuesIndex);

    } else {
        alert("你還沒選答案喔！");

    }
}



//計算分數  單題
function CalculateScore() {

    //AnswerList   [1,0,2,4,.......] ;
    //SolutionList ["B","A","C","C",.......] ;
    let Otplist = ["A","B","C","D"];

    score = 0.0;
    for(i in SolutionList) {

        let ans = AnswerList[i];
        let sol = SolutionList[i];

        //判斷答案是否正確
        if (Otplist[ans] === sol){
            score += QuesPoints ;
        }
    }
}