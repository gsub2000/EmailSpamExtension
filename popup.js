document.addEventListener('DOMContentLoaded', function () {
    var i = document.getElementById('mybtn');
    if (i){
        i.addEventListener("click", onclick, false)
    }

    var j = document.getElementById('clearbtn');
    if (j){
        j.addEventListener("click", onclick2, false)
    }

    function onclick () {
        chrome.tabs.query({currentWindow: true, active: true},
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, 'data', setChecked)
                
            }    
        )
        
    }
    function onclick2 () {
        chrome.tabs.query({currentWindow: true, active: true},
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, 'clear', setChecked)
                
            }    
        )
        
    }
    function setChecked (res) {
        const div = document.createElement('div')
        console.log('here')
        // div.textContent = res['count']
        // document.body.appendChild(div)
        $.ajax({
            type: 'POST',
            url: 'https://spam-bot-heroku.herokuapp.com/test',
            data: JSON.stringify(res),
            encoding: 'UTF-8',
            success: function (resp){
                div.textContent = resp
                document.body.appendChild(div)
            },
            error: function(er,a,b){
                console.log("error has occurred");
            }
        });
        return true;
    }
}, false);

