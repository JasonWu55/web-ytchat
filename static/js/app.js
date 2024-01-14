// Existing JavaScript code remains unchanged

function getChatMessages() {
    fetch('/get_chat_messages')
        .then(response => response.json())
        .then(chatMessages => {
            const chatMessagesList = document.getElementById('chat-messages-list');
            chatMessagesList.innerHTML = '';

            chatMessages.forEach(message => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <img src="${message.avator}" alt="User Avatar" class="avatar">
                    <div>
                        <strong>${message.author}</strong>: ${message.message}
                    </div>
                `;
                chatMessagesList.appendChild(listItem);
            });
        })
        .catch(error => console.error(error));
}

// Fetch chat messages initially and then every 5 seconds
getChatMessages();
setInterval(getChatMessages, 5000);

