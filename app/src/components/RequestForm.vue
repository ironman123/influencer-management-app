<template>
    <div :class="['container popup-container', { 'dark-theme': isDarkTheme }]">
      <form class="p-4 shadow rounded border" action="/" method="post" :class="[ isDarkTheme ? 'detail-form-dark' : 'detail-form-light']" @submit="submitForm">
        <h2 class="text-center mb-4 text-primary" :class="[isDarkTheme ? 'glow-text-dark' : 'glow-text-light']">Add Request</h2>
        <!-- Campaign Select with Search -->
        <div class="mb-3">
          <label for="campaign_id" class="form-label">Campaign</label>
          <select id="campaign_id" class="form-control" v-model="campaign_id" @focus="error.campaign_id=''" @focusout="validateCampaignID">
            <!-- <option v-for="campaign in campaigns" :key="campaign.id" :value="`${campaign.id},${campaign.sponsor_id}`">{{ campaign.name }}</option> -->
            <option v-for="campaign in campaigns" :key="campaign.id" :value="`${campaign.id},${campaign.sponsor_id}`">{{ campaign.name }}</option>
          </select>
          <div class="error-text" v-if="error.campaign_id">{{ error.campaign_id }}</div>
        </div>

        <!-- Influencer Select with Search -->
        <div v-if="userType !== 'Influencer'" class="mb-3">
          <label for="influencer_id" class="form-label">Influencer</label>
          <select id="influencer_id" class="form-control" v-model="influencer_id" @focus="error.influencer_id=''" @focusout="validateInfluencerID">
            <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id "> {{ influencer.name }} :({{ influencer.email }})</option>
          </select>
          <div class="error-text" v-if="error.influencer_id">{{ error.influencer_id }}</div>
        </div>
        
        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label for="requirements" class="form-label">Requirements</label>
                    <input type="text" id="requirements" class="form-control" v-model="requirements" placeholder="Something about the Ad Request" @focusout="validateRequirements" @focus="error.requirements=''"/>
                    <div class="error-text" v-if="error.requirements">{{ error.requirements }}</div>
                </div>
            </div>
            <div class="col">
                <div class="mb-3">
                    <label for="payment_amount" class="form-label">Payment Amount</label>
                    <input type="number" id="payment_amount" class="form-control" v-model="payment_amount" placeholder="1000" @focusout="validatePayment_amount" @focus="error.payment_amount=''"/>
                    <div class="error-text" v-if="error.payment_amount">{{ error.payment_amount }}</div>
                </div>        
            </div>
        </div>
        
        <div class="row">
            <div class="col">
                <button type="submit" class="btn-primary w-100">Request</button>
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
    name: "RequestForm",
    props:{
      data:{
        type:Object,
        default: null,
      },
      campaign:{
        type:Object,
        default:null
      },
      influencer:{
        type:Object,
        default:null
      }
    },
    data() {
      return {
        campaigns:[],
        influencers:[],
        to: this.data ? this.data.to : null, 
        from: this.data ? this.data.from : null, 
        campaign_id: this.data ? this.data.campaign_id : null,
        influencer_id: this.data ? this.data.influencer_id : null,
        requirements: this.data ? this.data.requirements : "",
        payment_amount: this.data ? this.data.payment_amount : 0,
        status: this.data ? this.data.status : 'Pending',

        // startDate: this.data ? new Date(this.data.startDate).toISOString().split('T')[0] : "", 
        // endDate: this.data ? new Date(this.data.endDate).toISOString().split('T')[0] : "",
        
        error:{
            to: "", 
            from: "", 
            campaign_id:"",
            influencer_id: "",
            requirements: "", 
            payment_amount: "",
            status: ""
        }
      };
    },
    mounted() {
      this.fetchCampaigns();
      if (this.userType === 'Influencer'){
        console.log()
      }
      else if(this.userType === 'Sponsor')
      {
        this.fetchInfluencers();
      }
      
      this.from=this.userID
    },
    methods: {
        resetErrors() {
            this.error = {
            to: "", 
            from: "", 
            campaign_id:"",
            influencer_id: "",
            requirements: "", 
            payment_amount: "",
            status: ""
          };
        },
        closePopup() {
            this.resetErrors();
            this.$emit('close');
        },
        validateCampaignID()
        {
          this.error.campaign_id = "";
          if (!this.campaign_id) {
            this.error.campaign_id = "Please select a campaign.";
          }
          else{
            const [selectedCampaignID, selectedSponsorID] = this.campaign_id.split(',');
            if (this.userType === 'Influencer'){
              this.to=selectedSponsorID;
            }
            this.campaign_id=selectedCampaignID;
          }
        },
        validateInfluencerID()
        {
          this.error.influencer_id = "";
          if (!this.influencer_id) {
            this.error.influencer_id = "Please select an influencer.";
          }
          if (this.userType === 'Sponsor'){
            this.to = this.influencer_id;
          }
        },
        validateRequirements()
        {
          
        },
        validatePayment_amount()
        {
          this.error.payment_amount ="";
          if(this.payment_amount < 0)
          {
            this.error.payment_amount = "Payment Cannot Be Negative!";
            return false;
          }
          return true;
        },
        
        validateForm()
        {
          return (this.validateCampaignID()
              && this.validateInfluencerID()
              && this.validateRequirements()
              && this.validatePayment_amount()
          );
        },
        async submitForm(event) {
          event.preventDefault();
          if (this.validateForm()) {
            // handle form submission
            const isEdit = !!this.data; // Determine if it's an edit
            console.log("isEdit:",isEdit);
            const url = 'http://127.0.0.1:5000/auth/requests';
            const payload = {
              to_:this.to,
              from_:this.from,
              campaign_id:this.campaign_id,
              influencer_id:this.influencer_id,
              requirements:this.requirements,
              payment_amount:this.payment_amount,
              status:this.status
            }
            if (isEdit)
            {
              payload.id=this.data.id;
            }
            const method = isEdit ? "PUT" : "POST";
            console.log(payload)
            try{
                console.log("Adding Request: ",payload)
                const response = await fetch(url,{
                    method:method,
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
        async fetchCampaigns() {
          try {
            const url = "http://127.0.0.1:5000/auth/campaigns";
            const headers = {
              "Content-Type": "application/json",
              "Authorization":this.token,
              // "search-query": this.searchQuery,
            };
            const response = await fetch(url, {
              method: "GET",
              headers: headers,
            });
            if (!response.ok) {
              throw new Error(`API error: ${response.status}`);
            }
            const data = await response.json();
            this.campaigns = data;
          } catch (error) {
            console.error("Failed to fetch campaigns:", error);
          }
        },
        async fetchInfluencers() {
          try {
            const url = "http://127.0.0.1:5000/auth/users";
            const headers = {
              "Content-Type": "application/json",
              "Authorization": this.token,
              "search-query": this.searchQuery, // If needed, you can still pass the search query
            };
            const params = new URLSearchParams({
              type: 'Influencer' // This parameter filters the users by type on the server side
            });
          
            const response = await fetch(`${url}?${params.toString()}`, {
              method: "GET",
              headers: headers,
            });
          
            if (!response.ok) {
              throw new Error(`API error: ${response.status}`);
            }
          
            const data = await response.json();
            this.influencers = data;
          } catch (error) {
            console.error("Failed to fetch users:", error);
          }
        },
    },
    computed:{
      ...mapGetters(['isDarkTheme','token','userType','userID'])
    },
    watch:{
      from(v){
        console.log('From: ',v);
      },
      to(v){
        console.log('To: ',v);
      },
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
  