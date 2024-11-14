<template>
    <div :class="['container', { 'dark-theme': isDarkTheme }]">
      <form class="p-4 shadow rounded border" action="/" method="post" :class="[ isDarkTheme ? 'detail-form-dark' : 'detail-form-light']">
        <h2 class="text-center mb-4 text-primary" :class="[isDarkTheme ? 'glow-text-dark' : 'glow-text-light']">Register</h2>
        
        <div class="row">
            <div class="col">
            <!-- User Type Selection -->
                <div class="mb-3">
                    <label for="user-type" class="form-label">Register as</label>
                    <select id="user-type" class="form-control" v-model="userType" @change="handleUserTypeChange" required>
                        <option value="influencer">Influencer</option>
                        <option value="sponsor">Sponsor</option>
                    </select>
                </div>
            </div>        
            <div v-if="userType === 'influencer'"  class="col">
                <!-- Influencer Platform Selection -->
                <div v-show="userType === 'influencer'" class="mb-3">
                    <label for="platform" class="form-label">Select Platform</label>
                    <select id="platform" class="form-control" v-model="platform" required>
                        <option value="" disabled>Select platform</option>
                        <option value="instagram">Instagram</option>
                        <option value="facebook">Facebook</option>
                        <option value="youtube">YouTube</option>
                    </select>
                </div>
            </div>
            <div v-if="userType === 'sponsor'" class="col">
                <!-- Sponsor Industry Selection -->
                <div class="mb-3">
                    <label for="industry" class="form-label">Select Industry</label>
                    <select id="industry" class="form-control" v-model="industry" required>
                        <option value="" disabled>Select industry</option>
                        <option value="tech">Technology</option>
                        <option value="fashion">Fashion</option>
                        <option value="food">Food</option>
                        <option value="health">Health</option>
                    </select>
                </div>
            </div>
        </div>
  
        <!-- Common Fields: Name and Email -->
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input type="text" id="name" class="form-control" v-model="name" placeholder="Enter your full name" required />
        </div>
  
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input type="email" id="email" class="form-control" v-model="email" placeholder="user@email.com" required />
        </div>
  
        <div class="row">
            <div class="col">
                <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" id="password" class="form-control" v-model="password" placeholder="Enter your password" required />
                </div>
            </div>
            <div class="col">
                <div class="mb-3">
                <label for="confirm-password" class="form-label">Confirm Password</label>
                <input type="password" id="confirm-password" class="form-control" v-model="confirmPassword" placeholder="Confirm your password" required />
                <div class="error-text">{{ passwordError }}</div>
                </div>
            </div>
        </div>
  
        <button type="submit" class="btn-primary w-100">Register</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "RegisterForm",
    props:{
      isDarkTheme: {
        type: Boolean,
        default: false,
      }
    },
    data() {
      return {
        userType: "influencer", // influencer or sponsor
        platform: "", // influencer platform
        industry: "", // sponsor industry
        name: "", // full name
        email: "", // email
        password: "", // password
        confirmPassword: "", // confirm password
        passwordError: "", // password mismatch error message
      };
    },
    methods: {
      handleUserTypeChange() {
        this.platform = ""; // Reset platform when user type changes
        this.industry = ""; // Reset industry when user type changes
      },
      validateForm() {
        if (this.password !== this.confirmPassword) {
          this.passwordError = "Passwords do not match!";
          return false;
        }
        this.passwordError = "";
        return true;
      },
      submitForm(event) {
        event.preventDefault();
        if (this.validateForm()) {
          // handle form submission
          console.log({
            userType: this.userType,
            platform: this.platform,
            industry: this.industry,
            name: this.name,
            email: this.email,
            password: this.password,
          });
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* General layout */
  .container {
    width: 100%;
    max-height: 90vh;
    min-width: 45vw;
    max-width: 45vw;
    margin: 0 auto;
  }
  
  /* Form styling */
  .glow-text-light {
    font-size: 1.9em;
    font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
    font-weight: 600;
    text-align: center;
    background: linear-gradient(50deg, #0F1035, #365486, #6d9ee7, #4b4eee, #6d9ee7, #365486, #0F1035);
    background-size: 300%;
    -webkit-text-fill-color: transparent;
    -webkit-background-clip: text;
    animation: animate 10s linear infinite alternate;
    }
    .glow-text-dark {
        font-size: 1.9em;
        font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
        font-weight: 600;
        text-align: center;
        background: linear-gradient(150deg, #8b8cf0, #6d9ee7, #9abef1, #b5c6f4, #9abef1, #6d9ee7, #8b8cf0);
        background-size: 300%;
        -webkit-text-fill-color: transparent;
        -webkit-background-clip: text;
        animation: animate 10s linear infinite alternate; /* Ensures animation is still applied in dark theme */
    }
  .detail-form-light {
    display: flex;
    flex-direction: column;
    font-family: 'Josefin Sans', sans-serif;
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
        font-family: 'Josefin Sans', sans-serif;
        background: linear-gradient(60deg, #2c3e4f, #3b5261, #20232a, #3b5261, #2c3e4f);
        background-size: 300%;
        border: 1px solid #444;
        animation: animate 9s linear infinite alternate; /* Ensures animation is still applied in dark theme */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #ddd;
    }
  
  @keyframes animate {
    0% {
      background-position: 0%;
    }
    100% {
      background-position: 100%;
    }
  }
  
  /* Text styling */
  h2.text-primary {
    font-weight: 600;
    background-size: 300%;
    color: transparent;
    -webkit-background-clip: text;
    animation: animate 10s linear infinite alternate;
  }
  
  /* Input and button styling */
  .form-control {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    margin-top: 8px;
    margin-bottom: 10px;
  }
  
  .form-label {
    display: block;
    text-align: left;
    margin-left: 0.5vw;
  }
  
  button[type="submit"] {
    padding: 12px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    margin:auto;
    max-width: 75%;
  }
  
  button[type="submit"]:hover {
    background-color: #0056b3;
  }
  </style>
  