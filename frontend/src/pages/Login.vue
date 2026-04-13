<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-dark py-16 sm:py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary/20 via-transparent to-accent/10"></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
        <h2 class="text-3xl sm:text-5xl font-bold text-white mb-3 tracking-tight">Conectare</h2>
        <p class="text-white/50 text-sm sm:text-lg font-normal">Bine ai revenit la Biblioteca</p>
      </div>
    </section>

    <!-- Login Form -->
    <main class="max-w-md mx-auto px-4 sm:px-6 -mt-8 relative z-10 pb-16">
      <div class="bg-white rounded-2xl shadow-elevated p-6 sm:p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <img src="/logo.webp" alt="Biblioteca" class="h-14 w-14 mx-auto mb-3 rounded-xl">
          <h1 class="text-xl font-bold text-dark">Biblioteca</h1>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-600 mb-1.5">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="Introdu email"
              class="input-field"
              required
            >
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-600 mb-1.5">Parolă</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              placeholder="Introdu parola"
              class="input-field"
              required
            >
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="form.rememberMe" type="checkbox" class="w-4 h-4 rounded border-gray-300 text-secondary focus:ring-secondary">
              <span class="text-gray-500 text-sm">Ține-mă minte</span>
            </label>
          </div>

          <!-- Error -->
          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>

          <!-- Success -->
          <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-sm">{{ successMessage }}</p>
          </div>

          <button type="submit" class="btn-primary w-full">
            Conectare
          </button>
        </form>

        <p class="mt-6 text-center text-gray-500 text-sm">
          Nu ai cont?
          <router-link to="/signup" class="text-secondary hover:text-secondary/80 font-semibold">Înregistrare</router-link>
        </p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: '',
        rememberMe: false
      },
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      // Resetează mesajele
      this.errorMessage = ''
      this.successMessage = ''

      // Validare de bază
      if (!this.form.email || !this.form.password) {
        this.errorMessage = 'Te rog completează toate câmpurile'
        return
      }

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            email: this.form.email,
            password: this.form.password
          })
        })

        const data = await response.json()
        if (response.ok) {
          this.successMessage = 'Conectare reușită! Se redirecționează...'
          setTimeout(() => {
            this.$router.push('/')
          }, 1500)
        } else {
          this.errorMessage = data.message || 'Email sau parolă invalidă'
        }
      } catch (error) {
        this.errorMessage = 'Eroare de rețea. Încearcă din nou.'
      }
    }
  }
}
</script>

<style scoped>
</style>
