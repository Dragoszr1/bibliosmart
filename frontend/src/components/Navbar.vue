<template>
  <nav class="bg-dark/95 backdrop-blur-md border-b border-white/5 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3 group">
          <img src="/logo.webp" alt="Biblioteca" class="h-9 w-9 rounded-lg transition-transform duration-200 group-hover:scale-105">
          <div class="hidden sm:block">
            <h1 class="text-lg font-bold text-white leading-tight">Biblioteca</h1>
            <p class="text-[11px] text-white/40 font-medium -mt-0.5">Colegiul Național de Informatică ,,Spiru-Haret"</p>
          </div>
        </router-link>

        <!-- Desktop Nav -->
        <div class="hidden md:flex items-center gap-1">
          <router-link 
            to="/" 
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
            exact
          >
            Acasă
          </router-link>
          <router-link 
            to="/books" 
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
          >
            Cărți
          </router-link>
          <router-link 
            v-if="isLoggedIn" 
            to="/profile" 
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
          >
            Profil
          </router-link>
          <router-link
            v-if="inClub"
            to="/club"
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
          >
            Club
          </router-link>

          <button 
            id="tts-toggle-btn"
            @click="toggleTTS"
            :class="[
              'px-3 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-2',
              ttsActive ? 'bg-blue-500/20 text-blue-400' : 'text-white/70 hover:text-white hover:bg-white/5'
            ]"
            title="Mod Citire Text (Treci cu mouse-ul peste orice text pentru a-l citi)"
          >
            <i class="pi pi-volume-up"></i>
          </button>

          <div class="w-px h-6 bg-white/10 mx-2"></div>

          <button 
            @click="handleAuthClick"
            :class="[
              'px-5 py-2 rounded-lg text-sm font-semibold transition-all duration-200',
              isLoggedIn
                ? 'text-white/70 hover:text-white hover:bg-white/5'
                : 'bg-secondary hover:bg-secondary/90 text-white shadow-soft'
            ]"
          >
            {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
          </button>
        </div>

        <!-- Mobile toggle -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-colors"
        >
          <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-lg"></i>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="mobileMenuOpen" class="md:hidden bg-dark border-t border-white/5">
        <div class="px-4 py-3 space-y-1">
          <router-link to="/" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Acasă
          </router-link>
          <router-link to="/books" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Cărți
          </router-link>
          <router-link v-if="isLoggedIn" to="/profile" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Profil
          </router-link>
          <router-link v-if="inClub" to="/club" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Club
          </router-link>
          <button 
            @click="toggleTTS"
            :class="[
              'w-full text-left px-4 py-2.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
              ttsActive ? 'bg-blue-500/20 text-blue-400' : 'text-white/70 hover:text-white hover:bg-white/5'
            ]"
          >
            <i class="pi pi-volume-up"></i> Citire Text {{ ttsActive ? '(Activat)' : '' }}
          </button>

          <div class="pt-2 border-t border-white/5">
            <button 
              @click="handleAuthClick"
              :class="[
                'w-full text-left px-4 py-2.5 rounded-lg text-sm font-semibold transition-all',
                isLoggedIn
                  ? 'text-white/70 hover:text-white hover:bg-white/5'
                  : 'bg-secondary text-white'
              ]"
            >
              {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      isLoggedIn: false,
      inClub: false,
      mobileMenuOpen: false,
      ttsActive: false,
      currentHoverTarget: null,
      hoverTimeout: null
    }
  },
  mounted() {
    this.checkAuth()
  },
  beforeUnmount() {
    if (this.ttsActive) {
      document.body.removeEventListener('mouseover', this.handleTTSHover, true);
      document.body.removeEventListener('mouseout', this.handleTTSOut, true);
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    }
  },
  watch: {
    '$route'() {
      this.checkAuth()
    },
    ttsActive(newVal) {
      if (newVal) {
        document.body.addEventListener('mouseover', this.handleTTSHover, true);
        document.body.addEventListener('mouseout', this.handleTTSOut, true);
        if (window.speechSynthesis) window.speechSynthesis.getVoices();
      } else {
        document.body.removeEventListener('mouseover', this.handleTTSHover, true);
        document.body.removeEventListener('mouseout', this.handleTTSOut, true);
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        if (this.hoverTimeout) clearTimeout(this.hoverTimeout);
        if (this.currentHoverTarget) {
          if (this.currentHoverTarget.dataset.oldOutline !== undefined) {
            this.currentHoverTarget.style.outline = this.currentHoverTarget.dataset.oldOutline;
          }
          this.currentHoverTarget = null;
        }
      }
    }
  },
  methods: {
    toggleTTS() {
      this.ttsActive = !this.ttsActive;
    },
    handleTTSHover(e) {
      if (e.target.closest('#tts-toggle-btn') || e.target.closest('nav')) return;

      const validTags = ['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'SPAN', 'A', 'BUTTON', 'LI', 'LABEL'];
      let targetElement = e.target;
      
      if (!validTags.includes(targetElement.tagName)) {
         if (targetElement.tagName === 'DIV' && targetElement.innerText.trim().length > 0) {
            // It's fine to read the div if it has text
         } else {
            return;
         }
      }

      if (this.currentHoverTarget === targetElement) return;
      this.currentHoverTarget = targetElement;

      if (this.hoverTimeout) clearTimeout(this.hoverTimeout);
      
      this.hoverTimeout = setTimeout(() => {
        let text = targetElement.innerText || targetElement.textContent;
        if (text && text.trim().length > 0) {
          if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text.trim());
            utterance.lang = 'ro-RO';
            
            const voices = window.speechSynthesis.getVoices();
            const roVoices = voices.filter(v => v.lang.startsWith('ro'));
            const selectedVoice = roVoices.find(v => v.name.includes('Google') || v.name.includes('Online') || v.name.includes('Microsoft Andrei')) || roVoices[0];
            
            if (selectedVoice) {
              utterance.voice = selectedVoice;
            }
            
            utterance.rate = 0.9;
            
            targetElement.dataset.oldOutline = targetElement.style.outline;
            targetElement.style.outline = '2px solid #3b82f6';
            
            const clearOutline = () => {
              if (targetElement.dataset.oldOutline !== undefined) {
                targetElement.style.outline = targetElement.dataset.oldOutline;
                delete targetElement.dataset.oldOutline;
              }
            };
            
            utterance.onend = clearOutline;
            utterance.onerror = clearOutline;
            
            window.speechSynthesis.speak(utterance);
          }
        }
      }, 300);
    },
    handleTTSOut(e) {
      if (this.currentHoverTarget === e.target) {
        if (this.hoverTimeout) clearTimeout(this.hoverTimeout);
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        
        if (this.currentHoverTarget.dataset.oldOutline !== undefined) {
          this.currentHoverTarget.style.outline = this.currentHoverTarget.dataset.oldOutline;
          delete this.currentHoverTarget.dataset.oldOutline;
        }
        
        this.currentHoverTarget = null;
      }
    },
    async checkAuth() {
      try {
        const response = await fetch('/api/auth/me', { credentials: 'include' })
        if (response.ok) {
          const data = await response.json()
          this.isLoggedIn = true
          this.inClub = !!data.club
        } else {
          this.isLoggedIn = false
          this.inClub = false
        }
      } catch {
        this.isLoggedIn = false
        this.inClub = false
      }
    },
    async handleAuthClick() {
      if (this.isLoggedIn) {
        try {
          await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
        } catch { /* ignore */ }
        this.isLoggedIn = false
        this.inClub = false
        this.mobileMenuOpen = false
        this.$router.push('/')
      } else {
        this.mobileMenuOpen = false
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from, .slide-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
