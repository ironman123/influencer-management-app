<template>
  <div id="app">
      <PageContainer>
      </PageContainer>
  </div>
</template>

<script>

import PageContainer from './components/PageContainer.vue';

export default {
  name: 'App',
  components: {
    PageContainer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#app {
  height: 100%;
  width: 100%;
}
</style>
