window.seed = 10;


function use_model_1_run(){
        var roc = document.getElementById('roc_1');
        $.ajax({
        url: "/use1/",
        type: "POST",
        success: function (rsp) {
            console.log('Success');
            var score = rsp['score'];
            var roc_name = rsp['file_name'];
            roc.src='static/temp/result_1/' + roc_name + '.png';
            document.getElementById('model1_score').innerHTML = score;
        }
    })
}

function use_model_2_run(){
        var roc = document.getElementById('roc_2');
        $.ajax({
        url: "/use2/",
        type: "POST",
        success: function (rsp) {
            console.log('Success');
            var score = rsp['score'];
            var roc_name = rsp['file_name'];
            roc.src='static/temp/result_2/' + roc_name + '.png';
            document.getElementById('model2_score').innerHTML = score;
        }
    })
}

function use_model_3_run(){
        var roc = document.getElementById('roc_3');
        $.ajax({
        url: "/use3/",
        type: "POST",
        success: function (rsp) {
            console.log('Success');
            var score = rsp['score'];
            var roc_name = rsp['file_name'];
            roc.src='static/temp/result_3/' + roc_name + '.png';
            document.getElementById('model3_score').innerHTML = score;
        }

    })
}

function choose_dataset() {
     var dataset_num = document.getElementById("choose_form").value;
     //
     $.ajax({
         url: '/choose_dataset/',
         type: "POST",
         data: dataset_num,
         contentType: 'application/json; charset=UTF-8',
         success: function (rsp) {
             console.log('The number of dataset now is: ', rsp);
        },
        error: function (rsp) {
             console.log(rsp);
             alert(rsp['responseText']);
        }
     });
}

