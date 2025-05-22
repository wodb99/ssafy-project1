<!-- views/LoginView.vue -->

<template>
  <div>
    <h1>로그인 페이지</h1>

    <form @submit.prevent="login">
      <label for="username">아이디: </label> <br>
      <input type="text" id="username" v-model.trim="username" /> <br>

      <label for="password">비밀번호: </label> <br>
      <input type="password" id="password" v-model.trim="password" /> <br>

      <input type="submit" value="로그인">
    </form>

  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts.js'

  const username = ref('')
  const password = ref('')

  const accountStore = useAccountStore()

  const login = () => {
    const payload = {
      username: username.value,
      password: password.value
    }
    accountStore.logIn(payload)
  }

</script>

<style>

</style>
