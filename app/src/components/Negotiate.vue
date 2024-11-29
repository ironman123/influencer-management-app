<template>
  <div :class="['container popup-container', { 'dark-theme': isDarkTheme }]">
    <form class="p-4 shadow rounded border" action="/" method="post" :class="[ isDarkTheme ? 'detail-form-dark' : 'detail-form-light']" @submit="submitForm">
      <h2 class="text-center mb-4 text-primary" :class="[isDarkTheme ? 'glow-text-dark' : 'glow-text-light']">Negotiate</h2>
      
      <!-- Messages display area -->
      <div class="messages-area mb-4" v-if="messages.length">
        <div v-for="message in messages" :key="message.id" :class="['message-item', isDarkTheme ? 'message-item-dark' : 'message-item-light']">
          <p><strong>{{ message.sender_name }}</strong> <span class="text-muted">({{ formatDate(message.timestamp) }})</span></p>
          <p>{{ message.message_text }}</p>
        </div>
      </div>
      
      <!-- Message input -->
      <div class="mb-3">
        <label for="message_text" class="form-label">Your Message</label>
        <textarea id="message_text" class="form-control" v-model="messageText" placeholder="Type your message..." @focus="error.message_text=''" @focusout="validateMessageText"></textarea>
        <div class="error-text" v-if="error.message_text">{{ error.message_text }}</div>
      </div>

      <div class="row">
        <div class="col">
          <button type="submit" class="btn-primary w-100">Send</button>
        </div>
        <div class="col">
          <button class="btn-cancel w-100" @click="closePopup">Cancel</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: "NegotiateForm",
  props: {
    adRequestId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      messageText: '',
      messages: [],
      error: {
        message_text: '',
      },
      userID: this.userID,
    };
  },
  mounted() {
    this.fetchMessages();
  },
  methods: {
    resetErrors() {
      this.error = {
        message_text: '',
      };
    },
    closePopup() {
      this.resetErrors();
      this.$emit('close');
    },
    validateMessageText() {
      this.error.message_text = '';
      if (!this.messageText) {
        this.error.message_text = "Message cannot be empty.";
        return false;
      }
      return true;
    },
    async fetchMessages() {
      try {
        const url = `http://127.0.0.1:5000/auth/messages`;
        const params = new URLSearchParams({
            ad_request_id:this.adRequestId
        })
        const response = await fetch(`${url}?${params.toString()}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": this.token,
          },
        });
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const data = await response.json();
        this.messages = data;
      } catch (error) {
        console.error("Failed to fetch messages:", error);
      }
    },
    async submitForm(event) {
      event.preventDefault();
      if (this.validateMessageText()) {
        const payload = {
          ad_request_id: this.adRequestId,
          message_text: this.messageText,
          sender_id: this.userID,
        };
        try {
          const url = 'http://127.0.0.1:5000/auth/messages';
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": this.token,
            },
            body: JSON.stringify(payload),
          });
          if (response.ok) {
            // Clear message text and fetch updated messages
            this.messageText = '';
            this.fetchMessages();
          } else {
            console.error("Failed to send message");
          }
        } catch (error) {
          console.error("Error sending message:", error);
        }
      }
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    }
  },
  computed: {
    ...mapGetters(['isDarkTheme', 'token', 'userType', 'userID'])
  },
};
</script>
<style scoped>
/* General layout */
.popup-container {
    position: fixed;
    top: 50%;
    left: 50%; /* Adjusted to ensure the popup is centered even with a larger width */
    transform: translate(-50%, -53%); /* Keeps the centering in place */
    background: rgba(0, 0, 0, 0.5);
    border-radius: 2%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.container {
    max-width: 33vw;
    max-height: 90vh;
    width: 100%;
    margin: 1.5vh auto;
}
/* Form styling */
.detail-form-light {
  display: flex;
  flex-direction: column;
  background: linear-gradient(60deg, #92c7cf, #aad7d9, #fbf9f1, #e5e1da, #fbf9f1, #aad7d9, #92c7cf);
  background-size: 300%;
  animation: animate 9s linear infinite alternate;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
}

.detail-form-dark {
  display: flex;
  flex-direction: column;
  background: linear-gradient(60deg, #2c3e4f, #3b5261, #20232a, #3b5261, #2c3e4f);
  background-size: 300%;
  border: 1px solid #444;
  animation: animate 9s linear infinite alternate;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.messages-area {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
  max-height: 12rem;
  padding:0.25rem;
}

.message-item {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.message-item p {
  margin: 0;
}

.message-item-light {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.message-item-light p {
  margin: 0;
}

/* For Dark Theme */
.message-item-dark {
  background-color: #444;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  color: #fff;  /* Ensures text is visible on dark background */
}

.message-item-dark p {
  margin: 0;
}

.error-text {
  color: #dc3545;
  font-size: smaller;
  font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
  margin-top: 0;
  text-align: left;
}

button[type="submit"] {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #3c89db;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.btn-cancel {
    display: inline-block;
    font-weight: 400;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    user-select: none;
    border: 1px solid transparent;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: 0.375rem;
    height: 2.9rem;
    width: Auto;
    color: #fff;
    background-color: #f72234; /* Light red background */
    border-color: #f5c2c7; /* Slightly darker border for contrast */
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
</style>
