<template>
  <div class="min-h-screen bg-base">
    <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col lg:flex-row gap-8 items-start">
      
      <!-- Left Column: Threads Widget -->
      <div class="w-full lg:w-[350px] xl:w-[400px] flex-shrink-0 lg:sticky lg:top-24 z-10 order-2 lg:order-1 mt-12 lg:mt-0 bg-white rounded-sm border border-[#2a1410]/10 p-6 sm:p-8">
        <h2 class="text-sm font-bold tracking-tight uppercase text-[#2a1410] mb-6">Discuții Recente</h2>
        
        <div class="space-y-4">
          <template v-if="recentThreads.length > 0">
            <div v-for="(thread, index) in recentThreads" :key="thread.thread_id" class="group cursor-pointer border-b border-[#2a1410]/10 pb-4 last:border-0 last:pb-0" @click="$router.push('/club/threads?id=' + thread.thread_id)">
              <div class="flex items-start justify-between gap-3">
                <div class="flex-1 min-w-0">
                  <h4 class="text-sm font-bold text-[#2a1410] group-hover:text-[#8b4513] transition-colors line-clamp-2 leading-snug">{{ thread.titlu }}</h4>
                  <p class="text-xs text-[#7a5a55] mt-1 truncate">de {{ thread.autor }}</p>
                </div>
                <div class="flex items-center gap-1 text-xs font-bold text-[#8b4513] shrink-0">
                  <i class="pi pi-comment text-[10px]"></i> {{ thread.comentarii_count || 0 }}
                </div>
              </div>
            </div>
          </template>
          <div v-else class="text-xs text-[#7a5a55] text-center py-4">
            Nu există discuții recente.
          </div>
        </div>
        
        <button @click="$router.push('/club/threads')" class="w-full text-center mt-6 pt-2 text-[#8b4513] font-bold text-[10px] uppercase tracking-widest hover:underline flex items-center justify-center gap-1">
          TOATE DISCUȚIILE <i class="pi pi-arrow-right text-[8px]"></i>
        </button>
      </div>

      <!-- Right Column: Main Activities -->
      <div class="flex-1 w-full mx-auto order-1 lg:order-2">

      <!-- Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-3xl sm:text-4xl font-serif font-bold text-[#2a1410] flex items-center gap-3">
            <i class="pi pi-bookmark text-[#8b4513]"></i> Club de Lectură
          </h1>
          <p class="text-[#7a5a55] text-base mt-2">Activitățile săptămânii curente</p>
        </div>
        <div class="flex flex-wrap gap-3 self-start">
          <router-link
            to="/club/anterioare"
            class="px-5 py-2.5 bg-white border border-[#2a1410]/20 hover:bg-[#2a1410]/5 text-[#2a1410] text-[10px] font-mono tracking-widest uppercase font-bold rounded-sm transition-colors flex items-center gap-2"
          >
            <i class="pi pi-calendar text-sm"></i> Săptămâna anterioară
          </router-link>
          <button
            v-if="isBibliotecar"
            @click="openAddModal"
            class="px-5 py-2.5 bg-[#8b4513] hover:opacity-90 text-white text-[10px] font-mono tracking-widest uppercase font-bold rounded-sm transition-colors flex items-center gap-2"
          >
            <i class="pi pi-plus text-sm"></i> Activitate nouă
          </button>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-20 text-gray-400">
        <i class="pi pi-spin pi-spinner text-3xl mb-3 block"></i>
        <p class="text-sm">Se încarcă activitățile...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="loadError" class="text-center py-20 text-gray-400">
        <i class="pi pi-exclamation-circle text-4xl mb-3 block text-gray-200"></i>
        <p class="text-sm">Nu s-au putut încărca activitățile.</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="activitati.length === 0" class="text-center py-20 text-gray-400">
        <i class="pi pi-calendar text-4xl mb-3 block text-gray-200"></i>
        <p class="text-sm">Nicio activitate pentru săptămâna curentă.</p>
        <p v-if="isBibliotecar" class="text-xs mt-1 text-[#8b4513] cursor-pointer hover:underline" @click="openAddModal">
          Adaugă prima activitate →
        </p>
      </div>

      <!-- Activity feed -->
      <div v-else class="space-y-6">
        <div
          v-for="act in activitati"
          :key="act.activitate_id"
          class="bg-white rounded-sm border border-[#2a1410]/10 shadow-[0_1px_4px_rgba(42,20,16,0.04)] p-6 sm:p-8"
        >
          <!-- Activity header -->
          <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-2">
              <span
                :class="tipBadge(act.tip).cls"
                class="inline-flex items-center gap-1 px-2 py-1 rounded-sm text-[10px] font-bold tracking-widest uppercase"
              >
                {{ tipBadge(act.tip).label }}
              </span>
              <span class="text-xs text-[#7a5a55]">{{ act.creat_la }} • Scris de <span class="font-bold text-[#2a1410]">{{ act.autor }}</span></span>
            </div>
            <div class="flex items-center gap-3">
              <span v-if="act.autor_rol === 'bibliotecar'" class="text-[10px] bg-gray-100 text-gray-600 font-bold px-2 py-1 rounded-sm uppercase tracking-widest">BIBLIOTECAR</span>
              <button
                v-if="isBibliotecar"
                @click="confirmDelete(act)"
                class="text-gray-300 hover:text-red-500 text-sm transition-colors"
                title="Șterge activitatea"
              >
                <i class="pi pi-trash"></i>
              </button>
            </div>
          </div>

          <h3 class="text-3xl font-serif font-bold text-[#2a1410] leading-snug break-words mb-4">{{ act.titlu }}</h3>
          <p v-if="act.continut" class="text-base text-[#4a3a35] whitespace-pre-line leading-relaxed break-words">{{ act.continut }}</p>
          
          <img v-if="act.imagine_url && act.tip === 'anunt'" :src="act.imagine_url" alt="Imagine anunț" class="w-full h-56 object-cover rounded-sm mt-5" />

          <!-- Thread toggle (Footer) -->
          <div class="mt-6 pt-4 border-t border-[#2a1410]/10 flex items-center justify-between">
            <button
              @click="toggleThread(act.activitate_id)"
              class="flex items-center gap-2 text-[#8b4513] font-bold text-sm hover:underline font-sans"
            >
              <i class="pi pi-comment"></i>
              <span v-if="openThreads[act.activitate_id]">Ascunde comentariile</span>
              <span v-else>{{ act.nr_comentarii > 0 ? `${act.nr_comentarii} comentarii` : '0 comentarii' }}</span>
            </button>
            <button
              @click="toggleThread(act.activitate_id)"
              class="text-[#4a3a35] font-bold text-sm flex items-center gap-2 hover:text-[#2a1410] transition-colors font-sans"
            >
              Răspunde <i class="pi pi-arrow-right text-xs"></i>
            </button>
          </div>

          <!-- Thread panel -->
          <div v-if="openThreads[act.activitate_id]" class="border-t border-[#8b4513]/20 bg-transparent mt-4 pt-4 space-y-4 font-sans">
            <!-- Loading comments -->
            <div v-if="loadingThread[act.activitate_id]" class="text-center text-gray-400 text-sm py-4">
              <i class="pi pi-spin pi-spinner mr-1"></i> Se încarcă...
            </div>

            <!-- Comment list -->
            <div
              v-for="com in (threadData[act.activitate_id] || [])"
              :key="com.comentariu_id"
              class="flex gap-3"
            >
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-[#8b4513]/10 flex items-center justify-center text-[#8b4513] text-xs font-bold uppercase">
                {{ com.autor.charAt(0) }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-0.5">
                  <span class="text-xs font-bold text-dark">{{ com.autor }}</span>
                  <span v-if="com.autor_rol === 'bibliotecar'" class="text-[10px] bg-[#8b4513]/10 text-[#8b4513] font-semibold px-1.5 py-0.5 rounded-full">bibliotecar</span>
                  <span class="text-[11px] text-gray-400">{{ com.creat_la }}</span>
                </div>
                <p class="text-sm text-gray-700 whitespace-pre-line break-words">{{ com.continut }}</p>
              </div>
              <button
                v-if="canDeleteComment(com)"
                @click="deleteComment(act.activitate_id, com.comentariu_id)"
                class="text-gray-300 hover:text-accent text-sm flex-shrink-0 transition-colors self-start mt-0.5"
                title="Șterge comentariul"
              >
                <i class="pi pi-times"></i>
              </button>
            </div>

            <!-- No comments yet -->
            <p v-if="!loadingThread[act.activitate_id] && (threadData[act.activitate_id] || []).length === 0" class="text-xs text-gray-400 text-center py-2">
              Niciun comentariu încă. Fii primul!
            </p>

            <!-- New comment input -->
            <div class="flex gap-2 pt-1">
              <input
                v-model="newComment[act.activitate_id]"
                @keydown.enter.exact.prevent="submitComment(act.activitate_id)"
                type="text"
                placeholder="Scrie un comentariu... (Enter pentru a trimite)"
                maxlength="2000"
                class="w-full text-sm border border-[#2a1410]/10 rounded-sm px-4 py-3 bg-cream-dark focus:outline-none focus:ring-1 focus:ring-[#8b4513]/40"
              />
              <button
                @click="submitComment(act.activitate_id)"
                :disabled="!(newComment[act.activitate_id] || '').trim()"
                class="px-5 py-3 bg-[#8b4513] hover:bg-[#8b4513]/90 disabled:opacity-40 text-white rounded-xl text-sm font-semibold transition-all"
              >
                <i class="pi pi-send text-sm"></i>
              </button>
            </div>
            <p v-if="threadError[act.activitate_id]" class="text-xs text-red-500">{{ threadError[act.activitate_id] }}</p>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- Add Activity Modal -->
    <div v-if="addModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="addModalOpen = false">
      <div class="w-full max-w-lg bg-white border border-[#2a1410]/10 rounded-2xl shadow-2xl p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-[#2a1410] flex items-center gap-2">
            <i class="pi pi-plus-circle text-[#8b4513]"></i> Activitate nouă
          </h2>
          <button @click="addModalOpen = false" class="text-gray-400 hover:text-[#2a1410] text-2xl font-bold leading-none">&times;</button>
        </div>

        <div class="space-y-5">
          <div>
            <label class="block text-sm font-bold text-[#7a5a55] mb-2">Titlu *</label>
            <input v-model="addForm.titlu" type="text" maxlength="255" placeholder="Titlul activității..." class="w-full text-base border border-[#2a1410]/10 rounded-xl px-4 py-3 bg-cream-dark focus:outline-none focus:border-[#8b4513]/40" />
          </div>
          <div>
            <label class="block text-sm font-bold text-[#7a5a55] mb-2">Descriere</label>
            <textarea v-model="addForm.continut" rows="4" maxlength="5000" placeholder="Detalii, instrucțiuni, linkuri..." class="w-full text-base border border-[#2a1410]/10 rounded-xl px-4 py-3 bg-cream-dark focus:outline-none focus:border-[#8b4513]/40 resize-none"></textarea>
          </div>
          <div class="flex gap-3">
            <div class="flex-1">
              <label class="block text-sm font-bold text-[#7a5a55] mb-2">Tip</label>
              <select v-model="addForm.tip" @change="onActivityTypeChange" class="w-full text-base border border-[#2a1410]/10 rounded-xl px-4 py-3 bg-cream-dark focus:outline-none focus:border-[#8b4513]/40">
                <option value="activitate">Activitate</option>
                <option value="sarcina">Sarcină</option>
                <option value="anunt">Anunț</option>
              </select>
            </div>
          </div>
          <div v-if="addForm.tip === 'anunt'" class="pt-2">
            <label class="block text-xs font-semibold text-gray-600 mb-1">Imagine anunț</label>
            <input
              ref="activityImageInput"
              type="file"
              accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
              @change="onActivityImageChange"
              class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[#8b4513] file:text-white hover:file:bg-[#8b4513]/90"
            />
          </div>
        </div>

        <p v-if="addError" class="mt-3 text-xs text-accent">{{ addError }}</p>

        <div class="flex gap-4 mt-8">
          <button @click="addModalOpen = false" class="px-5 py-2.5 border border-[#2a1410]/20 text-[#7a5a55] text-[10px] font-mono tracking-widest uppercase font-bold rounded-sm hover:bg-black/5 transition-colors">
            Anulează
          </button>
          <button
            @click="submitActivity"
            :disabled="addSaving || !addForm.titlu.trim()"
            class="px-5 py-2.5 bg-[#8b4513] hover:opacity-90 disabled:opacity-50 text-white text-[10px] font-mono tracking-widest uppercase font-bold rounded-sm transition-colors flex items-center justify-center gap-2"
          >
            <i :class="addSaving ? 'pi pi-spin pi-spinner' : 'pi pi-check'" class="text-sm"></i>
            Publică
          </button>
        </div>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="deleteTarget = null">
      <div class="w-full max-w-sm bg-white border border-[#2a1410]/10 rounded-2xl shadow-2xl p-8 text-center">
        <i class="pi pi-exclamation-triangle text-4xl text-red-500 mb-4 block"></i>
        <h3 class="font-bold text-[#2a1410] text-xl mb-2">Ștergi activitatea?</h3>
        <p class="text-sm text-[#7a5a55] mb-8">„{{ deleteTarget.titlu }}" și toate comentariile aferente vor fi șterse definitiv.</p>
        <div class="flex gap-4">
          <button @click="deleteTarget = null" class="flex-1 px-4 py-3 border border-[#2a1410]/20 text-[#2a1410] font-bold rounded-xl text-sm hover:bg-[#2a1410]/5">Anulează</button>
          <button @click="executeDelete" :disabled="deleteSaving" class="flex-1 px-4 py-3 bg-red-500 hover:bg-red-600 disabled:opacity-50 text-white font-bold rounded-xl text-sm">
            <i :class="deleteSaving ? 'pi pi-spin pi-spinner' : 'pi pi-trash'" class="text-sm mr-1"></i>Șterge
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ScrollWidget from '../components/ScrollWidget.vue'

export default {
  name: 'Club',
  components: { ScrollWidget },
  data() {
    return {
      loading: true,
      loadError: '',
      activitati: [],
      recentThreads: [],
      currentUser: null,

      // Thread state (per activitate_id)
      openThreads: {},
      loadingThread: {},
      threadData: {},
      threadError: {},
      newComment: {},

      // Add activity modal
      addModalOpen: false,
      addForm: { titlu: '', continut: '', tip: 'activitate', saptamana: 'curenta' },
      activityImageFile: null,
      activityImagePreview: null,
      addError: '',
      addSaving: false,

      // Delete
      deleteTarget: null,
      deleteSaving: false
    }
  },
  computed: {
    isBibliotecar() {
      return this.currentUser?.rol === 'bibliotecar'
    }
  },
  async mounted() {
    await this.fetchMe()
    await this.fetchActivitati()
    await this.fetchRecentThreads()
  },
  methods: {
    async fetchRecentThreads() {
      try {
        const res = await fetch('/api/club/threads', { credentials: 'include' })
        const data = await res.json()
        if (res.ok) {
          this.recentThreads = (data.threads || []).slice(0, 5)
        }
      } catch (err) { /* ignore */ }
    },
    async fetchMe() {
      try {
        const res = await fetch('/api/auth/me', { credentials: 'include' })
        if (res.ok) this.currentUser = await res.json()
      } catch { /* ignorăm */ }
    },

    async fetchActivitati() {
      this.loading = true
      this.loadError = ''
      try {
        const res = await fetch('/api/club/activitati?saptamana=curenta', { credentials: 'include' })
        const data = await res.json()
        if (res.status === 403) {
          this.$router.push('/')
          return
        }
        if (!res.ok) {
          this.loadError = data.message || 'Eroare la încărcarea activităților.'
        } else {
          this.activitati = data.activitati
        }
      } catch {
        this.loadError = 'Eroare de rețea.'
      } finally {
        this.loading = false
      }
    },

    tipBadge(tip) {
      const map = {
        anunt:      { label: 'ANUNȚ',      cls: 'bg-[#e0f2fe] text-[#0369a1]' },
        sarcina:    { label: 'SARCINĂ',    cls: 'bg-[#fef3c7] text-[#b45309]' },
        activitate: { label: 'ACTIVITATE', cls: 'bg-[#8b4513]/10 text-[#8b4513]' }
      }
      return map[tip] || map.activitate
    },

    async toggleThread(id) {
      const wasOpen = !!this.openThreads[id]
      this.openThreads = { ...this.openThreads, [id]: !wasOpen }
      if (!wasOpen && !this.threadData[id]) {
        await this.loadComments(id)
      }
    },

    async loadComments(activitateId) {
      this.loadingThread = { ...this.loadingThread, [activitateId]: true }
      this.threadError = { ...this.threadError, [activitateId]: '' }
      try {
        const res = await fetch(`/api/club/activitati/${activitateId}/comentarii`, { credentials: 'include' })
        const data = await res.json()
        this.threadData = { ...this.threadData, [activitateId]: data.comentarii || [] }
      } catch {
        this.threadError = { ...this.threadError, [activitateId]: 'Eroare la încărcarea comentariilor.' }
      } finally {
        this.loadingThread = { ...this.loadingThread, [activitateId]: false }
      }
    },

    async submitComment(activitateId) {
      const text = (this.newComment[activitateId] || '').trim()
      if (!text) return
      this.threadError = { ...this.threadError, [activitateId]: '' }
      try {
        const res = await fetch(`/api/club/activitati/${activitateId}/comentarii`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ continut: text })
        })
        const data = await res.json()
        if (!res.ok) {
          this.threadError = { ...this.threadError, [activitateId]: data.message || 'Eroare.' }
        } else {
          this.newComment = { ...this.newComment, [activitateId]: '' }
          await this.loadComments(activitateId)
          // Update comment count in list
          const act = this.activitati.find(a => a.activitate_id === activitateId)
          if (act) act.nr_comentarii++
        }
      } catch {
        this.threadError = { ...this.threadError, [activitateId]: 'Eroare de rețea.' }
      }
    },

    canDeleteComment(com) {
      if (!this.currentUser) return false
      return com.user_id === this.currentUser.user_id || this.isBibliotecar
    },

    async deleteComment(activitateId, comentariuId) {
      try {
        await fetch(`/api/club/activitati/${activitateId}/comentarii/${comentariuId}`, {
          method: 'DELETE', credentials: 'include'
        })
        const list = this.threadData[activitateId] || []
        this.threadData = { ...this.threadData, [activitateId]: list.filter(c => c.comentariu_id !== comentariuId) }
        const act = this.activitati.find(a => a.activitate_id === activitateId)
        if (act && act.nr_comentarii > 0) act.nr_comentarii--
      } catch { /* ignorăm */ }
    },

    openAddModal() {
      this.addForm = { titlu: '', continut: '', tip: 'activitate', saptamana: 'curenta' }
      this.activityImageFile = null
      this.activityImagePreview = null
      this.addError = ''
      this.addModalOpen = true
    },

    onActivityTypeChange() {
      if (this.addForm.tip !== 'anunt') {
        this.activityImageFile = null
        this.activityImagePreview = null
        if (this.$refs.activityImageInput) {
          this.$refs.activityImageInput.value = ''
        }
      }
    },

    onActivityImageChange(event) {
      const file = event.target.files[0]
      if (!file) {
        this.activityImageFile = null
        this.activityImagePreview = null
        return
      }
      this.activityImageFile = file
      this.activityImagePreview = URL.createObjectURL(file)
    },

    async submitActivity() {
      if (!this.addForm.titlu.trim()) return
      this.addSaving = true
      this.addError = ''
      try {
        const formData = new FormData()
        formData.append('titlu', this.addForm.titlu)
        formData.append('continut', this.addForm.continut)
        formData.append('tip', this.addForm.tip)
        formData.append('saptamana', this.addForm.saptamana)
        if (this.activityImageFile && this.addForm.tip === 'anunt') {
          formData.append('image', this.activityImageFile)
        }

        const res = await fetch('/api/club/activitati', {
          method: 'POST',
          credentials: 'include',
          body: formData
        })
        const data = await res.json()
        if (!res.ok) {
          this.addError = data.message || 'Eroare la publicare.'
        } else {
          this.addModalOpen = false
          this.activityImageFile = null
          this.activityImagePreview = null
          if (this.$refs.activityImageInput) {
            this.$refs.activityImageInput.value = ''
          }
          await this.fetchActivitati()
        }
      } catch {
        this.addError = 'Eroare de rețea.'
      } finally {
        this.addSaving = false
      }
    },

    confirmDelete(act) {
      this.deleteTarget = act
    },

    async executeDelete() {
      if (!this.deleteTarget) return
      this.deleteSaving = true
      try {
        await fetch(`/api/club/activitati/${this.deleteTarget.activitate_id}`, {
          method: 'DELETE', credentials: 'include'
        })
        this.activitati = this.activitati.filter(a => a.activitate_id !== this.deleteTarget.activitate_id)
        this.deleteTarget = null
      } catch { /* ignorăm */ } finally {
        this.deleteSaving = false
      }
    }
  }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 8px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 8px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
