<template>
  <div class="container">
    <div class="jumbotron">
      <h1><span class="glyphicon glyphicon-tree-conifer"></span><span class="glyphicon glyphicon-glass"></span> Christmas Bar</h1> 
      <p>Welcome to the Christmas drinks selector, please login by telling me your name.</p> 
    </div>

    <div id="logon-box">
      <form v-on:submit.prevent="login">
        <input type="text" v-model="name" required autofocus></input>
        <input type="submit" class="btn btn-default" value="Login" ></input>
      </form>
    </div>
  </div>
</template>

<script>
import {isButler} from '@/shared'

export default {
  name: 'Login',
  data () {
    return {
      name: ''
    }
  },
  methods: {
    login () {
      localStorage.setItem('name', this.name)
      if (isButler()) {
        this.$router.push('/butler')
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  @import "~bootstrap-sass/assets/stylesheets/bootstrap/variables";

  #logon-box {
    @media (min-width: $screen-md-min) {
      width: 40%;
      margin: auto;
      text-align: right;
    }
  }
  
  #logon-box input[type="text"] {
    width: 100%;
    margin-bottom: 10px;
  }
  
  #logon-box input[type="submit"] {
    @media (max-width: $screen-md-min) {
      width: 100%;
    }
  }
</style>
