<template>
  <div 
    class="sidebar-item" 
    @click="onClick" 
    :class="{ dark: isDarkTheme }"
  >
    <img 
      :src="icon" 
      :alt="name" 
      class="icon" 
      :class="{ dark: isDarkTheme }" 
      height="30vh"
    />
    <span v-if="!isCollapsed">{{ name }}</span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'SidebarItem',
  props: {
    name: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
    isCollapsed: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    onClick() {
      this.$emit('click');
    },
  },
  computed: {
    ...mapGetters(['isDarkTheme']),
  },
};
</script>

<style scoped>
.sidebar-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Default Light Theme */
.sidebar-item {
  background-color: #ffffff;
  color: #000000;
}

.icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  filter: invert(90%);
}

/* Dark Theme Styles */
.sidebar-item.dark {
  background-color: #1a1a1a;
  color: #ffffff;
}

.icon.dark {
  filter: invert(10%);
}

/* Optional Hover Effect */
.sidebar-item:hover {
  background-color: #fdfdfd;
}

.sidebar-item.dark:hover {
  background-color: #3b3b3b;
}
</style>
