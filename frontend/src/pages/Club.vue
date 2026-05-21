<template>
  <div class="min-h-screen bg-base">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

      <!-- Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-dark flex items-center gap-2">
            <i class="pi pi-bookmark-fill text-secondary"></i> Club de Lectură
          </h1>
          <p class="text-gray-500 text-sm mt-1">Activitățile săptămânii curente</p>
        </div>
        <div class="flex flex-wrap gap-2 self-start">
          <router-link
            to="/club/anterioare"
            class="px-4 py-2.5 border border-gray-200 hover:bg-gray-50 text-gray-600 font-semibold rounded-xl text-sm transition-all flex items-center gap-2"
          >
            <i class="pi pi-history text-xs"></i> Săptămâna anterioară
          </router-link>
          <button
            v-if="isBibliotecar"
            @click="openAddModal"
            class="px-5 py-2.5 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-xl text-sm transition-all flex items-center gap-2"
          >
            <i class="pi pi-plus text-xs"></i> Activitate nouă
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
        <p v-if="isBibliotecar" class="text-xs mt-1 text-secondary cursor-pointer hover:underline" @click="openAddModal">
          Adaugă prima activitate →
        </p>
      </div>

      <!-- Activity feed -->
      <div v-else class="space-y-6">
        <div
          v-for="act in activitati"
          :key="act.activitate_id"
          class="bg-white rounded-2xl shadow-card border border-gray-100"
        >
          <!-- Activity header -->
          <div class="p-5 sm:p-6">
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <div class="flex flex-wrap items-center gap-2 mb-1">
                  <span
                    :class="tipBadge(act.tip).cls"
                    class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold"
                  >
                    <i :class="tipBadge(act.tip).icon" class="text-[10px]"></i>
                    {{ tipBadge(act.tip).label }}
                  </span>
                  <span class="text-xs text-gray-400">{{ act.creat_la }} · {{ act.autor }}</span>
                  <span v-if="act.autor_rol === 'bibliotecar'" class="text-xs bg-secondary/10 text-secondary font-semibold px-2 py-0.5 rounded-full">bibliotecar</span>
                </div>
                <h3 class="text-base sm:text-lg font-bold text-dark leading-snug">{{ act.titlu }}</h3>
                <p v-if="act.continut" class="text-sm text-gray-600 mt-2 whitespace-pre-line leading-relaxed">{{ act.continut }}</p>
                <img v-if="act.imagine_url && act.tip === 'anunt'" :src="act.imagine_url" alt="Imagine anunț" class="w-full h-56 object-cover rounded-2xl mt-4" />
              </div>
              <button
                v-if="isBibliotecar"
                @click="confirmDelete(act)"
                class="text-gray-300 hover:text-accent text-lg leading-none flex-shrink-0 transition-colors"
                title="Șterge activitatea"
              >
                <i class="pi pi-trash"></i>
              </button>
            </div>

            <!-- Thread toggle -->
            <button
              @click="toggleThread(act.activitate_id)"
              class="mt-4 text-xs font-semibold text-secondary hover:underline flex items-center gap-1"
            >
              <i class="pi pi-comments text-xs"></i>
              <span v-if="openThreads[act.activitate_id]">Ascunde comentariile</span>
              <span v-else>{{ act.nr_comentarii > 0 ? `${act.nr_comentarii} comentarii` : 'Comentează' }}</span>
            </button>
          </div>

          <!-- Thread panel -->
          <div v-if="openThreads[act.activitate_id]" class="border-t border-gray-100 bg-gray-50 rounded-b-2xl px-5 sm:px-6 py-4 space-y-4">
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
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center text-secondary text-xs font-bold uppercase">
                {{ com.autor.charAt(0) }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-0.5">
                  <span class="text-xs font-bold text-dark">{{ com.autor }}</span>
                  <span v-if="com.autor_rol === 'bibliotecar'" class="text-[10px] bg-secondary/10 text-secondary font-semibold px-1.5 py-0.5 rounded-full">bibliotecar</span>
                  <span class="text-[11px] text-gray-400">{{ com.creat_la }}</span>
                </div>
                <p class="text-sm text-gray-700 whitespace-pre-line">{{ com.continut }}</p>
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
                class="flex-1 text-sm border border-gray-200 rounded-xl px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-secondary/40 placeholder-gray-400"
              />
              <button
                @click="submitComment(act.activitate_id)"
                :disabled="!(newComment[act.activitate_id] || '').trim()"
                class="px-4 py-2 bg-secondary hover:bg-secondary/90 disabled:opacity-40 text-white rounded-xl text-sm font-semibold transition-all"
              >
                <i class="pi pi-send text-xs"></i>
              </button>
            </div>
            <p v-if="threadError[act.activitate_id]" class="text-xs text-accent">{{ threadError[act.activitate_id] }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Activity Modal -->
    <div v-if="addModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="addModalOpen = false">
      <div class="w-full max-w-lg bg-white rounded-2xl shadow-modal p-6">
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-bold text-dark flex items-center gap-2">
            <i class="pi pi-plus-circle text-secondary"></i> Activitate nouă
          </h2>
          <button @click="addModalOpen = false" class="text-gray-400 hover:text-secondary text-2xl font-bold leading-none">&times;</button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Titlu *</label>
            <input v-model="addForm.titlu" type="text" maxlength="255" placeholder="Titlul activității..." class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Descriere</label>
            <textarea v-model="addForm.continut" rows="4" maxlength="5000" placeholder="Detalii, instrucțiuni, linkuri..." class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40 resize-none"></textarea>
          </div>
          <div class="flex gap-3">
            <div class="flex-1">
              <label class="block text-xs font-semibold text-gray-600 mb-1">Tip</label>
              <select v-model="addForm.tip" @change="onActivityTypeChange" class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40 bg-white">
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
              class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-secondary file:text-white hover:file:bg-secondary/90"
            />
          </div>
        </div>

        <p v-if="addError" class="mt-3 text-xs text-accent">{{ addError }}</p>

        <div class="flex gap-3 mt-6">
          <button @click="addModalOpen = false" class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 font-semibold rounded-xl text-sm hover:bg-gray-50 transition-colors">
            Anulează
          </button>
          <button
            @click="submitActivity"
            :disabled="addSaving || !addForm.titlu.trim()"
            class="flex-1 px-4 py-2.5 bg-secondary hover:bg-secondary/90 disabled:opacity-50 text-white font-semibold rounded-xl text-sm transition-colors flex items-center justify-center gap-2"
          >
            <i :class="addSaving ? 'pi pi-spin pi-spinner' : 'pi pi-check'" class="text-xs"></i>
            Publică
          </button>
        </div>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="deleteTarget = null">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-modal p-6 text-center">
        <i class="pi pi-exclamation-triangle text-3xl text-accent mb-3 block"></i>
        <h3 class="font-bold text-dark mb-1">Ștergi activitatea?</h3>
        <p class="text-sm text-gray-500 mb-5">„{{ deleteTarget.titlu }}" și toate comentariile aferente vor fi șterse definitiv.</p>
        <div class="flex gap-3">
          <button @click="deleteTarget = null" class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 font-semibold rounded-xl text-sm hover:bg-gray-50">Anulează</button>
          <button @click="executeDelete" :disabled="deleteSaving" class="flex-1 px-4 py-2.5 bg-accent hover:bg-accent/90 disabled:opacity-50 text-white font-semibold rounded-xl text-sm">
            <i :class="deleteSaving ? 'pi pi-spin pi-spinner' : 'pi pi-trash'" class="text-xs mr-1"></i>Șterge
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Club',
  data() {
    return {
      loading: true,
      loadError: '',
      activitati: [],
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
  },
  methods: {
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
        anunt:      { label: 'Anunț',      icon: 'pi pi-megaphone', cls: 'bg-blue-50 text-blue-600' },
        sarcina:    { label: 'Sarcină',    icon: 'pi pi-check-square', cls: 'bg-amber-50 text-amber-600' },
        activitate: { label: 'Activitate', icon: 'pi pi-star', cls: 'bg-secondary/10 text-secondary' }
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
