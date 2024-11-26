<template>
    <div :class="['container popup-container', { 'dark-theme': isDarkTheme }]">
      <form class="p-4 shadow rounded border" action="/" method="post" :class="[ isDarkTheme ? 'detail-form-dark' : 'detail-form-light']" @submit="submitForm">
        <h2 class="text-center mb-4 text-primary" :class="[isDarkTheme ? 'glow-text-dark' : 'glow-text-light']">Add Campaign</h2>
        <!-- Common Fields: Name and Email -->
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" id="name" class="form-control" v-model="name" placeholder="Campaign Name" @focusout="validateName" @focus="error.name=''"/>
            <div class="error-text" v-if="error.name">{{ error.name }}</div>
        </div>

        <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <input type="text" id="description" class="form-control" v-model="description" placeholder="Description..." @focusout="validateDescription" @focus="error.description=''"/>
            <div class="error-text" v-if="error.description">{{ error.description }}</div>
        </div>
        
        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label for="goals" class="form-label">Goal</label>
                    <input type="number" id="goals" class="form-control" v-model="goals" placeholder="100" @focusout="validateGoal" @focus="error.goals=''"/>
                    <div class="error-text" v-if="error.goals">{{ error.goals }}</div>
                </div>
            </div>
            <div class="col">
                <div class="mb-3">
                    <label for="budget" class="form-label">Budget</label>
                    <input type="number" id="budget" class="form-control" v-model="budget" placeholder="1000" @focusout="validateBudget" @focus="error.budget=''"/>
                    <div class="error-text" v-if="error.budget">{{ error.budget }}</div>
                </div>        
            </div>
            <div class="col">
                <div class="mb-3">
                <label for="visibility" class="form-label">Visibility</label>
                <select id="visibility" class="form-control" v-model="visibility" @change="handleUserTypeChange" @focusout="validateUser">
                  <option v-for="option in [{ value: 'public', label: 'Public' },{ value: 'private', label: 'Private' }]" 
                    :key="option.value"
                    :value="option.value" 
                    :id="'visibility-'+option.value"
                    >{{ option.label }}
                  </option>
                </select>
                <div class="error-text" v-if="error.userType">{{ error.userType }}</div>
              </div>
            </div>
        </div>
        
  
        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label for="start-date" class="form-label">Start Date:</label>
                    <input type="date" id="start-date" class="form-control" v-model="startDate" placeholder="Enter your password" @focusout="validateStartDate" @focus="error.startDate=''"/>
                    <div class="error-text" v-if="error.startDate">{{ error.startDate }}</div>
                </div>
            </div>
            <div class="col">
                <div class="mb-3">
                    <label for="end-date" class="form-label">End Date:</label>
                    <input type="date" id="end-date" class="form-control" v-model="endDate" placeholder="Enter your password" @focusout="validateEndDate" @focus="error.endDate=''"/>
                    <div class="error-text" v-if="error.endDate">{{ error.endDate }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <button type="submit" class="btn-primary w-100">Register</button>
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
    name: "RegisterForm",
    props:{
    },
    data() {
      return {
        name: "", 
        description: "", 
        goals:0,
        budget: 0,
        startDate: "", 
        endDate: "", 
        visibility:"public",
        error:{
            name: "", 
            description: "", 
            goals:"",
            budget: "",
            startDate: "", 
            endDate: "",
            visibility: ""
        }
      };
    },
    methods: {
        resetErrors() {
            this.error = {
            name: "", 
            description: "", 
            goals: "",
            budget: "",
            startDate: "", 
            endDate: "",
            visibility: ""
            };
        },
        closePopup() {
            this.resetErrors();
            this.$emit('close');
        },
        validateName()
        {
          this.error.name ="";
          if(this.name === "" || this.name.length < 3)
          {
            this.error.name = "Please Enter a Valid Name!";
            return false;
          }
          return true;
        },
        validateDescription()
        {
          this.error.description ="";
          if(this.description === "" || this.description.length < 15)
          {
            this.error.description = "Please Enter a Brief Description!";
            return false;
          }
          return true;
        },
        validateGoal()
        {
          this.error.goals ="";
          if(this.goals === 0 || this.goals < 0)
          {
            this.error.goals = "Goal Should be Greater than 0!";
            return false;
          }
          return true;
        },
        validateBudget()
        {
          this.error.budget ="";
          if(this.budget < 0)
          {
            this.error.budget = "Budget Cannot Be Negative!";
            return false;
          }
          return true;
        },
        validateStartDate()
        {
          this.error.startDate = "";
          const today = new Date().toISOString().split('T')[0];
          if (this.startDate === "") {
              this.error.startDate = "Start date cannot be empty!";
              return false;
          } else if (this.startDate < today) {
              this.error.startDate = "Start date cannot be in the past!";
              return false;
          }
          return true;
        },
        validateEndDate()
        {
          this.error.endDate = "";
          const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
          if (this.endDate === "") {
              this.error.endDate = "End date cannot be empty!";
              return false;
          } else if (this.endDate < today) {
              this.error.endDate = "End date cannot be in the past!";
              return false;
          } else if (this.endDate <= this.startDate) {
              this.error.endDate = "End date must be after start date!";
              return false;
          }
          return true;
        },
        validateVisibility()
        {
          this.error.visibility="";
          if(this.visibility !== "public" && this.visibility !== "private")
          {
              this.error.visibility = "Invalid Visibility!";
              return false;
          }
          return true;
        },    
        validateForm()
        {
          return (this.validateName()
              && this.validateDescription()
              && this.validateGoal()
              && this.validateBudget()
              && this.validateStartDate()
              && this.validateEndDate()
              && this.validateVisibility()
          );
        },
        async submitForm(event) {
          event.preventDefault();
          if (this.validateForm()) {
            // handle form submission
            const url = 'http://127.0.0.1:5000/auth/campaigns';
            const payload = {
              name:this.name,
              description:this.description,
              budget:this.budget,
              goals:this.goals,
              startDate:this.startDate,
              endDate:this.endDate,
              visibility:this.visibility
            }
            console.log(payload)
            try{
                console.log("Adding Campaign: ",payload)
                const response = await fetch(url,{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authorization":this.token
                    },
                  body:JSON.stringify(payload)
                })
                if(response.ok)
                {
                    this.closePopup();
                }
                else if(response.status == 400)
                {
                    const data = await response.json();
                    this.error.name=data['message']
                }
                else if(response.status == 403)
                {
                  const data = await response.json();
                  this.error.name=data['message']
                }
            }
            catch(error)
            {
                this.error.name = "Network Error! Please try again.";
                // this.error.password = "Network Error! Please try again.";
            }
          }

        },
    },
    computed:{
      ...mapGetters(['isDarkTheme','token'])
    },
    watch:{
      
    }
  };
</script>
  
<style scoped>
    .popup-container {
        width: auto;
        height: auto;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-30%, -53%);
        background: rgba(0, 0, 0, 0.5);
        border-radius: 2%;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
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

  /* Error text */
  .error-text {
    color: #dc3545;
    font-size: smaller;
    font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
    animation: shake 0.21s 0.1s;
    margin-top: 0;
    text-align: left;
    margin-left: 0.5vw;
  }
  @keyframes shake {
      0%,100% {
        transform: translateX(0);
    }
      25%,75% {
        transform: translateX(-0.72em);
    }
      50% {
        transform: translateX(1em);
    }
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

.btn-cancel:hover {
    background-color: #f83044; /* Slightly darker on hover */
    border-color: #f1b0b7; /* Adjust border for hover effect */
    color: #fff; /* Keep text white */
    text-decoration: none;
}

.btn-cancel:focus {
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25); /* Light red focus shadow */
}

.btn-cancel:active {
    background-color: #e93042; /* Even darker when active */
    border-color: #eea1a8; /* Adjust border for active effect */
}

.btn-cancel.disabled,
.btn-cancel:disabled {
    opacity: 0.65;
    background-color: #f8d7da;
    border-color: #f5c2c7;
    cursor: not-allowed;
}

</style>
  