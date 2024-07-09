<template>
  <div class="chatbot-container">
    <div class="chat-window">
      <div class="chat-header">
        <button class="toggle-sidebar" @click="toggleSidebar" v-if="!showSidebar">&#9776;</button>
        <div class="h2-chat">
          <h2>Chat Assistant</h2>
        </div>
      </div>
      <div class="chatBot-background">
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(message, index) in messages" :key="index" class="chat-message" :class="{ 'user': message.isUser, 'bot': !message.isUser }">
            {{ message.text }}
          </div>
          <div v-if="loading" class="loading-indicator">
            <div v-if="fileProcessing">
              <img src="path/to/your/file-icon.png" alt="File Processing" class="file-icon">
              Processing file...
            </div>
            <div v-else>
              Loading...
            </div>
          </div>
        </div>
        <div class="chat-input">
          <input type="text" v-model="newMessage" @keyup.enter="sendMessageOrFile" placeholder="Type your message here..." />
          <input type="file" @change="handleFileUpload" ref="fileInput">
          <button @click="sendMessageOrFile">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import ApiService from '@/services/ApiService';

export default {
  name: 'ChatbotPage',
  data() {
    return {
      newMessage: '',
      messages: [
        { text: 'Hi there! What can I help you with today?', isUser: false },
      ],
      showSidebar: true,
      file: null,
      loading: false,
      fileProcessing: false, // Добавленное свойство
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim()) {
        const userMessage = {
          text: this.newMessage,
          isUser: true,
        };
        this.messages.push(userMessage);

        this.loading = true; // Начало загрузки
        ApiService.sendMessageToBot(this.newMessage)
          .then(response => {
            this.messages.push({
              text: response.data.response, // Обновлено для работы со строкой
              isUser: false,
            });
            this.newMessage = '';
            this.scrollToEnd();
          })
          .catch(error => {
            console.error('Error sending message:', error);
          })
          .finally(() => {
            this.loading = false; // Конец загрузки
          });
      }
    },
    sendFile() {
      if (this.file) {
        this.loading = true; // Начало загрузки
        this.fileProcessing = true; // Начало обработки файла
        ApiService.uploadDocument(this.file)
          .then(response => {
            this.messages.push({
              text: response.data.analysis,
              isUser: false,
            });
            this.file = null;
            this.$refs.fileInput.value = ''; // Очистить поле ввода файла
            this.scrollToEnd();
          })
          .catch(error => {
            console.error('Error uploading file:', error);
          })
          .finally(() => {
            this.loading = false; // Конец загрузки
            this.fileProcessing = false; // Конец обработки файла
          });
      } else {
        alert('Please select a file first.');
      }
    },
    sendMessageOrFile() {
      if (this.file) {
        this.sendFile();
      } else {
        this.sendMessage();
      }
    },
    scrollToEnd() {
      this.$nextTick(() => {
        const chatMessages = this.$refs.chatMessages;
        if (chatMessages) {
          chatMessages.scrollTop = chatMessages.scrollHeight;
        }
      });
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
  },
  mounted() {
    document.body.style.backgroundColor = "#f0f0f0";
    this.scrollToEnd();
  },
};
</script>

<style scoped>
.chatbot-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: "PT Sans", sans-serif;
}

.chat-window {
  width: 100%;
  max-width: 1200px; /* Увеличено в два раза */
  height: 800px; /* Увеличено в два раза */
  background: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #183961;
  color: white;
}

.toggle-sidebar {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

.h2-chat {
  flex-grow: 1;
  text-align: center;
}

.chatBot-background {
  padding: 10px;
  background: #f0f0f0;
  height: calc(100% - 80px); /* Подстроить под высоту */
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex-grow: 1;
  max-height: calc(100% - 50px);
  overflow-y: auto;
  margin-bottom: 10px;
}

.chat-message {
  padding: 10px;
  margin: 5px 0;
}

.chat-message.user {
  text-align: right;
  background: #183961;
  color: white;
}

.chat-message.bot {
  text-align: left;
  background: #e0e0e0;
  color: black;
}

.loading-indicator {
  text-align: center;
  font-size: 14px;
  color: #999;
}

.file-icon {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin-right: 5px;
}

.chat-input {
  display: flex;
  align-items: center;
}

.chat-input input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.chat-input input[type="file"] {
  margin-left: 10px;
}

.chat-input button {
  margin-left: 10px;
  padding: 10px 20px;
  background: #183961;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
