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
        <h2 class="text-3xl sm:text-5xl font-black text-white mb-3 tracking-tight font-display drop-shadow uppercase">Creează o nouă parolă</h2>
        <p class="text-[#c9a84c] text-sm sm:text-lg font-serif italic tracking-widest">Alege o parolă sigură pentru contul tău</p>
      </div>
    </section>

    <main class="max-w-md mx-auto px-4 sm:px-6 -mt-8 relative z-10 pb-16">
      <div class="bg-white rounded-sm shadow-[0_1px_4px_rgba(42,20,16,0.04)] border border-[#2a1410]/10 p-6 sm:p-8">

        <!-- Logo -->
        <div class="text-center mb-8">
          <img src="/logo.webp" alt="Biblioteca Logo" class="h-16 w-16 mx-auto mb-4 rounded-sm border border-[#2a1410]/10 shadow-sm" />
          <h1 class="text-xl font-bold font-display uppercase tracking-tight text-[#2a1410]">Biblioteca</h1>
        </div>

        <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-4 mb-6 text-center">
          <i class="pi pi-check-circle text-3xl text-green-500 mb-2"></i>
          <p class="text-green-700 text-sm font-medium">{{ successMessage }}</p>
          <router-link to="/login" class="inline-block mt-4 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition-colors">Mergi la conectare</router-link>
        </div>

        <form v-else @submit.prevent="handleReset" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Parolă nouă</label>
            <input
              v-model="password"
              type="password"
              placeholder="Minim 6 caractere"
              class="input-field"
              required
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Confirmă parola nouă</label>
            <input
              v-model="passwordConfirm"
              type="password"
              placeholder="Confirmă parola"
              class="input-field"
              required
            >
          </div>

          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>

          <button type="submit" :disabled="loading" class="w-full px-5 py-3 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors bg-[#c9a84c] text-dark hover:opacity-90 font-bold flex items-center justify-center gap-2 shadow-sm border border-[#c9a84c]/20">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se salvează...' : 'Salvează noua parolă' }}
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',
  data() {
    return {
      password: '',
      passwordConfirm: '',
      loading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleReset() {
      this.errorMessage = ''
      this.successMessage = ''
      
      if (!this.password || !this.passwordConfirm) {
        this.errorMessage = 'Te rugăm să completezi ambele câmpuri.'
        return
      }

      if (this.password !== this.passwordConfirm) {
        this.errorMessage = 'Parolele nu se potrivesc.'
        return
      }
      
      if (this.password.length < 6) {
        this.errorMessage = 'Parola trebuie să aibă minim 6 caractere.'
        return
      }

      this.loading = true
      const token = this.$route.params.token
      
      try {
        const res = await fetch(`/api/auth/reset-password/${token}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ password: this.password })
        })
        const data = await res.json()
        
        if (res.ok) {
          this.successMessage = 'Parola ta a fost resetată cu succes!'
        } else {
          this.errorMessage = data.message || 'Link-ul de resetare a expirat sau este invalid.'
        }
      } catch (err) {
        this.errorMessage = 'Eroare de rețea. Te rugăm să încerci din nou mai târziu.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
