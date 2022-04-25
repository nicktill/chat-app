var messages = "";
var chat_window;

function setup() {
    chat_window = document.getElementById("chat_window");
    getMessages()
    document.getElementById("new_message_submit").addEventListener("click", newMessage);
}

function newMessage() {
    let message = document.getElementById('message').value;
    let author = document.getElementById('usernameForAjax').innerText;
    author = author.substring(author.indexOf(':') + 2);
    fetch("/new_message/", {
        method: "POST",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `message=${message}&author=${author}`
    })
        .then((response) => response.json())
        .then((results) => {
            let current_set = results[0];
            let temp = `<p class="fw-bold"> ${current_set['author']}: ${current_set['message']}</p><hr>`;
            chat_window.innerHTML += temp;
        })
        .catch((e) => {
            console.log('Error getting the new message: ', e)
        })
}


function getMessages() {
    fetch("/messages/")
        .then((response) => response.json())
        .then((results) => {
            var tempMessages = "";
            for (index in results) {
                let current_set = results[index];
                tempMessages += `<p class="fw-bold"> ${current_set['author']}: ${current_set['message']}</p><hr>`;
            }
            if (tempMessages !== messages) {
                messages = tempMessages;
                chat_window.innerHTML = messages;
            }
        })
        .catch(() => {
            chat_window.value = "error retrieving messages from server";
        })
    setTimeout(getMessages, 200);
};

window.addEventListener('load', setup);
