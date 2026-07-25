<template>
  <div class="min-h-screen font-sans text-[#2a1410] bg-cream pb-12">
    <!-- Hero Section -->
    <section class="relative overflow-hidden border-b border-[#ede0cc] py-16 sm:py-24 flex items-center">
      <img
        src="https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1600&h=900&fit=crop&auto=format"
        alt="Library bookshelves"
        class="absolute inset-0 w-full h-full object-cover object-center"
      />
      <div
        class="absolute inset-0"
        style="background: linear-gradient(105deg, rgba(45,16,24,0.85) 0%, rgba(45,16,24,0.65) 45%, rgba(45,16,24,0.35) 70%, rgba(45,16,24,0.1) 100%)"
      ></div>
      <div
        class="absolute inset-0 opacity-[0.03]"
        style="background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px)"
      ></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10 w-full">
        <h2 class="text-3xl sm:text-5xl font-black text-white mb-3 tracking-tight font-display drop-shadow uppercase">Conectare</h2>
        <p class="text-[#c9a84c] text-sm sm:text-lg font-serif italic tracking-widest">Bine ai revenit la Biblioteca</p>
      </div>
    </section>

    <main class="max-w-md mx-auto px-4 sm:px-6 -mt-8 relative z-10 pb-16">
      <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-6 sm:p-8">

        <!-- Logo -->
        <div class="text-center mb-8">
          <img src="/logo.webp" alt="Biblioteca Logo" class="h-16 w-16 mx-auto mb-4 rounded-sm border border-[#2a1410]/10 shadow-sm" />
          <h1 class="text-xl font-bold font-display uppercase tracking-tight text-[#2a1410]">Biblioteca</h1>
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
            <div class="flex justify-between mb-1.5">
              <label class="block text-sm font-medium text-gray-600">Parolă</label>
              <router-link to="/forgot-password" class="text-sm font-semibold text-secondary hover:text-secondary/80">Ai uitat parola?</router-link>
            </div>
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

          <button type="submit" :disabled="loading" class="w-full px-5 py-3 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors bg-[#c9a84c] text-dark hover:opacity-90 font-bold flex items-center justify-center gap-2 shadow-sm border border-[#c9a84c]/20">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se verifică...' : 'Continuă' }}
          </button>
        </form>

        <!-- STEP 2: 2FA code -->
        <form v-else @submit.prevent="handleVerifyCode" class="space-y-5">
          <div class="text-center mb-2">
            <div class="w-12 h-12 rounded-sm border border-[#c9a84c]/30 bg-[#c9a84c]/10 flex items-center justify-center mx-auto mb-4">
              <i class="pi pi-envelope text-[#c9a84c] text-xl"></i>
            </div>
            <p class="text-sm text-[#7a5a55] font-serif italic">Am trimis un cod de 6 cifre la</p>
            <p class="text-sm font-bold text-[#2a1410] font-mono tracking-widest mt-1">{{ form.email }}</p>
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

          <button type="submit" :disabled="loading || code.length !== 6" class="w-full px-5 py-3 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors bg-[#c9a84c] text-dark hover:opacity-90 font-bold flex items-center justify-center gap-2 shadow-sm border border-[#c9a84c]/20 disabled:opacity-50">
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