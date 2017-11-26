<template>
  <button class="btn selected" v-on:click="cancelDrink(drinkId)" v-if="isOrdered(drinkId)">
    Cancel
  </button>
  <button class="btn" v-on:click="orderDrink(drinkId)" v-else-if="showButton(drinkId)">
    Drink
  </button>
</template>

<script>
import {isOrdered, showButton, orderDrink, cancelDrink} from '@/components/shared'

export default {
  name: 'DrinkButton',
  props: [ 'drinkId' ],
  methods: {
    orderDrink,
    cancelDrink,
    isOrdered,
    showButton
  }
}
</script>

<style lang="scss" scoped>
</style>
