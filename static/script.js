document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const promptForm = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt-input');
    const thinkingIndicator = document.getElementById('thinking');

    promptForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const prompt = promptInput.value.trim();
        if (!prompt) return;

        addMessageToChat('user', prompt);
        promptInput.value = '';
        thinkingIndicator.classList.remove('hidden');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) {
                throw new Error('Failed to get response from server');
            }

            const data = await response.json();
            addMessageToChat('ai', data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessageToChat('ai', 'Sorry, there was an error processing your request.');
        } finally {
            thinkingIndicator.classList.add('hidden');
        }
    });

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});