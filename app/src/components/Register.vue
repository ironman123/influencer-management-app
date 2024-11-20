<template>
    <div :class="['container', { 'dark-theme': isDarkTheme }]">
      <form class="p-4 shadow rounded border" action="/" method="post" :class="[ isDarkTheme ? 'detail-form-dark' : 'detail-form-light']" @submit="validateForm">
        <h2 class="text-center mb-4 text-primary" :class="[isDarkTheme ? 'glow-text-dark' : 'glow-text-light']">Register</h2>
        <div class="row">
            <div class="col">
            <!-- User Type Selection -->
              <div class="mb-3">
                <label for="user-type" class="form-label">Register as</label>
                <select id="user-type" class="form-control" v-model="userType" @change="handleUserTypeChange" @focusout="validateUser">
                  <!-- <option value="influencer">Influencer</option>
                  <option value="sponsor">Sponsor</option> -->
                  <option v-for="option in userTypeOptions" 
                    :key="option.value"
                    :value="option.value" 
                    :id="'user-type-'+option.value"
                    >{{ option.label }}
                  </option>
                </select>
              </div>
            </div>        
            <div v-if="userType === 'influencer'"  class="col">
              <!-- Influencer Platform Selection -->
              <div v-show="userType === 'influencer'" class="mb-3">
                <label for="platform" class="form-label">Select Platform(s)</label>
                <div
                  id="platform"
                  :class="['custom-multi-select rounded p-2', isDarkTheme ? 'custom-multi-select-dark' : 'custom-multi-select-light']"
                  style="height: 3.15rem; overflow-y: auto;"
                  @focusout="validateOptions"
                >
                  <div v-for="option in platformOptions" :key="option.value" class="form-check">
                    <input
                      type="checkbox"
                      class="form-check-input"
                      :id="'platform-' + option.value"
                      :value="option.value"
                      v-model="platforms"
                    />
                    <label
                      class="form-check-label"
                      :for="'platform-' + option.value"
                    >{{ option.label }}</label>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="userType === 'sponsor'" class="col" @focusout="validateForm">
                <!-- Sponsor Industry Selection -->
                <div class="mb-3">
                    <label for="industry" class="form-label">Select Industry</label>
                    <select id="industry" class="form-control" v-model="industry" @focusout="validateOptions">
                        <option value="" disabled>Select industry</option>
                        <option v-for="option in industryOptions" 
                          :key="option.value"
                          :value="option.value" 
                          :id="'industry-type-'+option.value"
                          >{{ option.label }}
                        </option>
                    </select>
                </div>
            </div>
        </div>
  
        <!-- Common Fields: Name and Email -->
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input type="text" id="name" class="form-control" v-model="fullname" placeholder="Enter your full name" @focusout="validateFullName" />
        </div>
  
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input type="email" id="email" class="form-control" v-model="email" placeholder="user@email.com" @focusout="validateEmail"  />
        </div>
  
        <div class="row">
            <div class="col">
                <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" id="password" class="form-control" v-model="password" placeholder="Enter your password" @focusout="validatePassword" />
                </div>
            </div>
            <div class="col">
                <div class="mb-3">
                <label for="confirm-password" class="form-label">Confirm Password</label>
                <input type="password" id="confirm-password" class="form-control" v-model="confirmPassword" placeholder="Confirm your password" @focusout="validatePassword" />
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
        userTypeOptions:[
          { value: "influencer", label: "Influencer" },
          { value: "sponsor", label: "Sponsor" },
        ],
        platforms: [], // influencer platform
        platformOptions: [
          { value: "instagram", label: "Instagram" },
          { value: "facebook", label: "Facebook" },
          { value: "youtube", label: "YouTube" },
        ],
        industry: "", // sponsor industry
        industryOptions: [
          { value: "technology", label: "Technology" },
          { value: "fashion", label: "Fashion" },
          { value: "food", label: "Food" },
          { value: "health", label: "Health" },
        ],
        fullname: "", // full name
        email: "", // email
        password: "", // password
        confirmPassword: "", // confirm password
        error:{
          userType:"",
          platforms:"",
          industry:"",
          fullname:"",
          email:"",
          password:"",
          confirmPassword:""
        }
      };
    },
    methods: {
      handleUserTypeChange() {
        this.platforms = []; // Reset platform when user type changes
        this.industry = ""; // Reset industry when user type changes
      },
      validateUser()
      {
        this.error.userType="";
        if(!this.userTypeOptions.some(option=>option.value !== this.userType))
        {
          this.error.userType = "Invalid User Type!";
          return false;
        }
        return true;
      },
      validateOptions()
      {
        if(this.userType === 'influencer')
        {
          this.error.platforms="";
          if(this.platforms.length == 0)
          {
            this.error.platforms="Select Atleast One!";
            return false;
          }
          else
          {
            const validOptions = this.userTypeOptions.map(a=>a.value);
            if(!this.platforms.every(platform=>validOptions.includes(platform.value)))
            {
              this.error.platforms="Invalid Platform Selected!"
              return false;
            }
          }
          return true;
        }
        else if(this.userType === "sponsor")
        { 
          this.error.industry = "";
          if(this.industry === "" || this.industryOptions.some(option=>option.value !== this.industry))
          {
            this.error.industry = "Invalid Industry!";
            return false;
          }
          return true;
        }
      },
      validateFullName()
      {
        this.error.fullname ="";
        if(this.fullname === "" || this.fullname.length < 3)
        {
          this.error.fullname = "Please Enter a Valid Full Name!";
          return false;
        }
        return true;
      },
      validateEmail()
      {
        this.error.email="";
        if(!this.email.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/))
        {
          this.error.email="Incorrect Email Format!"; 
          return false;
        }
        return true;
      },
      validatePassword()
      {
        this.error.password="";
        this.error.confirmPassword="";
        if (this.password.length < 5) 
        {
          this.error.password = "Password too Short!";
          return false;
        }
        else if(this.password !== this.confirmPassword)
        {
          this.error.confirmPassword = "Passwords does not match!";
          return false;
        }
        return true;
      },
      validateForm(event)
      {
        event.preventDefault();
        this.validateUser();
        this.validateOptions();
        this.validateFullName();
        this.validateEmail();
        this.validatePassword();
        console.log(this.error);
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
    watch:{
      
    }
  };
</script>
  
<style scoped>
  /* General layout */
  .container {
    width: 100%;
    max-height: 90vh;
    min-width: 45vw;
    max-width: 45vw;
    margin: 1.5vh auto;
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
  .detail-form-dark input,
  .detail-form-dark select,
  .detail-form-dark textarea {
      background-color: #2c3e4f;
      color: #fff; /* Text color for better contrast */
      border: 1px solid #444;
      border-radius: 5px;
  }
  .detail-form-dark input::placeholder,
  .detail-form-dark textarea::placeholder {
      color: #aaa; /* Placeholder text color */
  }
  .detail-form-dark input:focus,
  .detail-form-dark select:focus,
  .detail-form-dark textarea:focus {
      outline: none;
      border-color: #007bff;
      box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
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
    background-color: #3c89db;
  }

  .custom-multi-select {
    font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
    font-size: 0.9rem;
    background-color: #fff;
  }

  .form-check {
    display: flex;
    align-items: center;
  }

  .form-check-input {
    margin-right: 0.5rem;
  }

  input:hover, select:hover, .custom-multi-select:hover {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  }
  .custom-multi-select-light {
    font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 8px;
  }

  .custom-multi-select-dark {
    font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
    background-color: #2c3e4f;
    border: 1px solid #444;
    border-radius: 5px;
    padding: 8px;
    color: #ddd; /* Text color for dark theme */
  }

  .custom-multi-select-dark .form-check-input {
    background-color: #3b5261;
    border-color: #555;
  }

  .custom-multi-select-dark .form-check-label {
    color: #ddd; /* Checkbox label text color in dark theme */
  }
</style>
  