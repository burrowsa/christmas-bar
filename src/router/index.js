import Vue from 'vue'
import Router from 'vue-router'
import DrinkList from '@/pages/DrinkList'
import DrinkDetails from '@/pages/DrinkDetails'
import Login from '@/pages/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
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
