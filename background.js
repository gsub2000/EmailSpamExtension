console.log("hey its the bg page");

// chrome.runtime.onMessage.addListener(
//     function(request, sender, sendResponse) {
//         console.log("Entered");
//         chrome.tabs.executeScript(null, {file: "script.js"});   
        
//     }
// );

chrome.runtime.onMessage.addListener(
    function(request, sender, response) {
        console.log(request); 
        var itemList = [];
        myStorage = window.localStorage;
        for(let i = 0; i < myStorage.length; i++){
            itemList.push(myStorage.getItem(i.toString()));
            console.log(myStorage.getItem(i.toString()))
        }
        console.log("local storage items")
        
        var emails = JSON.stringify({msg: request, items: itemList})

        $.ajax({
            type: 'POST',
            url: 'https://spam-bot-heroku.herokuapp.com/data',
            data: emails,
            encoding: 'UTF-8',
            success: function (resp){
                console.log(resp);
                response(resp)
            },
            error: function(er,a,b){
                console.log("error has occurred");
            }
            });
            return true;
        
        
            // sendResponse({ message: "Background has received that message" });
        });