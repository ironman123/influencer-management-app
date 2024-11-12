<template>
    <div class="container mt-5">
        <form class="detail-form p-4 shadow rounded border" action="/" method="post">
            <h2 class="text-center mb-4 text-primary">Sign In</h2>
            
            <div class="mb-3">
              <label for="user-name" class="form-label">Email address</label>
              <input type="email" class="form-control" id="user-name" name="username" placeholder="user@email.com" required />
              <div class="error-text">{{ userError }}</div>
            </div>
            
          
            <div class="mb-3">
              <label for="user-password" class="form-label">Password</label>
              <input type="password" class="form-control" id="user-password" name="password" placeholder="Password" required />
              <div class="error-text">{{ passwordError }}</div>
            </div>
          
            <button type="submit" class="btn-primary w-100">Submit</button>
        </form>
    </div>
</template>
  
<script>
  export default {
    name: "SignInForm",
    data() {
      return {
        userError: "", // Example error handling
        passwordError: "", // Example error handling
      };
    },
  };
</script>
  
<style scoped>
  /* General layout */
  .container {
    width: 100%;
    max-width: 24vw;
    margin: 0 auto;
  }
  
  /* Form styling */
  .detail-form {
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
    background: linear-gradient(50deg, #0f1035, #365486, #6d9ee7, #4b4eee, #6d9ee7, #365486, #0f1035);
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
    background-color: #0056b3;
  }
  
  /* Error text */
  /* .error-text {
    color: #dc3545;
    font-size: 14px;
    margin-top: 5px;
  } */
</style>
  