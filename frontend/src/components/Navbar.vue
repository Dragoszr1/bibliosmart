<template>
  <nav class="bg-dark/95 backdrop-blur-md border-b border-white/5 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-center h-16">
        <!-- Logo -->
        <div class="flex-1 flex justify-start">
          <router-link to="/" class="flex items-center gap-3 group w-fit">
            <img src="/logo.webp" alt="Biblioteca" class="h-9 w-9 rounded-lg transition-transform duration-200 group-hover:scale-105">
            <div class="hidden sm:block">
              <span class="text-white font-black text-lg leading-none tracking-tight font-display uppercase">Biblioteca</span>
              <p class="font-mono text-[10px] tracking-widest uppercase leading-none mt-0.5 text-[#c9a84c]">
                Colegiul Național de Informatică „Spiru Haret" Suceava 
              </p>
            </div>
          </router-link>
        </div>

        <!-- Desktop Nav -->
        <div class="hidden md:flex items-center justify-center gap-8">
          <router-link 
            to="/" 
            class="font-mono text-xs tracking-wider text-white/70 hover:text-white transition-colors uppercase"
            active-class="!text-white font-bold"
            exact
          >
            Acasă
          </router-link>
          <router-link 
            to="/books" 
            class="font-mono text-xs tracking-wider text-white/70 hover:text-white transition-colors uppercase"
            active-class="!text-white font-bold"
          >
            Cărți
          </router-link>
          <router-link 
            v-if="isLoggedIn" 
            to="/profile" 
            class="font-mono text-xs tracking-wider text-white/70 hover:text-white transition-colors uppercase"
            active-class="!text-white font-bold"
          >
            Profil
          </router-link>
          <router-link
            v-if="inClub"
            to="/club"
            class="font-mono text-xs tracking-wider text-white/70 hover:text-white transition-colors uppercase"
            active-class="!text-white font-bold"
          >
            Club
          </router-link>
        </div>

        <!-- Right Side: Desktop Buttons & Mobile Toggle -->
        <div class="flex-1 flex justify-end items-center gap-4">
          <div class="hidden md:flex items-center gap-4">
            <button 
              id="tts-toggle-btn"
              @click="toggleTTS"
              :class="[
                'flex items-center justify-center w-8 h-8 rounded-sm transition-colors',
                ttsActive ? 'bg-blue-500/20 text-blue-400' : 'text-white/70 hover:text-white hover:bg-white/5'
              ]"
              title="Mod Citire Text (Treci cu mouse-ul peste orice text pentru a-l citi)"
            >
              <i class="pi pi-volume-up text-sm"></i>
            </button>

            <div class="w-px h-6 bg-white/15"></div>

            <button 
              @click="handleAuthClick"
              :class="[
                'flex items-center gap-2 px-4 py-2 rounded-sm text-xs font-mono tracking-wider uppercase transition-colors',
                isLoggedIn
                  ? 'text-white border border-white/15 hover:border-white/30 hover:bg-white/5'
                  : 'bg-[#c9a84c] text-dark hover:opacity-90'
              ]"
            >
              <i :class="isLoggedIn ? 'pi pi-sign-out' : 'pi pi-user'" class="text-[11px]"></i>
              {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
            </button>
          </div>

          <!-- Mobile toggle -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-white/70 hover:text-white p-1 transition-colors"
          >
            <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-xl"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="mobileMenuOpen" class="md:hidden bg-dark border-t border-white/10 absolute w-full left-0 shadow-lg">
        <div class="px-6 py-5 flex flex-col gap-4">
          <router-link to="/" @click="mobileMenuOpen = false" class="font-mono text-xs tracking-wider text-white/70 hover:text-white uppercase" active-class="!text-white font-bold">
            Acasă
          </router-link>
          <router-link to="/books" @click="mobileMenuOpen = false" class="font-mono text-xs tracking-wider text-white/70 hover:text-white uppercase" active-class="!text-white font-bold">
            Cărți
          </router-link>
          <router-link v-if="isLoggedIn" to="/profile" @click="mobileMenuOpen = false" class="font-mono text-xs tracking-wider text-white/70 hover:text-white uppercase" active-class="!text-white font-bold">
            Profil
          </router-link>
          <router-link v-if="inClub" to="/club" @click="mobileMenuOpen = false" class="font-mono text-xs tracking-wider text-white/70 hover:text-white uppercase" active-class="!text-white font-bold">
            Club
          </router-link>
          
          <div class="h-px w-full bg-white/10 my-1"></div>

          <button 
            @click="toggleTTS"
            :class="[
              'w-full text-left font-mono text-xs tracking-wider uppercase transition-all flex items-center gap-2',
              ttsActive ? 'text-blue-400' : 'text-white/70 hover:text-white'
            ]"
          >
            <i class="pi pi-volume-up text-sm"></i> Citire Text {{ ttsActive ? '(Activat)' : '' }}
          </button>

          <button 
            @click="handleAuthClick"
            :class="[
              'flex items-center justify-center gap-2 px-4 py-2.5 mt-2 rounded-sm text-xs font-mono tracking-wider uppercase w-full transition-colors',
              isLoggedIn
                ? 'text-white border border-white/15 bg-white/5 hover:bg-white/10'
                : 'bg-[#c9a84c] text-dark hover:opacity-90'
            ]"
          >
            <i :class="isLoggedIn ? 'pi pi-sign-out' : 'pi pi-user'" class="text-[11px]"></i>
            {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
          </button>
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
