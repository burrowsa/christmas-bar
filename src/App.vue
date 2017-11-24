<template>
  <div id="app">
    <header-bar></header-bar>
  
    <router-view/>
  </div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar'

export default {
  name: 'app',
  components: {
    HeaderBar
  }
}
</script>

<style lang="scss">
  $icon-font-path: "~bootstrap-sass/assets/fonts/bootstrap/";
  @import "~bootstrap-sass/assets/stylesheets/bootstrap";
  @import 'App.scss';
</style>
