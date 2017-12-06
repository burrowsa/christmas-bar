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
      <h4>
        {{ state.drinks[drinkId].type }}
      </h4>
      <h6>
        {{ state.quantities[drinkId] || 0 }} remaining
        <stock-adjust :drinkId="drinkId"></stock-adjust>
      </h6>
      {{ state.drinks[drinkId].description }}
      <div>
      <drink-button :drinkId="drinkId"></drink-button>
      <router-link :to="`/butler/edit/${drinkId}`" class="btn btn-default" v-if="isButler()">Edit</router-link>
      <button class="btn btn-default" v-if="isButler()" v-on:click="deleteDrink">Delete</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import {state, isButler, socket} from '@/shared'
import HeaderBar from '@/components/HeaderBar'
import DrinkButton from '@/components/DrinkButton'
import StockAdjust from '@/components/StockAdjust'

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
    DrinkButton,
    StockAdjust
  },
  methods: {
    isButler,
    deleteDrink () {
      if (confirm('Are you sure?') === true) {
        socket.emit('delete_drink', {drinkId: this.drinkId})
      }
    }
  },
  updated: function () {
    if (!state.drinks[this.drinkId]) {
      this.$router.push(`/`)
    }
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

.media {
  @media (min-width: $screen-md-min) {
    margin: 30px;
  }
}

.btn.selected {
  background-color: pink;
}
</style>
