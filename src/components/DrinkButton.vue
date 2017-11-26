<template>
  <button class="btn selected" v-on:click="cancelDrink(drinkId)" v-if="isOrdered(drinkId)">
    Cancel
  </button>
  <button class="btn" v-on:click="orderDrink(drinkId)" v-else-if="isAvailable(drinkId)">
    Drink
  </button>
</template>

<script>
import {isOrdered, isAvailable, orderDrink, cancelDrink} from '@/components/shared'

export default {
  name: 'DrinkButton',
  props: [ 'drinkId' ],
  methods: {
    orderDrink,
    cancelDrink,
    isOrdered,
    isAvailable
  }
}
</script>

<style lang="scss" scoped>
</style>
