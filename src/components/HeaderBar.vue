<template>
  <div class="my-nav">
    <router-link to="/" class="brand">Christmas Bar</router-link>
    <a href="#" class="right">logout</a>
  </div>
</template>

<script>
</script>

<style>
  .my-nav {
    background-color: #333;
    padding: 10px;
    margin-bottom: 10px;
  }
  
  .my-nav > a {
    display: inline-block;
    text-decoration: none;
    color: white;
    font-size: 1.4em;
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
