<template>
    <div :class="['container', { 'dark-theme': isDarkTheme }]">
        <form class="p-4 shadow rounded border" @submit="signIn" action="/" method="post" :class="[ isDarkTheme ? 'detail-form-dark' : 'detail-form-light']" >
            <h2 class="text-center mb-4 text-primary" :class="[isDarkTheme ? 'glow-text-dark' : 'glow-text-light']">Sign In</h2>
            
            <div class="mb-3">
              <label for="user-name" class="form-label">Email address</label>
              <input 
                type="text" 
                class="form-control" 
                id="user-name" 
                name="email" 
                v-model="email"
                placeholder="user@email.com" 
                @focus="error.email=''"
              />
              <div class="error-text" v-if="error.email">{{ error.email }}</div>
            </div>
                        
          
            <div class="mb-3">
              <label for="user-password" class="form-label">Password</label>
              <input 
              type="password" 
              class="form-control" 
              id="user-password" 
              name="password" 
              v-model="password"
              placeholder="Password"
              @focus="error.password=''"
            />
            <div class="error-text" v-if="error.password">{{ error.password }}</div>
            </div>
          
            <button type="submit" class="btn-primary w-100">Submit</button>
        </form>
    </div>
</template>
  
<script>
  export default {
    name: "SignInForm",
    props: {
      isDarkTheme: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        email: "",
        password: "",
        error:{
          email:"",
          password:""
        }
      };
    },
    methods:{
      signIn(event){
        event.preventDefault();
        this.error={
          email:"",
          password:"",
        };
        if(!this.email.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/))
        {
          this.error.email="Incorrect Email Format!";
          //console.log("email error");
          return;
        }
        else if(this.password.length < 5)
        {
          this.error.password="Password Too Short!";
          return;
        }
        else if (this.email === "user@email.com" && this.password === "12345") {
          this.$store.dispatch('signIn');
          this.$router.push('/dashboard');
        }
        else{
          this.error.email="Incorrect Email!";
          this.error.password="Incorrect Password!";
        }
        
      }
    },
    watch:{
      error(v){
        console.log(v);
      }
    }
  };
</script>
  
<style scoped>
  /* General layout */
  .container {
    font-family: 'Josefin Sans', 'Lucida Sans', 'sans-serif';
    width: 100%;
    min-width: 27vw;
    max-width: 27vw;
    margin: 1.5vh auto;
    color:#242a31;
  }
  
  /* Form styling */

    .glow-text-light {
        font-size: 1.9em;
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
  .form-label
  {
    display: block;  /* Ensures label takes full width */
    text-align: left;
    margin-left: 0.5vw;
  }
  button[type="submit"] {
    padding: 12px 20px;
    background-color: #007bff;
    color: white;
    margin: auto;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    max-width: 60%;
  }
  
  button[type="submit"]:hover {
    background-color: #3c89db;
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
</style>
  