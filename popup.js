document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('mybtn').addEventListener('click', onclick)
    // document.querySelector('button').addEventListener('click', onclick)
});

function onclick () {
    // var bgp = chrome.extension.getBackgroundPage()
    // var selected = document.getElementsByClassName("oZ-jc T-Jo J-J5-Ji T-Jo-Jp");

   

    alert("DONE")
    
    // chrome.tabs.query({currentWindow:true, active: true},
    //     function (tabs) {
    //         chrome.tabs.sendMessage(tabs[0].id, document.getElementsByClassName("oZ-jc T-Jo J-J5-Ji T-Jo-Jp").length)
    //     }    
    // )
};

