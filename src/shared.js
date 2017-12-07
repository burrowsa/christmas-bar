import Vue from 'vue'

import io from 'socket.io-client'

let socketURL = location.protocol + '//' + document.domain + ':' + location.port + '/v1'

if (process.env.NODE_ENV === 'development') {
  socketURL = 'https://isthebaropen.co.uk/v1'
}

export const socket = io(socketURL)

socket.on('update', function (msg) {
  if (msg.drinks != null) {
    Vue.set(state, 'drinks', msg.drinks)
  }
  if (msg.quantities != null) {
    Vue.set(state, 'quantities', msg.quantities)
  }
  if (msg.orders != null) {
    Vue.set(state, 'orders', msg.orders)
  }
})

socket.on('update_drink', function (msg) {
  for (let [key, value] of Object.entries(msg)) {
    Vue.set(state.drinks, key, value)
  }
})

socket.on('remove_drink', function (msg) {
  Vue.delete(state.drinks, msg.drinkId)
})

socket.on('error', function (msg) {
  Vue.toast(msg, {
    className: 'et-alert',
    horizontalPosition: 'center'
  })
})

socket.on('disconnect', function () {
  state.connected = false
})

socket.on('connect', function () {
  state.connected = true
})

export const state = {
  drinks: {},
  quantities: {},
  orders: {},
  connected: false,
  showAll: false,
  typeFilter: '!!!!Any!!!!'
}

export function getUserName () {
  return localStorage.getItem('name')
}

export function isButler () {
  const username = getUserName()
  return username != null && username.toLowerCase() === 'butler'
}
