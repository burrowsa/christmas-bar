<template>
  <div class="my-nav">
    <router-link to="/" class="brand"><span class="glyphicon glyphicon-tree-conifer"></span><span class="glyphicon glyphicon-glass"></span></router-link>
    <span class="right">
      <template v-if="butler">
        <router-link to="/butler" class="right">{{ userName }}</router-link>
      </template>
      <template v-else>
        {{ userName }}
      </template>
      
      <span class="glyphicon glyphicon-log-out" v-on:click="logout"></span>
    </span>
  </div>
</template>

<script>
import {getUserName, isButler} from '@/components/shared'

export default {
  name: 'HeaderBar',
  computed: {
    canLogout () {
      return getUserName() != null
    },
    userName () {
      return getUserName()
    },
    butler () {
      return isButler()
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('name')
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="scss" scoped>
  .my-nav {
    background-color: #333;
    padding: 10px;
    margin-bottom: 10px;
    color: white;
    font-size: 1.4em;
    font-weight: bolder;   
  }
  
  .my-nav a {
    display: inline-block;
    text-decoration: none;
    color: white;
    font-weight: lighter;
    margin-right: 30px;
  }
  
  .my-nav > .brand {
    font-weight: bolder;
  }
  
  .my-nav > .right {
    float: right;
    text-align: right;
    margin-right: 0px; 
  }
</style>
