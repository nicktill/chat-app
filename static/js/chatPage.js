fetch("/messages/")
    .then((response) => {
        return response.json();
    })
    .then((results) => {
        let chat_window = document.getElementById("chat_window");

        let messages = "";
        for (let index in results) {
            current_set = results[index];
            for (let key in current_set) {
                author = key;
                message = current_set[key];
                messages += `${author}:\n${message}\n\n`;
            }
        }
        chat_window.value = messages;
    })
    .catch(() => {
        chat_window.value = "error retrieving messages from server";
    });

fetch("/new_message/", {
    method: "post",
    headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
    body: `username=${author}&message=${message}`
})

