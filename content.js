console.log("Hello World");

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    console.log(request);
    if (request == "data"){
        var selectedList = [];
        var person = document.getElementsByTagName('tr');
        for (let i = 4; i < person.length; i++){
            var item = person.item(i);
            var found = item.getElementsByClassName("oZ-jc T-Jo J-J5-Ji T-Jo-Jp");
            if (found.length > 0){
                var div = item.getElementsByClassName('yX xY ');
                for (let j = 0; j < div.length; j++){
                    var email = div.item(j).getElementsByClassName('bA4');
                    var emailID = email.item(0).innerHTML.split(' ')[3];    
                    
                    var finalEmail = emailID.substring(7, emailID.length-1);

                    var dataItem = {};
                    var temp = "";
                    if (div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[1].trim() != "unread"){
                        temp = "read"
                    }
                    else{
                        temp = div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[0];
                    }
                    
                    if (email.length == 5){
                        dataItem = {
                            "sender" : div.item(j).getElementsByClassName('bA4').item(0).textContent,
                            "subject" : div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[2],
                            "status" : temp,
                            "reply" : true,
                            "email" : finalEmail
                        }
                    }
                    else if (email.length == 7){
                        dataItem = {
                            "sender" : div.item(j).getElementsByClassName('bA4').item(0).textContent,
                                "subject" : div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[2],
                            "status" : temp,
                            "reply" : true,
                            "email" : finalEmail
                        }
                    }
                    else{
                        if (temp == "read"){
                            dataItem = {
                                "sender" : div.item(j).getElementsByClassName('bA4').item(0).textContent,
                                "subject" : div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[2],
                                "status" : temp,
                                "reply" : false,
                                "email" : finalEmail
                            }
                        }
                        else{
                            dataItem = {
                                "sender" : div.item(j).getElementsByClassName('bA4').item(0).textContent,
                                "subject" : div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[3].trim(),
                                "status" : temp,
                                "reply" : false,
                                "email" : finalEmail
                            }
                        }
                    }
                    selectedList.push(dataItem);
                }
            }
        }
        sendResponse({items: selectedList, count: selectedList.length});
    }
    else {
        sendResponse("clear");
    }
})

var data = [];
setTimeout(() => {
    var person = document.getElementsByTagName('tr');
    finalDict = {}
    console.log(person.length);
    for (let i = 1; i < person.length; i++){
        var item = person.item(i);
        // highlight(item);
        var div = item.getElementsByClassName('yX xY ');
        for (let j = 0; j < div.length; j++){
            // console.log(div.item(j).getElementsByClassName('afn').item(0).textContent);
            var email = div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span')
            
            var emailID = email.item(0).innerHTML.split(' ')[3]
            
            var finalEmail = emailID.substring(7, emailID.length-1);
            
            if (Object.keys(finalDict).includes(finalEmail)){
                finalDict[finalEmail].push(item);
            }
            else{
                finalDict[finalEmail] = [item];
            }
            var dataItem = {};
            var temp = "";
            if (div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[0] == div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(1).textContent){
                temp = "read"
            }
            else{
                temp = div.item(j).getElementsByClassName('afn').item(0).textContent.split(',')[0];
            }
            
            if (email.length == 5){
                dataItem = {
                    "sender" : div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(1).textContent,
                    "subject" : div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(3).textContent,
                    "status" : temp,
                    "reply" : true,
                    "email" : finalEmail,
                    "selected" : false
                }
                data.push(dataItem);
            }
            else if (email.length == 7){
                dataItem = {
                    "sender" : div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(1).textContent,
                    "subject" : div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(5).textContent,
                    "status" : temp,
                    "reply" : true,
                    "email" : finalEmail,
                    "selected" : false
                }
                data.push(dataItem);
            }
            else{
                dataItem = {
                    "sender" : div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(1).textContent,
                    "subject" : div.item(j).getElementsByClassName('afn').item(0).getElementsByTagName('span').item(2).textContent,
                    "status" : temp,
                    "reply" : false,
                    "email" : finalEmail,
                    "selected" : false
                }
                data.push(dataItem);
            }
            
        }
    }
    console.log(Object.keys(finalDict).length)
    chrome.runtime.sendMessage(JSON.stringify(data), function(response) {
        console.log(response)
        var cleanData = []
        var flagged = response.substring(1, response.length-1).split(',');
        for(let i = 0; i < flagged.length; i++){
            if (flagged[i].length > 5){
                if(i == 0)
                    cleanData.push(flagged[i].trim().substring(1, flagged[i].length-1))
                else
                    cleanData.push(flagged[i].trim().substring(1, flagged[i].length-2))
            }
        }
        for(let i = 0; i < cleanData.length; i++){
            console.log(cleanData[i])
            if(cleanData[i] in finalDict){
                finalDict[cleanData[i]].forEach(element => {
                    highlight(element);
                });
                // highlight();
                // highlight(finalDict['security@mail.gitguardian.com'])
            }
        }
        
    });
    

}, 9000);

function highlight(tag){
    if(tag){
        // console.log(tag)
        var html = tag.outerHTML;
        //adds high span tag to the innerHTML
        s2 = html.substring(0,4) + 'style="background-color: aqua;" ' + html.substring(4);
        s = '<span style="background-color: aqua;">' + html + '</span>'
        // sets the innerHTML to the new high tag html
        // tag.outerHTML = s2;
        try{
            tag.style.backgroundColor = "aqua";
            // tag.outerHTML = ""
        }
        catch(err){
            console.log(err)
        }
        
        // tag.style.backgroundColor = "black";
    }

};


