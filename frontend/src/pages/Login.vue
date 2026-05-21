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

    <main class="max-w-md mx-auto px-4 sm:px-6 -mt-8 relative z-10 pb-16">
      <div class="bg-white rounded-2xl shadow-elevated p-6 sm:p-8">

        <!-- Logo -->
        <div class="text-center mb-8">
          <img src="/logo.webp" alt="Biblioteca" class="h-14 w-14 mx-auto mb-3 rounded-xl">
          <h1 class="text-xl font-bold text-dark">Biblioteca</h1>
        </div>

        <!-- STEP 1: credentials -->
        <form v-if="step === 'credentials'" @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Email</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="Introdu email"
              class="input-field"
              required
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Parolă</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="Introdu parola"
              class="input-field"
              required
            >
          </div>

          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>

          <button type="submit" :disabled="loading" class="btn-primary w-full flex items-center justify-center gap-2">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se verifică...' : 'Continuă' }}
          </button>
        </form>

        <!-- STEP 2: 2FA code -->
        <form v-else @submit.prevent="handleVerifyCode" class="space-y-5">
          <div class="text-center mb-2">
            <div class="w-12 h-12 rounded-full bg-secondary/10 flex items-center justify-center mx-auto mb-3">
              <i class="pi pi-envelope text-secondary text-xl"></i>
            </div>
            <p class="text-sm text-gray-600">Am trimis un cod de 6 cifre la</p>
            <p class="text-sm font-semibold text-dark">{{ form.email }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Cod de verificare</label>
            <input
              v-model="code"
              type="text"
              inputmode="numeric"
              maxlength="6"
              placeholder="000000"
              class="input-field text-center text-2xl font-mono tracking-[0.5em]"
              autocomplete="one-time-code"
              required
              autofocus
            >
          </div>

          <p class="text-xs text-gray-400 text-center">Codul expiră în 10 minute. Verifică și folderul spam.</p>

          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>

          <button type="submit" :disabled="loading || code.length !== 6" class="btn-primary w-full flex items-center justify-center gap-2">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se verifică...' : 'Verifică codul' }}
          </button>

          <button type="button" @click="resetToCredentials" class="w-full text-sm text-gray-400 hover:text-secondary text-center transition-colors">
            Înapoi la autentificare
          </button>
        </form>

        <p v-if="step === 'credentials'" class="mt-6 text-center text-gray-500 text-sm">
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
      step: 'credentials',
      form: { email: '', password: '' },
      code: '',
      tempToken: '',
      errorMessage: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.errorMessage = ''
      if (!this.form.email || !this.form.password) {
        this.errorMessage = 'Te rog completează toate câmpurile'
        return
      }
      this.loading = true
      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ email: this.form.email, password: this.form.password })
        })
        const data = await res.json()
        if (res.ok && data.step === 'verify') {
          this.tempToken = data.temp_token
          this.step = 'verify'
        } else {
          this.errorMessage = data.message || 'Email sau parolă invalidă'
        }
      } catch {
        this.errorMessage = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.loading = false
      }
    },

    async handleVerifyCode() {
      this.errorMessage = ''
      this.loading = true
      try {
        const res = await fetch('/api/auth/verify-code', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ temp_token: this.tempToken, code: this.code })
        })
        const data = await res.json()
        if (res.ok) {
          const redirect = this.$route.query.redirect
          this.$router.push(redirect && redirect.startsWith('/') ? redirect : '/')
        } else {
          this.errorMessage = data.message || 'Cod incorect'
          this.code = ''
        }
      } catch {
        this.errorMessage = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.loading = false
      }
    },

    resetToCredentials() {
      this.step = 'credentials'
      this.code = ''
      this.tempToken = ''
      this.errorMessage = ''
    }
  }
}
</script>