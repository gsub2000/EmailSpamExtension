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
                chrome.tabs.sendMessage(tabs[0].id, 'clear', clearSelections)
                
            }    
        )
        
    }
    function setChecked (res) {
        const div = document.createElement('div')
        div.textContent = "Worked."
        document.body.appendChild(div)
        itemList = res['items']
        myStorage = window.localStorage;
        for(let i = 0; i < res['count']; i++){
            var key = myStorage.length + i;
            myStorage.setItem(key.toString(), JSON.stringify(itemList[i]))
        }
        return true;
    }

    function clearSelections (res) {
        //whenever button is pressed, local storage is cleared
        const div = document.createElement('div')
        // var itemString = [];
        // myStorage = window.localStorage;
        // for(let i = 0; i < myStorage.length; i++){
        //     itemString.push(myStorage.getItem(i.toString()) + "\n");
        // }
        window.localStorage.clear();
        div.textContent = "Cleared."
        document.body.appendChild(div)
        return true;
    }
}, false);

