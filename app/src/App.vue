<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/about">About</router-link>
      </nav>
    </header>
    
    <router-view /> 

    <footer>
      <p>Footer content here</p>
      
    <AboutPage></AboutPage>
    <HomePage></HomePage>
    <about-page></about-page>
    </footer>
  </div>
</template>

<script>
import AboutPage from './components/About.vue';
import HomePage from './components/Home.vue';

export default {
  name: 'App',
  components: {
    AboutPage,
    HomePage
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
  margin-top: 60px;
}

nav a {
  margin-right: 10px;
}
</style>
