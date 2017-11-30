<template>
  <span v-if="isButler()">
    <button class="btn btn-default" v-on:click="adjustQuantity(drinkId, 1)">+</button>
    <button class="btn btn-default" v-on:click="adjustQuantity(drinkId, -1)">-</button>
  </span>
</template>

<script>
import {isButler, socket} from '@/components/shared'

export default {
  name: 'StockAdjust',
  props: ['drinkId'],
  methods: {
    isButler,
    adjustQuantity (drinkId, delta) {
      socket.emit('adjust_quantity', {drinkId, delta})
    }
  }
}
</script>

<style lang="scss" scoped>
.btn {
border-radius: 50%;
width: 34px;
height: 34px;
}
</style>