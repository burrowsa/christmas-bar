<template>
<div>
  <h1><router-link to="/" class="brand">Christmas Bar</router-link></h1>

  <template v-for="orders, user in state.orders">
    <div v-if="orders.length > 0">
      <h2>{{user}}</h2}
      <ul>
        <li v-for="drinkId in orders">
          {{ state.drinks[drinkId].name }} <button v-on:click="removeOrder(user, drinkId)">[X]</button>
        </li>
      </ul>
    </div>
  </template>
</div>
</template>

<script>
import {state, removeOrder} from '@/components/shared'

export default {
  name: 'Butler',
  data () {
    return {
      state
    }
  },
  methods: {
    removeOrder
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
