<template>
  <div :class="['campaign-card card mb-3', { dark: isDarkTheme }]">
    <div :class="['card-header d-flex justify-content-between align-items-center', { dark: isDarkTheme }]">
    <!-- Card Title aligned to the start -->
    <h5 class="card-title mb-0">{{ campaign.name }}</h5>
    
    <!-- Visibility Badge aligned to the end -->
      <div>
        <span style="margin-right: 0.5rem;" :class="['badge', { 'bg-success': campaign.visibility === 'public', 'bg-secondary': campaign.visibility !== 'public' }, { dark: isDarkTheme }]">
          {{ campaign.visibility }}
        </span>

        <!-- Status Badge aligned to the end with color changes based on the status -->
        <span :class="[
              'badge',
              { 'bg-danger': campaign.status === 'Flagged', 
                'bg-warning': campaign.status === 'Active', 
                'bg-success': campaign.status === 'Completed' },
              { dark: isDarkTheme }
            ]"
        >
            {{ campaign.status }}
        </span>
      </div>
    </div>
    <div :class="['card-body', { dark: isDarkTheme }]">
      <p class="card-text"><strong>Sponsor:</strong> {{ campaign.owner }}</p>
      <strong>Description:</strong>
      <p class="card-text"> {{ campaign.description }}</p>
      <div class="row" style="width: 100%;">
        <div class="col">
          <p class="card-text"><strong>Goals:</strong> {{ campaign.goals }}</p>
        </div>
        <div class="col">
          <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
        </div>
      </div>
      
      
    </div>
    <div :class="['card-footer d-flex justify-content-between align-items-center', { dark: isDarkTheme }]">
      <div>
        <!-- <button class="btn btn-primary btn-sm" @click="viewCampaign">View</button> -->
        <button
          v-if="isSponsor && campaign.status !== 'Completed'"
          class="btn btn-warning btn-sm"
          @click="editCampaign"
        >
          Edit
        </button>
        <button
          v-if="isAdmin && campaign.status !== 'Completed'"
          class="btn btn-secondary btn-sm"
          @click="toggleFlag"
        >
          Toggle Flag
        </button>
        <button
          v-if="(isInfluencer || isSponsor) && (campaign.status !== 'Flagged' && campaign.status !== 'Completed')"
          class="btn btn-info btn-sm"
          @click="requestAd"
        >
          Ad Request
        </button>
      </div>
      <div class="row" style="width: 60%;">
        <div class="col">
          <p class="card-text">
            <strong>Start Date:</strong> {{ formatDate(campaign.start_date) }}
          </p>    
        </div>
        <div class="col">
          <p class="card-text">
            <strong>End Date:</strong> {{ formatDate(campaign.end_date) }}
          </p>    
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
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
    ...mapGetters(['isDarkTheme']),
    isSponsor() {
      return this.campaign.sponsor_id === Number(this.userID);
    },
    isAdmin() {
      return this.userType === "admin";
    },
    isInfluencer() {
      return this.userType === "Influencer";
    },
  },
  methods: {
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    editCampaign() {
      this.$emit('edit-campaign',this.campaign)
    },
    toggleFlag() {
      this.$emit('toggle-flag',this.campaign);
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
  transition: background 0.3s ease, color 0.3s ease;
}

.campaign-card.dark {
  background-color: #333;
  color: #f4f4f4;
}

.card-header {
  background-color: #f8f9fa;
}

.card-header.dark {
  background-color: #444;
}

.card-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-body.dark {
  background-color: #444;
}

.card-footer {
  background-color: #f8f9fa;
}

.card-footer.dark {
  background-color: #444;
}

.badge {
  font-size: 0.8rem;
  padding: 0.5em;
}

.badge.dark {
  color: #f4f4f4;
}

.btn {
  margin-right: 0.5em;
}

.card-text {
  overflow: auto;
  text-overflow: ellipsis;
  /* word-break: break-word;
  word-wrap: break-word; */
  max-width: 60rem;
  max-height: 6rem;
}

.card-text::-webkit-scrollbar {
  display: none;
}

.card-text.dark {
  color: #f4f4f4;
}
</style>
