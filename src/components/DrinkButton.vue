<template>
  <button class="btn btn-default selected" v-on:click="cancelOrder(drinkId)" v-if="isOrdered(drinkId)">
    Cancel
  </button>
  <button class="btn btn-default" v-on:click="placeOrder(drinkId)" v-else-if="showButton(drinkId)">
    Drink
  </button>
</template>

<script>
import {state, getUserName, socket} from '@/shared'

export default {
  name: 'DrinkButton',
  props: [ 'drinkId' ],
  methods: {
    isOrdered (drinkId) {
      return (state.orders[getUserName()] || []).includes(drinkId)
    },
    showButton (drinkId) {
      return (getUserName().toLowerCase() !== 'butler') && (state.quantities[drinkId] > 0)
    },
    placeOrder (drinkId) {
      socket.emit('place_order', {username: getUserName(), drinkId})
    },
    cancelOrder (drinkId) {
      socket.emit('cancel_order', {username: getUserName(), drinkId})
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
