<template>
<div>
  <header-bar></header-bar>
  
  <div id="drink-list">
    <div class="form-check">
      <label class="form-check-label">
        <input class="form-check-input" type="checkbox" v-model="showAll">
        Show All
      </label>
    </div>

    <ul class="list-unstyled">
      <template v-for="(drink, drinkId) in state.drinks">
        <li class="media mt-0" v-if="showAll || isAvailable(drinkId) || isOrdered(drinkId)">
          <div class="media-left">
            <router-link :to="`/drink/${drinkId}`">
              <img :src="drink.image" :alt="drink.name">
            </router-link>
          </div>
          <div class="media-body">
            <h3 class="media-heading">
              <router-link :to="`/drink/${drinkId}`">
                {{ drink.name }} ({{ getQuantityRemaining(drinkId) }})
              </router-link>
            </h3>
            {{ drink.manufacturer }}
          </div>
          <div class="media-right">
            <drink-button :drinkId="drinkId"></drink-button>
          </div>
        </li>
      </template>
    </ul>
  </div>
</div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar'
import DrinkButton from '@/components/DrinkButton'
import {state, isOrdered, getQuantityRemaining, isAvailable} from '@/components/shared'

export default {
  name: 'DrinkList',
  data () {
    return {
      state,
      showAll: false
    }
  },
  components: {
    HeaderBar,
    DrinkButton
  },
  methods: {
    isOrdered,
    getQuantityRemaining,
    isAvailable
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "~bootstrap-sass/assets/stylesheets/bootstrap/variables";

#drink-list {
  @media (min-width: $screen-md-min) {
    width: 50%;
    margin: auto;
  }
}

#drink-list img {
  border-radius: 50%;
  width: 80px;
  height: 80px;
}

#drink-list > ul > li {
  border-top: 1px solid $table-border-color;
  padding-top: 1%;
}

#drink-list > ul > li:nth-of-type(1) {
  border-top: none;
}

.btn {
  width: 80px;
  height: 80px;
}

.btn.selected {
  background-color: pink;
}
</style>
