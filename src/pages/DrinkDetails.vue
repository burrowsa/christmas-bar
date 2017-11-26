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
      </h6>
      {{ state.drinks[drinkId].description }}
      <div>
      <DrinkButton :drinkId="drinkId"></DrinkButton>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import {state} from '@/components/shared'
import HeaderBar from '@/components/HeaderBar'
import DrinkButton from '@/components/DrinkButton'

export default {
  name: 'Drink',
  data () {
    return {
      state
    }
  },
  props: ['drinkId'],
  components: {
    HeaderBar,
    DrinkButton
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "~bootstrap-sass/assets/stylesheets/bootstrap/variables";

.media-left {
  @media (min-width: $screen-md-min) {
    width: auto;
  }
  width: 30%;
}

.media-left > img {
  @media (min-width: $screen-md-min) {
    width: auto;
  }
  width:100%;
}

.btn {
  margin-top: 10px;
  @media (min-width: $screen-md-min) {
    width: 300px;
  }
  width: 90%;
}

.btn.selected {
  background-color: pink;
}
</style>
