<template>
    <div class="campaign-card card mb-3">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">{{ campaign.name }}</h5>
        <span class="badge" :class="campaign.visibility === 'public' ? 'bg-success' : 'bg-secondary'">
          {{ campaign.visibility }}
        </span>
      </div>
      <div class="card-body">
        <strong>Description:</strong>
        <p class="card-text"> {{ campaign.description }}</p>
        <strong>Goals:</strong>
        <p class="card-text"> {{ campaign.goals }}</p>
        <p class="card-text">
          <strong>Start Date:</strong> {{ formatDate(campaign.start_date) }} <br />
          <strong>End Date:</strong> {{ formatDate(campaign.end_date) }}
        </p>
        <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
      </div>
      <div class="card-footer d-flex justify-content-between align-items-center">
        <div>
          <button class="btn btn-primary btn-sm" @click="viewCampaign">View</button>
          <button
            v-if="isSponsor"
            class="btn btn-warning btn-sm"
            @click="editCampaign"
          >
            Edit
          </button>
          <button
            v-if="isAdmin"
            class="btn btn-secondary btn-sm"
            @click="toggleFlag"
          >
            Toggle Flag
          </button>
          <button
            v-if="isInfluencer || isSponsor"
            class="btn btn-info btn-sm"
            @click="requestAd"
          >
            Ad Request
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CampaignCard",
    props: {
      campaign: {
        type: Object,
        required: true,
      },
      userType: {
        type: String, // e.g., 'admin', 'sponsor', 'influencer'
        required: true,
      },
      userName: {
        type: String,
        required: true,
      },
      userID: {
        type: String,
        required: true,
      },
    },
    computed: {
      isSponsor() {
        return this.campaign.sponsor_id === Number(this.userID);
      },
      isAdmin() {
        return this.userType === "admin";
      },
      isInfluencer() {
        return this.userType === "influencer";
      },
    },
    methods: {
      formatDate(date) {
        const options = { year: "numeric", month: "long", day: "numeric" };
        return new Date(date).toLocaleDateString(undefined, options);
      },
      viewCampaign() {
        // Implement viewing logic
        alert(`Viewing campaign: ${this.campaign.name}`);
      },
      editCampaign() {
        // Implement editing logic
        alert(`Editing campaign: ${this.campaign.name}`);
      },
      toggleVisibility() {
        // Implement visibility toggle logic
        alert(
          `Toggling visibility for campaign: ${this.campaign.name}`
        );
      },
      requestAd() {
        // Implement ad request logic
        alert(`Requesting ad for campaign: ${this.campaign.name}`);
      },
    },
  };
</script>
  
<style scoped>
    .campaign-card {
      border: 1px solid #ddd;
      border-radius: 0.25rem;
    }

    .card-header {
      background-color: #f8f9fa;
    }
    .card-body{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .card-footer {
      background-color: #f8f9fa;
    }

    .badge {
      font-size: 0.8rem;
      padding: 0.5em;
    }

    .btn {
      margin-right: 0.5em;
    }
    .card-text
    {
      overflow: auto;
      text-overflow: ellipsis;
      word-wrap: break-word;
      word-break: break-word;
      max-width: 60rem;
      max-height: 6rem;
    }
    .card-text::-webkit-scrollbar {
        display: none;
    }
</style>
  