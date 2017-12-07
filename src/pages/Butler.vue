<template>
<div>
  <header-bar></header-bar>
  <div class="container" id="butler">
    <template v-for="orders, user in state.orders">
      <div v-if="orders.length > 0">
        <h2>{{user}}</h2>
        <div class="list-group">
          <template v-for="drinkId in orders">
            <a href="#" class="list-group-item list-group-item-action" v-on:click="fulfilOrder(user, drinkId)" v-if="drinkId in state.drinks">
              <span>{{ state.drinks[drinkId].name }}</span>
              <button class="btn btn-default pull-right" v-on:click="cancelOrder(user, drinkId)"><span class="glyphicon glyphicon-remove"></span></button>
            </a>
            <a href="#" class="list-group-item list-group-item-action" v-else>
              <span>Deleted</span>
              <button class="btn btn-default pull-right" v-on:click="cancelOrder(user, drinkId)"><span class="glyphicon glyphicon-remove"></span></button>
            </a>
          </template>
        </div>
      </div>
    </template>
  </div>
</div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar'
import {state, socket} from '@/shared'

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
    fulfilOrder (username, drinkId) {
      socket.emit('fulfil_order', {username, drinkId})
    },
    cancelOrder (username, drinkId) {
      socket.emit('cancel_order', {username, drinkId})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "~bootstrap-sass/assets/stylesheets/bootstrap/variables";

.list-group-item {
  @media (min-width: $screen-md-min) {
    width: 30%;
  }
}

.btn {
  position: relative;
  top: -0.5em;
  left: 0.9em;
  background-color: crimson;
  color: white;
}

#butler {
  @media (min-width: $screen-md) {
    margin: 10px;
  }
}

</style>
