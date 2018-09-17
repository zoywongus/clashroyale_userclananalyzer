const cardid = [26000000, 26000001, 26000002, 26000003, 26000004, 26000005, 26000006, 26000007, 26000008, 26000009, 26000010, 26000011, 26000012, 26000013, 26000014, 26000015, 26000016, 26000017, 26000018, 26000019, 26000020, 26000021, 26000022, 26000023, 26000024, 26000025, 26000026, 26000027, 26000028, 26000029, 26000030, 26000031, 26000032, 26000033, 26000034, 26000035, 26000036, 26000037, 26000038, 26000039, 26000040, 26000041, 26000042, 26000043, 26000044, 26000045, 26000046, 26000047, 26000048, 26000049, 26000050, 26000052, 26000053, 26000054, 26000055, 26000056, 26000057, 26000059, 26000060, 26000062, 27000000, 27000001, 27000002, 27000003, 27000004, 27000005, 27000006, 27000007, 27000008, 27000009, 27000010, 28000000, 28000001, 28000002, 28000003, 28000004, 28000005, 28000006, 28000007, 28000008, 28000009, 28000010, 28000011, 28000012, 28000013, 28000015, 28000016, 28000017];
const apikey = "Bearer ttAeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjMxMTkyYmQwLTE3YWQtNDZhMy1hOTJjLTYxY2FmYjU2MDI3YiIsImlhdCI6MTUzNzA2ODMxOCwic3ViIjoiZGV2ZWxvcGVyLzIyM2E4N2JiLTNlMjgtYzk4YS1iMzA2LTI2MTkyY2MzODQ1NiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4zMS44OC4xOTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.jM18jTx0J0hXR2IXJB-rPlAvJShX9wK37VxkZdppkqQJ1fUjNbK0ncwbqwR_W7Yo1qqGkEnw9vtxCh3UqwHQ1Q";


const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
var request = require('request');
app.set('view engine' , 'ejs');
app.use(bodyParser.urlencoded({extended:false}));
//app.use(express.static('./public'));

app.use("/public",express.static(path.join(__dirname + '/public')));
app.use(express.static(__dirname));
app.use('/assets',express.static('assets'));

app.get('/', function(req,res) {
  //res.render('index');
	res.sendFile(path.join(__dirname + '/public/index.html'));
});

/*app.get('/thankyou',function(req,res){
	res.sendFile(path.join(__dirname + '/thankyou.html'));
});*/

app.post('/getmember', function(req,res){
  var spawn = require("child_process").spawn;
  var respjson = {};
  var process = spawn('python',["./pythons/main.py",
                            req.body.playertag,
                            req.body.clantag,
                            apikey] );
  process.stdout.on('data', function(data) {
        var string = data.toString().trim();
        respjson = JSON.parse(string);
  });

  if (respjson == {}) {
    res.render('errorpage', {title: 'Profile Submit Error'});
  }
  res.render('testing',
    {
      tablename: 'Profile Input Results',
      header1: 'Category',
      header2: 'Result',
      name: respjson['name'],
      winpercent: respjson['winpercent'],
      donateratio: respjson['donateratio'],
      favecard: respjson['favecard'],
      maxoutcost: respjson['costsforupgrades'],
      numcards: respjson['cardsleft'],
      crownstotal: respjson['crownspergame'],
      opponentcrowns: respjson['opponentcrownspergame'],
      trophyadvantage: respjson['trophyadvantage'],
      cardadvantage: respjson['lvladvantagepercard']
    });
});


app.post('/compareplayer', function(req,res){
  var spawn = require("child_process").spawn;
  var respjson = {};
  var process = spawn('python',["./pythons/compareplayer.py",
                            req.body.playertag,
                            req.body.player2tag,
                            apikey] );
  process.stdout.on('data', function(data) {
        var string = data.toString().trim();
        respjson = JSON.parse(string);
        res.send('!!!Beta Testing: ' + respjson);
  });

});


app.post('/predictor', function(req,res){
  var spawn = require("child_process").spawn;
  var respjson = {};
  var process = spawn('python',["./pythons/predictor.py",
                            req.body.playertag,
                            req.body.clantag,
                            apikey,
                            req.body.thirdvar] );
  process.stdout.on('data', function(data) {
        var string = data.toString().trim();
        respjson = JSON.parse(string);
        res.render('scikittable',{
          row1: respjson['crownshort'],
          row2: respjson['crownlong'],
          row3: respjson['mestrong'],
          row4: respjson['oppstrong'],
          row5: respjson['meweak'],
          row6: respjson['oppweak'],
          row7:respjson['next3crown']
        });
      });
    });

app.get('/testing', function(req,res){
  res.render('testing', {title: 'Response!'});
});

app.post('/compareclan', function(req,res){
  console.log('compare clan');
  res.redirect('https://zoywongus.github.io');
});

app.post('/sharedeck', function(req,res){
  var url = 'https://link.clashroyale.com/deck/en?deck=';
  url += req.body.card1 + ';' + req.body.card2 + ';'+req.body.card3 + ';'+req.body.card4 + ';'+req.body.card5 + ';'+req.body.card6+';'+req.body.card7+';'+req.body.card8;
  res.redirect(url);
});

app.post('/randdeck', function(req,res){
  var urltest = 'https://link.clashroyale.com/deck/en?deck=';
  var arr = [];
  var randid = cardid[Math.floor(Math.random()*cardid.length)];
  while (arr.length < 8){
    while (arr.includes(randid)) {
      randid = cardid[Math.floor(Math.random()*cardid.length)];
    }
    arr[arr.length] = (randid);
  }
  urltest += arr[0].toString() + ';' + arr[1].toString() + ';' + arr[2].toString() + ';' + arr[3].toString() + ';' + arr[4].toString() + ';' + arr[5].toString() + ';' + arr[6].toString() + ';' + arr[7].toString();
  res.redirect(urltest);
});

app.get('/info_submit', function(req,res){
	//sendtoapi(req.body.txtcardname,req.body.txtcardnum,req.body.txtdate,req.body.txtcvc);
	res.render('errorpage', {title: 'Profile Submit Error'});
});

app.get('*', function(req, res) {
  res.redirect('/public/public2/');
    //res.sendFile(path.join(__dirname + '/public/public2/index.html'));
});

app.listen(3000);
