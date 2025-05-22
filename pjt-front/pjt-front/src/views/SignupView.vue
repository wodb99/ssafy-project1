<!-- views/SignUpView.vue -->

<template>
  <div>
    <h1>회원 가입 페이지</h1>
    <form @submit.prevent="signUp">
      <label for="username">아이디 : </label>
      <input type="text" id="username" v-model.trim="username" /> <br>

      <label for="password1">비밀번호 : </label>
      <input type="password" id="password1" v-model.trim="password1" /> <br>

      <label for="password2">비밀번호 확인: </label>
      <input type="password" id="password2" v-model.trim="password2" /> <br>

      <input type="submit" value="회원가입">
    </form>

  </div>
</template>

<script setup>
  import { useAccountStore } from '@/stores/accounts'
  import { ref } from 'vue'

  const username = ref('')
  const password1 = ref('')
  const password2 = ref('')

  const accountStore = useAccountStore()
  const signUp = function() {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
    }
    accountStore.signUp(payload)
  }
</script>

<style>

</style>
