<template>
  <div :class="headerStyle">
    <router-link to="/" class="brand"><span class="glyphicon glyphicon-tree-conifer"></span><span class="glyphicon glyphicon-glass"></span></router-link>
    <span class="right">
      <template v-if="butler">
        <span class="glyphicon glyphicon-fullscreen" v-on:click="fullscreen"></span>
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
import {state, getUserName, isButler} from '@/shared'

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
    },
    headerStyle () {
      if (state.connected) {
        return 'my-nav my-nav-norm'
      } else {
        return 'my-nav my-nav-err'
      }
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('name')
      this.$router.push('/login')
    },
    fullscreen () {
      document.documentElement.webkitRequestFullscreen()
      this.screenstate = !this.screenstate
    }
  }
}
</script>

<style lang="scss" scoped>
  .my-nav {
    padding: 10px;
    margin-bottom: 10px;
    font-size: 1.4em;
    font-weight: bolder;
  }
  
  .my-nav-norm {
    background-color: #333;
    color: white;
  }
  
  .my-nav-err {
    background-color: red;
    color: black;
  }
  
  .my-nav-err .brand::after {
    color: black;
    content: "Connecting..";
    font-weight: 100;
    margin-left: 50px;
  }
  
  .my-nav a {
    display: inline-block;
    text-decoration: none;
    font-weight: lighter;
    margin-right: 30px;
  }
  
  .my-nav-norm a {
      color: white;
  }
  
  .my-nav-err a {
    color: black;
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
