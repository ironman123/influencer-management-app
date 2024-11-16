<template>
  <div class="sidebar-item" @click="onClick">
    <img :src="icon" :alt="name" class="icon" height="30vh"/>
    <span v-if="!isCollapsed">{{ name }}</span>
  </div>
</template>

<script>
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
  watch:{
    
  }
};
</script>

<style scoped>
.sidebar-item {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  filter: invert(80%);
}
</style>
  