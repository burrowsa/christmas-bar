import Vue from 'vue'
import Router from 'vue-router'
import DrinkList from '@/pages/DrinkList'
import DrinkDetails from '@/pages/DrinkDetails'
import DrinkEditDetails from '@/pages/DrinkEditDetails'
import Butler from '@/pages/Butler'
import Login from '@/pages/Login'
import {getUserName, isButler} from '@/shared'

Vue.use(Router)

const router = new Router({
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
    },
    {
      path: '/butler/edit/:drinkId',
      name: 'EditDrink',
      component: DrinkEditDetails,
      props: true
    },
    {
      path: '/butler',
      name: 'Butler',
      component: Butler
    }
  ]
})

router.beforeEach(function (to, from, next) {
  if ((to.path.startsWith('/butler') && !isButler()) || (to.path !== '/login' && getUserName() == null)) {
    next('/login')
  } else {
    next()
  }
})

export default router
