<template>
  <div class="min-h-screen bg-base flex items-center justify-center px-4">
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-8 max-w-md w-full text-center">
      <!-- Loading -->
      <div v-if="state === 'loading'">
        <i class="pi pi-spin pi-spinner text-3xl text-secondary mb-4"></i>
        <p class="text-gray-500 text-sm">Se procesează invitația...</p>
      </div>

      <!-- Not logged in -->
      <div v-else-if="state === 'not_logged_in'">
        <i class="pi pi-lock text-4xl text-secondary mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">Trebuie să fii conectat</h2>
        <p class="text-gray-500 text-sm mb-6">Conectează-te la cont pentru a accesa invitația la Clubul de Literatură.</p>
        <router-link
          :to="{ path: '/login', query: { redirect: $route.fullPath } }"
          class="inline-block px-6 py-2.5 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-sm transition-all"
        >
          Conectare
        </router-link>
      </div>

      <!-- Already a member -->
      <div v-else-if="state === 'already_member'">
        <i class="pi pi-check-circle text-4xl text-green-500 mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">Ești deja membru!</h2>
        <p class="text-gray-500 text-sm mb-6">Faci deja parte din Clubul de Literatură.</p>
        <router-link to="/club" class="inline-block px-6 py-2.5 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-sm transition-all">
          Mergi la Club
        </router-link>
      </div>

      <!-- Success -->
      <div v-else-if="state === 'success'">
        <i class="pi pi-star-fill text-4xl text-secondary mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">Bun venit în Club!</h2>
        <p class="text-gray-500 text-sm mb-6">Ai fost adăugat cu succes în Clubul de Literatură. Bucură-te de experiență!</p>
        <router-link to="/club" class="inline-block px-6 py-2.5 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-sm transition-all">
          Deschide Clubul
        </router-link>
      </div>

      <!-- Expired -->
      <div v-else-if="state === 'expired'">
        <i class="pi pi-clock text-4xl text-amber-400 mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">Link expirat</h2>
        <p class="text-gray-500 text-sm mb-6">Acest link de invitație nu mai este valabil. Cere un link nou de la bibliotecar.</p>
        <router-link to="/" class="inline-block px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-dark font-semibold rounded-lg text-sm transition-all">
          Înapoi acasă
        </router-link>
      </div>

      <!-- Invalid / Error -->
      <div v-else>
        <i class="pi pi-times-circle text-4xl text-accent mb-4"></i>
        <h2 class="text-xl font-bold text-dark mb-2">{{ errorTitle }}</h2>
        <p class="text-gray-500 text-sm mb-6">{{ errorMessage }}</p>
        <router-link to="/" class="inline-block px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-dark font-semibold rounded-lg text-sm transition-all">
          Înapoi acasă
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClubJoin',
  data() {
    return {
      state: 'loading', // loading | not_logged_in | success | already_member | expired | error
      errorTitle: 'Link invalid',
      errorMessage: 'Invitația nu a putut fi procesată.'
    }
  },
  async mounted() {
    // Verificăm dacă utilizatorul e autentificat
    try {
      const meRes = await fetch('/api/auth/me', { credentials: 'include' })
      if (!meRes.ok) {
        this.state = 'not_logged_in'
        return
      }
    } catch {
      this.state = 'not_logged_in'
      return
    }

    // Trimitem cererea de join
    const token = this.$route.params.token
    try {
      const res = await fetch(`/api/club/join/${token}`, {
        method: 'POST',
        credentials: 'include'
      })
      const data = await res.json()

      if (res.status === 410) {
        this.state = 'expired'
      } else if (res.status === 404) {
        this.state = 'error'
        this.errorTitle = 'Link invalid'
        this.errorMessage = 'Acest link de invitație nu există.'
      } else if (!res.ok) {
        this.state = 'error'
        this.errorTitle = 'Eroare'
        this.errorMessage = data.message || 'Eroare la procesarea invitației.'
      } else if (data.already_member) {
        this.state = 'already_member'
      } else {
        this.state = 'success'
        // Forțăm reîncărcarea navbar-ului (club devine true)
        window.dispatchEvent(new Event('club-joined'))
      }
    } catch {
      this.state = 'error'
      this.errorTitle = 'Eroare de rețea'
      this.errorMessage = 'Nu s-a putut contacta serverul.'
    }
  }
}
</script>
