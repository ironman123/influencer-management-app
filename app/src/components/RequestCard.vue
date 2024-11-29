<template>
  <div :class="['request-card card mb-3', { dark: isDarkTheme }]">
    <div :class="['card-header d-flex justify-content-between align-items-center', { dark: isDarkTheme }]">
    <!-- Card Title aligned to the start -->
    <h5 class="card-title mb-0">{{ request.campaignName }}</h5>
    
    <!-- Visibility Badge aligned to the end -->
      <div>
        <!-- <span style="margin-right: 0.5rem;" :class="['badge', { 'bg-success': request.visibility === 'public', 'bg-secondary': request.visibility !== 'public' }, { dark: isDarkTheme }]">
          {{ request.status }}
        </span> -->

        <!-- Status Badge aligned to the end with color changes based on the status -->
        <span :class="[
              'badge',
              { 'bg-info': request.status === 'Pending', 
                'bg-warning': request.status === 'Accepted', 
                'bg-danger': request.status === 'Rejected', 
                'bg-success': request.status === 'Completed' },
              { dark: isDarkTheme }
            ]"
        >
            {{ request.status }}
        </span>
      </div>
    </div>
    <div :class="['card-body', { dark: isDarkTheme }]">
      <p class="card-text"><strong>Sponsor:</strong> {{ request.sponsor }}</p>
      <strong>Requirements:</strong>
      <p class="card-text"> {{ request.requirements }}</p>
      <div class="row" style="width: 100%;">
        <div class="col">
          <p class="card-text"><strong>From:</strong> {{ request.fromUser }}</p>
        </div>
        <div class="col">
          <p class="card-text"><strong>To:</strong> {{ request.toUser }}</p>
        </div>
        <div class="col">
          <p class="card-text"><strong>Amount:</strong> {{ request.paymentAmount }}</p>
        </div>
      </div>
    </div>
    <div :class="['card-footer d-flex justify-content-between align-items-center', { dark: isDarkTheme }]">
      <div>
        <!-- <button class="btn btn-primary btn-sm" @click="viewRequest">View</button> -->
        <button
          v-if="isSponsor && request.status === 'Pending'"
          class="btn btn-info btn-sm"
          @click="editRequest"
        >
          Edit
        </button>
        <button
          v-if="request.status === 'Pending' && (isSponsor || isInfluencer)"
          class="btn btn-primary btn-sm"
          @click="negotiate"
        >
          Negotiate
        </button>
        <button
          v-if="isSponsor && request.status === 'Accepted'"
          class="btn btn-info btn-sm"
          @click="updateStatus('Completed')"
        >
          Complete
        </button>
        <button
          v-if="isInfluencer && request.status === 'Pending'"
          class="btn btn-success btn-sm"
          @click="updateStatus('Accepted')"
        >
          Accept Request
        </button>
        <button
          v-if="isInfluencer && request.status === 'Pending'"
          class="btn btn-danger btn-sm"
          @click="updateStatus('Rejected')"
        >
          Reject Request
        </button>
      </div>
      <div class="row" style="width: 60%;">
        <div class="col">
          <p class="card-text">
            <strong>Start Date:</strong> {{ formatDate(request.start_date) }}
          </p>    
        </div>
        <div class="col">
          <p class="card-text">
            <strong>End Date:</strong> {{ formatDate(request.end_date) }}
          </p>    
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { reject } from 'core-js/fn/promise';
import { mapGetters } from 'vuex';
export default {
  name: "RequestCard",
  props: {
    request: {
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
      return this.request.sponsor_id === Number(this.userID)&& this.userType == 'Sponsor';
    },
    isInfluencer() {
      return this.request.influencer_id === Number(this.userID) && this.userType == 'Influencer';
    },
    isAdmin() {
      return this.userType === "admin";
    },
    // isInfluencer() {
    //   return this.userType === "influencer";
    // },
  },
  methods: {
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    editRequest() 
    {
      this.$emit('edit-request',this.request)
    },
    updateStatus(status)
    {
      console.log('Emitting: ',status)
      this.$emit('update-status',this.request,status)
    },
    negotiate()
    {
      this.$emit('negotiate',this.request)
    }
  },
};
</script>

<style scoped>
.request-card {
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  transition: background 0.3s ease, color 0.3s ease;
}

.request-card.dark {
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
