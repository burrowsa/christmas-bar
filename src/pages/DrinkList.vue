<template>
  <div id="drink-list">

    <div class="form-check">
      <label class="form-check-label">
        <input class="form-check-input" type="checkbox" v-model="showAll">
        Show All
      </label>
    </div>

    <ul class="list-unstyled">
      <template v-for="(drink, drinkId) in state.drinks">
        <li class="media mt-0" v-if="showAll || (drink.quantity > 0)">
          <div class="media-left">
            <router-link :to="`/drink/${drinkId}`">
              <img :src="drink.image" :alt="drink.name">
            </router-link>
          </div>
          <div class="media-body">
            <h3 class="media-heading">
              <router-link :to="`/drink/${drinkId}`">
                {{ drink.name }} ({{ drink.quantity }})
              </router-link>
            </h3>
            {{ drink.manufacturer }}
          </div>
          <div class="media-right">
            <button class="btn" v-on:click="drink.quantity--">
              Drink
            </button>
          </div>
        </li>
      </template>
    </ul>

  </div>
</template>

<script>
import state from '@/components/shared'

export default {
  name: 'Drink',
  data () {
    return {
      state,
      showAll: false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  @import 'DrinkList';
</style>
