<template>
<div>
  <header-bar></header-bar>

  <div id="drink-list">
    <input v-model="state.search" placeholder="Search..." class="form-control"></input>
    <select v-model="state.typeFilter" class="form-control">
      <option value="!!!!Any!!!!">Any</option>
      <option :value="drinkType" v-for="drinkType in drinkTypes">
        {{ drinkType.replace(/\b\S/g, function(t) { return t.toUpperCase() }) /* Convert to title case */ }}
      </option>
      <option value="" v-if="isButler()">No Type Specified</option>
    </select>
    
    <label class="radio-inline">
    <input type="radio" name="sort" v-model="state.sort" value="name">Name
    </label>
    <label class="radio-inline">
    <input type="radio" name="sort" v-model="state.sort" value="manufacturer">Manufacturer
    </label>
    <label class="radio-inline">
    <input type="radio" name="sort" v-model="state.sort" value="quantity">Quantity
    </label>

    <div class="form-check">
      <label class="form-check-label">
        <input class="form-check-input" type="checkbox" v-model="state.showAll">
        Show Out Of Stock Products
      </label>
      <a href="#" class="add-drink" v-on:click="addDrink" v-if="isButler()">Add Drink</a>
    </div>

    <ul class="list-unstyled">
      <template v-for="{drinkId, drink} in drinks">
        <li class="media mt-0" v-if="(state.showAll || (state.quantities[drinkId] > 0) || isOrdered(drinkId)) && (state.typeFilter==='!!!!Any!!!!' || state.typeFilter===drink.type || (state.typeFilter==='' && !drink.type)) && (!state.search || drink.name.toLowerCase().includes(state.search.toLowerCase()))">
          <div class="media-left">
            <router-link :to="`/drink/${drinkId}`">
              <img :src="drink.image" :alt="drink.name">
            </router-link>
          </div>
          <div class="media-body">
            <h3 class="media-heading">
              <router-link :to="`/drink/${drinkId}`">
                {{ drink.name }}
              </router-link>
              <span class="badge badge-primary badge-pill">{{ state.quantities[drinkId] || 0 }}</span>
            </h3>
            {{ drink.manufacturer }}
            <stock-adjust :drinkId="drinkId"></stock-adjust>
          </div>
          <div class="media-right">
            <drink-button :drinkId="drinkId"></drink-button>
            <button v-on:click="$router.push(`/butler/edit/${drinkId}`)" class="btn btn-default" v-if="isButler()">Edit</button>
          </div>
        </li>
      </template>
    </ul>
  </div>
</div>
</template>

<script>
import Vue from 'vue'
import HeaderBar from '@/components/HeaderBar'
import DrinkButton from '@/components/DrinkButton'
import StockAdjust from '@/components/StockAdjust'
import {state, getUserName, isButler} from '@/shared'

export default {
  name: 'DrinkList',
  data () {
    return {
      state
    }
  },
  components: {
    HeaderBar,
    DrinkButton,
    StockAdjust
  },
  methods: {
    isButler,
    isOrdered (drinkId) {
      return (state.orders[getUserName()] || []).includes(drinkId)
    },
    addDrink () {
      const guid = () => {
        const s4 = () => Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1)
        return `${s4() + s4()}-${s4()}-${s4()}-${s4()}-${s4() + s4() + s4()}`
      }
      const drinkId = guid()
      Vue.set(state.drinks, drinkId, {})
      this.$router.push(`/butler/edit/${drinkId}`)
    }
  },
  computed: {
    drinkTypes () {
      const types = new Set()
      for (var drinkId in state.drinks) {
        if (state.drinks[drinkId].type) {
          types.add(state.drinks[drinkId].type)
        }
      }
      const arr = Array.from(types)
      arr.sort()
      return arr
    },

    drinks () {
      let lst = []

      for (const drinkId in state.drinks) {
        const drink = state.drinks[drinkId]
        lst.push({drinkId, drink})
      }

      if (state.sort) {
        if (state.sort === 'quantity') {
          lst.sort((a, b) => (state.quantities[b.drinkId] || 0) - (state.quantities[a.drinkId] || 0))
        } else {
          lst.sort((a, b) => a.drink[state.sort].toLowerCase().localeCompare(b.drink[state.sort].toLowerCase()))
        }
      }

      return lst
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "~bootstrap-sass/assets/stylesheets/bootstrap/variables";

#drink-list {
  @media (min-width: $screen-md) {
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
  border-top: 1px solidtable-border-color;
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

.form-control {
  margin-bottom: 3px;
}
</style>
