import Vue from 'vue'

import io from 'socket.io-client'

export const socket = io(location.protocol + '//' + document.domain + ':' + location.port + '/v1')

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

export const state = {
  drinks: {},
  quantities: {},
  orders: {}
}

export function getUserName () {
  return localStorage.getItem('name')
}

export function isButler () {
  const username = getUserName()
  return username != null && username.toLowerCase() === 'butler'
}
