import Vue from 'vue'

export let state = {
  drinks: {
    1: {
      name: 'Old Yummy Yum',
      manufacturer: 'Ancient Legends',
      type: 'beer',
      description: 'Brewed by bearded elves this is the tastiest beer ever invented. With flavours of fruits, chocolate and sausage.',
      image: '/static/img/pint.png',
      quantity: 10
    },
    2: {
      name: 'Unicorn Fart',
      manufacturer: 'Mysterious Bros',
      type: 'beer',
      description: 'With added unobtainium for a unique flavour.',
      image: '/static/img/pint.png',
      quantity: 0
    },
    3: {
      name: 'Hop Monster',
      manufacturer: 'Hipster Brews',
      type: 'beer',
      description: 'Made exclusively from hops, no malt, no wheat, no water!!',
      image: '/static/img/pint.png',
      quantity: 3
    },
    4: {
      name: 'Malbec',
      manufacturer: 'Argentina',
      type: 'red wine',
      description: 'Red wine',
      image: '/static/img/redwine.png',
      quantity: 3
    },
    5: {
      name: 'Sauvignon Blanc',
      manufacturer: 'NZ',
      type: 'white wine',
      description: 'White wine',
      image: '/static/img/whitewine.png',
      quantity: 6
    },
    6: {
      name: 'Cava',
      manufacturer: 'Spain',
      type: 'sparkling wine',
      description: 'Sparkling wine',
      image: '/static/img/champagne.png',
      quantity: 6
    }
  },
  orders: {}
}

export function getUserName () {
  return localStorage.getItem('name')
}

export function isOrdered (drinkId) {
  const userName = getUserName()
  return (userName in state.orders) && (state.orders[userName].includes(parseInt(drinkId)))
}

export function isAvailable (drinkId) {
  return state.drinks[parseInt(drinkId)].quantity > 0
}

export function addOrder (userName, drinkId) {
  drinkId = parseInt(drinkId)
  let orders = [drinkId]
  if (userName in state.orders) {
    orders = state.orders[userName]
    orders.push(drinkId)
  }
  Vue.set(state.orders, userName, orders)
}

export function orderDrink (drinkId) {
  const userName = getUserName()
  addOrder(userName, drinkId)
  state.drinks[drinkId].quantity--
}

export function removeOrder (userName, drinkId) {
  drinkId = parseInt(drinkId)
  const orders = state.orders[userName]
  const index = orders.indexOf(drinkId)
  if (index > -1) {
    orders.splice(index, 1)
  }
  Vue.set(state.orders, userName, orders)
}

export function cancelDrink (drinkId) {
  const userName = getUserName()
  removeOrder(userName, drinkId)
  state.drinks[drinkId].quantity++
}