<template>
<div>
  <header-bar></header-bar>
  <div class="media">
    <div class="media-left">
      <img :src="state.drinks[drinkId].image" :alt="state.drinks[drinkId].name">
    </div>
    <div class="media-body">
      <h1 class="media-heading">
        {{ state.drinks[drinkId].name }}
      </h1>
      <h4>
        {{ state.drinks[drinkId].manufacturer }}
      </h4>
      <h6>
        {{ state.drinks[drinkId].quantity }} remaining
        <button v-on:click="state.drinks[drinkId].quantity++">+</button>
        <button  v-on:click="state.drinks[drinkId].quantity--">-</button>
      </h6>
      {{ state.drinks[drinkId].description }}
    </div>
  </div>
</div>
</template>

<script>
import state from '@/components/shared'
import HeaderBar from '@/components/HeaderBar'

export default {
  name: 'Drink',
  data () {
    return {
      state
    }
  },
  props: ['drinkId'],
  components: {
    HeaderBar
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
   @import 'DrinkDetails'
</style>
