<template>
<div>
  <header-bar></header-bar>

  <template v-for="orders, user in state.orders">
    <div v-if="orders.length > 0">
      <h2>{{user}}</h2}
      <ul>
        <li v-for="drinkId in orders">
          {{ state.drinks[drinkId].name }}
          <button v-on:click="removeOrder(user, drinkId)">[/]</button>
          <button v-on:click="cancelDrinkForUser(user, drinkId)">[X]</button>
        </li>
      </ul>
    </div>
  </template>
</div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar'
import {state, removeOrder, cancelDrinkForUser} from '@/components/shared'

export default {
  name: 'Butler',
  data () {
    return {
      state
    }
  },
  components: {
    HeaderBar
  },
  methods: {
    removeOrder,
    cancelDrinkForUser
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
