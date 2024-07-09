<template>
  <div class="mainPage-container">
    <main>
      <div class="slider-Main">
        <h1>Business Consulting</h1>
        <div class="slider-wrapper">
          <div class="slider-image"></div>
          <div class="slider-name"></div>
          <a href="#">
            <div class="slider-name-content">
              <div class="name">Weekly Statistics</div>
              <router-link to="/statistic-page"><div class="arrow"><img src="../assets/arrow.svg" alt="arrow"></div></router-link>
            </div>
          </a>
          <div class="dots">
            <img src="../assets/dots.svg" alt="">
          </div>
          <div class="price">€ 1 670</div>
        </div>
      </div>
      <div class="main">
        <div class="youtube-cotent">
        <div class="content">
          <div class="Youtube">
          <div class="texts">
            <h2>Interviews with Successful Entrepreneurs</h2>
          </div>

          <div class="card-container">
            <div class="first-row">
              <div class="card">
                <iframe width="560" height="355" src="https://www.youtube.com/embed/M2VP64Tc60w?si=SMKoWjjV4xKSEgOs"
                  frameborder="0" allowfullscreen></iframe>
              </div>
              <div class="card">
                <iframe width="100" height="355" src="https://www.youtube.com/embed/Ko5AJh2J4xU?si=5LBNCwvUrQCGF_1A"
                  frameborder="0" allowfullscreen></iframe>
              </div>
            </div>

            <div class="second-row">
              <div class="card">
                <iframe width="560" height="355" src="https://www.youtube.com/embed/amdXa3CfzHw?si=WrWcfthcLYat713L"
                  frameborder="0" allowfullscreen></iframe>
              </div>

              <div class="card">
                <iframe width="560" height="355" src="https://www.youtube.com/embed/A54VFBYfF9U?si=WjDRLNtRBLT3Z703"
                  frameborder="0" allowfullscreen></iframe>
              </div>
            </div>
            <div class="second-row">
              <div class="card">
                <iframe width="560" height="355" src="https://www.youtube.com/embed/bXLZ8I7s8tw?si=OIj-ytgQzlobznb-"
                  frameborder="0" allowfullscreen></iframe>
              </div>

              <div class="card">
                <iframe width="560" height="355" src="https://www.youtube.com/embed/RZbpSe9pdFs?si=XoCSD6u18ldSmuk5"
                  frameborder="0" allowfullscreen></iframe>
              </div>
            </div>
          </div>
        </div>
        </div>
        </div>
        <!-- Chatbot Section Start -->
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
        <!-- Chatbot Section End -->
      </div>
    </main>
  </div>
</template>

<script>
import ApiService from '@/services/ApiService';

export default {
  name: 'MainPage',
  data() {
    return {
      newMessage: '',
      messages: [
        { text: 'Hi there! What can I help you with today?', isUser: false },
      ],
      showSidebar: true,
      file: null,
      loading: false,
      fileProcessing: false,
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

        this.loading = true;
        ApiService.sendMessageToBot(this.newMessage)
          .then(response => {
            this.messages.push({
              text: response.data.response,
              isUser: false,
            });
            this.newMessage = '';
            this.scrollToEnd();
          })
          .catch(error => {
            console.error('Error sending message:', error);
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    sendFile() {
      if (this.file) {
        this.loading = true;
        this.fileProcessing = true;
        ApiService.uploadDocument(this.file)
          .then(response => {
            this.messages.push({
              text: response.data.analysis,
              isUser: false,
            });
            this.file = null;
            this.$refs.fileInput.value = '';
            this.scrollToEnd();
          })
          .catch(error => {
            console.error('Error uploading file:', error);
          })
          .finally(() => {
            this.loading = false;
            this.fileProcessing = false;
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
/* Existing styles */

h2 {
  font-family: "PT Sans", sans-serif;
  font-weight: 700;
  color: #000000;
  font-size: 18.6px;
  line-height: 15px;
}

.mainPage-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.slider-Main,
.main {
  width: 100%;
}

.youtube-cotent{
  padding: 10px;
}
.content,
.chat {
  box-sizing: border-box;
  padding: 10px;
  flex: 1;
}

@media (max-width: 1200px) {
  .main {
    flex-direction: column;
  }

  .content,
  .chatbot-container{
    width: 100%;
  }

  .card-container{
    flex-direction: column;
  }

  .card {
    width: 100%;
  }
}

.Youtube{
  width: 600px;
}
.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.first-row,
.second-row,
.third-row {
  width: 100%;
}

.card {
  flex-basis: calc(50% - 20px);
  margin-bottom: 20px;
}

/* For large screens */
@media (min-width: 1000px) {
  .mainPage-container {
    max-width: 1140px;
  }

  .content
  {
    padding: 20px 30px;
    width: 100%;
  }
  .chatbot-container{
    padding: 20px 30px;
    width: 100%;
  }

  .card, .chat-window {
    position: relative;
    overflow: hidden;
  }

}

.card iframe {
  padding: 5%;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8%;
}

/* Chatbot-specific styles with updates */
.chatbot-container {
  /* max-width: 100%; */
  padding: 10px;
  box-sizing: border-box;
  font-family: "PT Sans";
}
.chat-window {
  background: #ffffff;
  border: 1px solid #cccccc;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
  height: 730px; /* Set a max-width for the chat window */
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #183961;
  color: white;
  border-bottom: 1px solid #cccccc;
  border-radius: 10px 10px 0 0;
  padding: 10px;
}

.h2-chat h2 {
  margin: 0;
  color: white;
}

.chatBot-background {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  background: #f9f9f9; /* Change background color */
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
}

.chat-message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.chat-message.user {
  background: #4CAF50; /* User message color */
  color: #ffffff;
  align-self: flex-end;
}

.chat-message.bot {
  background: #e0e0e0; /* Bot message color */
  color: #000000;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  border-top: 1px solid #cccccc;
  padding: 10px;
  background: #ffffff;
  border-radius: 0 0 10px 10px;
}

.chat-input input[type="text"] {
  flex: 1;
  border: 1px solid #cccccc;
  border-radius: 5px;
  padding: 10px;
  margin-right: 10px;
}

.chat-input button {
  padding: 10px 20px;
  border: none;
  background: #183961;
  color: #ffffff;
  border-radius: 5px;
  cursor: pointer;
}

.chat-input input[type="file"] {
  display: none;
}

.loading-indicator {
  display: flex;
  align-items: center;
}

.loading-indicator .file-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}
</style>
