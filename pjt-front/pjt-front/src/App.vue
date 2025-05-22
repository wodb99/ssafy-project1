<template>
  <header>
    <nav>
      <!-- <RouterLink :to="{ name:'ArticleView' }">Articles</RouterLink> | -->
      <RouterLink :to="{ name:'SignUpView' }">SignUpPage</RouterLink> |
      <RouterLink :to="{ name:'LogInView'}">LogInPage</RouterLink> |
      <form @submit.prevent="logOut">
        <input type="submit" value="LogOut">
      </form>
    </nav>
  </header>
  <RouterView />
  <div>
    <MapView />
  </div>
</template>

<script>
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const logOut = function () {
  accountStore.logOut()
}
import MapView from './components/MapView.vue'
export default { components: { MapView } }
</script>
