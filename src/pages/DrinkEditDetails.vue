<template>
<div>
  <header-bar></header-bar>
  <div class="media">
    <div class="media-left">
      <webcam ref='webcam' v-if="captureMode" :width="300" :height="300"></webcam>
      <img :src="state.drinks[drinkId].image || '/static/img/question-mark.jpg'" :alt="state.drinks[drinkId].name" v-if="!captureMode">
      <center>
        <button class="btn btn-default glyphicon glyphicon-chevron-left" v-on:click="captureMode = false" v-if="captureMode"></button>
        <button class="btn btn-default glyphicon glyphicon-camera" v-on:click="takePhoto"></button>
      </center>
    </div>
    <div class="media-body">
      <h1 class="media-heading">
        <input type="text" v-model="state.drinks[drinkId].name" placeholder="Product Name" autofocus></input>
      </h1>
      <h4>
        <input type="text" v-model="state.drinks[drinkId].manufacturer" placeholder="Manufacturer"></input>
      </h4>
      <h4>
        <input type="text" v-model="state.drinks[drinkId].type" placeholder="Product Type"></input>
      </h4>
      <h6>
        {{ state.quantities[drinkId] || 0 }} remaining
        <stock-adjust :drinkId="drinkId"></stock-adjust>
      </h6>
      <textarea rows="5" v-model="state.drinks[drinkId].description" placeholder="Description"></textarea>
      <div>
        <button class="btn btn-default glyphicon glyphicon-remove" v-on:click="$router.push(`/drink/${drinkId}`)"></button>
        <button class="btn btn-default glyphicon glyphicon-floppy-disk" v-on:click="saveDrink"></button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import {state, socket} from '@/components/shared'
import HeaderBar from '@/components/HeaderBar'
import StockAdjust from '@/components/StockAdjust'
import Webcam from '@/components/webcam'

export default {
  name: 'Drink',
  data () {
    return {
      state,
      captureMode: false
    }
  },
  props: ['drinkId'],
  components: {
    HeaderBar,
    StockAdjust,
    Webcam
  },
  methods: {
    saveDrink () {
      const msg = {}
      msg[this.drinkId] = state.drinks[this.drinkId]
      socket.emit('save_drink', msg)
      this.$router.push(`/drink/${this.drinkId}`)
    },
    takePhoto () {
      if (this.captureMode) {
        state.drinks[this.drinkId].image = this.$refs.webcam.getPhoto()
      }

      this.captureMode = !this.captureMode
    }
  },
  beforeRouteLeave (to, from, next) {
    socket.emit('reload_drink', {drinkId: this.drinkId})
    next()
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
  height: auto;
}

.media-left .btn {
  margin-top: 10px;
  width: 45%;
}

.media-left .btn:only-of-type {
  margin-top: 10px;
  width: 90%;
}

.media-body .btn {
  margin-top: 10px;
  @media (min-width: $screen-md-min) {
    width: 150px;
  }
  width: 22%;
}

.media {
  @media (min-width: $screen-md-min) {
    margin: 30px;
  }
}

.btn.selected {
  background-color: pink;
}

input, textarea {
  width: 100%;
  border-color: #EEE;
  border-style: solid;
}
</style>
