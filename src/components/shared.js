import Vue from 'vue'

import S3 from 'aws-sdk/clients/S3'

var s3 = new S3({
  credentials: {
    accessKeyId: 'AKIAIDUP6DVKSPIH3DJQ',
    secretAccessKey: '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'
  },
  region: 'eu-west-1'
})

function s3GetObject (key) {
  return s3.getObject({
    Bucket: 'christmas-bar',
    Key: key
  }).promise()
}

function s3PutObject (key, value) {
  return s3.putObject({
    Bucket: 'christmas-bar',
    Key: key,
    Body: value
  }).promise()
}

function parseJSON (data) {
  return JSON.parse(new TextDecoder('utf-8').decode(data.Body))
}

function emitJSON (data) {
  return new TextEncoder('utf-8').encode(JSON.stringify(data))
}

function loadDrinks () {
  return s3GetObject('drinks.json').then(parseJSON).then(function (obj) { Vue.set(state, 'drinks', obj) })
}

function loadQuantities () {
  return s3GetObject('quantities.json').then(parseJSON).then(function (obj) { Vue.set(state, 'quantities', obj) })
}

function loadOrders () {
  return s3GetObject('orders.json').then(parseJSON).then(function (obj) { Vue.set(state, 'orders', obj) })
}

function loadQuantitiesAndOrders () {
  return loadQuantities().then(loadOrders)
}

function loadEverything () {
  return loadDrinks().then(loadQuantitiesAndOrders)
}

function writeQuantities (data) {
  return s3PutObject('quantities.json', emitJSON(data))
}

function writeOrders (data) {
  return s3PutObject('orders.json', emitJSON(data))
}

loadEverything().catch(console.log)

setInterval(function () { loadQuantitiesAndOrders().catch(console.log) }, 500)

export let state = {
  drinks: {},
  quantities: {},
  orders: {}
}

export function getUserName () {
  return localStorage.getItem('name')
}

export function isButler () {
  const userName = getUserName()
  return userName != null && userName.toLowerCase() === 'butler'
}

export function isOrdered (drinkId) {
  const userName = getUserName()
  return (userName in state.orders) && (state.orders[userName].includes(drinkId))
}

export function getQuantityRemaining (drinkId) {
  if (drinkId in state.quantities) {
    return state.quantities[drinkId]
  } else {
    return 0
  }
}

export function setQuantityRemaining (drinkId, value) {
  var quantitiesCopy = Object.assign({}, state.quantities)
  quantitiesCopy[drinkId] = value
  return writeQuantities(quantitiesCopy).then(loadQuantities)
}

export function incQuantityRemaining (drinkId) {
  return setQuantityRemaining(drinkId, getQuantityRemaining(drinkId) + 1)
}

export function decQuantityRemaining (drinkId) {
  return setQuantityRemaining(drinkId, getQuantityRemaining(drinkId) - 1)
}

export function isAvailable (drinkId) {
  return getQuantityRemaining(drinkId) > 0
}

export function showButton (drinkId) {
  return (getUserName().toLowerCase() !== 'butler') && isAvailable(drinkId)
}

export function addOrder (userName, drinkId) {
  var ordersCopy = Object.assign({}, state.orders)
  if (userName in ordersCopy) {
    ordersCopy[userName].push(drinkId)
  } else {
    ordersCopy[userName] = [drinkId]
  }
  return writeOrders(ordersCopy).then(loadOrders)
}

export function orderDrink (drinkId) {
  const userName = getUserName()
  var p1 = addOrder(userName, drinkId)
  var p2 = decQuantityRemaining(drinkId)
  Promise.all([p1, p2]).catch(console.log)
}

function removeOrder (userName, drinkId) {
  var ordersCopy = Object.assign({}, state.orders)
  const index = ordersCopy[userName].indexOf(drinkId)
  if (index > -1) {
    ordersCopy[userName].splice(index, 1)
  }
  return writeOrders(ordersCopy).then(loadOrders)
}

export function fulfilOrder (userName, drinkId) {
  removeOrder(userName, drinkId).catch(console.error)
}

export function cancelDrinkForUser (userName, drinkId) {
  var p1 = removeOrder(userName, drinkId)
  var p2 = incQuantityRemaining(drinkId)
  Promise.all([p1, p2]).catch(console.log)
}

export function cancelDrink (drinkId) {
  cancelDrinkForUser(getUserName(), drinkId)
}
