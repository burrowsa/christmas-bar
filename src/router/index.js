import Vue from 'vue'
import Router from 'vue-router'
import DrinkList from '@/pages/DrinkList'
import DrinkDetails from '@/pages/DrinkDetails'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Drinks',
      component: DrinkList
    },
    {
      path: '/drink/:drinkId',
      name: 'Drink',
      component: DrinkDetails,
      props: true
    }
  ]
})
